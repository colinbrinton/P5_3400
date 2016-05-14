# AUTHOR: Colin Brinton
# FILENAME: P3.py
# DATE: 04/22/2016
# REVISION HISTORY: 1.0

# DESCRIPTION:
# This program finds all prices in a provided file that adhere to a valid format. A valid format is defined as a price
# that starts with a non-zero integer, followed optionally by 5 more digits, followed optionally by cents. The price
# may have a comma separating the thousands from the hundreds. The comma may be omitted and still be valid. The cents
# portion must be separated by a dot and contain exactly two digits. After finding all the valid prices using the
# regular expression defined below, the program outputs the valid prices into three predetermined files.
# bucks.txt will contain all the valid prices that take the form $x
# sale.txt will contain all the valid prices that that the form $x.99
# misc.txt will contain all other valid prices. i.e. prices that have a cents portion other than .99

# ASSUMPTIONS:
# It is assumed that all prices will be less than $999,999.99, prices larger than this will be rejected
# It is assumed that the user wants the prices formatted with a comma separating the hundreds and thousands in the
#      output file, regardless of the original format
# It is assumed that prices may be valid without commas. i.e. $5678 is equivalent to $5,678
# It is assumed that the user wants their files named 'bucks.txt', 'sale.txt', 'misc.txt'
# It is assumed that deliminators between prices will not be a digit, dot or comma
# It is also assumed that no valid price will be immediately followed by a dot or comma

from re import compile, X
from sys import argv, exit

FILE = 1
THOUSANDS = 0
HUNDREDS = 1
CENTS = 2
SALE = '.99'
OUTPUT1 = 'bucks.txt'
OUTPUT2 = 'sale.txt'
OUTPUT3 = 'misc.txt'
PREFIX = '$'
DELIM = '\n'
SEPARATOR = ','
EMPTY = ''

try:
    f = open(argv[FILE], 'r')
    string = f.read()
    f.close()
except IndexError:
    print('Pass a text files as a command line argument:')
    print('P3.py <file1>.txt')
    exit()

price = compile(r"""
                     \$              # Start of a valid price signified by dollar sign
                                     # First capturing group:
                     ([1-9]\d{0,2})  #     Price must start with a non-zero digit, followed optionally by
                                     #     one or two other digits
                                   # Optional comma for thousands formatting
                                     # Second capturing group:
                     ((?:,\d{3})*)        #     Optional three more digits to support prices up to $999,999
                                     # Third capturing group:
                     (\.\d\d)?       #     The cent portion of the price is optional, one dot and two any digits match
                                     # Negative Lookahead:
                     (?![\d])      #     Reject the price if the cent portion has an extra digit, dot or comma """, X)

# Find all valid prices
valid_prices = price.findall(string)
print(valid_prices)

# Find prices in $x format, output prices to bucks file
bucks = [price for price in valid_prices if not price[CENTS]]
b = open(OUTPUT1, 'w')
for price in bucks:
    b.write(PREFIX)
    b.write(price[THOUSANDS])
    if price[HUNDREDS] != EMPTY:
        b.write(SEPARATOR)
        b.write(price[HUNDREDS])
    b.write(DELIM)
b.close()

# Find prices in $x.99 format, output prices to sale file
sale = [price for price in valid_prices if price[CENTS] == SALE]
s = open(OUTPUT2, 'w')
for price in sale:
    s.write(PREFIX)
    s.write(price[THOUSANDS])
    if price[HUNDREDS] != EMPTY:
        s.write(SEPARATOR)
        s.write(price[HUNDREDS])
    s.write(price[CENTS])
    s.write(DELIM)
s.close()

# Find all other prices, output to misc file
misc = [price for price in valid_prices if price not in bucks and price not in sale]
m = open(OUTPUT3, 'w')
for price in misc:
    m.write(PREFIX)
    m.write(price[THOUSANDS])
    if price[HUNDREDS] != EMPTY:
        m.write(SEPARATOR)
        m.write(price[HUNDREDS])
    m.write(price[CENTS])
    m.write(DELIM)
m.close()