from app import mail
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait


def test_send(app):
    with mail.record_messages() as outbox:

        driver = webdriver.Chrome()
        driver.get("http://localhost:5000/contact")
        email = driver.find_element_by_name("email")
        title = driver.find_element_by_name("title")
        message = driver.find_element_by_name("message")
        send_message = driver.find_element_by_name('send_message')

        email.send_keys('tieto.library.testing@gmail.com')
        title.send_keys('testing selenium')
        message.send_keys('testing selenium')
        send_message.click()
        driver.close()
