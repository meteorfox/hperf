import page

class Benchmark():
    """Measure performance of pages"""
    def __init__(self, browser, url, num=1):
        self._browser = browser
        self._url = url
        self._samples = None
        self._num = num

    @property
    def samples(self):
        if not self._samples:
            self._samples = [self._browser.get(self._url)
                             for _ in range(self._num)]
        return self._samples
