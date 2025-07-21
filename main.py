import time
from selenium import webdriver
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# --- Configuration ---
FPL_LOGIN_URL = "https://fantasy.premierleague.com/"
REFRESH_INTERVAL_SECONDS = 3  # Set the refresh interval in seconds

# --- Set up Firefox options ---
# This is set up to run headlessly, but for the first run, 
# you might want to run with a GUI to log in easily.
# We will run it with a display inside the docker container.
options = Options()
# options.add_argument("--headless") # Disabled for manual login

# --- Main Script ---
print("🚀 Starting FPL Refresher Script")

try:
    # Using a remote WebDriver to connect to the Selenium standalone container
    # The 'selenium' hostname works because Docker's networking will resolve it
    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub',
        options=options
    )
    print("✅ WebDriver connected")

    # Open the FPL login page
    driver.get(FPL_LOGIN_URL)
    print(f"🌍 Navigated to: {FPL_LOGIN_URL}")
    print("❗ ACTION REQUIRED: Please log in to your FPL account in the browser window.")

    # Wait for the user to log in and the page to redirect.
    # We'll detect this by waiting for an element that only appears after login,
    # for example the 'Points/Rank' tab.
    WebDriverWait(driver, 300).until(
        EC.presence_of_element_located((By.XPATH, "//a[contains(text(), 'Points/Rank')]"))
    )
    print("✅ Login detected! Starting auto-refresh loop...")

    # --- Refresh Loop ---
    while True:
        print(f"🔄 Refreshing page at {time.strftime('%Y-%m-%d %H:%M:%S')}")
        driver.refresh()
        time.sleep(REFRESH_INTERVAL_SECONDS)

except Exception as e:
    print(f"❌ An error occurred: {e}")

finally:
    if 'driver' in locals():
        driver.quit()
    print("🛑 Script finished.")