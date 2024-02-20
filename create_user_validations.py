import time
import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
import constants
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class CreateUserTest(unittest.TestCase):

    def setUp(self):
        self.driverChrome = webdriver.Firefox()
        self.driverChrome.get(constants.url)
        register_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//a[normalize-space()='Register']")))

        register_button.click()

    def testValidateWordings(self):
        #  TODO - Verify the title of the page contains correct message
        # WebDriverWait(self.driverChrome, 10).until(
        #     EC.presence_of_element_located((By.XPATH, "//h1[normalize-space()='" + constants.signUpMessage + "']")))

        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='usuario']")))
        username_input.send_keys(constants.username)
        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='Username']")))

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)
        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='Password']")))

        email_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='email']")))
        email_input.send_keys(constants.username_email)
        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//label[normalize-space()='Email']")))

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//a[normalize-space()='Already a user? Login']")))

    def testEmptyPasswordAndEmail(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username)
        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))

        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='The email is not valid']")))

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='The password is not valid']")))

    def testEmptyPassword(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username)

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys(constants.username_email)

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))

        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='" + constants.emptyPassword + "']")))

    def testEmptyEmail(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username)

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='" + constants.emptyEmail + "']")))

    def testUsernameExistsError(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username)

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys("email_no_exist@yopmail.com")

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='" + constants.usernameExists + "']")))

    def testUsernameWithSpacesError(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username + " " + "tester")

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys(constants.username_email)

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        error_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//p[@class='text-red-500 text-sm'])[1]")))

        assert constants.usernameSpaceError in error_message.text, "Error message not found."

    def testUsernameNoSpecialCharacters(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys("audri_12")

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys(constants.username_email)

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[normalize-space()='" + constants.usernameNoSpecialCharacters + "']")))

    def testUsernameMoreThan25Characters(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys("1234567890123456789o12345678")

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys("email_no_exist1@yopmail.com")

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[normalize-space()='" + constants.usernameMoreThan25Characters + "']")))

    def testUsernameNoEnoughLong(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys("au")

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys("email_no_exist@yopmail.com")

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[normalize-space()='" + constants.usernameNoLongEnough + "']")))

    def testEmailExistsError(self):
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username + "12345")

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys(constants.password)

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys(constants.username_email)

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='" + constants.emailExists + "']")))

    def testPasswordNoNumericPresent(self):
        number = "12345678"
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username + number)

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys("password")

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys("valid_email_" + number + "@yopmail.com")

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//p[normalize-space()='" + constants.passwordNoNumeric + "']")))

    def testPasswordNotEnoughLong(self):
        number = "12345678"
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username + number)

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys("pwd123")

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys("valid_email_" + number + "@yopmail.com")

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[normalize-space()='" + constants.passwordNoEnoughLong + "']")))

    def testPasswordNoLowerCases(self):
        number = "12345678"
        username_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='usuario'])[1]")))
        username_input.send_keys(constants.username + number)

        password_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "//input[@id='password']")))
        password_input.send_keys("PWD1234")

        mail_input = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//input[@id='email'])[1]")))
        mail_input.send_keys("valid_email_" + number + "@yopmail.com")

        sign_up_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "//button[normalize-space()='Signup']")))
        sign_up_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//p[normalize-space()='" + constants.passwordNoLowerCases + "']")))

    def tearDown(self):
        self.driverChrome.quit()
