import time
import unittest
from selenium.webdriver.support import expected_conditions as EC
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
import commons.login as login
import commons.move as move
import commons.player_turn as player_turn
import constants


class GameMoves(unittest.TestCase):

    def setUp(self):
        self.driverChrome = webdriver.Chrome()
        self.driverChrome.get(constants.url)

        self.driverFirefox = webdriver.Firefox()
        self.driverFirefox.get(constants.url)
        login.login(self.driverChrome, constants.username, constants.password)
        login.login(self.driverFirefox, constants.username1, constants.password1)

        play_chrome = WebDriverWait(self.driverChrome, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )
        play_firefox = WebDriverWait(self.driverFirefox, 10).until(
            EC.element_to_be_clickable((By.XPATH, "(//div[contains(.,'Play')])[31]"))
        )

        play_chrome.click()
        play_firefox.click()

    def testCheckMate(self):
        white, black = player_turn.player_turn(self.driverChrome, self.driverFirefox)

        # e2e4
        move.perform_move(white, "//div[contains(@id,'game-board-P-e2')]")
        move.perform_move(white, "//div[contains(@id,'game-board-e4')]")
        time.sleep(1)

        # d7d5
        move.perform_move(black, "//div[contains(@id,'game-board-p-e7')]")
        move.perform_move(black, "//div[contains(@id,'game-board-e5')]")
        time.sleep(1)

        move.perform_move(white, "//div[contains(@id,'game-board-Q-d1')]")
        move.perform_move(white, "//div[contains(@id,'game-board-h5')]")
        time.sleep(1)

        move.perform_move(black, "//div[contains(@id,'game-board-n-b8')]")
        move.perform_move(black, "//div[contains(@id,'game-board-c6')]")
        time.sleep(1)

        move.perform_move(white, "//div[contains(@id,'game-board-B-f1')]")
        move.perform_move(white, "//div[contains(@id,'game-board-c4')]")
        time.sleep(1)

        move.perform_move(black, "//div[contains(@id,'game-board-p-a7')]")
        move.perform_move(black, "//div[contains(@id,'game-board-a5')]")
        time.sleep(1)

        move.perform_move(white, "//div[contains(@id,'game-board-Q-h5')]")
        move.perform_move(white, "//div[contains(@id,'game-board-f7')]")

        WebDriverWait(black, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[normalize-space()='"
                                            + constants.endCardLossMessage + "'])[1]"))
        )

        WebDriverWait(white, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[normalize-space()='"
                                            + constants.endCardWinMessage + "'])[1]"))
        )

    def testFoolMate(self):
        white, black = player_turn.player_turn(self.driverChrome, self.driverFirefox)

        move.perform_move(white, "//div[contains(@id,'game-board-P-f2')]")
        move.perform_move(white, "//div[contains(@id,'game-board-f3')]")
        time.sleep(1)

        move.perform_move(black, "//div[contains(@id,'game-board-p-e7')]")
        move.perform_move(black, "//div[contains(@id,'game-board-e5')]")
        time.sleep(1)

        # 2. g4 Qh4#
        move.perform_move(white, "//div[contains(@id,'game-board-P-g2')]")
        move.perform_move(white, "//div[contains(@id,'game-board-g4')]")
        time.sleep(1)

        move.perform_move(black, "//div[contains(@id,'game-board-q-d8')]")
        move.perform_move(black, "//div[contains(@id,'game-board-h4')]")
        WebDriverWait(white, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[normalize-space()='"
                                            + constants.endCardLossMessage + "'])[1]"))
        )

        WebDriverWait(black, 10).until(
            EC.presence_of_element_located((By.XPATH, "(//div[normalize-space()='"
                                            + constants.endCardWinMessage + "'])[1]"))
        )

    def tearDown(self):
        self.driverChrome.quit()
        self.driverFirefox.quit()
