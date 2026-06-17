import pyautogui
import pyperclip
import pyscreeze
import time
from datetime import datetime

pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.5
pyautogui.hotkey('win', 'r')  # Open the Run dialog
time.sleep(1) 
pyautogui.typewrite('chrome')  # Open Google Chrome
pyautogui.press('enter')  
time.sleep(3) 
pyautogui.hotkey('ctrl', 't')  # Open a new tab 
time.sleep(1)

pyautogui.typewrite('https://www.accuweather.com/en/in/chennai/206671/current-weather/206671')   # ask google for weather
pyautogui.press('enter')  # Press Enter to search
time.sleep(2)  # Wait for the search results to load
pyautogui.moveTo(577, 668)  # Move the mouse to the location of the weather information
time.sleep(1)  # Wait for a moment 
pyautogui.dragTo(625, 668, button='left', duration=1)  # Click and drag to select the weather information
time.sleep(1)  # Wait for a moment
pyautogui.hotkey('ctrl', 'c')  # Copy the selected text
time.sleep(1)  # Wait for a moment
pasted_data = pyperclip.paste()
pyautogui.hotkey('win', 'r')  # Open the Run dialog
time.sleep(1) 

pyautogui.typewrite('excel')  # Open Microsoft Excel
pyautogui.press('enter')
time.sleep(5)  # Wait for Excel to open
current_time = datetime.now().strftime("%Y-%m-%d")  # Get the current date and time
pyautogui.typewrite(current_time)  # Type the current date and time in Excel
time.sleep(1)  # Wait for a moment
pyautogui.press('tab')  # Move to the next cell
time.sleep(1)  # Wait for a moment
pyautogui.hotkey('ctrl', 'v')  # Paste the copied weather information into Excel
time.sleep(1)  # Wait for a moment
pyautogui.press('tab')  # Move to the next cell
time.sleep(1)  # Wait for a moment

if pasted_data >= "30°C":  # Check if the temperature is above or equal to 30°C
        pyautogui.typewrite("It's a hot day! Stay hydrated.")  # Type a message in Excel if it's a hot day
else:
        pyautogui.typewrite("Weather in Chennai: " + pasted_data) # Type the pasted weather information in Excel
time.sleep(2)  # Wait for a moment

screenshot = pyscreeze.screenshot('weather_info.png')  # Load the screenshot
screenshot.save(r'C:\Users\Admin\OneDrive\Desktop\weather_info.png')  # Save the screenshot as a PNG file
time.sleep(1)  # Wait for a moment
pyautogui.hotkey('ctrl', 's')  # Save the Excel file
time.sleep(1)  # Wait for a moment

pyautogui.typewrite('Daily_Weather_Report')  # Type the file name
# pyautogui.press('enter')  # Press Enter to save the file
time.sleep(1)  # Wait for a moment

# pyautogui.hotkey('alt', 'f4')  # Close Excel
