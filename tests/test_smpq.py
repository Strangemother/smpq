import unittest2 as unittest
from mock import patch
from smpq import ProcessQueue
from multiprocessing import Process, JoinableQueue
import time


def handler(item):
    time.sleep(3)


class ProcessQueueTestCase(unittest.TestCase):

    @patch('smpq.ProcessQueue.create')
    def test_create(self, create):
        '''
        Create is called on __init__
        '''
        ProcessQueue()
        create.assert_called_once_with()

    def test_create_params(self):
        pq = ProcessQueue()
        self.assertIsNone(pq.process)
        self.assertEqual(pq.started, False)
        self.assertEqual(pq.done, False)

    def test_status(self):
        r = {'length': 0, 'is_alive': False}
        pq = ProcessQueue()
        self.assertDictEqual(r, pq.status())

    def test_append(self):

        pq = ProcessQueue()
        pq.append([2, 6])
        self.assertDictEqual(pq.status(), {'length': 1, 'is_alive': False})
        pq.append([2, 6])
        self.assertDictEqual(pq.status(), {'length': 2, 'is_alive': False})

    def test_queue_length(self):
        pq = ProcessQueue()
        pq.append([2, 6])
        pq.append([2, 6])
        self.assertDictEqual(pq.status(), {'length': 2, 'is_alive': False})
        self.assertEqual(len(pq), 2)
        self.assertEqual(pq.queue_len(), 2)
        self.assertEqual(pq.queue.qsize(), 2)

    def test_is_alive(self):
        pq = ProcessQueue()
        self.assertFalse(pq.is_alive())

        pq.start([1,2])
        self.assertTrue(pq.is_alive())
        pq.stop()
        self.assertFalse(pq.is_alive())

    def test_stop(self):
        pq = ProcessQueue()
        self.assertFalse(pq.is_alive())

        pq.start([1])
        ret = pq.stop()
        self.assertTrue(ret)
        self.assertFalse(pq.is_alive())

    def test_begin_process(self):
        pq = ProcessQueue()

        global handler

        pq.handler = handler
        pq.append([1])
        ret = pq.begin_process()
        self.assertTrue(ret)
        self.assertIsNotNone(pq.process)
        self.assertTrue(pq.is_alive())
        pq.stop()

    def test_begin_process_restart(self):
        pq = ProcessQueue()

        global handler

        pq.handler = handler
        pq.append([1])
        ret = pq.begin_process()
        self.assertTrue(ret)
        ret = pq.begin_process()
        self.assertFalse(ret)
        pq.stop()

    def test_done(self):
        global handler
        pq = ProcessQueue(handler)
        pq.start([])
        time.sleep(.1)

