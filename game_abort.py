import time
import unittest
from selenium import webdriver
from selenium.common import TimeoutException
from selenium.webdriver import ActionChains
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


class GamePremoves(unittest.TestCase):

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

    def test15SecondsAbort(self):

        end_game_message_chrome = WebDriverWait(self.driverChrome, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='abort']"))
        )
        end_game_message_firefox = WebDriverWait(self.driverFirefox, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='abort']"))
        )
        assert end_game_message_chrome.text == "ABORT"
        assert end_game_message_firefox.text == "ABORT"

    def testAbortIfBlackPlayerDoesNotMove(self):

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

        perform_move(whiteColor, "//div[contains(@id,'game-board-P-e2')]")
        perform_move(whiteColor, "//div[contains(@id,'game-board-e4')]")

        abort_message = WebDriverWait(blackColor, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]"))
        )
        assert constants.abortMessage in abort_message.text

        end_game_message_chrome = WebDriverWait(self.driverChrome, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='abort']"))
        )
        end_game_message_firefox = WebDriverWait(self.driverFirefox, 20).until(
            EC.presence_of_element_located((By.XPATH, "//div[normalize-space()='abort']"))
        )
        assert end_game_message_chrome.text == "ABORT"
        assert end_game_message_firefox.text == "ABORT"

    def tearDown(self):
        self.driverChrome.quit()
        self.driverFirefox.quit()
