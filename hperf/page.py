import os
import selenium.webdriver.support.ui as ui

class HPerfPage(object):
    """
    Loads a page from a URL and retrieves, if available,
    the performance.timing and Resource timing data from the page.
    """

    def __init__(self, driver, url):
        """(WebDriver, String)"""
        self._url = url
        self._driver = driver
        self._hperf_script = None
        self._perf_timing = None
        self._res_timings = []
        self._has_ran = False


    @property
    def url(self):
        """
        () -> String
        Returns the page's URL
        """
        return self._url


    @property
    def hperf_script(self):
        """
        () -> String
        Reads hperf JavaScript file from disk, and returns the script
        as a string.
        """
        if not self._hperf_script:
            this_dirname = os.path.dirname(__file__)
            hperf_js = os.path.join(this_dirname, 'lib', 'js', 'hperf.js')
            with open(hperf_js, 'r') as js_fd:
                self._hperf_script = js_fd.read()

        return self._hperf_script


    @property
    def performance_timing(self):
        """
        () -> Dict
        Returns the window.performance.timing for the page, or
        None if it has not been loaded previously, or is not supported by
        the browser.
        """
        return self._perf_timing


    @property
    def resource_timings(self):
        """
        () -> List
        Returns the window.performance.getEntries() from the page if it's
        supported by the browser, and the page has been loaded, otherwise [].
        """
        return self._res_timings


    def load(self):
        """Loads the page"""
        self._driver.get(self.url)
        self._wait_page_load()
        self._driver.execute_script(self.hperf_script)
        self._load_perf_timing()
        self._load_resource_timing()


    def _load_perf_timing(self):
        """
        Executes a js snippet to retrive the performance.timing from the
        page.
        """
        wpt_script = 'return window.performance.timing'
        js_script = 'return window.HPerf.performanceTimingSupport()'
        browser_support = self._driver.execute_script(js_script)
        if browser_support:
            self._perf_timing = self._driver.execute_script(wpt_script)


    def _load_resource_timing(self):
        """
        Executes a js snippet to retrieve the performance.timing.getEntries()
        from the page.
        """
        resource_support = 'return window.HPerf.resourceTimingSupport()'
        wre_script = 'return window.performance.getEntries()'
        browser_support = self._driver.execute_script(resource_support)
        if browser_support:
            self._res_timings = self._driver.execute_script(wre_script)


    def _wait_page_load(self):
        """Waits until onLoad event is fired on the page."""
        def load_event_end(driver):
            """Executes the load_event_scripts on the browser, and
            returns the timer for loadEventEnd"""
            load_event_script = 'return window.performance.timing.loadEventEnd'
            on_load = driver.execute_script(load_event_script)
            return int(on_load) > 0 if on_load else False

        ui.WebDriverWait(self._driver, 10).until(load_event_end)
