import os
import time
import pyautogui
import cv2
import numpy as np


class ExcelScreenshotTaker:
    def __init__(self, file_path, save_path):
        self.file_path = file_path
        self.save_path = save_path

    
    def open_excel_file(self):
        os.startfile(self.file_path)
        time.sleep(2)
        
    def handle_auto_recover(self, x_coordinate = 270, y_coordinate = 950):
        # Move the mouse to the specific coordinate and left-click to close the auto recover dialog
        pyautogui.moveTo(x_coordinate, y_coordinate)
        pyautogui.click()
        
    def take_screenshot(self):
        pyautogui.sleep(4)  # Wait for Excel to open (adjust if needed)
        screenshot = pyautogui.screenshot()
        image = cv2.cvtColor(
            np.array(screenshot),
            cv2.COLOR_RGB2BGR
        )
        cropped_image = self.crop_image(image)  # Crop the image from below
        cv2.imwrite(self.save_path, cropped_image)
        
    def crop_image(self, image):
        # Define the cropping dimensions
        crop_height = 100  # Adjust the value as needed
        height, width = image.shape[:2]
        cropped_image = image[:height-crop_height, :]
        return cropped_image

    def save_file(self):
        pyautogui.hotkey('ctrl', 's')
        time.sleep(2)

    def close_excel_file(self):
        os.system("taskkill /f /im excel.exe")
        time.sleep(2)

    def run(self):
        self.open_excel_file()
        self.handle_auto_recover() 
        self.take_screenshot()
        self.save_file()
        self.close_excel_file()