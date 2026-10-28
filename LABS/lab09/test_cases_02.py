import pytest
from function_02 import computeFee
@pytest.mark.parametrize("args,expected", [((10,2,1,1),10),((10,5,1,4),10),((10,5,1,0),50),((10,1,1,0),10),((10,2,0,2),20),((0,3,1,2),0)])
def test_fee(args,expected): assert computeFee(*args) == pytest.approx(expected)
@pytest.mark.parametrize("args", [(10,6,1,2),(10,0,0,0),(10,3,2,2),(10,3,-1,1),(-1,2,1,1),(10,2.5,1,1),(10,True,0,0)])
def test_invalid_fee(args):
    with pytest.raises(ValueError): computeFee(*args)
