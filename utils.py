# This Python file uses the following encoding: utf-8


def num(s):
    try:
        return int(s)
    except ValueError:
        return float(s)


def integerify(iterable):
    return [int(i) for i in iterable]


def floatify(iterable):
    return [float(i) for i in iterable]


def numberify(iterable):
    return [num(i) for i in iterable]


# if__name__ == "__main__":
#     pass
