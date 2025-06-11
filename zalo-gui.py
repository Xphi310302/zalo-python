import os
import time
import platform
import pandas as pd
import streamlit as st
import pyautogui
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.firefox import GeckoDriverManager
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager


def naive_linechunk():
    # Remove all CSV files in the current directory when starting the app
    for file in os.listdir():
        if file.endswith(".csv"):
            try:
                os.remove(file)
                print(f"Removed old status file: {file}")
            except Exception as e:
                print(f"Error removing file {file}: {e}")


# Run the function when defined
naive_linechunk()

# Set page config
st.set_page_config(
    page_title="Zalo Automation Tool",
    page_icon="📱",
    layout="wide",
    initial_sidebar_state="expanded",
)

# CSS for better styling
st.markdown(
    """
<style>
    .main {
        padding: 2rem;
    }
    .status-success {
        color: green;
        font-weight: bold;
    }
    .status-failed {
        color: red;
        font-weight: bold;
    }
    .status-running {
        color: blue;
        font-weight: bold;
    }
</style>
""",
    unsafe_allow_html=True,
)

# Initialize session state variables if they don't exist
if "phone_status" not in st.session_state:
    st.session_state.phone_status = pd.DataFrame(
        columns=["Phone Number", "Status", "Timestamp"]
    )
if "is_running" not in st.session_state:
    st.session_state.is_running = False
if "completed" not in st.session_state:
    st.session_state.completed = False
if "browser" not in st.session_state:
    st.session_state.browser = None
