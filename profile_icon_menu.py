import unittest

from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import constants


class LoginLogout(unittest.TestCase):

    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get(constants.url)

        username_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "usuario"))
        )
        password_input = WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.ID, "password"))
        )
        login_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
        )
        username_input.send_keys(constants.username)
        password_input.send_keys(constants.password)
        login_button.click()

    def testLoginLogout(self):

        WebDriverWait(self.driver, 10).until(EC.title_contains(constants.appTitle))

        WebDriverWait(self.driver, 1).until(
            lambda d: d.find_element(By.TAG_NAME, "h1").text == constants.welcomeMessage,
            "The word 'Welcome back to Chessings' was not found in the h1 element."
        )

        div_to_click = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'')])[5]"))
        )
        div_to_click.click()

        logout_button = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[contains(.,'Logout')]"))
        )
        logout_button.click()

        WebDriverWait(self.driver, 10).until(
            lambda d: d.find_element(By.TAG_NAME, "h1").text == constants.welcomeMessage,
            "The word 'Welcome back to Chessings' was not found in the h1 element."
        )

    def testEstablishConnection(self):
        div_to_click = WebDriverWait(self.driver, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'')])[5]"))
        )
        div_to_click.click()

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Connecting']"))
        )

        self.driver.find_element(By.XPATH, "//img[contains(@alt,'connecting')]")

        WebDriverWait(self.driver, 10).until(
            EC.presence_of_element_located((By.XPATH, "//button[normalize-space()='Connected']"))
        )

        self.driver.find_element(By.XPATH, "//img[contains(@alt,'connected')]")

    def tearDown(self):
        self.driver.quit()
