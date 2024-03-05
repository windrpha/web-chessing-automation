from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def player_turn(driver1, driver2):
    try:
        WebDriverWait(driver1, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        return driver1, driver2
    except TimeoutException as e:
        WebDriverWait(driver2, 10).until(
            EC.presence_of_element_located(
                (By.XPATH, "//div[contains(@id,'game-board-countdown-for-move')]")))
        return driver2, driver1
