#!/usr/bin/env python3
import sys
from operator import add, sub, mul, truediv

USAGE = "Usage: python3 calculator.py <num1> <op> <num2>"

def main(args):
    if len(args) != 3:
        print(USAGE)
        return
    a, op, b = args
    try:
        a = float(a)
        b = float(b)
    except ValueError:
        print("Numbers must be valid.")
        return
    operations = {
        '+': add,
        '-': sub,
        '*': mul,
        '/': truediv,
    }
    if op not in operations:
        print(f"Unknown operator {op}")
        return
    result = operations[op](a, b)
    # Show integer results without decimal point
    if isinstance(result, float) and result.is_integer():
        result = int(result)
    print(result)

if __name__ == "__main__":
    main(sys.argv[1:])
