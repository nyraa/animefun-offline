import queue
import requests
import threading
import os

class mtd:
    def __init__(self, header, base, length, store_base, max_thread=10):
        self._download_queue = queue.Queue()
        self._worker_running = False
        self._header = header
        self._base = base
        self._length = length
        self._store_base = store_base
        self._threading = 0
        self._pop = 0
        self._finished = 0
        self.max_thread = max_thread

    def _worker(self):
        while self._download_queue.qsize() > 0:
            if self._threading < self.max_thread:
                self._threading += 1
                self._pop += 1
                name = self._download_queue.get()
                threading.Thread(target=self._download, args=(name,)).start()
        self._worker_running = False

    def _download(self, name):
        try:
            print(f'Downloading {name}...({self._pop + 1}/{self._length})\n', end='')
            res = requests.get(self._base + name, headers=self._header)
            res.raise_for_status()
        except Exception as ex:
            print(f'Error: {name}: {ex}')
            return
        with open(os.path.join(self._store_base, name), 'wb') as file:
            file.write(res.content)
        self._threading -= 1
        self._finished += 1

    def push(self, name):
        self._download_queue.put(name)
        if not self._worker_running:
            self._worker_running = True
            threading.Thread(target=self._worker).start()

    def join(self):
        while self._threading > 0 and self._download_queue.qsize() > 0:
            pass