if "csv_path" not in st.session_state:
    st.session_state.csv_path = (
        f"zalo_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    )

# Default delay times (in seconds)
if "delay_times" not in st.session_state:
    st.session_state.delay_times = {
        "page_load": 10,
        "after_click": 2,
        "after_search": 2,
        "after_message_button": 2,
        "between_messages": 2,
        "after_send": 1.0,  # Make sure this is a float
        "between_contacts": 40,
    }


# Function to update status and export to CSV
def update_status(phone_number, status, rerun=False):
    print(f"Updating status for {phone_number}: {status}")

    # Add new row to the status dataframe
    new_row = pd.DataFrame(
        {
            "Phone Number": [phone_number],
            "Status": [status],
            "Timestamp": [datetime.now().strftime("%Y-%m-%d %H:%M:%S")],
        }
    )
    st.session_state.phone_status = pd.concat(
        [st.session_state.phone_status, new_row], ignore_index=True
    )

    # Export to CSV in real-time
    st.session_state.phone_status.to_csv(st.session_state.csv_path, index=False)

    # Only rerun if explicitly requested
    # During automation, we don't want to rerun as it disrupts the flow
    if rerun:
        st.rerun()


# We'll use session state to store the browser instead of a global variable


# Function to initialize the browser
def initialize_browser(headless=False):
    try:
        # Detect operating system
        os_name = platform.system()
        print(f"Detected operating system: {os_name}")

        # Try browsers in order of preference
        browser_instance = None
        browsers_to_try = ["firefox", "chrome", "edge"]

        for browser_name in browsers_to_try:
            try:
                if browser_instance is not None:
                    break

                print(f"Attempting to initialize {browser_name} browser...")

                if browser_name == "firefox":
                    # Set up Firefox options
                    options = webdriver.FirefoxOptions()
                    if headless:
                        options.add_argument("--headless")

                    # Try to use webdriver_manager to get the driver
                    try:
                        service = FirefoxService(GeckoDriverManager().install())
                        browser_instance = webdriver.Firefox(
                            service=service, options=options
                        )
                        print("Firefox browser initialized using webdriver_manager")
                    except Exception as e:
                        print(
                            f"Failed to initialize Firefox with webdriver_manager: {str(e)}"
                        )

                        # Try with system path as fallback
                        if os_name == "Linux":
                            geckodriver_path = "/snap/bin/geckodriver"
                        else:  # Windows or other
                            geckodriver_path = "geckodriver.exe"

                        if os.path.exists(geckodriver_path):
                            service = FirefoxService(executable_path=geckodriver_path)
                            browser_instance = webdriver.Firefox(
                                service=service, options=options
                            )
                            print(
                                f"Firefox browser initialized using system path: {geckodriver_path}"
                            )

                elif browser_name == "chrome":
                    # Set up Chrome options
                    options = webdriver.ChromeOptions()
                    if headless:
                        options.add_argument("--headless")

                    # Try to use webdriver_manager to get the driver
                    service = ChromeService(ChromeDriverManager().install())
                    browser_instance = webdriver.Chrome(
                        service=service, options=options
                    )
                    print("Chrome browser initialized")

                elif browser_name == "edge":
                    # Set up Edge options
                    options = webdriver.EdgeOptions()
                    if headless:
                        options.add_argument("--headless")

                    # Try to use webdriver_manager to get the driver
                    service = EdgeService(EdgeChromiumDriverManager().install())
                    browser_instance = webdriver.Edge(service=service, options=options)
                    print("Edge browser initialized")

            except Exception as e:
                print(f"Failed to initialize {browser_name} browser: {str(e)}")

        if browser_instance is None:
            raise Exception(
                "Failed to initialize any browser. Please install Firefox, Chrome, or Edge."
            )

        # Opening the Zalo website
        browser_instance.get("https://chat.zalo.me/")

        # Maximize the browser window
        browser_instance.maximize_window()

        print("Browser initialized and navigated to Zalo")

        # Wait for the page to load (important for Zalo)
        time.sleep(st.session_state.delay_times["page_load"])
        print("Initial page load wait completed")

        # Store the browser in session state
        st.session_state.browser = browser_instance
        return True
    except Exception as e:
        st.error(f"Error initializing browser: {str(e)}")
        print(f"Browser initialization error: {str(e)}")
        return False


# Function to run the automation for a single phone number
def process_phone_number(
    browser_instance, phone_number, message_template, message_count, delay_times=None
):
    # Use the passed browser instance instead of the global one
    # Use provided delay times or defaults from session state
    if delay_times is None:
        delay_times = st.session_state.delay_times
    try:
        # First navigate to the main page to ensure we're in the right context
        print("Navigating to main Zalo page...")
        browser_instance.get("https://chat.zalo.me/")
        time.sleep(5)
        print("Navigation complete, page loaded")

        # Take screenshot for debugging
        screenshot_path = f"zalo_before_click_{phone_number}.png"
        # browser_instance.save_screenshot(screenshot_path)
        print(f"Screenshot saved to {screenshot_path}")

        # Click add friend button - using the same approach as in zalo.py
        try:
            print("Waiting for add friend button...")
            # Print page source to help debug
            print("Page title:", browser_instance.title)
            print("Current URL:", browser_instance.current_url)

            # Try to find the add friend button
            add_friend_button = WebDriverWait(browser_instance, 20).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//i[@class="fa fa-outline-add-new-contact-2 pre"]')
                )
            )
            print("Add friend button found, clicking...")
            add_friend_button.click()
            print("Add friend button clicked successfully")
            time.sleep(delay_times["after_click"])

            # Take another screenshot after clicking
            # browser_instance.save_screenshot(f"zalo_after_click_{phone_number}.png")
        except TimeoutException as e:
            print(f"Could not find the add friend button: {str(e)}")
            print("Taking screenshot for debugging...")
            # browser_instance.save_screenshot(f"error_add_friend_{phone_number}.png")
            print(
                "Page source:", browser_instance.page_source[:500]
            )  # Print first 500 chars of page source
            update_status(
                phone_number, "Failed - Add Friend Button Not Found", rerun=False
            )
            return False

        # Wait for phone number input field and enter the number
        try:
            print("Waiting for phone number input field...")
            phone_input = WebDriverWait(browser_instance, 10).until(
                EC.presence_of_element_located(
                    (By.XPATH, '//input[@class="phone-i-input flx-1"]')
                )
            )
            phone_input.clear()
            phone_input.send_keys(phone_number)
            print(f"Entered phone number: {phone_number}")
            # browser_instance.save_screenshot(f"entered_number_{phone_number}.png")
        except TimeoutException as e:
            print(f"Could not find the phone number input field: {str(e)}")
            # browser_instance.save_screenshot(f"phone_input_error_{phone_number}.png")
            update_status(phone_number, "Failed - Phone Input Not Found", rerun=False)
            return False

        # Try to click "Tìm kiếm" (Search) button
        try:
            print("Clicking search button...")
            search_button = WebDriverWait(browser_instance, 10).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[@data-id="btn_Main_AddFrd_Search"]')
                )
            )
            search_button.click()
            print("Search button clicked successfully")
            # browser_instance.save_screenshot(f"search_clicked_{phone_number}.png")
            time.sleep(delay_times["after_search"])  # Wait for search results
        except Exception as e:
            print(f"Error clicking search button: {str(e)}")
            # browser_instance.save_screenshot(f"search_button_error_{phone_number}.png")
            update_status(phone_number, "Failed - Search Button Error", rerun=False)
            return False

        # Try to click "Nhắn tin" (Message) button
        try:
            print("Waiting for message button...")
            message_button = WebDriverWait(browser_instance, 3).until(
                EC.element_to_be_clickable(
                    (By.XPATH, '//div[@data-translate-inner="STR_CHAT"]')
                )
            )
            message_button.click()
            print("Message button clicked successfully")
            # browser_instance.save_screenshot(f"message_clicked_{phone_number}.png")
            time.sleep(
                delay_times["after_message_button"]
            )  # Wait for chat window to open
        except Exception as e:
            print(f"Error clicking message button: {str(e)}")
            # browser_instance.save_screenshot(f"message_button_error_{phone_number}.png")
            update_status(phone_number, "Failed - Message Button Error", rerun=False)
            return False

        # Send multiple messages
        messages_sent = 0
        for i in range(message_count):
            try:
                print(f"Preparing to send message {i + 1}/{message_count}")

                # Target the richInput element which is the contenteditable div
                time.sleep(1)
                rich_input = WebDriverWait(browser_instance, 10).until(
                    EC.presence_of_element_located((By.ID, "richInput"))
                )
                rich_input.click()
                print("Clicked on rich input field")

                # Use PyAutoGUI to type the message (simulates actual keyboard typing)
                time.sleep(0.5)
                message_text = message_template.replace("{i}", str(i + 1))

                # Clear any existing text first
                rich_input.clear()

                # Type the message using PyAutoGUI with interval
                pyautogui.write(message_text, interval=0.1)
                print(f"Typed message using PyAutoGUI: {message_text}")

                # Wait a moment for the UI to update after typing
                time.sleep(0.1)

                # Try multiple methods to send the message
                try:
                    # Method 1: Press Enter using PyAutoGUI
                    pyautogui.press("enter")
                    print(f"Message {i + 1} sent by pressing Enter with PyAutoGUI")
                    messages_sent += 1
                except Exception as e:
                    print(f"PyAutoGUI Enter method failed: {str(e)}")
                    try:
                        # Method 2: Try clicking the send button
                        send_button = WebDriverWait(browser_instance, 5).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//div[@data-translate-inner="STR_SEND"]')
                            )
                        )
                        send_button.click()
                        print(f"Message {i + 1} sent by clicking send button")
                        messages_sent += 1
                    except Exception as e2:
                        print(f"Send button method failed: {str(e2)}")
                        # Method 3: Try using Selenium's Keys.RETURN
                        rich_input.send_keys(Keys.RETURN)
                        print(f"Message {i + 1} sent using Selenium Keys.RETURN")
                        messages_sent += 1

                # Wait between messages
                time.sleep(delay_times["between_messages"])

            except Exception as e:
                print(f"Error sending message {i + 1}: {str(e)}")
                continue

        # Update status based on how many messages were sent
        if messages_sent == message_count:
            update_status(phone_number, "Success - All Messages Sent", rerun=False)
            return True
        elif messages_sent > 0:
            update_status(
                phone_number,
                f"Partial - {messages_sent}/{message_count} Messages Sent",
                rerun=False,
            )
            return True
        else:
            update_status(phone_number, "Failed - No Messages Sent", rerun=False)
            return False

    except Exception as e:
        print(f"Error processing phone number {phone_number}: {str(e)}")
        update_status(phone_number, f"Failed - {str(e)[:50]}", rerun=False)
        return False


