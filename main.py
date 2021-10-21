# This is a sample Python script.

# Press ⌃R to execute it or replace it with your code.
# Press Double ⇧ to search everywhere for classes, files, tool windows, actions, and settings.
from time import sleep
from selenium import webdriver
from PIL import Image
from aip import AipOcr
from selenium.common.exceptions import TimeoutException, UnexpectedAlertPresentException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait as Wait
#import login_gui
import desktop


def yan_zheng(driver):
    alert = EC.alert_is_present()(driver)
    if alert:
        alert.accept()
        code_yzm(driver)
        yan_zheng(driver)
    else:
        driver = load_page(driver)


def code_yzm(driver):
    driver.find_element_by_id("password_zsxh").clear()
    driver.find_element_by_id("password_zsxh").send_keys('2018213035')
    # driver.save_screenshot('whole.png')
    with open("code.png", "wb") as f:
        f.write(driver.find_element_by_id("yzmmsg_xh").screenshot_as_png)
    # img = Image.open('whole.png')
    # rate = img.size[0] / desktop.ex.screenRect.width()
    # box_px = [520, 458]
    # box_size = [i * rate for i in box_px]
    # left = img.size[0] / 2 - box_size[0] / 2
    # right = img.size[0] / 2 + box_size[0] / 2
    # top = img.size[1] / 2 - box_size[1] / 2
    # down = img.size[1] / 2 + box_size[1] / 2
    # box = img.crop((left, top, right, down))
    # box.save('box.png')
    # img = Image.open('box.png')
    # local = [400, 366, 470, 390]
    # local_really = [i * rate for i in local]
    # code_image = img.crop(local_really)
    # code_image.save('code_image.png')
    captcha = get_capt()
    captcha = captcha[0] + captcha[2:]
    driver.find_element_by_id('xhYzm').clear()
    driver.find_element_by_id('xhYzm').send_keys(captcha)
    driver.find_element_by_id('login_zsxh').click()


def login(driver):
    driver.find_element_by_class_name("header-dengl").click()
    driver.find_element_by_xpath('//div[@class="login-two-btn"]/a').click()
    driver.find_element_by_id("bjssxy").click()
    driver.find_element_by_xpath('//option[@value="4111010013"]').click()
    driver.find_element_by_id("usercode_zsxh").send_keys('2018213035')
    code_yzm(driver)


def get_capt():
    code = Image.open('code.png')
    code = code.convert('L')
    count = 160
    table = []
    for i in range(256):
        if i < count:
            table.append(0)
        else:
            table.append(1)
    code = code.point(table, '1')
    code.save('captcha.png')
    captcha = discern_capt()
    return captcha


def discern_capt():
    APP_ID = '23930361'
    API_KEY = 'SiA5Ax6rKmx1t7BMgGugUvNb'
    SECRET_KEY = 'eTccqW18ey509qCA9Tww5imL58D2a5Gy'
    client = AipOcr(APP_ID, API_KEY, SECRET_KEY)
    image = get_file_content('captcha.png')
    # 定义参数变量
    options = {'language_type': 'ENG', }  # 识别语言类型，默认为'CHN_ENG'中英文混合
    #  调用通用文字识别
    result = client.basicAccurate(image, options)  # 高精度接口 basicAccurate
    for word in result['words_result']:
        captcha = (word['words'])
        return captcha


def get_file_content(file_path):
    with open(file_path, 'rb') as f:
        return f.read()


def switch_window(driver):
    current_window = driver.current_window_handle
    all_windows = driver.window_handles
    for window in all_windows:
        if window != current_window:
            driver.switch_to_window(window)
            print("1")
    return driver


def load_page(driver):
    try:
        sleep(5)
        driver = switch_window(driver)
    except TimeoutException:
        print("timeout")
        load_page(driver)
    return driver


def class_choose(driver):
    ul = driver.find_element_by_class_name("zxin-b-list")
    lis = ul.find_elements_by_xpath('li')
    for i in range(len(lis)):
        ul = driver.find_element_by_class_name("zxin-b-list")
        lis = ul.find_elements_by_xpath('li')
        button = lis[i].find_element_by_class_name('styu-b-r').find_elements_by_tag_name('a')
        button[0].click()
        driver = load_page(driver)
        driver = choose_lesson(driver)
    print("all class have finished!")
    return driver


def choose_lesson(driver):
    table = driver.find_element_by_class_name("xx-left-main")
    section = table.find_elements_by_tag_name('dl')
    for i in range(1, len(section) - 1):
        chapters = section[i].find_elements_by_tag_name('dd')
        for j in range(len(chapters)):
            have_looked = chapters[j].find_element_by_tag_name('i').get_attribute('id')
            if have_looked == 'a':
                continue
            elif have_looked == 'r' and j != len(chapters) - 1:
                chapters[j].find_element_by_tag_name('a').click()
                take_lesson(driver)
            else:
                chapters[j].find_element_by_tag_name('a').click()
                sleep(5)
                driver.switch_to.frame('zwshow')
                if driver.find_element_by_id('sp_index_1').get_attribute('innerHTML') == "已完成":
                    driver.switch_to.default_content()
                    continue
                else:
                    driver.switch_to.default_content()
                    take_lesson(driver)
    driver = page_back(driver)
    return driver


def take_lesson(driver):
    sleep(5)
    driver.switch_to.frame('zwshow')
    start_box = driver.find_element_by_class_name('video-img')
    start_box.find_element_by_tag_name('a').click()
    sleep(10)
    start = driver.find_element_by_class_name('videobtn_popups')
    start.find_element_by_class_name('videobtn_boxw').click()
    try:
        Wait(driver, 1800, 10).until(EC.text_to_be_present_in_element((By.ID, 'sp_index_1'), "已完成"))
    except TimeoutException:
        Wait(driver, 1800, 10).until(EC.text_to_be_present_in_element((By.ID, 'sp_index_2'), "已完成"))
    driver.switch_to.default_content()


def page_back(driver):
    box = driver.find_element_by_class_name('header-c-me')
    hook = box.find_element_by_tag_name('h5')
    ActionChains(driver).move_to_element(hook).perform()
    user = box.find_element_by_class_name('user-center-box')
    ul = user.find_element_by_class_name('clearfix')
    lis = ul.find_elements_by_tag_name('li')
    lis[0].find_element_by_tag_name('a').click()
    driver = load_page(driver)
    return driver


if __name__ == '__main__':
    try:
        driver = webdriver.Chrome("./chromedriver")
        driver.get("https://www.livedu.com.cn/ispace4.0/moocMainIndex/mainIndex.do")
        # driver.get('https://www.livedu.com.cn/ispace4.0/captchaImage?id=8278')
        # driver.maximize_window()
        login(driver)
        yan_zheng(driver)
        driver = class_choose(driver)
    finally:
        driver.close()

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
