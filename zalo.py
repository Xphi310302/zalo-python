import time
import sys
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import (
    TimeoutException,
    NoSuchElementException,
    WebDriverException,
)

# Path to geckodriver
geckodriver_path = "/snap/bin/geckodriver"

# Set up service
service = Service(executable_path=geckodriver_path)

# Initialize the Firefox webdriver
browser = webdriver.Firefox(service=service)

# Opening the Zalo website
browser.get("https://chat.zalo.me/")

# Maximize the browser window
browser.maximize_window()

# Wait for the page to load
time.sleep(20)

try:
    # Wait for add friend button to be clickable and click it
    print("Waiting for add friend button...")
    add_friend_button = WebDriverWait(browser, 20).until(
        EC.element_to_be_clickable(
            (By.XPATH, '//i[@class="fa fa-outline-add-new-contact-2 pre"]')
        )
    )
    add_friend_button.click()
    print("Add friend button clicked successfully")

    # Wait for the add friend dialog to appear
    time.sleep(1)
except TimeoutException:
    print("Could not find the add friend button. Taking screenshot for debugging...")
    # browser.save_screenshot("error_add_friend.png")
    print(
        "Page source:", browser.page_source[:500]
    )  # Print first 500 chars of page source
    raise


# Hard-coded phone numbers for mock testing
phone_numbers = ["913524579", "0368321314"]

try:
    # Loop through each phone number
    for phone_number in phone_numbers:
        try:
            print(f"Processing phone number: {phone_number}")

            # Wait for phone number input field and enter the number
            phone_input = WebDriverWait(browser, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@class="phone-i-input flx-1"]')
                )
            )
            phone_input.clear()
            phone_input.send_keys(phone_number)
            print(f"Entered phone number: {phone_number}")

            # Try to click "Tìm kiếm" (Search) button
            try:
                print("Clicking search button...")
                search_button = WebDriverWait(browser, 10).until(
                    EC.element_to_be_clickable(
                        (By.XPATH, '//div[@data-id="btn_Main_AddFrd_Search"]')
                    )
                )
                search_button.click()
                print("Search button clicked successfully")

                # Try to click "Nhắn tin" (Message) button
                try:
                    print("Waiting for message button...")
                    message_button = WebDriverWait(browser, 10).until(
                        EC.element_to_be_clickable(
                            (By.XPATH, '//div[@data-translate-inner="STR_CHAT"]')
                        )
                    )
                    message_button.click()
                    print("Message button clicked successfully")
                except Exception as e:
                    print(f"Error clicking message button: {str(e)}")
                    # browser.save_screenshot(f"message_button_error_{phone_number}.png")
                    continue  # Skip to the next phone number
            except Exception as e:
                print(f"Error clicking search button: {str(e)}")
                # browser.save_screenshot(f"search_button_error_{phone_number}.png")
                continue  # Skip to the next phone number

            # Send multiple messages
            message_count = 3  # Reduced from 50 for testing
            for i in range(message_count):
                try:
                    # Wait for the input field to be ready
                    print(f"Preparing to send message {i + 1}/{message_count}")

                    # Target the specific rich text input field based on the HTML structure
                    try:
                        # Target the richInput element which is the contenteditable div
                        time.sleep(1)
                        rich_input = WebDriverWait(browser, 10).until(
                            EC.presence_of_element_located((By.ID, "richInput"))
                        )
                        rich_input.click()
                        print("Clicked on rich input field")

                        # Use PyAutoGUI to type the message (simulates actual keyboard typing)
                        time.sleep(0.5)
                        message_text = f"Hello! This is automated message #{i + 1}"

                        # Clear any existing text first
                        rich_input.clear()

                        # Type the message using PyAutoGUI with pauses between characters

                        pyautogui.write(message_text, interval=0.1)
                        print(f"Typed message using PyAutoGUI: {message_text}")

                        # Wait a moment for the UI to update after typing
                        time.sleep(0.1)

                        # Try multiple methods to send the message
                        try:
                            # Method 1: Press Enter using PyAutoGUI
                            pyautogui.press("enter")
                            print(
                                f"Message {i + 1} sent by pressing Enter with PyAutoGUI"
                            )
                        except Exception as e:
                            print(f"PyAutoGUI Enter method failed: {str(e)}")
                            try:
                                # Method 2: Try clicking the send button
                                send_button = WebDriverWait(browser, 5).until(
                                    EC.element_to_be_clickable(
                                        (
                                            By.XPATH,
                                            '//div[@data-translate-inner="STR_SEND"]',
                                        )
                                    )
                                )
                                send_button.click()
                                print(f"Message {i + 1} sent by clicking send button")
                            except Exception as e2:
                                print(f"Send button method failed: {str(e2)}")
                                # Method 3: Try using Selenium's Keys.RETURN
                                rich_input.send_keys(Keys.RETURN)
                                print(
                                    f"Message {i + 1} sent using Selenium Keys.RETURN"
                                )

                        # Take a screenshot after sending
                        # browser.save_screenshot(f"sent_message_{phone_number}_{i}.png")

                    except Exception as e:
                        print(f"Error sending message {i + 1}: {str(e)}")
                        # browser.save_screenshot(f"error_message_{phone_number}_{i}.png")

                except Exception as e:
                    print(f"Error sending message {i + 1}: {str(e)}")
                    # browser.save_screenshot(f"error_message_{phone_number}_{i}.png")

            # Wait between contacts
            print(
                f"Finished sending messages to {phone_number}. Waiting before next contact..."
            )

            # Go back to add friend screen for the next contact
            # browser.get("https://chat.zalo.me/")
            # print("Navigated back to main page")

            # Wait for page to load and click add friend button again
            time.sleep(1)
            add_friend_button = WebDriverWait(browser, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//i[@class="fa fa-outline-add-new-contact-2 pre"]')
                )
            )
            add_friend_button.click()
            print("Add friend button clicked for next contact")
            time.sleep(0.5)

        except Exception as e:
            print(f"Error processing phone number {phone_number}: {str(e)}")
            # browser.save_screenshot(f"error_{phone_number}.png")
            continue  # Continue with next phone number

except Exception as e:
    print(f"Fatal error in main loop: {str(e)}")
    # browser.save_screenshot("fatal_error.png")
    sys.exit(1)

# Print completion message and close the browser
print("Script completed successfully!")
try:
    browser.quit()
    print("Browser closed successfully")
except Exception as e:
    print(f"Error closing browser: {str(e)}")

print("Script execution finished")
