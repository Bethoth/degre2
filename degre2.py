from math import sqrt
from uuid import uuid4
import re
import yaml
import ctypes
import locale

DEFAULT = uuid4()

with open("config.yaml", "r") as yamlfile:
    data = yaml.load(yamlfile, Loader=yaml.FullLoader)

windll = ctypes.windll.kernel32
language = locale.windows_locale[windll.GetUserDefaultUILanguage()][:2]


def roots(a, b, c):
    delta = b ** 2 - 4 * a * c

    if delta > 0:
        x1 = (-b + delta ** 0.5) / (2 * a)
        x2 = (-b - delta ** 0.5) / (2 * a)

        return [x1, x2]

    elif delta == 0:
        x0 = -b / (2 * a)

        return [x0]

    else:
        return []


def fromDevelopedToCanonical(a, b, c):
    alpha = -b / (2 * a)
    beta = a * alpha ** 2 + b * alpha + c

    strAlpha = strBeta = strA = ""

    if alpha > 0:
        if alpha.is_integer():
            strAlpha = " - " + str(int(abs(alpha)))
        else:
            strAlpha = " - " + str(abs(alpha))
    elif alpha < 0:
        if alpha.is_integer():
            strAlpha = " + " + str(int(abs(alpha)))
        else:
            strAlpha = " + " + str(abs(alpha))
    else:
        strAlpha = " + " + str(int(abs(alpha)))

    if beta > 0:
        if beta.is_integer():
            strBeta = " + " + str(int(abs(beta)))
        else:
            strBeta = " + " + str(abs(beta))
    elif beta < 0:
        if beta.is_integer():
            strBeta = " - " + str(int(abs(beta)))
        else:
            strBeta = " - " + str(abs(beta))
    else:
        strBeta = " + " + str(int(abs(beta)))

    if a > 0:
        if a.is_integer():
            strA = str(int(abs(a)))
        else:
            strA = str(abs(a))
    elif a < 0:
        if a.is_integer():
            strA = "-" + str(int(abs(a)))
        else:
            strA = "-" + str(abs(a))
    else:
        strA = " + " + str(int(abs(a)))

    result = strA + "(x" + strAlpha + ")²" + strBeta

    return result


def fromDevelopedToFactorised(a, b, c):
    if len(roots(a, b, c)) == 0:
        return ""
    elif len(roots(a, b, c)) == 1:
        x1 = x2 = x0 = roots(a, b, c)[0]

        strA = strX0 = ""

        if x0 > 0:
            if x0.is_integer():
                strX0 = " - " + str(int(abs(x0)))
            else:
                strX0 = " - " + str(abs(x0))
        elif x0 < 0:
            if x0.is_integer():
                strX0 = " + " + str(int(abs(x0)))
            else:
                strX0 = " + " + str(abs(x0))
        else:
            strX0 = " + " + str(int(abs(x0)))

        if a > 0:
            if a.is_integer():
                strA = str(int(abs(a)))
            else:
                strA = str(abs(a))
        elif a < 0:
            if a.is_integer():
                strA = "-" + str(int(abs(a)))
            else:
                strA = "-" + str(abs(a))
        else:
            strA = " + " + str(int(abs(a)))

        result = strA + "(x" + strX0 + ")²"

        return result
    elif len(roots(a, b, c)) == 2:
        x1, x2 = roots(a, b, c)[0], roots(a, b, c)[1]

        strA = strX1 = strX2 = ""

        if x1 > 0:
            if x1.is_integer():
                strX1 = " - " + str(int(abs(x1)))
            else:
                strX1 = " - " + str(abs(x1))
        elif x1 < 0:
            if x1.is_integer():
                strX1 = " + " + str(int(abs(x1)))
            else:
                strX1 = " + " + str(abs(x1))
        else:
            strX1 = " + " + str(int(abs(x1)))

        if x2 > 0:
            if x2.is_integer():
                strX2 = " - " + str(int(abs(x2)))
            else:
                strX2 = " - " + str(abs(x2))
        elif x2 < 0:
            if x2.is_integer():
                strX2 = " + " + str(int(abs(x2)))
            else:
                strX2 = " + " + str(abs(x2))
        else:
            strX2 = " + " + str(int(abs(x2)))

        if a > 0:
            if a.is_integer():
                strA = str(int(abs(a)))
            else:
                strA = str(abs(a))
        elif a < 0:
            if a.is_integer():
                strA = "-" + str(int(abs(a)))
            else:
                strA = "-" + str(abs(a))
        else:
            pass

        result = strA + "(x" + strX1 + ")(x" + strX2 + ")"
        return result


