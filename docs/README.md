# Python Simple Multiprocessing Queue

Handling information in another process is boring. Using another thread to work your data is fun.

Simple Multiprocessing Queue or SMQ is a `Queue` built into a `multiprocess`. You fill a queue, `smq` will handle a process.

### Highlights

+ Always handle your queue within a process, ignoring the need to handle the process
+ Provide real _non-blocking_ utilies for web frameworks _(tornado, django...)_
+ Well-behaved handling of a `multiprocessing.Process` not a `Thread` type.
+ Extremely lightweight.
+ No framework, no dependencies, no data-wrangling.

## Getting Started

`smq` has no dependencies. Import `smq.ProcessQueue` and give it a function.

Install `smpq` from `pip`
```py
$> pip install smpq
```

```py
from smq import ProcessQueue
import time

def process_item(item):
    time.sleep(1)

pq = ProcessQueue(process_item)
```

The `ProcessQueue` requires a `start([])` with a list of _stuff_.

```py
items = [
    {}, {}, {}
]

new_instance, queue_length = pq.start(items)
```

Keep calling `start` with additional items to process.

```py
item = ['dave', 'mike', 'eric']
new_instance, queue_length = pq.start(items)
print 'new instance:', new_instance

item = ['kevin', 'bernard', 'simon']
new_instance, queue_length = pq.start(items)
print 'new instance:', new_instance
```

Each call to `start`, appends to process queue. If a `Process` does not exist, a new instance is created.

The process lives until all items within the list are complete. Once done the process will silently die.

If you call `start()`, a new process instance is created.


### Understanding

It's that simple. Call `ProcessQueue.start` when required and your elements are handled on a different core.

The module utilizes the `multiprocessing` `Process` and `JoinableQueue`. A `ProcessQueue` will spawn one `Process`.

Every instance of `ProcessQueue` is a new multiprocess thread. You should care for this manually.


You don't need to worry about the processing or the queue. Adding items to `start([])` will manage the thread safely.


### Things To Remember

Enough is extrapolated to provide a quick prototype layer and a cheap extendable class, but you're still handling process and interfacing with the `Queue` type.

+ You're _piping_ messages between threads
+ Your _handler_ function is a different thread - Therefore a seperate context from the main thread _(and the current script)_
+ One thread process per `ProcessQueue` instance. You're limited by CPU and thread processing limits.


### Usage

Due to the independant packaging, `smq.ProcessQueue` will work within _probably_ any python enviroment. The core reason for the project highlights lack of efficiently cheap mutiprocessing tools.

Lets get started with a recap of the simple use:

```py
from smq import ProcessQueue

def handler(item):
    pass

pq = ProcessQueue(handler)
pq.start([])
```

You may hate the easy life. Here is a verbose example using other methods:

```py
from smq import ProcessQueue

def handler(item):
    pass

pq = ProcessQueue()
pq.handler = hander
pq.append([])
pq.begin_process()
True
```

You can check the amount processed using methods. Check the length of the processed queue:

```py
len(pq)
pq.queue_len()
pq.queue.qsize()
```

Dermine if the process is running:

```py
pq.is_alive()
True
```

Check for `done` and stop if required. returns the opposite of `is_alive()`.

```py
pq.done
False
pq.stop()
True
pq.done
True
```

## Tests

Usual tests apply. I've used `nosetests`. Multiprocessing maybe tricky. `smpq` can be managed by the main process, so the usual command works:

```bash
$ smtp/src> nosetests
...
```

It may fail due to process allowances. Provide additional options for more process workers:

```bash
$> nosetests --processes=1 --process-timeout=1
```

The cli command provides an extra layer of tests; ensuring we don't leak ophans.  A test _hander_ is designed to sleep for `3` seconds.

The `TestCase` method running a `ProcesQueue` calls `ProcessQueue.stop` after a test. This will kill a process before the 3 second sleep.

The CLI command `process-timeout` could definately be lower; calibrated for the length of time a method takes.

## What else?

:( Effort.

