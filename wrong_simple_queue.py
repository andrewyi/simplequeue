#!/usr/bin/env python3

'''
simple queue implementation
'''

from threading import (
        Lock,
        Condition,
        get_ident,
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

        self.l = Lock()
        self._r_l = Lock()
        self._w_l = Lock()
        self.r_c = Condition(self._r_l)
        self.w_c = Condition(self._w_l)

    def _get_no_lock(self):
        if self.empty:
            raise Empty()

        v = self.q[self.ri]
        self.ri = self.ri + 1
        if self.ri == self.size:
            self.ri = 0

        if self.ri == self.wi:
            self.empty = True

        if self.full:
            self.full = False
            print('get', get_ident(), 'w_c notify', 'w_c is locked', self._w_l.locked())
            self.w_c.acquire()
            self.w_c.notify_all()
            self.w_c.release()
            print('get', get_ident(), 'w_c notified')

        return v

    def _get_locked(self, block):
        print('get', get_ident(), 'l acquire', 'l is locked', self.l.locked())
        self.l.acquire()
        print('get', get_ident(), 'l acquired')
        v = None

        try:
            v = self._get_no_lock()

        except Empty:
            if block:
                print('get', get_ident(), 'r_c acquire', 'r_c locked', self._r_l.locked())
                self.r_c.acquire()
                print('get', get_ident(), 'r_c acquired')
            raise

        finally:
            self.l.release()
            print('get', get_ident(), 'l released')

        return v

    def get(self, block=True):
        is_wait = False

        while True:
            try:
                v = self._get_locked(block)

            except Empty:
                if block:
                    is_wait = True
                    print('get', get_ident(), 'r_c wait')
                    self.r_c.wait()
                    print('get', get_ident(), 'r_c waited')
                    continue

                else:
                    raise

            else:
                if is_wait:
                    self.r_c.release()
                    print('get', get_ident(), 'r_c released')

                print('get', get_ident(), 'successfully')
                return v

    def _put_no_lock(self, v):
        if self.full:
            raise Full()

        self.q[self.wi] = v
        self.wi = self.wi + 1
        if self.wi == self.size:
            self.wi = 0

        if self.wi == self.ri:
            self.full = True

        if self.empty:
            self.empty = False
            print('put', get_ident(), 'r_c notify', 'r_c locked', self._r_l.locked())
            self.r_c.acquire()
            self.r_c.notify_all()
            self.r_c.release()
            print('put', get_ident(), 'r_c notified')

    def _put_locked(self, v, block):
        print('put', get_ident(), 'l acquire', 'l is locked', self.l.locked())
        self.l.acquire()
        print('put', get_ident(), 'l acquired')

        try:
            self._put_no_lock(v)

        except Full:
            if block:
                print('put', get_ident(), 'w_c acquire', 'w_c locked', self._w_l.locked())
                self.w_c.acquire()
                print('put', get_ident(), 'w_c acquired')
            raise

        finally:
            self.l.release()
            print('put', get_ident(), 'l released')

    def put(self, v, block=True):
        is_wait = False

        while True:
            try:
                self._put_locked(v, block)

            except Full:
                if block:
                    is_wait = True
                    print('put', get_ident(), 'w_c wait')
                    self.w_c.wait()
                    print('put', get_ident(), 'w_c waited')
                    continue

                else:
                    raise

            else:
                if is_wait:
                    self.w_c.release()
                    print('put', get_ident(), 'w_c released')
                print('put', get_ident(), 'successfully')
                return
