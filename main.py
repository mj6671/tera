from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import os

# Path to the portable Chrome executable
PORTABLE_CHROME_PATH = r'C:\portable-chrome\Chrome-bin\chrome.exe'

def get_driver():
    options = Options()
    options.binary_location = PORTABLE_CHROME_PATH
    options.add_argument(r'--user-data-dir=C:/Users/Mahendran/AppData/Local/Google/Chrome/User Data')
    options.add_argument('--profile-directory=Profile 2')
    options.add_argument("--headless")  # Enable headless mode
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")
    options.add_argument("--disable-gpu")
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--start-maximized")
    options.add_argument("--remote-debugging-port=9222")  # Enable remote debugging
    options.add_argument("--disable-software-rasterizer")  # Disable software rasterizer
    options.add_experimental_option("prefs", {
        "download.default_directory": r"C:\path\to\download\folder",  # Replace with your actual download folder path
        "download.prompt_for_download": False,
        "safebrowsing.enabled": True
    })
    service = Service(r"C:\Users\Mahendran\Downloads\chromedriver-win64\chromedriver-win64\chromedriver.exe")
    return webdriver.Chrome(service=service, options=options)

def is_download_complete(directory, file_name):
    while True:
        files = [f for f in os.listdir(directory) if file_name in f and not f.endswith(".crdownload")]
        if files:
            print(f"Download complete: {files[0]}")
            return True
        time.sleep(1)

def infromwe(url):
    driver = get_driver()
    try:
        driver.get(url)
        print("Browser launched successfully with the specified profile!")

        wait = WebDriverWait(driver, 20)

        save_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "action-bar-save")))
        save_button.click()
        print("Save button clicked successfully.")

        folder_checkbox = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "folder-checkbox")))
        folder_checkbox.click()
        print("Folder checkbox clicked successfully.")

        confirm_button = wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "create-confirm")))
        confirm_button.click()
        print("Confirmation clicked successfully.")

        try:
            folder_name_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "file-item-name-link")))
            folder_name = folder_name_element.text.strip()
            print("Folder Name:", folder_name)
            return folder_name
        except Exception as e:
            print("Folder name not found. Checking for video name...")
            try:
                video_name_element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, "file-name")))
                video_name = video_name_element.text.strip()
                print("Video Name:", video_name)
                return video_name
            except Exception as e:
                print("Error:", e)
                return None
    finally:
        driver.quit()

def download(file_name):
    driver = get_driver()
    try:
        driver.get("https://www.1024terabox.com/main?category=all&path=%2Fteradownload")
        wait = WebDriverWait(driver, 20)

        tbody = wait.until(EC.presence_of_element_located((By.TAG_NAME, "tbody")))
        rows = tbody.find_elements(By.CLASS_NAME, "wp-s-table-skin-hoc__tr")

        for row in rows:
            try:
                file_name_element = row.find_element(By.CLASS_NAME, "list-name-text")
                if file_name in file_name_element.text:
                    print("File found:", file_name_element.text)

                    actions = ActionChains(driver)
                    actions.move_to_element(file_name_element).perform()
                    checkbox = row.find_element(By.CLASS_NAME, "u-checkbox__inner")
                    checkbox.click()
                    print("File selected.")

                    download_button = driver.find_element(By.CLASS_NAME, "u-icon-download")
                    download_button.click()
                    print("Download initiated.")

                    is_download_complete(r"C:\path\to\download\folder", file_name)
                    break
            except Exception as e:
                print("Error processing row:", e)
        else:
            print("File not found.")
    finally:
        driver.quit()
