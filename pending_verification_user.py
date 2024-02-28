import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants


def register(driver):
    register_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Register']")))

    register_button.click()


def fill_registration_form(driver, username, email, password):
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='usuario']")))
    username_input.send_keys(username)

    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
    password_input.send_keys(password)

    email_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
    email_input.send_keys(email)

    sign_up_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='" + constants.signUpButtonWording + "']")))

    sign_up_button.click()


class PendingVerificationUser(unittest.TestCase):

    def setUp(self):
        self.driverChrome = webdriver.Chrome()
        self.driverChrome.get(constants.url)
        register(self.driverChrome)
        fill_registration_form(self.driverChrome, constants.pendingUser, constants.pendingUserEmail,
                               constants.pendingPassword)

    def testPendingVerificationUser(self):
        pending_verification_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//h1[normalize-space()='" + constants.verifyEmailMessage + "']")))

        assert constants.verifyEmailMessage in pending_verification_message.text, "Error message not found."

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//button[normalize-space()='Verify email']")))

    def tearDown(self):
        self.driverChrome.quit()
