from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import time
import csv

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
dict()


def get_linkslist(file_name):
    f = open(file_name, 'r+')
    get_lists = f.read()
    links_lists = get_lists.split(', ')
    return links_lists


def list_to_dict(list):
    dic = dict()
    key = ''
    bound = len(list)
    i = 1
    while i < bound:
        if i % 2 == 1:
            key = list[i]
        else:
            value = list[i]
            dic[key] = value
        i = i + 1
    return dic


tienich_dict = {
    'Máy lạnh': 0,
    'WC riêng': 0,
    'Chổ để xe': 0,
    'Wifi': 0,
    'Tự do': 0,
    'Không chung chủ': 0,
    'Tủ lạnh': 0,
    'Máy giặt': 0,
    'Bảo vệ': 0,
    'Giường ngủ': 0,
    'Nấu ăn': 0,
    'Tivi': 0,
    'Thú cưng': 0,
    'Tủ đồ': 0,
    'Cửa sổ': 0,
    'Máy nước nóng': 0,
    'Gác lửng': 0
}


def getdata(link):
    driver.get(link)
    time.sleep(0.05)
    driver.get(link)
    time.sleep(0.05)
    title = driver.find_elements("xpath", '//*[@id="root"]/div/div[2]/div[2]/h1')[0].text
    thongtinphong = driver.find_elements("xpath", '//*[@id="root"]/div/div[2]/div[4]/div[1]/div[1]')[0].text
    tienich = driver.find_elements("xpath", '//*[@id="root"]/div/div[2]/div[4]/div[1]/div[2]/div[2]')[0].text
    motathem = driver.find_elements("xpath", '//*[@id="root"]/div/div[2]/div[4]/div[1]/div[4]/div[2]/pre')[0].text
    ngaydang = driver.find_elements("xpath", '//*[@id="root"]/div/div[2]/div[4]/div[2]/div[2]/div[2]/span[2]')[0].text
    thongtinchuphong = driver.find_elements("xpath", '//*[@id="root"]/div/div[2]/div[4]/div[2]/div[2]/div[1]/span')[0].text
    luuy = driver.find_elements("xpath", '//*[@id="root"]/div/div[2]/div[4]/div[1]/div[3]')[0].text
    thongtinphong = thongtinphong.split('\n')
    tienich = tienich.split('\n')
    print(tienich)
    for ele in tienich:
        tienich_dict[ele] = 1
    dict2 = list_to_dict(thongtinphong)
    dict = {'Title': title,
            'Mô tả thêm': motathem,
            'Thông tin chủ phòng': thongtinchuphong,
            'Ngày đăng': ngaydang,
            'Lưu ý': luuy,
            'GIÁ PHÒNG': 'NO VALUE', ''
            'DIỆN TÍCH': 'NO VALUE',
            'ĐẶT CỌC': 'NO VALUE',
            'SỨC CHỨA': 'NO VALUE',
            'TRẠNG THÁI': 'NO VALUE',
            'ĐIẠ CHỈ': 'NO VALUE'
            }
    dict.update(dict2)
    dict.update(tienich_dict)
    print(dict)
    return dict


fields = ['Loại phòng', 'Title', 'Mô tả thêm', 'Thông tin chủ phòng',
          'Ngày đăng', 'Lưu ý', 'GIÁ PHÒNG', 'DIỆN TÍCH',
          'ĐẶT CỌC', 'SỨC CHỨA', 'TRẠNG THÁI', 'ĐIẠ CHỈ',
          'ĐIỆN', 'NƯỚC', 'WIFI',
          'Máy lạnh', 'WC riêng', 'Chổ để xe', 'Wifi', 'Tự do',
          'Không chung chủ', 'Tủ lạnh', 'Máy giặt', 'Bảo vệ', 'Giường ngủ',
          'Nấu ăn', 'Tivi', 'Thú cưng', 'Tủ đồ', 'Cửa sổ', 'Máy nước nóng', 'Gác lửng']


def write_csv(dictionary):
    file_path = "data.csv"
    try:
        with open(file_path, 'a') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fields)
            #writer.writeheader()
            #for data in dictionary:
            writer.writerow(dictionary)
    except IOError:
        print("I/O error")


#links_list = get_linkslist('linkslistHanoi.txt')
# 1520 index
links_list = get_linkslist('linkslistHCM.txt')
#30970 index HCM
# crawl dc tu trang thu start_index den trang end_index - 1
for i in range(28000, 30970):
    print("Crawling trang web thứ: " + str(i))
    link = links_list[i].split('\\')
    print('-----------------------------------------------------------')
    print(link[0])
    print(link[1])
    dict_loaiphong = {'Loại phòng': link[1]}
    try:
        data_new = getdata(link[0])
        data_new.update(dict_loaiphong)
        write_csv(data_new)
    except:
        print("Error at page " + str(i))
