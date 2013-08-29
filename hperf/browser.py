import os
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from page import HPerfPage


def _make_driver(browser_name, **options):
    """ Creates, configures, and launches the specified browser"""
    if browser_name == "firefox":
        profile = webdriver.FirefoxProfile()
        beacon_filepath = os.path.abspath(os.path.join(
            os.path.dirname(__file__), '..', 'data'))

        domain = "extensions.firebug"
        profile.set_preference("%s.currentVersion" % domain, "1.11.2")
        profile.set_preference("%s.allPagesActivation" % domain, "on")
        profile.set_preference("%s.defaultPanelName" % domain, "net")
        profile.set_preference("%s.net.enableSites" % domain, True)
        profile.set_preference("%s.netexport.alwaysEnableAutoExport" % domain,
                               True)
        profile.set_preference("%s.netexport.showPreview" % domain, False)
        profile.set_preference("%s.netexport.defaultLogDir" % domain,
                               beacon_filepath)
        profile.set_preference("browser.cache.disk.enable",
                               options['cache_enabled'])
        profile.set_preference("browser.cache.offline.enable",
                               options['cache_enabled'])
        profile.set_preference("network.http.use-cache",
                               options['cache_enabled'])

        lib_path = os.path.join(os.path.dirname(__file__) , 'lib')
        profile.add_extension(
            extension=os.path.join(lib_path, 'firebug-1.11.2.xpi'))
        profile.add_extension(
            extension=os.path.join(lib_path, 'netExport-0.9b3.xpi'))

        browser = webdriver.Firefox(firefox_profile=profile)
        time.sleep(5) # Wait for extensions to load
    else:
        chrome_options = Options()
        chrome_options.add_argument('--allow-running-insecure-content')
        if not options['cache_enabled']:
            chrome_options.add_argument('--disable-application-cache')
        browser = webdriver.Chrome(chrome_options=chrome_options)

    return browser


class Browser(object):
    """Creates a browser instances and initializes the Webdriver."""
    def __init__(self, browser="chrome", **options):
        self.browser = browser
        self.options = options
        self._driver = None


    @property
    def driver(self):
        if not self._driver:
            self._driver = _make_driver(browser_name=self.browser,
                                        **self.options)
        return self._driver


    def get(self, url):
        """
        String -> HPerfPage
        Given an URL the browser will navigate to that URL and produce
        a Page object.
        """
        hperf_page = HPerfPage(self.driver, url)
        hperf_page.load()
        return hperf_page


    def close(self):
        """Close the webdriver session"""
        self.driver.close()
