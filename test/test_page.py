import unittest
import pprint

from hperf.page import HPerfPage
from selenium import webdriver

class HPerfPageTest(unittest.TestCase):

    def test_load_chrome(self):
        wd = webdriver.Chrome()
        page = HPerfPage(wd, 'http://www.google.com/')
        page.load()
        self.assertIsNotNone(page.performance_timing)
        self.assertTrue(all(
            map(lambda k: k in ('connectEnd', 'connectStart', 'domComplete',
                                'domContentLoadedEventEnd', 'domInteractive',
                                'domContentLoadedEventStart', 'domLoading',
                                'domainLookupEnd', 'domainLookupStart',
                                'fetchStart', 'loadEventEnd', 'loadEventStart',
                                'navigationStart', 'redirectEnd',
                                'redirectStart', 'requestStart', 'responseEnd',
                                'responseStart', 'secureConnectionStart',
                                'unloadEventEnd', 'unloadEventStart'),
                page.performance_timing.keys())))

        self.assertIsNotNone(page.resource_timings)
        self.assertTrue(page.resource_timings)
        wd.close()


    def test_load_firefox(self):
        wd = webdriver.Firefox()
        page = HPerfPage(wd, 'http://www.google.com/')
        page.load()
        self.assertIsNotNone(page.performance_timing)
        self.assertTrue(all(
            map(lambda k: k in ('connectEnd', 'connectStart', 'domComplete',
                                'domContentLoadedEventEnd', 'domInteractive',
                                'domContentLoadedEventStart', 'domLoading',
                                'domainLookupEnd', 'domainLookupStart',
                                'fetchStart', 'loadEventEnd', 'loadEventStart',
                                'navigationStart', 'redirectEnd',
                                'redirectStart', 'requestStart', 'responseEnd',
                                'responseStart', 'secureConnectionStart',
                                'unloadEventEnd', 'unloadEventStart'),
                page.performance_timing.keys())))


        self.assertFalse(page.resource_timings)

        wd.close()
