from importlib import import_module
from selenium_stealth import stealth
from scrapy_selenium.middlewares import SeleniumMiddleware


class SeleniumStealthMiddleware(SeleniumMiddleware):
    def __init__(self, driver_name, driver_executable_path, driver_arguments,
                 browser_executable_path):
        webdriver_base_path = f'selenium.webdriver.{driver_name}'

        driver_klass_module = import_module(f'{webdriver_base_path}.webdriver')
        driver_klass = getattr(driver_klass_module, 'WebDriver')

        driver_options_module = import_module(f'{webdriver_base_path}.options')
        driver_options_klass = getattr(driver_options_module, 'Options')

        driver_options = driver_options_klass()
        if browser_executable_path:
            driver_options.binary_location = browser_executable_path
        for argument in driver_arguments:
            driver_options.add_argument(argument)

        driver_kwargs = {
            'executable_path': driver_executable_path,
            f'{driver_name}_options': driver_options
        }

        driver_options.add_experimental_option(
            "excludeSwitches", ["enable-automation"])
        driver_options.add_experimental_option('useAutomationExtension', False)

        self.driver = driver_klass(**driver_kwargs)

        stealth(
            self.driver,
            vendor='Google Inc.',
            platform='Win32',
            webgl_vendor='Intel Inc.',
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )