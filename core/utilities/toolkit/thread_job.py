import queue
import threading
import time


class ThreadJob:
    # The queue for tasks
    q = queue.Queue()

    # Worker, handles each task
    def worker(self):
        while True:
            item = self.q.get()
            if item is None:
                break
            print("Working on", item)
            time.sleep(1)
            self.q.task_done()

    def start_workers(self, worker_pool=1000):
        threads = []
        for i in range(worker_pool):
            t = threading.Thread(target=self.worker)
            t.start()
            threads.append(t)
        return threads

    def stop_workers(self, threads):
        # stop workers
        for i in threads:
            self.q.put(None)
        for t in threads:
            t.join()

    def create_queue(self, task_items):
        for item in task_items:
            self.q.put(item)
