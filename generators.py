#!/usr/bin/env python

import argparse
import timeit


def main(args):
    """

    :param args: LIST; like ['-p manual']
    :return: None
    """

    cli_args = return_parsed_args(args)

    squares_func_map = {
        'gen': gen_squares,
        'non-gen': fetch_squares,
        'class': SquaresIterator,
    }
    square_func = squares_func_map.get(cli_args.function, gen_squares)
    if cli_args.program == 'squares':
        if cli_args.timer is True:
            square_processor('time', square_func, cli_args.max)
        else:
            square_processor('print', square_func, cli_args.max)
    elif cli_args.program == 'log':
        process_log_file()
    elif cli_args.program == 'house':
        process_house_data()


def return_parsed_args(args):
    """Parse and define command line arguments.

    :param args: LIST; like ['-t 40']
    :return: OBJ; Namespace object looking something like this:
        Namespace(post=False, schedule=None, threshold=40)
    """

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('program', type=str, help="""Enter a program to run. 
                        Current choices:
                        \n* squares
                        \n* log
                        \n* house
                        """)
    parser.add_argument('-f', '--function', type=str, default='gen',
                        help="""Use with the 'squares' program to set the 
                        function type. Current choices:
                        \n* gen
                        \n* non-gen
                        \n* class
                        """)
    parser.add_argument('-m', '--max', type=int, default=5, help="""Use with the
                        'squares' program to set the maximum integer for which 
                        to return a square.
                        """)
    # parser.add_argument('-s', '--silent', action='store_false')
    parser.add_argument('-t', '--timer', action='store_true', help="""Use with 
                        the 'squares' program to return function run time.
                        """)

    return parser.parse_args(args)


# Create list of squares without using a generator:
def fetch_squares(max_root):
    squares = []
    for n in range(max_root):
        squares.append(n**2)
    return squares


# Use a class to generate squares:
class SquaresIterator:

    def __init__(self, max_root):
        self.max_root_value = max_root
        self.current_root_value = 0

    def __iter__(self):
        return self

    def __next__(self):
        if self.current_root_value >= self.max_root_value:
            raise StopIteration
        square_value = self.current_root_value ** 2
        self.current_root_value += 1
        return square_value


def return_squares_class(max_):
    for square in SquaresIterator(max_):
        return square


# Use a generator to produce squares:
def gen_squares(max_root):
    for num in range(max_root):
        yield num ** 2


def square_processor(op_, func, max_):
    return {
        'print': lambda: print_squares(func, max_),
        'time': lambda: print(timeit.timeit(
            f'{func.__name__}({max_})', f'from __main__ import {func.__name__}'
        )),
    }.get(op_, lambda: None)()


def print_squares(func, max_):
    for square in func(max_):
        print(square)
    print(f'Function used: {func.__name__}')


def timer(func, max_):
    runtime = timeit.timeit(
        f'{func.__name__}({max_})', f'from __main__ import {func.__name__}'
    )
    print(runtime)


def lines_from_file(path):
    with open(path) as handle:
        for line in handle:
            yield line.rstrip('\n')


def matching_lines(lines, pattern):
    for line in lines:
        if pattern in line:
            yield line


# Replaced by lines_from_file() and matching_lines()
# def matching_lines_from_file(path, pattern):
#     with open(path) as handle:
#         for line in handle:
#             if pattern in line:
#                 yield line.rstrip('\n')


def parse_log_records(lines):
    for line in lines:
        level, message = line.split(': ', 1)
        yield {'level': level, 'message': message}


def process_log_file():
    lines = lines_from_file('generator_log.txt')
    matches = matching_lines(lines, 'WARNING:')
    # log_lines = matching_lines_from_file('generator_log.txt', 'WARNING:')
    for record in parse_log_records(matches):
        print(record)


# def house_records(lines):
#     house = {}
#     for line in lines:
#         if 'address' in line:
#             house['address'] = line[line.find(' '):]
#         elif 'square_feet' in line:
#             house['square_feet'] = line[line.find(' '):]
#         elif 'price_usd' in line:
#             house['price_usd'] = line[line.find(' '):]
#         else:
#             yield house
#     yield house


# Book solution, using my variable names:
def house_records(lines):
    house = {}
    for line in lines:
        if line == '':
            yield house
            house = {}
            continue
        key, value = line.split(': ', 1)
        house[key] = value
    yield house


def process_house_data():
    lines_of_house_data = lines_from_file('generator_housedata.txt')
    houses = house_records(lines_of_house_data)
    for house in houses:
        print(house)
        # print(house['address'])


if __name__ == '__main__':
    import sys
    main(sys.argv[1:])
