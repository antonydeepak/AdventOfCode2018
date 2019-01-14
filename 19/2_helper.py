total = 10551275 #1 is going all the way to this value
# during the time of this journey how is reg 0 changed w.r.t eqrr *5,10551275
# *5 = *1 x *3

_0value = 0
for _1value in range(1, total):
    _5value = total // _1value
    if _5value*_1value == total:
        _0value += _1value
print(_0value)