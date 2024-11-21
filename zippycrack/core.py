from multiprocessing import Process, Queue
import sys

# Constants
ROUND_ROBIN = 1
EXIT_ = 77777  # Marker for thread termination

# Class definition
class zippycrack:
    def __init__(self, func, passfile, numthreads=4, cont=False, mode=ROUND_ROBIN):
        self.func = func
        self.passfile = passfile
        self.numthreads = numthreads
        self.cont = cont
        self.mode = mode
        self.printqueue = Queue()

    def worker_thread(self, queue, tid):
        while True:
            pwd = queue.get()
            if pwd == EXIT_:
                self.printqueue.put(f"_EXIT_ {tid}")
                break
            if self.func(pwd):
                self.printqueue.put(f"Thread {tid} found a match: {pwd}")
                if not self.cont:
                    for q in self.queues:
                        q.put(EXIT_)
                    return

    def run(self):
        self.threads = []
        self.queues = []
        for i in range(self.numthreads):
            nq = Queue()
            self.queues.append(nq)
            th = Process(target=self.worker_thread, args=(self.queues[i], i))
            th.start()
            self.threads.append(th)

        with open(self.passfile, 'r', encoding='utf-8', errors='ignore') as pfile:
            if self.mode == ROUND_ROBIN:
                current = 0
                for line in pfile:
                    pwd = line.strip()
                    self.queues[current].put(pwd)
                    current = (current + 1) % self.numthreads

        for q in self.queues:
            q.put(EXIT_)

        runningt = [True] * self.numthreads
        passes = []
        while True in runningt:
            n = self.printqueue.get()
            if '_EXIT_' in n:
                runningt[int(n.split()[-1])] = False
            else:
                if "match: " in n:
                    passes.append(n.split('match: ', 1)[-1])
                print(n)

        for th in self.threads:
            th.join()

        print("Done")
        return passes
