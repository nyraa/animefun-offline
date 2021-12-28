import queue
import requests
import threading

class mtd:
    max_thread = 10
    __threading = 0
    __finished = 0
    def __init__(self, header, base, length):
        self.__download_queue = queue.Queue()
        self.__worker_running = False
        self.__header = header
        self.__base = base
        self.__length = length

    def __worker(self):
        while self.__download_queue.qsize() > 0:
            if self.__threading < self.max_thread:
                name = self.__download_queue.get()
                threading.Thread(target=self.__download, args=(name,)).start()
                self.__threading += 1
        self.__worker_running = False

    def __download(self, name):
        try:
            print(f'Downloading {name}...\n', end='')
            res = requests.get(self.__base + name, headers=self.__header)
            res.raise_for_status()
        except Exception as ex:
            print(f'Error: {name}: {ex}')
            return
        with open(name, 'wb') as file:
            file.write(res.content)
        self.__threading -= 1
        self.__finished += 1

    def push(self, name):
        self.__download_queue.put(name)
        if not self.__worker_running:
            self.__worker_running = True
            threading.Thread(target=self.__worker).start()

    def join(self):
        while self.__finished < self.__length:
            pass