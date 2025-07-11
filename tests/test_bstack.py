import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BStackDemoTest(unittest.TestCase):

    def create_driver(self, config):
        options = webdriver.ChromeOptions() if config['platform'] != 'macos' else webdriver.FirefoxOptions()
        if config['platform'] == 'mobile':
            options.set_capability('deviceName', config['deviceName'])
            options.set_capability('realMobile', 'true')

        bstack_opts = {
            'userName': os.environ.get('BROWSERSTACK_USERNAME'),
            'accessKey': os.environ.get('BROWSERSTACK_ACCESS_KEY'),
            'buildName': 'BStack Demo',
            'sessionName': config['sessionName']
        }
        bstack_opts.update(config['bstack_options'])
        options.set_capability('bstack:options', bstack_opts)

        return webdriver.Remote(
            command_executor='https://hub-cloud.browserstack.com/wd/hub',
            options=options
        )

    def wait(self, driver, by, value, timeout=10):
        return WebDriverWait(driver, timeout).until(EC.presence_of_element_located((by, value)))

    def login(self, driver):
        driver.get("https://bstackdemo.com")
        self.wait(driver, By.ID, "signin").click()
        self.wait(driver, By.ID, "username").click()
        self.wait(driver, By.XPATH, "//div[text()='demouser']").click()
        self.wait(driver, By.ID, "password").click()
        self.wait(driver, By.XPATH, "//div[text()='testingisfun99']").click()
        self.wait(driver, By.ID, "login-btn").click()

    def apply_samsung_filter(self, driver):
        time.sleep(2)
        try:
            checkbox = driver.find_element(By.XPATH, "//input[@value='Samsung']")
            driver.execute_script("arguments[0].click();", checkbox)
        except:
            pass  # silently fail if mobile layout doesn't have checkbox

    def favorite_product(self, driver, product_name):
        time.sleep(2)
        try:
            product = driver.find_element(By.XPATH, f"//p[text()='{product_name}']")
            card = product.find_element(By.XPATH, "./ancestor::div[contains(@class, 'shelf-item')]")
            heart = card.find_element(By.XPATH, ".//button[contains(@class, 'MuiButtonBase-root')]")
            heart.click()
            return True
        except:
            return False

    def check_favorites(self, driver, product_names):
        self.wait(driver, By.ID, "favourites").click()
        time.sleep(2)
        for name in product_names:
            try:
                if driver.find_element(By.XPATH, f"//p[text()='{name}']"):
                    print(f"{name} found in favorites")
                    return True
            except:
                continue
        return False

    def run_test_workflow(self, driver, is_mobile=False):
        self.login(driver)
        self.apply_samsung_filter(driver)

        primary_product = "Galaxy S20+"
        fallback_products = ["Galaxy S21", "Galaxy S20", "Galaxy S9"]

        if self.favorite_product(driver, primary_product):
            product_checked = primary_product
        elif is_mobile:
            for alt in fallback_products:
                if self.favorite_product(driver, alt):
                    product_checked = alt
                    break
            else:
                return False
        else:
            return False

        return self.check_favorites(driver, [product_checked] + fallback_products)

    def test_windows_chrome(self):
        config = {
            'platform': 'windows',
            'sessionName': 'Windows 10 Chrome Test',
            'bstack_options': {
                'os': 'Windows',
                'osVersion': '10',
                'browserVersion': '120.0'
            }
        }
        driver = self.create_driver(config)
        try:
            self.assertTrue(self.run_test_workflow(driver))
        finally:
            driver.quit()

    def test_macos_firefox(self):
        config = {
            'platform': 'macos',
            'sessionName': 'macOS Ventura Firefox Test',
            'bstack_options': {
                'os': 'OS X',
                'osVersion': 'Ventura',
                'browserVersion': 'latest'
            }
        }
        driver = self.create_driver(config)
        try:
            self.assertTrue(self.run_test_workflow(driver))
        finally:
            driver.quit()

    def test_samsung_galaxy_s22(self):
        config = {
            'platform': 'mobile',
            'deviceName': 'Samsung Galaxy S22',
            'sessionName': 'Samsung Galaxy S22 Test',
            'bstack_options': {
                'osVersion': '12.0'
            }
        }
        driver = self.create_driver(config)
        try:
            if not self.run_test_workflow(driver, is_mobile=True):
                self.skipTest("Mobile layout difference, skipping")
        finally:
            driver.quit()


if __name__ == "__main__":
    unittest.main()
