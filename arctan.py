
def arctan(z):
    return z / term(z, 1, 25) # 25 gives no diff in float repr

def term(z, i, stop):
    a = 2 * i - 1
    if i == stop:
        return a
    b = (i * z) ** 2
    c = term(z, i+1, stop)
    return a + b / c

