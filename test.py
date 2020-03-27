from threading import (
        Thread,
        )
'''
from queue import (
        Queue,
        Full,
        Empty,
        )
'''
from simple_queue import (
        SimpleQueue as Queue,
        Full,
        Empty,
        )


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
                    self.queue.put(i)
                except Full:
                    continue
                else:
                    # print('thread', self.ident, 'put', i)
                    break
            total = total + 1
        print('thread', self.ident, 'produced', total)


class Consumer(Thread):
    def __init__(self, queue, consume_range, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queue = queue
        self.consume_count = consume_range[1] - consume_range[0]
        self.s = set()

    def run(self):
        total = 0
        while True:
            try:
                v = self.queue.get()
            except Empty:
                continue
            # print('thread', self.ident, 'get', v)
            self.s.add(v)
            total = total + 1
            if total == self.consume_count:
                print('thread', self.ident, 'consume', total)
                break


class TE(Exception):
    pass


def divide_to_slots(total, slots):
    if not total or not slots:
        raise TE('empty total or slots')
    return tuple(
            ((total*i)//slots, (total*(i+1))//slots) for i in range(0, slots))


def main():
    if False:
        total_count = 30000000
        queue_size = 100
        producer_count = 10
        consumer_count = 5
    else:
        total_count = 2000000
        queue_size = 50
        producer_count = 8
        consumer_count = 7

    source_set = set(x for x in range(0, total_count))
    queue = Queue(queue_size)

    producer_slots = divide_to_slots(total_count, producer_count)
    index = 0
    for r in producer_slots:
        index = index + 1
        Producer(queue, r).start()

    consumer_slots = divide_to_slots(total_count, consumer_count)
    consumers = []
    index = 0
    for r in consumer_slots:
        index = index + 1
        c = Consumer(queue, r)
        consumers.append(c)
        c.start()

    for c in consumers:
        c.join()

    target_set = set()
    for c in consumers:
        target_set.update(c.s)

    print(target_set == source_set)

if __name__ == '__main__':
    main()
