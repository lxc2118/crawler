#!/usr/bin/env python
# coding=utf-8
import os

def func(n):
    print n


def decorator(func):
    def a_test():
        print 222
    return a_test


@decorator
def test():
    print 1


if __name__ == "__main__":
    a,b,c = os.path.walk("/root/")
    print c