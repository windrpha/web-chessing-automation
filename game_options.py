import unittest
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


def initial_board_moves(driver1, driver2):
    try:
        WebDriverWait(driver1, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        whiteColor = driver1
        blackColor = driver2
        print('white driver chrome')
    except TimeoutException as e:
        WebDriverWait(driver2, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        whiteColor = driver2
        blackColor = driver1
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


class GameOptions(unittest.TestCase):

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
        play_firefox = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )

        play_chrome.click()
        play_firefox.click()

    def test_new_game_option(self):
        initial_board_moves(self.driverChrome, self.driverFirefox)
        resign_button = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//div[normalize-space()='" + constants.endCardResignButton + "'])[1]")))
        resign_button.click()

        WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.endCardResignLossMessage + "'])[1]"))
        )

        WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.endCardResignWinMessage + "'])[1]"))
        )

    def test_accept_rematch(self):
        initial_board_moves(self.driverChrome, self.driverFirefox)
        resign_button = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//div[normalize-space()='" + constants.endCardResignButton + "'])[1]")))
        resign_button.click()

        rematch_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.endCardButtonRematchName + "'])[1]"))
        )
        rematch_button.click()

        accept_button = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.rematchAcceptButton + "'])[1]"))
        )

        # decline button
        WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.rematchDeclineButton + "'])[1]"))
        )

        accept_button.click()

        try:
            WebDriverWait(self.driverChrome, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        except TimeoutException as e:
            WebDriverWait(self.driverFirefox, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))

    def test_decline_rematch(self):
        initial_board_moves(self.driverChrome, self.driverFirefox)
        resign_button = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable(
                (By.XPATH, "(//div[normalize-space()='" + constants.endCardResignButton + "'])[1]")))
        resign_button.click()

        rematch_button = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.endCardButtonRematchName + "'])[1]"))
        )
        rematch_button.click()

        WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.rematchAcceptButton + "'])[1]"))
        )

        # decline button
        decline_button = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='"
                                        + constants.rematchDeclineButton + "'])[1]"))
        )

        decline_button.click()

        WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[normalize-space()='Rematch'])[1]"))
        )

    def tearDown(self):
        self.driverChrome.quit()
        self.driverFirefox.quit()