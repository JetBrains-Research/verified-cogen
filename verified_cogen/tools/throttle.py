import time
from multiprocessing.managers import SyncManager
from typing import no_type_check


class Throttle:
    _instance = None
    _initialized = False

    @no_type_check
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, manager: SyncManager, rate_limit_per_minute: int = 10):
        if not Throttle._initialized:
            self.request_times = manager.list()
            self.lock = manager.Lock()
            self.window = 60
            self.rate_limit = rate_limit_per_minute
            Throttle._initialized = True

    def _cleanup_old(self, now: float):
        cutoff = now - self.window
        with self.lock:
            while len(self.request_times) > 0 and self.request_times[0] < cutoff:
                self.request_times.pop(0)

    def wait(self) -> None:
        while True:
            now = time.time()
            self._cleanup_old(now)

            with self.lock:
                if len(self.request_times) < self.rate_limit:
                    self.request_times.append(now)
                    return

            time.sleep(0.1)

    def __enter__(self):
        self.wait()
        return self

    @no_type_check
    def __exit__(self, type, value, traceback):
        pass
