import unittest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class BStackTest(unittest.TestCase):
    def setUp(self):
        self.driver = self.options.driver
        self.wait = WebDriverWait(self.driver, 10)

    def test_favorite_samsung_product(self):
        driver = self.driver
        wait = self.wait

        driver.get("https://www.bstackdemo.com")

        # Login
        wait.until(EC.element_to_be_clickable((By.ID, "signin"))).click()
        wait.until(EC.visibility_of_element_located((By.ID, "username"))).send_keys("demouser")
        driver.find_element(By.ID, "password").send_keys("testingisfun99")
        driver.find_element(By.ID, "login-btn").click()

        # Filter Samsung
        wait.until(EC.element_to_be_clickable((By.XPATH, "//div[text()='Samsung']"))).click()

        # Favorite Galaxy S20+
        heart_xpath = "//p[text()='Galaxy S20+']/ancestor::div[contains(@class,'shelf-item')]//span[@class='favorite']"
        wait.until(EC.element_to_be_clickable((By.XPATH, heart_xpath))).click()

        # Go to Favorites page
        wait.until(EC.element_to_be_clickable((By.ID, "wishlist"))).click()

        # Verify it's in Favorites
        wait.until(EC.presence_of_element_located((By.XPATH, "//p[text()='Galaxy S20+']")))

    def tearDown(self):
        self.driver.quit()
