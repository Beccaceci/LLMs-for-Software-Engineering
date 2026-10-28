import pytest
from function_03 import computeMaxTime
@pytest.mark.parametrize("category,speed,expected", [("A",30,105),("A",30.001,110),("A",35,110),("A",35.001,115),("B",30,120),("B",30.001,125),("B",35,125),("B",35.001,130),("C",20,150),("C",40,150)])
def test_boundaries(category,speed,expected): assert computeMaxTime(100,speed,category) == pytest.approx(expected)
@pytest.mark.parametrize("args", [(0,30,"A"),(-1,30,"A"),(100,0,"A"),(100,-1,"A"),(100,30,"D"),(100,30,"a"),(float("nan"),30,"A"),(100,True,"A"),("100",30,"A")])
def test_invalid(args): assert computeMaxTime(*args) == 0
