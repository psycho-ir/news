__author__ = 'SOROOSH'

from abc import ABCMeta, abstractmethod
import multiprocessing
from time import sleep
import uuid
import threading

__registry__ = []


class Scheduler:
    __metaclass__ = ABCMeta

    def __init__(self, name, seconds, code, *args, **kwargs):
        __registry__.append(self)
        self.name = name
        self.seconds = seconds
        self.code = code
        self._stopped = False
        kwargs.get('daemon', False)

    def _decorate_task(self):
        def result():
            while (not self._stopped):
                try:
                    self.code()
                except Exception as e:
                    print 'Exception: %s occured. Scheduler continues its job.' % e
                sleep(self.seconds)


        return result

    def status(self):
        if self._stopped:
            return 'STOPPED'
        return 'RUNNING'


    def stop(self):
        self._stopped = True

    def resume(self):
        self._stopped = False
        self.run()

    @abstractmethod
    def run(self):
        pass

    def __unicode__(self):
        return self.name


class ThreadSimpleScheduler(Scheduler):
    def run(self):
        print 'scheduler started'
        thread = threading.Thread(name='SCHEDULER-' + str(uuid.uuid4()), target=self._decorate_task())
        thread.daemon = True
        thread.start()
        return thread


class ProcessSimpleScheduler(Scheduler):
    def run(self):
        process = multiprocessing.Process(name='SCHEDULER-' + str(uuid.uuid4()), target=self._decorate_task())
        process.daemon = True
        process.start()
        return process


# if __name__ == "__main__":
# logging.basicConfig(level=logging.INFO,
# format="[%(threadName)-15s] %(message)s")
#
# def say_hi():
# logging.info('hi')
#
# logging.info("Running...")
# # ts = ThreadSimpleScheduler(2, say_hi)
# # ts.run()
# # print threading.active_count()
#     # sleep(10)
#     # print threading.active_count()
#
#     ps = ProcessSimpleScheduler(2, say_hi)
#     ps.run()
#     children = multiprocessing.active_children()
#     print multiprocessing.cpu_count()
#     # multiprocessing.
#     print len(children)





