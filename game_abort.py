import time
import unittest
from selenium import webdriver
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

        self.driverFirefox = webdriver.Chrome()
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
        abort_message = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='flex justify-center items-center text-xs text-negative-color']"))
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

    def testAbortIfBlackPlayerDoesNotMove(self):

        element = WebDriverWait(self.driverChrome, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "(//div[contains(@class,'text-white font-bold text-sm')][normalize-space()])[1]")))

        if element.text == constants.username:
            print('white driver chrome')
            whiteColor = self.driverChrome
            blackColor = self.driverFirefox
        else:
            print('black driver chrome')
            whiteColor = self.driverFirefox
            blackColor = self.driverChrome

        # abort_message = WebDriverWait(whiteColor, 20).until(
        #     EC.presence_of_element_located(
        #         (By.XPATH, "//div[contains(@class,'flex justify-center items-center text-xs text-negative-color')]"))
        # )
        #
        # print(abort_message.text)
        #
        # assert constants.abortMessage in abort_message.text

        perform_move(whiteColor, "//div[contains(@style, 'P.svg') and contains(@style, 'top: 75%; left: 50%;')]")
        perform_move(whiteColor, "(//div[contains(@class,'relative')])[44]")

        abort_message = WebDriverWait(blackColor, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[@class='flex justify-center items-center text-xs text-negative-color']"))
        )
        assert constants.abortMessage in abort_message.text

    def tearDown(self):
        self.driverChrome.quit()
        self.driverFirefox.quit()
