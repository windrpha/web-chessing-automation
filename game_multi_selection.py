import time
import unittest
from selenium import webdriver
from selenium.common import TimeoutException
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


class GameMultiSelection(unittest.TestCase):

    def setUp(self):
        self.driverChrome = webdriver.Chrome()
        self.driverFirefox = webdriver.Firefox()
        self.driverChrome.get(constants.url)
        self.driverFirefox.get(constants.url)
        login(self.driverChrome, constants.username, constants.password)
        login(self.driverFirefox, constants.username1, constants.password1)

        play_chrome = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )

        play_chrome.click()

    def testMultiSelectionPressingCancelButton(self):
        # return to main menu using cancel button and relaunching
        cancel_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[@class='flex-1 text-center text-sm md:text-md'])[1]"))
        )
        cancel_button.click()

        play_chrome = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'flex-1 text-xl text-center')]["
                                                  "normalize-space()='Play'])[3]"))
        )
        play_firefox = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'flex-1 text-xl text-center')]["
                                                  "normalize-space()='Play'])[3]"))
        )
        play_chrome.click()
        play_firefox.click()

        try:
            WebDriverWait(self.driverChrome, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        except TimeoutException as e:
            WebDriverWait(self.driverFirefox, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))

    def testMultiSelectionLaunchingDirectNewGame(self):
        # return to main menu using play button
        play_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'jsx-aa52c581ebd5882b')])[1]"))
        )
        play_button.click()

        play_chrome = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'flex-1 text-xl text-center')]["
                                                  "normalize-space()='Play'])[3]"))
        )
        play_firefox = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(@class,'flex-1 text-xl text-center')]["
                                                  "normalize-space()='Play'])[3]"))
        )
        play_chrome.click()
        play_firefox.click()

        try:
            WebDriverWait(self.driverChrome, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        except TimeoutException as e:
            WebDriverWait(self.driverFirefox, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))

    def testMultiSelectionLaunchingSameGameMode(self):
        # return to main menu using play button
        play_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//button[contains(@class,'jsx-aa52c581ebd5882b')])[1]"))
        )
        play_button.click()

        play_chrome = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )
        play_firefox = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )

        play_chrome.click()
        play_firefox.click()

        try:
            WebDriverWait(self.driverChrome, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        except TimeoutException as e:
            WebDriverWait(self.driverFirefox, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))

    def tearDown(self):
        self.driverChrome.quit()
        self.driverFirefox.quit()
