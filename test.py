#!/usr/bin/env python3

# global define to guide the test
USE_SYSTEM_QUEUE = False
USE_BLOCK = True


from threading import (
        Thread,
        )


if USE_SYSTEM_QUEUE:
    from queue import (
            Queue,
            Full,
            Empty,
            )

else:
    from simple_queue import (
            SimpleQueue as Queue,
            Full,
            Empty,
            )


class TestParam:

    @classmethod
    def large(cls):
        return cls(
                total=30000000,
                q_size=123,
                prod_num=37,
                con_num=29,
                )

    @classmethod
    def small(cls):
        return cls(
                total=100000,
                q_size=10,
                prod_num=4,
                con_num=3,
                )

    @classmethod
    def tiny(cls):
        return cls(
                total=10,
                q_size=3,
                prod_num=2,
                con_num=2,
                )

    def __init__(self, total, q_size, prod_num, con_num):
        self.total = total
        self.q_size = q_size
        self.prod_num = prod_num
        self.con_num = con_num



class Producer(Thread):
    def __init__(self, queue, prod_range, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.prod_range = prod_range

    def run(self):
        total = 0
        for i in range(*self.prod_range):
            while True:
                try:
                    self.queue.put(i, USE_BLOCK)
                except Full:
                    continue
                else:
                    break
            total = total + 1
        print('thread', self.ident, 'produced', total)


class Consumer(Thread):
    def __init__(self, queue, con_range, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.should_con_count = con_range[1] - con_range[0]
        self.s = set()

    def run(self):
        total = 0
        while True:
            try:
                v = self.queue.get(USE_BLOCK)
            except Empty:
                continue
            self.s.add(v)
            total = total + 1
            if total == self.should_con_count:
                print('thread', self.ident, 'consume', total)
                break


class TE(Exception):
    pass


def divide_to_ranges(total, slots):
    if not total or not slots:
        raise TE('empty total or slots')
    return tuple(
            ((total*i)//slots, (total*(i+1))//slots) for i in range(0, slots))


def main():
    # tp = TestParam.small()
    # tp = TestParam.large()
    tp = TestParam.tiny()

    source_set = set(x for x in range(0, tp.total))
    queue = Queue(tp.q_size)

    producer_ranges = divide_to_ranges(tp.total, tp.prod_num)
    for r in producer_ranges:
        Producer(queue, r).start()

    consumer_ranges = divide_to_ranges(tp.total, tp.con_num)
    consumers = []
    for r in consumer_ranges:
        c = Consumer(queue, r)
        consumers.append(c)
        c.start()

    for c in consumers:
        c.join()

    target_set = set()
    for c in consumers:
        target_set.update(c.s)

    print('queue correctness passed', target_set == source_set)


if __name__ == '__main__':
    main()
