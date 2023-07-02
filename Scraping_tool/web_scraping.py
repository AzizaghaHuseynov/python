import os
import openai

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests



openai.api_key = "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"

os.environ["PATH"] += os.pathsep + r"C:\path\to\geckodriver.exe"

driver = webdriver.Firefox()


driver.get("https://news.google.com/home?hl=en-US&gl=US&ceid=US:en")

reject_all_cookies = driver.find_element(By.XPATH, '//span[contains(text(), "Reject all")]')
reject_all_cookies.click()


search = driver.find_element(By.CLASS_NAME, "Ax4B8")
search.send_keys("skincare")
search.send_keys(Keys.RETURN)

try:
    main = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CLASS_NAME, "HKt8rc")))

    articles = main.find_elements(By.CLASS_NAME, "MQsxIb")
    counter = 0
    for article in articles:
        counter += 1
        header = article.find_element(By.CLASS_NAME, "ipQwMb")
        article_name = header.text

        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=f"write article about {article_name}",
            max_tokens=400
        )

        # Process the response as needed
        generated_article = response.choices[0].text.strip()


        url = 'http://site-url/wp-json/wp/v2/posts'

        username = 'my-username'
        password = 'my password'

        data = {
            'title': article_name,
            'content': generated_article,
            'status': 'publish'
        }

        response2 = requests.post(url, auth=(username, password), json=data)


finally:
    driver.quit()



