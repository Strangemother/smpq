# The threaded handler should run in the background when needed
# Given a call function, a queue generates theads. The threads
# parse the queue until completion.
# When complete the thread handler will call the function
#
# If the thread pool exists, the new items are appnded to the queue.
#
# If  a pool does not exist, a new thread pool is started. The thread pool
# stays alive until all items are complete, closing down and returning the
# result.

from multiprocessing import Process, JoinableQueue
import time

class ProcessQueue(object):

    def __init__(self, handler=None):
        self.create()
        self.handler = handler

    def create(self):
        self.queue = JoinableQueue()
        self.process = None
        self.started = False
        self.done = False

    def status(self):
        v = {
            'length': self.queue_len(),
            'is_alive': self.is_alive(),
        }

        return v

    def start(self, data):
        '''
        Provide a value to add to the process queue.
        Returns Tuple: (new pool<Boolean>, size<int>)
        '''
        self.append(data)
        new_inst = self.begin_process()
        return (new_inst, self.queue_len())

    def append(self, data):
        '''
        Add the element to the queue
        '''
        self.queue.put(data, False)

    def queue_len(self):
        '''
        Return the size of the queue
        '''
        return self.queue.qsize()

    def __len__(self):
        return self.queue_len()

    def is_alive(self):
        '''
        Return True if an active process exists else returns False
        '''
        if self.process is not None and self.process.is_alive() is True:
            return True
        return False

    def begin_process(self):
        '''
        Start the process if it's not alive. Return True if a new process is
        started, return False if a process exists.
        Add data to the process queue using `append`
        '''
        '''
        Begin the processing pool
        '''

        if self.is_alive() is True:
            return False

        self.process = Process(target=self.thread_process,
                               args=(self.queue,),
                               kwargs=dict(handler=self.handler)
                               )
        self.process.start()
        return True

    def thread_process(self, queue, handler):
        '''
        Function runs within a process, isolated from the main application.
        '''
        self.loop_count = 0

        while queue.empty() is False:
            v = queue.get()

            while v:
                item = v.pop()
                handler(item)

                self.loop_count += 1

            queue.task_done()
        self.done = True

    def stop(self):
        '''
        terminate the pool process. Called after processing is complete.
        This can be called manually, terminating the processing instantly.
        '''
        print 'stop command'
        if self.is_alive():
            print 'terminate'
            self.process.terminate()
            time.sleep(.1)
        print 'alive:', self.is_alive(), self.process.is_alive()
        return (not self.is_alive())
