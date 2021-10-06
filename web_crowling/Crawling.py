# pip3 install selenium
# pip3 install beautifulSoup4

from selenium import webdriver
from bs4 import BeautifulSoup

# colab에서 selenium을 사용 시 아래 코딩 작성 필요
# chrome_options = webdriver.ChromeOptions()
# chrome_options.add_argument('--headless') # headless : 내부 창을 띄우지 못하므로 아예 창을 띄우지 않게 설정
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# driver = webdriver.Chrome('chromedriver', options=chrome_options)
driver = webdriver.Chrome('C:/playwithdata/chromedriver.exe')
url = "http://search.danawa.com/dsearch.php?query=무선청소기&tab=main"
driver.get(url)