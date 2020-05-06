THIS IS ABSOLUTLY A DEMO

My mates and I came across with queue.Queue in a project and I thought queue.Queue perfomanced very badly,
so I wrote this SimpleQueue to eliminate the overhead of queue.Queue.
Unfortunately I have no time to do benchmarks and this code became just a pity demo.

SimpleQueue uses a list as internal buffer.
Correctness is assured by running test.py multiple times with different kinds of scales.
Performance benchmark is not done yet, maybe I'll deal with it later.

"wrong_simple_queue.py" is a wrong implementation, keep it here for attention,
after I've check the source file of python queue (queue.py) I wrote the right code.
(it's really a shame that I never go deeper into the data structure implementations)

Thanks
