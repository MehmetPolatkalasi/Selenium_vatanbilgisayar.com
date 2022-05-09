from selenium import webdriver
from webdriver_manager.firefox import GeckoDriverManager
import time
import xlsxwriter

# Create a workbook and add a worksheet.
workbook = xlsxwriter.Workbook("apple_fiyatları.xlsx")   
worksheet = workbook.add_worksheet("apple_telefon_fiyatları")

bold = workbook.add_format({'bold': True})  # Add a bold format to use to highlight cells.
money = workbook.add_format({'num_format': '$#,##0'})  # Add a number format for cells with money.

# Write some data headers.
worksheet.write('A1', 'Model', bold)
worksheet.write('B1', 'Fiyat', bold)


browser = webdriver.Firefox(executable_path=GeckoDriverManager().install())

url = "https://www.vatanbilgisayar.com/cep-telefonu-modelleri/"

browser.get(url)
time.sleep(3)

# Choose Apple model
apple = browser.find_element_by_xpath("/html/body/main/div[3]/div/div/div[3]/div[4]/div[2]/div[2]/div/ul/li[1]/a/div/span[2]")
apple.click()

# Sort from expensive to cheap
sort_list = browser.find_element_by_xpath("/html/body/main/div[3]/div/div/div[2]/div[2]/div[2]/select/option[3]")
sort_list.click()
time.sleep(5)

# Models
models = browser.find_elements_by_xpath("/html/body/main/div[3]/div/div/div[4]/div[3]/div[*]/div[2]/a/div[2]")
count = 1

# Prices
prices = browser.find_elements_by_xpath("/html/body/main/div[3]/div/div/div[4]/div[3]/div[*]/div[2]/div[2]/span[1]")

model_list = []
price_list = []

for model in models:
    model_list.append(model.text)

for price in prices:
    price_list.append(price.text)

last_list = list(zip(model_list,price_list))

# Start from the first cell below the headers.
row = 1
col = 0

# Iterate over the data and write it out row by row.
for model,fiyat in last_list:
    worksheet.write(row,col,model)
    worksheet.write(row,col+1,fiyat,money)
    row +=1



    


workbook.close()
time.sleep(1)
browser.close()