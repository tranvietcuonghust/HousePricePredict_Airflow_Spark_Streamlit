from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time

chrome_options = Options()
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--window-size=1920x1080")
chrome_options.add_argument("--remote-debugging-port=9225")
chrome_options.add_argument("--ignore-certificate-errors")
chrome_prefs = {}
chrome_options.experimental_options['prefs'] = chrome_prefs
chrome_prefs['profile.default_content_settings'] = {'images': 2}
chrome_prefs['profile.managed_default_content_settings'] = {'images': 2}
driver = webdriver.Chrome(options=chrome_options, executable_path='/home/cuong/Downloads/chromedriver/chromedriver')


def get_pages(start, end):
    url = 'https://www.ohanaliving.vn/#/viewAll/newRooms/'
    link_pages = []
    for i in range(start, end+1):
        link_pages.append(url + str(i))
    return link_pages


def get_xpath1st(start, end):
    str1 = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div['
    str2 = ']/a'
    xpath = []
    for i in range(start, end+1):
        xpath.append(str1 + str(i) + str2)
    return xpath


def get_xpath2nd(start, end):
    str3 = '//*[@id="root"]/div/div[2]/div[2]/div/div[2]/div['
    str4 = ']/a/div/div[2]/div/div[1]/div[1]/span[2]'
    xpath = []
    for i in range(start, end+1):
        xpath.append(str3 + str(i) + str4)
    return xpath


def get_list_urls(xpath1st, xpath2nd, links_page):
    urls = []
    driver.get(links_page[0])
    time.sleep(5)
    for link in links_page:
        time.sleep(0.05)
        driver.get(link)
        time.sleep(0.05)
        nextlinks = [driver.find_elements("xpath", Xpath1)[0].get_attribute("href") for Xpath1 in xpath1st]
        loaicanho = [driver.find_elements("xpath", Xpath2)[0].text for Xpath2 in xpath2nd]
        print(nextlinks)
        print(loaicanho)
        for i in range(0, len(nextlinks)):
            urls.append(nextlinks[i] + '\\' + loaicanho[i])
    return urls


def write_linkslist(urls):
    for link in urls:
        f.write(link + ', ')


xpath1st = get_xpath1st(1, 10)
xpath2nd = get_xpath2nd(1, 10)

link_pages = get_pages(1, 3097)
print(link_pages)
#Hanoi: 152
#f = open('linkslistHanoi.txt', 'r+')
#HCM: 3097
f = open('linkslistHCM.txt', 'r+')
urls = get_list_urls(xpath1st, xpath2nd, link_pages)

print(type(urls))
print(urls)
write_linkslist(urls)
