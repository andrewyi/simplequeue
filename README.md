THIS IS ABSOLUTLY A DEMO

My mates and I came across with queue.Queue in a project and I thought queue.Queue perfomanced very bad,
so I wrote this SimpleQueue to eliminate the overhead of queue.Queue.
Unfortunately I have no time to do benchmarks and this code became just a pity demo.

SimpleQueue use a list as internal buffer.
Conrrectness is asured by running test.py multiple times with multiple scale.
Performance test is not done yet, maybe I'll deal with it later.

"wrong_simple_queue.py" is a wrong implementation, keep it here for attention,
after I've check the source file of python queue (queue.py) I wrote the right code.
(it's really a shame that I never go deeper into the data structure implementations)

Thanks
