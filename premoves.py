import time
import unittest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import constants


def login(driver, username, password):
    username_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "usuario"))
    )
    password_input = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.ID, "password"))
    )
    login_button = WebDriverWait(driver, 10).until(
        EC.element_to_be_clickable((By.XPATH, "//button[@type='submit']"))
    )
    username_input.send_keys(username)
    password_input.send_keys(password)
    login_button.click()


def perform_move(driver, xpath):
    actions = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located(
            (By.XPATH, xpath))
    )
    actions.move_to_element(element).click().perform()


def perform_secondary_click(driver, xpath):
    actions = ActionChains(driver)
    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.XPATH, xpath))
    )
    actions.move_to_element(element).context_click().perform()


def perform_escape_click(driver):
    actions = ActionChains(driver)
    actions.send_keys(Keys.ESCAPE).perform()


class LoginLogout(unittest.TestCase):

    def setUp(self):
        self.driverChrome = webdriver.Chrome()
        self.driverChrome.get(constants.url)

        self.driverFirefox = webdriver.Firefox()
        self.driverFirefox.get(constants.url)

        login(self.driverChrome, constants.username, constants.password)
        login(self.driverFirefox, constants.username1, constants.password1)

        play_chrome = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )
        play_firefox = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )

        play_chrome.click()
        play_firefox.click()

    def testPreMovesBeforePromotion(self):
        try:
            WebDriverWait(self.driverChrome, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
            whiteColor = self.driverChrome
            blackColor = self.driverFirefox
            print('white driver chrome')
        except TimeoutException as e:
            WebDriverWait(self.driverFirefox, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
            whiteColor = self.driverFirefox
            blackColor = self.driverChrome
            print('black driver chrome')

        # e2e4
        perform_move(whiteColor, "//div[contains(@id,'game-board-P-e2')]")
        perform_move(whiteColor, "//div[contains(@id,'game-board-e4')]")
        time.sleep(1)

        # d7d5
        perform_move(blackColor, "//div[contains(@id,'game-board-p-d7')]")
        perform_move(blackColor, "//div[contains(@id,'game-board-d5')]")
        time.sleep(1)
        # b2b4
        perform_move(whiteColor, "//div[contains(@id,'game-board-P-b2')]")
        perform_move(whiteColor, "//div[contains(@id,'game-board-b4')]")
        time.sleep(1)

        # pre-moves starts here
        perform_move(whiteColor, "//div[contains(@id,'game-board-P-b4')]")
        perform_move(whiteColor, "//div[contains(@id,'game-board-b5')]")

        perform_move(whiteColor, "//div[contains(@id,'game-board-P-b5')]")
        perform_move(whiteColor, "//div[contains(@id,'game-board-b6')]")

        perform_move(whiteColor, "//div[contains(@id,'game-board-P-b6')]")
        perform_move(whiteColor, "//div[contains(@id,'game-board-b7')]")

        perform_move(whiteColor, "//div[contains(@id,'game-board-P-b7')]")

        perform_escape_click(whiteColor)

        # //validate game returns to normal state after pressing scape
        WebDriverWait(whiteColor, 10).until(
            EC.presence_of_element_located((By.XPATH, "//div[@id='game-board-P-b4']"))
        )

    def tearDown(self):
        self.driverChrome.quit()
        self.driverFirefox.quit()
