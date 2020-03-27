#!/usr/bin/env python3

'''
simple queue implementation
'''

from threading import (
        Lock,
        Condition,
        )


class Full(Exception):
    pass


class Empty(Exception):
    pass


class SimpleQueue:


    def __init__(self, size):
        self.size = size
        self.q = [None] * size
        self.ri = 0
        self.wi = 0
        self.full = False
        self.empty = True

        self._l = Lock()
        self.cond = Condition(self._l)

    def get(self, block=True):
        self.cond.acquire()
        v = None

        try:
            if self.empty:
                if not block:
                    raise Empty()
                else:
                    while True:
                        self.cond.wait()
                        if not self.empty:
                            break

            v = self.q[self.ri]
            self.ri = self.ri + 1
            if self.ri == self.size:
                self.ri = 0

            if self.ri == self.wi:
                self.empty = True

            if self.full:
                self.full = False
                self.cond.notify_all()

        finally:
            self.cond.release()

        return v

    def put(self, v, block=True):
        self.cond.acquire()
        try:
            if self.full:
                if not block:
                    raise Full()
                else:
                    while True:
                        self.cond.wait()
                        if not self.full:
                            break

            self.q[self.wi] = v
            self.wi = self.wi + 1
            if self.wi == self.size:
                self.wi = 0

            if self.wi == self.ri:
                self.full = True

            if self.empty:
                self.empty = False
                self.cond.notify_all()

        finally:
            self.cond.release()
