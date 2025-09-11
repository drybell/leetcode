"""

Symbol	Value
I	1
V	5
X	10
L	50
C	100
D	500
M	1000

Roman numerals are formed by appending the conversions of decimal place values from highest to lowest. Converting a decimal place value into a Roman numeral has the following rules:

If the value does not start with 4 or 9, select the symbol of the maximal value that can be subtracted from the input, append that symbol to the result, subtract its value, and convert the remainder to a Roman numeral.
If the value starts with 4 or 9 use the subtractive form representing one symbol subtracted from the following symbol, for example, 4 is 1 (I) less than 5 (V): IV and 9 is 1 (I) less than 10 (X): IX. Only the following subtractive forms are used: 4 (IV), 9 (IX), 40 (XL), 90 (XC), 400 (CD) and 900 (CM).
Only powers of 10 (I, X, C, M) can be appended consecutively at most 3 times to represent multiples of 10. You cannot append 5 (V), 50 (L), or 500 (D) multiple times. If you need to append a symbol 4 times use the subtractive form.
Given an integer, convert it to a Roman numeral.

Example 1.
Input: num = 3749

Output: "MMMDCCXLIX"

Explanation:

3000 = MMM as 1000 (M) + 1000 (M) + 1000 (M)
 700 = DCC as 500 (D) + 100 (C) + 100 (C)
  40 = XL as 10 (X) less of 50 (L)
   9 = IX as 1 (I) less of 10 (X)
Note: 49 is not 1 (I) less of 50 (L) because the conversion is based on decimal places

Example 2:

Input: num = 58

Output: "LVIII"

Explanation:

50 = L
 8 = VIII


Example 3:

Input: num = 1994

Output: "MCMXCIV"

Explanation:

1000 = M
 900 = CM
  90 = XC
   4 = IV

Naive:

Given a number, attempt to divide by the breakpoints
specified by the translation table until > 1 is reached.

we iterate through the number until:
    * the remainder is 0
    * the value is 1

Number: 1994

1994 // 1000 -> M
    Value: 1
    Remainder: 994

994 // 900   -> CM
    Value: 1
    Remainder: 94

94 // 90     -> XC
    Value: 1
    Remainder: 4

4 // 4       -> IV
    Value: 1
    Remainder: 0

"""

def int_to_roman(num):
    roman_table = {
        1000:  "M"
        , 900: "CM"
        , 800: "DCCC"
        , 700: "DCC"
        , 600: "DC"
        , 500: "D"
        , 400: "CD"
        , 300: "CCC"
        , 200: "CC"
        , 100: "C"
        , 90:  "XC"
        , 80:  "LXXX"
        , 70:  "LXX"
        , 60:  "LX"
        , 50:  "L"
        , 40:  "XL"
        , 30:  "XXX"
        , 20:  "XX"
        , 10:  "X"
        , 9:   "IX"
        , 8:   "VIII"
        , 7:   "VII"
        , 6:   "VI"
        , 5:   "V"
        , 4:   "IV"
        , 3:   "III"
        , 2:   "II"
        , 1:   "I"
    }

    subsets = {
        1000: {
            900: "CM"
            , 800: "DCCC"
            , 700: "DCC"
            , 600: "DC"
        }
        , 500: {
            400: "CD"
            , 300: "CCC"
            , 200: "CC"
        }
        , 100: {
            90:  "XC"
            , 80:  "LXXX"
            , 70:  "LXX"
            , 60:  "LX"
        }
        , 50: {
            40:  "XL"
            , 30:  "XXX"
            , 20:  "XX"
        }
        , 10: {
            9:   "IX"
            , 8:   "VIII"
            , 7:   "VII"
            , 6:   "VI"
        }
        , 5: {
            4:   "IV"
            , 3:   "III"
            , 2:   "II"
        }
    }

    breakpoints = [
        (1000,  "M")
        , (900, "CM")
        , (500, "D")
        , (400, "CD")
        , (100, "C")
        , (90,  "XC")
        , (50,  "L")
        , (40,  "XL")
        , (10,  "X")
        , (9,   "IX")
        , (5,   "V")
        , (4,   "IV")
        , (1,   "I")
    ]

    def get_table(value):
        for d, t in breakpoints:
            if d <= value:
                return (d, t)

    def translate(value, letters):
        if value == 0:
            return letters

        divisor, translation = get_table(value)

        return translate(
            value % divisor
            , letters + ((value // divisor) * translation)
        )

    return translate(num, "")

    value = num

    TERMINATOR = 10000
    iters      = 0

    letters = ""

    if value == 1:
        return "I"

    while (
        value != 1
        and iters < TERMINATOR
    ):
        for divisor, translation in breakpoints.items():
            if value < divisor:
                continue

            v, r = value // divisor, value % divisor
            value = r

            letters += v * translation

        iters += 1

    return letters

test = [
    int_to_roman(3749)
    , int_to_roman(58)
    , int_to_roman(1994)
    , int_to_roman(843)
]

