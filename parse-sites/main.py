from selenium import webdriver
from selenium_stealth import stealth
from bs4 import BeautifulSoup
import time


def init_webdriver():
    init_driver = webdriver.Chrome()
    stealth(init_driver,
            platform="Win32")
    return init_driver


def scrolldown(driver, deep):
    for _ in range(deep):
        driver.execute_script('window.scrollBy(0, 500)')
        time.sleep(0.1)


def get_main_page_cards(driver, url):
    driver.get(url)
    scrolldown(driver, 50)

    main_page_html = BeautifulSoup(driver.page_source, "html.parser")

    content = main_page_html.find("div", {"class": "container"})
    children_last = content.findChildren(recursive=False)[-1].find("div")

    print(children_last)
    input("Cont ? ")


if __name__ == '__main__':
    driver = init_webdriver()
    get_main_page_cards(driver, 'https://ozon.ru')
    driver.quit()
