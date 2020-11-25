#!/usr/bin/env python

s = 'The quick brown fox jumped over the lazy brown dog.'


def words_in(text):
    start = 0
    end = text.find(" ")
    while end > 0:
        yield text[start:end]
        start = end + 1
        end = text.find(" ", start)
    yield text[start:]


for word in words_in(s):
    print(word)
# print(s.find(" ", 16))


# def fibonacci_numbers(nums):
#     x, y = 0, 1
#     for _ in range(nums):
#         x, y = y, x+y
#         yield x