# Function to run the automation process
def run_automation(
    phone_numbers, message_template, message_count, wait_time, rerun=False
):
    # Store current automation instance to detect reruns
    current_instance = st.session_state.automation_instance

    # Create status placeholder for updates
    status_placeholder = st.empty()
    status_placeholder.info("Starting automation process...")
    print("Starting automation process...")

    # Initialize browser if needed
    if "browser" not in st.session_state or st.session_state.browser is None:
        status_placeholder.info("Initializing browser...")
        print("Initializing browser...")
        if not initialize_browser():
            status_placeholder.error(
                "Failed to initialize browser. Please check your browser installation."
            )
            st.session_state.is_running = False
            st.session_state.completed = True
            print("Browser initialization failed!")
            return
        status_placeholder.info("Browser initialized successfully")
        print("Browser initialized successfully")

    # Use the browser from session state
    # Wait for Zalo to load and user to log in
    status_placeholder.info("Waiting for Zalo to load and user to log in...")
    print("Waiting for Zalo to load and user to log in...")
    time.sleep(st.session_state.delay_times["page_load"])
    print("Wait complete, starting to process phone numbers")
    print("Wait complete, starting to process phone numbers")

    # Process each phone number
    st.info(f"Found {len(phone_numbers)} phone numbers to process")
    print(f"Found {len(phone_numbers)} phone numbers to process")

    for i, phone_number in enumerate(phone_numbers):
        phone_number = phone_number.strip()
        if not phone_number:
            st.warning(f"Skipping empty phone number at position {i + 1}")
            print(f"Skipping empty phone number at position {i + 1}")
            continue

        # Update status to "Processing"
        status_message = (
            f"Processing phone number {i + 1}/{len(phone_numbers)}: {phone_number}"
        )
        status_placeholder.info(status_message)
        print(status_message)
        update_status(phone_number, "Processing", rerun=False)

        # Process the phone number
        try:
            st.info(f"Calling process_phone_number for {phone_number}")
            print(f"Calling process_phone_number for {phone_number}")
            result = process_phone_number(
                st.session_state.browser,
                phone_number,
                message_template,
                message_count,
                delay_times=st.session_state.delay_times,
            )
            st.info(f"process_phone_number completed with result: {result}")
            print(f"process_phone_number completed with result: {result}")
        except Exception as e:
            st.error(f"Error in process_phone_number: {str(e)}")
            print(f"Error in process_phone_number: {str(e)}")

        # Wait between contacts
        st.info(f"Waiting {wait_time} seconds before next contact...")
        print(f"Waiting {wait_time} seconds before next contact...")
        time.sleep(wait_time)

    # Mark automation as completed but keep browser open
    status_placeholder.success(
        "Automation completed! Browser remains open for further use."
    )
    print("Automation completed! Browser remains open for further use.")

    # Set states to indicate completion
    st.session_state.is_running = False
    st.session_state.completed = True
    st.session_state.last_completed_instance = current_instance

    # Exit the function to prevent any further processing
    return


