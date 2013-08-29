import unittest
from hperf.browser import Browser

class BrowserTest(unittest.TestCase):

    def test_get_chrome(self):
        browser = Browser('chrome')
        page = browser.get('https://172.18.48.32/')
        self.assertIsNotNone(page)
        self.assertTrue(page.performance_timing)
        self.assertTrue(page.resource_timings)
        browser.close()


    def test_get_firefox(self):
        browser = Browser('firefox')
        page = browser.get('http://172.18.48.32/')
        self.assertIsNotNone(page)
        self.assertTrue(page.performance_timing)
        self.assertFalse(page.resource_timings)
        browser.close()


if __name__ == '__main__':
    unittest.main()
