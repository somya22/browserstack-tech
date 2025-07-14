import os
import unittest
import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BStackDemoTest(unittest.TestCase):

    def create_driver(self, config):
        if config['platform'] == 'windows':
            options = webdriver.ChromeOptions()
        elif config['platform'] == 'macos':
            options = webdriver.FirefoxOptions()
        elif config['platform'] == 'mobile':
            options = webdriver.ChromeOptions()
            options.set_capability('browserName', 'chrome')
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
            pass

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

        
    def check_favorites(self, driver, product_name, platform_name):
        self.wait(driver, By.ID, "favourites").click()
        time.sleep(2)
        try:
            driver.find_element(By.XPATH, f"//p[text()='{product_name}']")
            print(f"[{platform_name}] '{product_name}' was favorited successfully and found in Favorites")
            return True
        except:
            print(f"[{platform_name}] '{product_name}' was not found in Favorites")
            return False

    def run_test_workflow(self, driver, product_name, platform_name):
        self.login(driver)
        self.apply_samsung_filter(driver)

        if self.favorite_product(driver, product_name):
            return self.check_favorites(driver, product_name, platform_name)
        else:
            print(f"[{platform_name}] Failed to favorite '{product_name}'")
            return False


    def test_windows_chrome(self):
        platform_name = "Windows 10 Chrome"
        config = {
            'platform': 'windows',
            'sessionName': f'{platform_name} Test',
            'bstack_options': {
                'os': 'Windows',
                'osVersion': '10',
                'browserVersion': '120.0'
            }
        }
        driver = self.create_driver(config)
        try:
            result = self.run_test_workflow(driver, "Galaxy S20+", platform_name)
            print(f"{platform_name} result: {'PASS' if result else 'FAIL'}")
            self.assertTrue(result)
        finally:
            driver.quit()

    def test_macos_firefox(self):
        platform_name = "macOS Ventura Firefox"
        config = {
            'platform': 'macos',
            'sessionName': f'{platform_name} Test',
            'bstack_options': {
                'os': 'OS X',
                'osVersion': 'Ventura',
                'browserVersion': 'latest'
            }
        }
        driver = self.create_driver(config)
        try:
            result = self.run_test_workflow(driver, "Galaxy S20+", platform_name)
            print(f"{platform_name} result: {'PASS' if result else 'FAIL'}")
            self.assertTrue(result)
        finally:
            driver.quit()

    def test_samsung_galaxy_s22(self):
        platform_name = "Samsung Galaxy S22 (Mobile)"
        config = {
            'platform': 'mobile',
            'deviceName': 'Samsung Galaxy S22',
            'sessionName': f'{platform_name} Test',
            'bstack_options': {
                'osVersion': '12.0'
            }
        }
        driver = self.create_driver(config)
        try:
            result = self.run_test_workflow(driver, "Galaxy S20+", platform_name)
            print(f"{platform_name} result: {'PASS' if result else 'FAIL'}")
            self.assertTrue(result)
        finally:
            driver.quit()


if __name__ == "__main__":
    unittest.main()