# Main app layout
st.title("Zalo Web Automation")

# Add a refresh button at the top right
if not st.session_state.is_running:
    col1, col2 = st.columns([10, 1])
    with col2:
        if st.button("🔄", help="Refresh the status table"):
            st.rerun()

# Check if we need to prevent automation from running again
# This handles the case where Streamlit reruns the script after completion
if "last_completed_instance" in st.session_state and st.session_state.completed:
    if st.session_state.last_completed_instance == st.session_state.automation_instance:
        st.session_state.is_running = False

# Tabs for different sections
tab1, tab2 = st.tabs(["Automation", "Status"])

# Automation tab content
with tab1:
    st.header("Automation Settings")

    # Message template
    message_template = st.text_area(
        "Message Template",
        "Hello! This is automated message #{i}",
        help="Use {i} as a placeholder for the message number",
    )

    # Number of messages per contact
    message_count = st.number_input(
        "Messages per Contact", min_value=1, max_value=50, value=3
    )

    # Wait time between contacts
    wait_time = st.number_input(
        "Wait Time Between Contacts (seconds)", min_value=5, max_value=300, value=5
    )

    # Advanced settings expander
    with st.expander("Advanced Timing Settings"):
        st.session_state.delay_times["page_load"] = st.slider(
            "Page Load Wait Time (seconds)",
            min_value=5,
            max_value=30,
            value=st.session_state.delay_times["page_load"],
        )
        st.session_state.delay_times["after_click"] = st.slider(
            "Wait After Button Click (seconds)",
            min_value=1,
            max_value=10,
            value=st.session_state.delay_times["after_click"],
        )
        st.session_state.delay_times["after_search"] = st.slider(
            "Wait After Search (seconds)",
            min_value=1,
            max_value=10,
            value=st.session_state.delay_times["after_search"],
        )
        st.session_state.delay_times["after_message_button"] = st.slider(
            "Wait After Message Button (seconds)",
            min_value=1,
            max_value=10,
            value=st.session_state.delay_times["after_message_button"],
        )
        st.session_state.delay_times["between_messages"] = st.slider(
            "Wait Between Messages (seconds)",
            min_value=1,
            max_value=10,
            value=st.session_state.delay_times["between_messages"],
        )
        st.session_state.delay_times["after_send"] = st.slider(
            "Wait After Send (seconds)",
            min_value=0.5,
            max_value=5.0,
            value=float(st.session_state.delay_times["after_send"]),
            step=0.5,
        )

    # Start/Stop button and browser control
    col1, col2 = st.columns(2)

    if st.session_state.is_running:
        if col1.button("Stop Automation", type="primary"):
            st.session_state.is_running = False
            st.rerun()
    else:
        # Only show browser controls when not running automation
        if st.session_state.browser is not None:
            # Browser is open
            if col1.button("Close Browser", type="secondary"):
                try:
                    st.session_state.browser.quit()
                    st.session_state.browser = None
                    st.success("Browser closed successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error closing browser: {str(e)}")

            if col2.button("Reset Browser", help="Close and reopen browser"):
                try:
                    st.session_state.browser.quit()
                    st.session_state.browser = None
                    initialize_browser()
                    st.success("Browser reset successfully")
                    st.rerun()
                except Exception as e:
                    st.error(f"Error resetting browser: {str(e)}")
        else:
            # No browser open
            if col1.button("Initialize Browser"):
                initialize_browser()
                st.rerun()

        # Start automation button
        start_button = st.button("Start Automation", type="primary")

