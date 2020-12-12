import datetime
import time

from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

# To remove Chrome console from .exe add creationflags=CREATE_NO_WINDOW parameter to Lib\site-packages\selenium\webdriver\common\services.py method of subprocess.Popen(**)
# from win32process import CREATE_NO_WINDOW
# pyinstaller --onefile -w main.py

driver = webdriver.Chrome('chromedriver/chromedriver.exe')
driver.get("http://www.instagram.com")
# driver.implicitly_wait(5)
wait = WebDriverWait(driver, 40)

username = ''
password = ''
followers = []


def login():
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='username']"))).click()
    driver.find_element_by_xpath("//input[@name='username']").send_keys(username)
    wait.until(ec.element_to_be_clickable((By.XPATH, "//input[@name='password']"))).click()
    driver.find_element_by_xpath("//input[@name='password']").send_keys(password)
    wait.until(ec.element_to_be_clickable((By.XPATH, "//div[contains(text(),'Log In')]"))).click()
    time.sleep(5)

    try:
        WebDriverWait(driver, 8).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
    except TimeoutException:
        pass

    try:
        WebDriverWait(driver, 8).until(
            ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Not Now')]"))).click()
    except TimeoutException:
        pass


def track_followers():
    time.sleep(4)
    wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[@href='/{username}/followers/']")))

    foll_num = driver.find_element_by_xpath(f"//a[@href='/{username}/followers/']/span").text
    foll_num = int(foll_num)

    wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[@href='/{username}/followers/']"))).click()
    time.sleep(2)

    wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[@href='/{username}/followers/']")))
    # find all li elements in list
    fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 0
    while scroll < 500:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(.5)
        scroll += 1

        foll_list = len(driver.find_elements_by_xpath("//div[@class='isgrP']//li"))
        if foll_list >= foll_num:
            break

    wait.until(ec.presence_of_all_elements_located((By.XPATH, "//div[@class='isgrP']//li//span/a")))
    follow_list = driver.find_elements_by_xpath("//div[@class='isgrP']//li//span/a")

    for folls in follow_list:
        followers.append(folls.text)

    # close window
    wait.until(ec.element_to_be_clickable((By.XPATH, "(//div[@class='QBdPU '])[2]"))).click()


# DRY principles do not always make sense while making independent scripts
def remove_nonfollowing():
    time.sleep(2)
    wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[@href='/{username}/following/']")))
    foll_num = driver.find_element_by_xpath(f"//a[@href='/{username}/following/']/span").text
    foll_num = int(foll_num)
    wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[@href='/{username}/following/']"))).click()
    time.sleep(2)

    wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[@href='/{username}/following/']")))

    fBody = driver.find_element_by_xpath("//div[@class='isgrP']")
    scroll = 0
    while scroll < 500:
        driver.execute_script('arguments[0].scrollTop = arguments[0].scrollTop + arguments[0].offsetHeight;', fBody)
        time.sleep(.5)
        scroll += 1

        foll_list = len(driver.find_elements_by_xpath("//div[@class='isgrP']//li"))
        if foll_list >= foll_num:
            break

    wait.until(ec.presence_of_all_elements_located((By.XPATH, "//div[@class='isgrP']//li//span/a")))
    following_list = driver.find_elements_by_xpath("//div[@class='isgrP']//li//span/a")

    xpath = 1
    for folls in following_list:
        if folls.text not in followers:
            print(folls.text + " Removed")
            time.sleep(150)
            wait.until(ec.element_to_be_clickable((By.XPATH, f"(//button[contains(text(), 'Follow')])[{xpath}]"))).click()
            wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Unfollow')]"))).click()
        xpath += 1

    # close window
    wait.until(ec.element_to_be_clickable((By.XPATH, "(//div[@class='QBdPU '])[2]"))).click()


def add_suggested():
    time.sleep(3)
    wait.until(ec.element_to_be_clickable((By.XPATH, "//div[contains(text(),'See All')]"))).click()
    time.sleep(2)
    wait.until(ec.presence_of_all_elements_located((By.XPATH, "//button[text()='Follow']")))
    wait.until(ec.visibility_of_all_elements_located((By.XPATH, "//button[text()='Follow']")))

    requested = driver.find_elements_by_xpath("//button[text()='Requested']")
    for req in requested:
        ActionChains(driver).move_to_element(req).click(req).perform()
        time.sleep(2)
        wait.until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'Unfollow')]"))).click()

        censor = driver.find_elements_by_xpath("//button[contains(text(),'OK')]")
        if censor:
            try:
                WebDriverWait(driver, 1).until(
                    ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK')]"))).click()
            except TimeoutException:
                pass
        time.sleep(5)


    new_friend = driver.find_elements_by_xpath("//button[text()='Follow']")

    added = 1
    for friend in new_friend:
        ActionChains(driver).move_to_element(friend).click(friend).perform()

        censor = driver.find_elements_by_xpath("//button[contains(text(),'OK')]")
        if censor:
            try:
                WebDriverWait(driver, 1).until(ec.element_to_be_clickable((By.XPATH, "//button[contains(text(),'OK')]"))).click()
            except TimeoutException:
                pass

        # Safety precautions to not get account suspended for being a bot.  Max 15 people a day in this scenario.
        if added == 15:
            break
        added += 1

        time.sleep(10)


def give_em_love(runtime):
    try:
        wait.until(ec.presence_of_all_elements_located((By.XPATH, "//*[local-name()='svg'][@aria-label='Like'][@width='24']")))
        wait.until(ec.visibility_of_all_elements_located((By.XPATH, "//*[local-name()='svg'][@aria-label='Like'][@width='24']")))
    except TimeoutException:
        pass

    hearts = driver.find_elements_by_xpath("//*[local-name()='svg'][@aria-label='Like'][@width='24']")
    for heart in hearts:
        ActionChains(driver).move_to_element(heart).click(heart).perform()
        time.sleep(1)

    more_hearts = driver.find_elements_by_xpath("//*[local-name()='svg'][@aria-label='Like'][@width='24']")
    if more_hearts and runtime < 700:
        give_em_love(runtime)
    else:
        print('exit recursion')


def main():

    login()

    day_of_week = datetime.datetime.today().weekday()
    # Remove nonfollowers on Friday
    if day_of_week == 4:
        # go to my account page
        wait.until(ec.element_to_be_clickable((By.XPATH, f"//a[contains(text(),'{username}')]"))).click()
        track_followers()
        time.sleep(2)
        remove_nonfollowing()

    time.sleep(2)
    # Go Home
    wait.until(ec.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@aria-label='Home']"))).click()
    add_suggested()

    time.sleep(2)
    # Go Home
    wait.until(ec.element_to_be_clickable((By.XPATH, "//*[local-name()='svg'][@aria-label='Home']"))).click()
    runtime = time.perf_counter()
    give_em_love(runtime)

    driver.close()


if __name__ == '__main__':
    main()
else:
    print('Not running main file!')
