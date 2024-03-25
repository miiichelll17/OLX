import time
from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException

# Function to get the data from the page
options = webdriver.ChromeOptions()
options.add_argument("start-maximized")
# Tambahkan opsi untuk mengabaikan kesalahan sertifikat
options.add_argument("--ignore-certificate-errors")
url = 'https://www.olx.co.id/jawa-barat_g2000009/mobil_c86'
# Tambahkan opsi saat inisialisasi driver
driver = webdriver.Chrome()
driver.maximize_window()
driver.get(url)

# Scroll down 50 times to load more data
for i in range(50):
    time.sleep(5)
    try:
        driver.find_element(By.CSS_SELECTOR, "div._38O09 > button").click()
        time.sleep(5)
    except NoSuchElementException:
        break

time.sleep(5)

products = []
soup = BeautifulSoup(driver.page_source, "html.parser")
for item in soup.find_all('li', class_='_1DNjI'):
    product_name = item.find('span', class_= '_2poNJ').text
    price = item.find('span', class_= '_2Ks63').text
    products.append((product_name, price))


# Perbaiki nama kolom di sini
df = pd.DataFrame(products, columns=['product_name', 'price'])
print(df)

df.to_csv('olxscrapping.csv', index=False)
print('Data has been saved')
driver.close()
