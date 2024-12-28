import time

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
import pandas as pd

web = 'https://www.thesun.co.uk/sport/football/'
path = "C:\\Users\\LENOVO\\Downloads\\chromedriver-win64 (1)\\chromedriver-win64\\chromedriver.exe"  # introduce path here

# Creating the driver
driver_service = Service(executable_path=path)
driver = webdriver.Chrome(service=driver_service)
driver.get(web)
driver.maximize_window()
# Finding Elements
containers = WebDriverWait(driver, 10).until(
    EC.presence_of_all_elements_located((By.XPATH, '//div[@class="teaser__copy-container"]'))
)

titles = []
subtitles = []
links = []
for container in containers:
    # print(container)
    try:
        highligted_title = container.find_element(by='xpath', value='./a/span').text
    except NoSuchElementException:
        print("highligted_title Element is not founded")
    try:
        title = container.find_element(by='xpath', value='./a/h3').text

        if highligted_title:
            text = highligted_title+' '+title
            titles.append(text)
        else:
            titles.append(title)

    except NoSuchElementException:
        print("Title Element is not founded")
    try:
        subtitle = container.find_element(by='xpath', value='./a/p').text
        subtitles.append(subtitle)
    except NoSuchElementException as e:
        print("Subtitle Element is not founded")
    try:
        link = container.find_element(by='xpath', value='./a').get_attribute('href')
        links.append(link)
    except NoSuchElementException:
        print("Link Element is not founded")


# Exporting data to a CSV file
# Find the minimum length of the lists
min_length = min(len(titles), len(subtitles), len(links))

# Trim all lists to the same length
titles = titles[:min_length]
subtitles = subtitles[:min_length]
links = links[:min_length]

# Create DataFrame
my_dict = {"Title": titles, "Subtitle": subtitles, "Link": links}
df_headlines = pd.DataFrame(my_dict)
df_headlines.to_csv('headline.csv')

driver.quit()
