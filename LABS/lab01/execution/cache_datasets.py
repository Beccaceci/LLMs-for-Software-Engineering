"""Cache official CIFAR archives with parallel ranges and exact torchvision MD5 checks."""
import concurrent.futures
import hashlib
import os
from pathlib import Path
import shutil
import time
import urllib.request

from torchvision.datasets import CIFAR10, CIFAR100
from torchvision.models import ResNet18_Weights, resnet18

ROOT = Path(__file__).resolve().parents[1]
CACHE = ROOT / 'data'
CACHE.mkdir(exist_ok=True)


def md5(path):
    digest = hashlib.md5()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(block)
    return digest.hexdigest()


def cache(dataset):
    destination = CACHE / dataset.filename
    if destination.exists() and md5(destination) == dataset.tgz_md5:
        print(f'{dataset.__name__}: existing archive verified', flush=True)
    else:
        with urllib.request.urlopen(urllib.request.Request(dataset.url, method='HEAD'), timeout=30) as response:
            total = int(response.headers['Content-Length'])
        parts_dir = CACHE / (dataset.filename + '.parts')
        parts_dir.mkdir(exist_ok=True)
        chunk_size = 4 * 1024 * 1024
        spans = [(i, min(i + chunk_size - 1, total - 1)) for i in range(0, total, chunk_size)]

        def fetch(span):
            start, stop = span
            target = parts_dir / f'{start:012d}.part'
            if target.exists() and target.stat().st_size == stop - start + 1:
                return target
            for attempt in range(4):
                try:
                    request = urllib.request.Request(dataset.url, headers={'Range': f'bytes={start}-{stop}'})
                    with urllib.request.urlopen(request, timeout=45) as response:
                        expected = f'bytes {start}-{stop}/{total}'
                        if response.status != 206 or response.headers.get('Content-Range') != expected:
                            raise RuntimeError(f'Unexpected range response: {response.status} {response.headers.get("Content-Range")}')
                        temporary = target.with_suffix('.tmp')
                        with temporary.open('wb') as handle:
                            shutil.copyfileobj(response, handle)
                    if temporary.stat().st_size != stop - start + 1:
                        raise RuntimeError('Incomplete range')
                    temporary.replace(target)
                    print(f'{dataset.__name__}: cached bytes {start}-{stop}', flush=True)
                    return target
                except Exception:
                    if attempt == 3:
                        raise
                    time.sleep(attempt + 1)

        with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
            parts = list(pool.map(fetch, spans))
        assembled = destination.with_suffix('.verified.tmp')
        with assembled.open('wb') as handle:
            for part in parts:
                with part.open('rb') as fragment:
                    shutil.copyfileobj(fragment, handle)
        actual = md5(assembled)
        if actual != dataset.tgz_md5:
            raise RuntimeError(f'{dataset.__name__}: archive hash mismatch: {actual}')
        assembled.replace(destination)
        shutil.rmtree(parts_dir)
        print(f'{dataset.__name__}: official MD5 verified: {actual}', flush=True)
    dataset(root=str(CACHE), train=True, download=True)
    dataset(root=str(CACHE), train=False, download=True)
    print(f'{dataset.__name__}: train/test files ready', flush=True)


if __name__ == '__main__':
    for dataset in (CIFAR10, CIFAR100):
        cache(dataset)
    resnet18(weights=ResNet18_Weights.DEFAULT)
    print('CIFAR-10, CIFAR-100, and official ResNet-18 weights cached.', flush=True)
