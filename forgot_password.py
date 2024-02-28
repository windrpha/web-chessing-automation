import time
import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

import constants


class ForgotPassword(unittest.TestCase):

    def setUp(self):
        self.driverChrome = webdriver.Firefox()
        self.driverChrome.get(constants.url)
        forgot_password_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Forgot your password?']")))

        forgot_password_button.click()

    def testWording(self):
        forgot_password = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='Forgot your password']")))

        forgot_password_label = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='text-auth-primary text-md my-10']")))

        assert constants.forgotPasswordMessage in forgot_password.text, "Error message not found."
        assert ("Enter your email address and we will send you a link to reset your password." ==
                forgot_password_label.text), "Error message not found."

    def testInvalidEmail(self):
        email_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
        )

        email_input.send_keys("invalidemail")

        submit_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Send code']"))
        )

        submit_button.click()

        error_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='text-red-500 text-sm']"))
        )
        assert constants.emailAddressInvalid == error_message.text

        email_input.clear()
        submit_button.click()
        error_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='text-red-500 text-sm']"))
        )
        assert constants.emailAddressInvalid == error_message.text

        email_input.clear()
        email_input.send_keys("no_existing_user@yopmail.com")
        submit_button.click()
        error_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='text-red-500 text-sm']"))
        )
        assert constants.emailAddressInvalid == error_message.text

    def testErrorsValidationWithCodeResend(self):
        email_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='email']"))
        )

        email_input.send_keys(constants.forgot_password_email)

        submit_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Send code']"))
        )

        submit_button.click()

        # TODO - VERIFY IF POSSIBLE TO REMOVE USERNAME FROM VALIDATION IN FORGOT PASSWORD
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='username']"))
        )
        username_input.send_keys(constants.username)

        code_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='code']"))
        )
        code_input.send_keys("123456")

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='password'])[1]"))
        )
        password_input.send_keys(constants.password)

        confirm_password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='password'])[2]"))
        )
        confirm_password_input.send_keys(constants.password)

        submit_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Change password']"))
        )

        submit_button.click()

        error_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[@class='text-red-500 text-sm']"))
        )
        assert constants.invalidCode == error_message.text

        resent_code = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Resend code']"))
        )

        resent_code.click()

        login_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Already a user? Login']"))
        )
        login_button.click()

        forgot_password_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Forgot your password?']")))

        forgot_password_button.click()

        code_requested_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[contains(@class,'text-sm')]"))
        )

        print(code_requested_message.text)
        assert constants.codeRequestedMessage == code_requested_message.text

    def tearDown(self):
        self.driverChrome.quit()
