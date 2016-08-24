"""
Module for finding an expression given a float

Note that this is of course just guessing.

"""
import math

def namednumber(num):
    """ attempt to find exact constant for float """
    def isnear(val):
        return abs(num-val)<0.00001
    if isnear(0.0): return "0"
    if num<0:
        sign = "-"
        num = -num
    else:
        sign = ""

    if isnear(1.0): return sign+"1"
    if isnear(math.pi): return sign+"pi"
    if isnear((math.sqrt(6)+math.sqrt(2))/4): return sign+"(sqrt(6)+sqrt(2))/4"
    if isnear((math.sqrt(6)-math.sqrt(2))/4): return sign+"(sqrt(6)-sqrt(2))/4"
    if isnear((math.sqrt(5)+1.0)/2): return sign+"(sqrt(5)+1)/2"
    if isnear((math.sqrt(5)-1.0)/2): return sign+"(sqrt(5)-1)/2"
    if isnear(math.sqrt((math.sqrt(5)+5.0)/2)): return sign+"sqrt((sqrt(5)+5)/2)"

    if isnear(math.atan((math.sqrt(5)+1.0)/2)): return sign+"atan((sqrt(5)+1)/2)"
    if isnear(math.atan((math.sqrt(5)-1.0)/2)): return sign+"atan((sqrt(5)-1)/2)"

    if isnear(math.pi-math.atan((math.sqrt(5)+1.0)/2)): return sign+"(pi-atan((sqrt(5)+1)/2))"
    if isnear(math.pi-math.atan((math.sqrt(5)-1.0)/2)): return sign+"(pi-atan((sqrt(5)-1)/2))"

    for div in range(2,20):
        if isnear(div): return sign+"%d" % div
        if isnear(1.0/div): return sign+"1/%d" % div
        if isnear(math.sqrt(div)): return sign+"sqrt(%d)" % div
        if isnear(1.0/math.sqrt(div)): return sign+"1/sqrt(%d)" % div

        if isnear(math.pi/div): return sign+"pi/%d" % div

        if isnear(math.atan(div)): return sign+"atan(%d)" % div
        if isnear(math.pi-math.atan(div)): return sign+"(pi-atan(%d))" % div
        if isnear(math.atan(1.0/div)): return sign+"atan(1/%d)" % div
        if isnear(math.pi-math.atan(1.0/div)): return sign+"(pi-atan(1/%d))" % div
        if isnear(math.atan(1.0/div)/2): return sign+"atan(1/%d)/2" % div
        if isnear((math.pi-math.atan(1.0/div))/2): return sign+"(pi-atan(1/%d))/2" % div
        if isnear(math.pi-math.atan(1.0/div)/2): return sign+"(pi-atan(1/%d)/2)" % div
        if isnear((math.pi+math.atan(1.0/div))/2): return sign+"(pi-atan(1/%d))/2" % div

        if isnear(math.atan(math.sqrt(div))): return sign+"atan(sqrt(%d))" % div
        if isnear(math.pi-math.atan(math.sqrt(div))): return sign+"(pi-atan(sqrt(%d)))" % div
        if isnear(math.atan(1.0/math.sqrt(div))): return sign+"atan(1/sqrt(%d))" % div
        if isnear(math.pi-math.atan(1.0/math.sqrt(div))): return sign+"(pi-atan(1/sqrt(%d)))" % div
        if isnear(math.atan(1.0/math.sqrt(div))/2): return sign+"atan(1/sqrt(%d))/2" % div
        if isnear((math.pi-math.atan(1.0/math.sqrt(div)))/2): return sign+"(pi-atan(1/sqrt(%d)))/2" % div
        if isnear(math.pi-math.atan(1.0/math.sqrt(div))/2): return sign+"(pi-atan(1/sqrt(%d))/2)" % div
        if isnear((math.pi+math.atan(1.0/math.sqrt(div)))/2): return sign+"(pi-atan(1/sqrt(%d)))/2" % div

    for div in range(2,20):
        for mul in range(2,19):
            if div==mul:
                continue
            if isnear(float(div)/mul): return sign+"%d/%d" % (div,mul)
            if isnear(math.sqrt(div)/mul): return sign+"sqrt(%d)/%d" % (div,mul)
            if isnear(mul*math.pi/div): return sign+"%d*pi/%d" % (mul,div)

    for div in range(2,20):
        for mul in range(2,19):
            if div==mul:
                continue
            if isnear(math.atan(float(mul)/div)): return sign+"atan(%d/%d)" % (mul, div)
            if isnear(math.pi-math.atan(float(mul)/div)): return sign+"(pi-atan(%d/%d))" % (mul, div)
            if isnear(math.atan(float(mul)/div)/2): return sign+"atan(%d/%d)/2" % (mul, div)
            if isnear((math.pi-math.atan(float(mul)/div))/2): return sign+"(pi-atan(%d/%d))/2" % (mul, div)
            if isnear(math.pi-math.atan(float(mul)/div)/2): return sign+"(pi-atan(%d/%d)/2)" % (mul, div)
            if isnear((math.pi+math.atan(float(mul)/div))/2): return sign+"(pi+atan(%d/%d))/2" % (mul, div)



            if isnear(math.atan(float(mul)/math.sqrt(div))): return sign+"atan(%d/sqrt(%d))" % (mul, div)
            if isnear(math.pi-math.atan(float(mul)/math.sqrt(div))): return sign+"(pi-atan(%d/sqrt(%d)))" % (mul, div)
            if isnear(math.atan(float(mul)/math.sqrt(div))/2): return sign+"atan(%d/sqrt(%d))/2" % (mul, div)
            if isnear((math.pi-math.atan(float(mul)/math.sqrt(div)))/2): return sign+"(pi-atan(%d/sqrt(%d)))/2" % (mul, div)
            if isnear(math.pi-math.atan(float(mul)/math.sqrt(div))/2): return sign+"(pi-atan(%d/sqrt(%d))/2)" % (mul, div)
            if isnear((math.pi+math.atan(float(mul)/math.sqrt(div)))/2): return sign+"(pi-atan(%d/sqrt(%d)))/2" % (mul, div)

    return str(num)

