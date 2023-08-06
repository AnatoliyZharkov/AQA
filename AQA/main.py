import time
from datetime import datetime
import json
import unittest
from appium import webdriver
from appium.webdriver.common.appiumby import AppiumBy
from selenium.webdriver import ActionChains
from selenium.webdriver.common.actions import interaction
from selenium.webdriver.common.actions.action_builder import ActionBuilder
from selenium.webdriver.common.actions.pointer_input import PointerInput


URL = 'http://127.0.0.1:4723'
HOTEL_TITLE = 'The Grosvenor Hotel'
SEARCH_BUTTON_XPATH = '//android.widget.FrameLayout[@content-desc="Search"]/android.widget.ImageView'
SEARCH_FIELD_ID = 'com.tripadvisor.tripadvisor:id/edtSearchString'
HOTEL_XPATH = ('/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
               'android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/'
               'android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/'
               'android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/android.view.ViewGroup[3]')
DATE_PICKER_ID = 'com.tripadvisor.tripadvisor:id/txtDate'
APPLY_BUTTON_ID = 'com.tripadvisor.tripadvisor:id/btnPrimary'
ALL_DEALS_ID = 'com.tripadvisor.tripadvisor:id/btnAllDeals'
PROVIDERS_ID = 'com.tripadvisor.tripadvisor:id/imgProviderLogo'


capabilities = dict(
    platformName='Android',
    automationName='uiautomator2',
    deviceName='samsung SM-G990B2',
    app='/home/anatoliy/Android/Apk/base.apk',
    appPackage='com.tripadvisor.tripadvisor',
    appActivity='com.tripadvisor.android.ui.primarynavcontainer.MainActivity',
    noReset=True,
    autoGrantPermissions=True
)


def get_date_xpath(n: int) -> str:
    return (f'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
            f'android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/'
            f'android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout[2]/'
            f'android.widget.FrameLayout/android.view.ViewGroup/androidx.recyclerview.widget.RecyclerView/'
            f'android.view.ViewGroup/android.widget.GridView/android.widget.FrameLayout[{n}]/android.widget.TextView')


def get_provider_xpath(n: int) -> str:
    return (f'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
            f'android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/'
            f'android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/'
            f'android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/'
            f'androidx.cardview.widget.CardView[{n}]/android.view.ViewGroup/android.widget.TextView[1]')


def get_price_xpath(n: int) -> str:
    return (f'/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/'
            f'android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/'
            f'android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.view.ViewGroup/'
            f'android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/'
            f'androidx.cardview.widget.CardView[{n}]/android.view.ViewGroup/android.widget.TextView[2]')


def save_screenshot_to_folder(title: str) -> str:
    return f'/your/project/folder/AQA/Screenshots/{title}.png'


def get_date_cell_number():
    current_date = datetime.today().day
    first_day_of_month = datetime.today().replace(day=1).weekday() + 1
    if first_day_of_month == 1:
        return current_date + 1
    else:
        return first_day_of_month + current_date


def make_scroll(driver, y_from: int, y_to: int):
    actions = ActionChains(driver)
    actions.w3c_actions = ActionBuilder(driver, mouse=PointerInput(interaction.POINTER_TOUCH, "touch"))
    actions.w3c_actions.pointer_action.move_to_location(513, y_from)
    actions.w3c_actions.pointer_action.pointer_down()
    actions.w3c_actions.pointer_action.move_to_location(513, y_to)
    actions.w3c_actions.pointer_action.release()
    actions.perform()


def get_providers_prices_dict(providers: list, prices: list) -> dict:
    return_dict = {}
    for i in range(len(providers)):
        return_dict[providers[i]] = prices[i]
    return return_dict


def convert_to_json(data: dict):
    f = json.dumps(data, indent=4)
    with open('result.json', 'w') as file:
        print(f, file=file)
        return file


class TestAppium(unittest.TestCase):

    def test_open_website(self):
        driver = webdriver.Remote(command_executor=URL, desired_capabilities=capabilities)

        search_button = driver.find_element(AppiumBy.XPATH, SEARCH_BUTTON_XPATH)
        search_button.click()

        get_search_field = driver.find_element(AppiumBy.ID, SEARCH_FIELD_ID)
        get_search_field.click()
        time.sleep(3)

        input_search_field = driver.find_element(AppiumBy.ID, SEARCH_FIELD_ID)
        input_search_field.send_keys(HOTEL_TITLE)
        time.sleep(3)

        hotel = driver.find_element(AppiumBy.XPATH, HOTEL_XPATH)
        hotel.click()
        time.sleep(3)

        make_scroll(driver, 1912, 1672)

        all_deals = driver.find_element(AppiumBy.ID, ALL_DEALS_ID)
        all_deals.click()
        time.sleep(3)

        return_dict = {}
        date_picker = driver.find_element(AppiumBy.ID, DATE_PICKER_ID)
        cell_number = get_date_cell_number()
        for i in range(cell_number, cell_number + 5):
            date_picker.click()
            time.sleep(3)

            date_1 = driver.find_element(AppiumBy.XPATH, get_date_xpath(i))
            date_1.click()
            date_2 = driver.find_element(AppiumBy.XPATH, get_date_xpath(i + 1))
            date_2.click()
            time.sleep(3)

            apply = driver.find_element(AppiumBy.ID, APPLY_BUTTON_ID)
            apply.click()
            time.sleep(3)

            providers = []
            prices = []
            providers.append(driver.find_element(AppiumBy.ID, PROVIDERS_ID).get_attribute('content-desc'))
            prices.append(driver.find_element(AppiumBy.XPATH, get_price_xpath(1)).text)
            time.sleep(3)

            for j in range(2, 5):
                providers.append(driver.find_element(AppiumBy.XPATH, get_provider_xpath(j)).text)
                prices.append(driver.find_element(AppiumBy.XPATH, get_price_xpath(j)).text)
                time.sleep(3)

            screenshot_name = driver.current_activity + time.strftime("%Y_%m_%d_%H:%M:%S")
            driver.save_screenshot(save_screenshot_to_folder(screenshot_name))
            return_dict[date_picker.text] = (get_providers_prices_dict(providers, prices) |
                                             {'screenshot': screenshot_name})

        driver.quit()
        return convert_to_json({HOTEL_TITLE: return_dict})


if __name__ == '__main__':
    unittest.main()