def fromCanonicalToDeveloped(a, alpha, beta):
    b = -2 * a * alpha
    c = a * (0 - alpha) ** 2 + beta

    strA = strB = strC = ""

    if a.is_integer():
        strA = str(int(a)) + "x²"
    else:
        strA = str(a) + "x²"

    if b > 0:
        if b.is_integer():
            strB = " + " + str(int(b)) + "x"
        else:
            strB = " + " + str(b) + "x"
    elif b < 0:
        if b.is_integer():
            strB = " - " + str(int(abs(b))) + "x"
        else:
            strB = " - " + str(abs(b)) + "x"
    else:
        strB = " + " + str(int(abs(b)))

    if c > 0:
        if c.is_integer():
            strC = " + " + str(int(c))
        else:
            strC = " + " + str(c)
    elif c < 0:
        if c.is_integer():
            strC = " - " + str(int(abs(c)))
        else:
            strC = " - " + str(abs(c))
    else:
        strC = " + " + str(int(abs(c)))

    result = strA + strB + strC

    return result


def fromCanonicalToFactorised(a, alpha, beta):
    if -beta / a >= 0:
        x1 = sqrt(-beta / a) + alpha
        x2 = -sqrt(-beta / a) + alpha
        x0 = 0
        if x1 == x2:
            x0 = x1

            strX0 = ""
            if x0 > 0:
                if x0.is_integer():
                    strX0 = " - " + str(int(abs(x0)))
                else:
                    strX0 = " - " + str(abs(x0))
            elif x0 < 0:
                if x0.is_integer():
                    strX0 = " + " + str(int(abs(x0)))
                else:
                    strX0 = " + " + str(abs(x0))
            else:
                strX0 = " + " + str(int(abs(x0)))

            if a.is_integer():
                result = str(int(a)) + "(x" + strX0 + ")²"
            else:
                result = str(a) + "(x" + strX0 + ")²"

            return result

        else:
            strX1 = strX2 = ""

            if x1 > 0:
                if x1.is_integer():
                    strX1 = " - " + str(int(abs(x1)))
                else:
                    strX1 = " - " + str(abs(x1))
            elif x1 < 0:
                if x1.is_integer():
                    strX1 = " + " + str(int(abs(x1)))
                else:
                    strX1 = " + " + str(abs(x1))
            else:
                strX1 = " + " + str(int(abs(x1)))

            if x2 > 0:
                if x2.is_integer():
                    strX2 = " - " + str(int(abs(x2)))
                else:
                    strX2 = " - " + str(abs(x2))
            elif x2 < 0:
                if x2.is_integer():
                    strX2 = " + " + str(int(abs(x2)))
                else:
                    strX2 = " + " + str(abs(x2))
            else:
                strX2 = " + " + str(int(abs(x2)))

            if a.is_integer():
                result = str(int(a)) + "(x" + strX1 + ")(x" + strX2 + ")"
            else:
                result = str(a) + "(x" + strX1 + ")(x" + strX2 + ")"

            return result
    else:
        return ""


def fromFactorisedToDeveloped(a, x1 = DEFAULT, x2 = DEFAULT, x0 = DEFAULT):
    if x1 is DEFAULT and x2 is DEFAULT and x0 is not DEFAULT:
        b = a * 2 * x0
        c = a * x0 ** 2

        strB = strC = ""

        if b > 0:
            if b.is_integer():
                strB = " + " + str(int(abs(b))) + "x"
            else:
                strB = " + " + str(abs(b)) + "x"
        elif b < 0:
            if b.is_integer():
                strB = " - " + str(int(abs(b))) + "x"
            else:
                strB = " - " + str(abs(b)) + "x"
        else:
            strB = " + " + str(int(abs(b)))

        if c > 0:
            if c.is_integer():
                strC = " + " + str(int(abs(c)))
            else:
                strC = " + " + str(abs(c))
        elif c < 0:
            if c.is_integer():
                strC = " - " + str(int(abs(c)))
            else:
                strC = " - " + str(abs(c))
        else:
            strC = " + " + str(int(abs(c)))

        if a.is_integer():
            result = str(int(a)) + "x²" + strB + strC
            return result
        else:
            result = str(a) + "x²" + strB + strC
            return result
    elif x0 is DEFAULT and x1 is not DEFAULT and x2 is not DEFAULT:
        b = a * (x1 + x2)
        c = a * x1 * x2

        strB = strC = ""

        if b > 0:
            if b.is_integer():
                strB = " + " + str(int(abs(b))) + "x"
            else:
                strB = " + " + str(abs(b)) + "x"
        elif b < 0:
            if b.is_integer():
                strB = " - " + str(int(abs(b))) + "x"
            else:
                strB = " - " + str(abs(b)) + "x"
        else:
            strB = " + " + str(int(abs(b))) + "x"
                
        if c > 0:
            if c.is_integer():
                strC = " + " + str(int(abs(c)))
            else:
                strC = " + " + str(abs(c))
        elif c < 0:
            if c.is_integer():
                strC = " - " + str(int(abs(c)))
            else:
                strC = " - " + str(abs(c))
        else:
            strC = " + " + str(int(abs(c)))
        
        if a.is_integer():
            result = str(int(a)) + "x²" + strB + strC
            return result
        else:
            result = str(a) + "x²" + strB + strC
            return result


