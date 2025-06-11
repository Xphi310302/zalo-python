import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
import openpyxl as xl

# Path to Firefox executable
firefox_path = "/usr/local/bin/firefox"

# Set up Firefox options
options = Options()
options.binary_location = firefox_path

# Initialize the Firefox webdriver
browser = webdriver.Firefox(options=options)

# Opening the Zalo website
browser.get("https://chat.zalo.me/")

# Maximize the browser window
browser.maximize_window()

# Wait for the page to load
time.sleep(20)

# Click add friend button
# <i class="fa fa-outline-add-new-contact-2 pre"></i>
clickaddfriend = browser.find_element(
    By.XPATH, '//i[@class="fa fa-outline-add-new-contact-2 pre"]'
).click()

# Wait for the add friend dialog to appear
time.sleep(2)


# Hard-coded phone numbers for mock testing
rangea = ["0368321314", "0348235724"]

# Loop through each phone number in the Excel range
for sdt in rangea:
    phone_number_in = browser.find_element(
        By.XPATH, '//input[@class="phone-i-input flx-1"]'
    )
    phone_number_in.clear()
    phone_number_in.send_keys(sdt)

    # Click "Tìm kiếm" (Search) button
    time.sleep(2)
    ctimkiem = browser.find_element(
        By.XPATH,
        '//div[@class="z--btn--v2 btn-primary large zl-modal_footer_button --rounded zl-modal_footer_button"]',
    ).click()

    # Click "Nhắn tin" (Message) button
    time.sleep(2)
    cnhantin = browser.find_element(By.XPATH, '//span[@class="btnpf-content"]').click()

    # Send multiple messages
    for i in range(50):
        # Wait for the input field to be ready
        time.sleep(2)

        # Find and click the message input field
        input_text = browser.find_element(By.XPATH, '//div[@id="input_line_0"]')
        input_text.click()

        # Type the message
        time.sleep(2)
        input_text.send_keys(f"Hello! This is automated message #{i + 1}")

        # Click send button
        time.sleep(2)
        sentmes = browser.find_element(
            By.XPATH, '//div[@data-translate-inner="STR_SEND"]'
        ).click()

    # Wait between contacts
    time.sleep(40)

    # Go back to add friend screen for the next contact
    browser.get("https://chat.zalo.me/")
    time.sleep(5)
    clickaddfriend = browser.find_element(
        By.XPATH, '//i[@class="fa fa-outline-add-new-contact-2 pre"]'
    ).click()
    time.sleep(2)

# Close the browser when done
browser.quit()
