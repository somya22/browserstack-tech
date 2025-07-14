import os
import unittest
import time
import yaml
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BStackDemoTest(unittest.TestCase):

    def load_config(self):
        # Load config from project root (one level up from tests/ folder)
        config_path = os.path.join(os.path.dirname(__file__), '..', 'browserstack.yml')
        with open(config_path, 'r') as file:
            config = yaml.safe_load(file)
        return config

    def create_driver(self, platform_config):
        browser_name = platform_config.get('browserName', 'chrome').lower()
        
        if browser_name == 'firefox':
            options = webdriver.FirefoxOptions()
        else:
            options = webdriver.ChromeOptions()
        
        options.set_capability('browserName', platform_config['browserName'])
        
        if 'deviceName' in platform_config:
            options.set_capability('deviceName', platform_config['deviceName'])
            options.set_capability('realMobile', platform_config.get('realMobile', True))
        
        bstack_opts = {
            'userName': os.environ.get('BROWSERSTACK_USERNAME'),
            'accessKey': os.environ.get('BROWSERSTACK_ACCESS_KEY'),
            'buildName': 'BStack Demo YAML Config',
            'sessionName': self.get_session_name(platform_config)
        }
        
        if 'os' in platform_config:
            bstack_opts['os'] = platform_config['os']
        if 'osVersion' in platform_config:
            bstack_opts['osVersion'] = platform_config['osVersion']
        if 'browserVersion' in platform_config:
            bstack_opts['browserVersion'] = platform_config['browserVersion']
            
        options.set_capability('bstack:options', bstack_opts)

        return webdriver.Remote(
            command_executor='https://hub-cloud.browserstack.com/wd/hub',
            options=options
        )

    def get_session_name(self, platform_config):
        if 'deviceName' in platform_config:
            return f"{platform_config['deviceName']} {platform_config['browserName']}"
        else:
            return f"{platform_config['os']} {platform_config['osVersion']} {platform_config['browserName']}"

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
        config = self.load_config()
        platform_config = config['platforms'][0]  # First platform (Windows Chrome)
        platform_name = self.get_session_name(platform_config)
        
        driver = self.create_driver(platform_config)
        try:
            result = self.run_test_workflow(driver, "Galaxy S20+", platform_name)
            print(f"{platform_name} result: {'PASS' if result else 'FAIL'}")
            self.assertTrue(result)
        finally:
            driver.quit()

    def test_macos_firefox(self):
        config = self.load_config()
        platform_config = config['platforms'][1]  # Second platform (macOS Firefox)
        platform_name = self.get_session_name(platform_config)
        
        driver = self.create_driver(platform_config)
        try:
            result = self.run_test_workflow(driver, "Galaxy S20+", platform_name)
            print(f"{platform_name} result: {'PASS' if result else 'FAIL'}")
            self.assertTrue(result)
        finally:
            driver.quit()

    def test_samsung_galaxy_s22(self):
        config = self.load_config()
        platform_config = config['platforms'][2]  # Third platform (Samsung Galaxy S22)
        platform_name = self.get_session_name(platform_config)
        
        driver = self.create_driver(platform_config)
        try:
            result = self.run_test_workflow(driver, "Galaxy S20+", platform_name)
            print(f"{platform_name} result: {'PASS' if result else 'FAIL'}")
            self.assertTrue(result)
        finally:
            driver.quit()


if __name__ == "__main__":
    unittest.main()