def fromFactorisedToCanonical(developedForm):
    trinomial = re.sub(" ", "", developedForm)

    a = float(trinomial[:trinomial.find("x²")])
    trinomial = trinomial[trinomial.find("²") + 1:]

    b = float(trinomial[:trinomial.find("x")])
    trinomial = trinomial[trinomial.find("x") + 1:]

    c = float(trinomial)

    canonicalForm = fromDevelopedToCanonical(a, b, c)
    return canonicalForm


print(data[0][language]['1'])
print(data[0][language]['2'])
print(data[0][language]['3'])
print(data[0][language]['4'])
print(data[0][language]['5'])


trinomial = input(data[0][language]['6'])

if trinomial[-1] == "d":
    trinomial = baseTrinomial = trinomial[:-1]

    a = float(trinomial[:trinomial.find("x²")])
    trinomial = trinomial[trinomial.find("²") + 1:]

    b = float(trinomial[:trinomial.find("x")])
    trinomial = trinomial[trinomial.find("x") + 1:]

    c = float(trinomial)

    canonicalForm = fromDevelopedToCanonical(a, b, c)
    factorisedForm = fromDevelopedToFactorised(a, b, c)

    print(data[0][language]['d1'] + baseTrinomial)
    print(data[0][language]['d2'] + canonicalForm)
    print(data[0][language]['d3'] + factorisedForm)

elif trinomial[-1] == "c":
    trinomial = baseTrinomial = trinomial[:-1]

    a = float(trinomial[:trinomial.find("(")])
    trinomial = trinomial[trinomial.find("x") + 1:]

    alpha = -float(trinomial[:trinomial.find(")")])
    trinomial = trinomial[trinomial.find("²") + 1:]

    beta = float(trinomial)

    developedForm = fromCanonicalToDeveloped(a, alpha, beta)
    factorisedForm = fromCanonicalToFactorised(a, alpha, beta)

    print(data[0][language]['c1'] + baseTrinomial)
    print(data[0][language]['c2'] + developedForm)
    print(data[0][language]['c3'] + factorisedForm)

elif trinomial[-1] == "f" and trinomial[-1] + trinomial[-2] != "ff":
    trinomial = baseTrinomial = trinomial[:-1]

    a = float(trinomial[:trinomial.find("(")])
    trinomial = trinomial[trinomial.find("x") + 1:]

    x0 = float(trinomial[:trinomial.find(")")])

    developedForm = fromFactorisedToDeveloped(a, x0=x0)
    canonicalForm = fromFactorisedToCanonical(developedForm)

    print(data[0][language]['f1'] + baseTrinomial)
    print(data[0][language]['f2'] + developedForm)
    print(data[0][language]['f3'] + canonicalForm)

elif trinomial[-1] + trinomial[-2] == "ff":
    trinomial = baseTrinomial = trinomial[:-1]
    trinomial = baseTrinomial = trinomial[:-1]

    a = float(trinomial[:trinomial.find("(")])
    trinomial = trinomial[trinomial.find("x") + 1:]

    x1 = float(trinomial[:trinomial.find(")")])
    trinomial = trinomial[trinomial.find("x") + 1:]

    x2 = float(trinomial[:trinomial.find(")")])

    developedForm = fromFactorisedToDeveloped(a, x1, x2)
    canonicalForm = fromFactorisedToCanonical(developedForm)

    print(data[0][language]['ff1'] + baseTrinomial)
    print(data[0][language]['ff2'] + developedForm)
    print(data[0][language]['ff3'] + canonicalForm)