# Main content area
col1, col2 = st.columns([3, 2])

with col1:
    st.header("Phone Numbers")
    phone_numbers_text = st.text_area(
        "Enter phone numbers (one per line)",
        height=300,
        help="Enter each phone number on a new line",
    )

    # Display current status
    if st.session_state.is_running:
        st.markdown(
            "<p class='status-running'>Automation is running...</p>",
            unsafe_allow_html=True,
        )

with col2:
    st.header("Status")

# Status tab content
with tab2:
    st.header("Status")
    st.dataframe(st.session_state.phone_status, use_container_width=True)

    # Display CSV path
    st.info(f"Status saved to: {st.session_state.csv_path}")

    # Add download button for CSV
    if not st.session_state.phone_status.empty:
        csv_data = st.session_state.phone_status.to_csv(index=False)
        st.download_button(
            label="Download CSV",
            data=csv_data,
            file_name=st.session_state.csv_path,
            mime="text/csv",
        )
    else:
        st.info("No phone numbers processed yet.")

# Create keys to track automation state across Streamlit reruns
if "automation_instance" not in st.session_state:
    st.session_state.automation_instance = 0

if "last_completed_instance" not in st.session_state:
    st.session_state.last_completed_instance = -1

# Handle the start button click
if not st.session_state.is_running and start_button:
    # Parse phone numbers
    phone_numbers = [
        num.strip() for num in phone_numbers_text.split("\n") if num.strip()
    ]

    if not phone_numbers:
        st.error("Please enter at least one phone number.")
    else:
        # Reset the completion flag when starting new automation
        st.session_state.is_running = True
        st.session_state.completed = False
        # Increment automation instance to track this specific run
        st.session_state.automation_instance += 1

        # Create a new CSV file for this run
        st.session_state.csv_path = (
            f"zalo_status_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        )

        # Start the automation in a separate thread
        st.info(f"Starting automation for {len(phone_numbers)} phone numbers...")

        # This will block the UI until completion in Streamlit
        # In a production app, you might want to use threading or async
        run_automation(phone_numbers, message_template, message_count, wait_time)

# Footer
st.markdown("---")
st.caption("Zalo Automation Tool - Use responsibly")
