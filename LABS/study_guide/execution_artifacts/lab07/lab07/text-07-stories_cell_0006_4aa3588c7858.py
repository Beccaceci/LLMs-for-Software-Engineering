import csv
import re


def extract_unique_roles(file_path: str):
    roles = set()
    with open(file_path, newline="", encoding="utf-8-sig") as stream:
        for row in csv.DictReader(stream):
            match = re.search(r"^As\s+(?:an?\s+)?(.+?)\s+I\s+want\b", row["Description"].strip(), flags=re.IGNORECASE)
            if match:
                roles.add(match.group(1).strip().lower())
    return sorted(roles)


def extract_list_items(text: str):
    """Keep only a leading numbered/bulleted list; reject explanatory prose."""
    items = []
    started = False
    for line in text.splitlines():
        line = line.strip()
        match = re.match(r"^(?:\d+\s*[.)-]?\s+|[-*•]\s+)(.+?)\s*$", line)
        if match:
            started = True
            item = match.group(1).strip().strip("* ")
            # Keep the role label and discard parenthetical/editorial commentary.
            item = re.split(r"\s+[–—]\s+|\s+-\s+", item, maxsplit=1)[0]
            item = re.sub(r"\s*\([^)]*\)", "", item).strip()
            item = re.sub(r"/s$", "s", item, flags=re.IGNORECASE)
            if item:
                items.append(item)
        elif started and line:
            break
    return list(dict.fromkeys(items))


def normalize_roles(role_list: list[str]):
    # Ignore whitespace, case and a final plural s as requested by the exercise.
    return {re.sub(r"\s+", "", role.lower()).removesuffix("s") for role in role_list if role.strip()}


def role_metrics(expected, actual):
    expected, actual = normalize_roles(expected), normalize_roles(actual)
    tp = len(expected & actual)
    fp = len(actual - expected)
    fn = len(expected - actual)
    return tp, fp, fn, tp / (tp + fp) if tp + fp else 0.0, tp / (tp + fn) if tp + fn else 0.0


file_path = "stories.csv"
expected_roles = extract_unique_roles(file_path)
print("Reference roles from stories.csv:", expected_roles)