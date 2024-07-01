import os
import time
import pyperclip
import pyautogui
import glob
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.alert import Alert
from selenium.common.exceptions import TimeoutException
import GenerateGPTArticle as GPT
import json
import random

class WordpressAutomation:
    def __init__(self):
        self.driver = webdriver.Chrome(executable_path ="C:/Program Files (x86)/chromedriver.exe")
        self.base_url = 'https://free-excel-templates.com'
        self.upload_completed = False

    def upload_file(self, file_path):
        self.driver.get('https://www.upfast.info/')
        upload_input = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'input[type="file"]')))

        upload_input.send_keys(file_path)
        time.sleep(10)
        copy_button = self.driver.find_element(By.ID, 'copy')
        copy_button.click()
        clipboard_text = pyperclip.paste()
        file_link = clipboard_text
        return file_link

    def extract_title_from_excel(self, excel_path):
        title = os.path.splitext(os.path.basename(excel_path))[0]
        return title

    def login(self, username, password):
        self.driver.get(self.base_url + '/wp-login.php')
        username_entry = self.driver.find_element(By.ID, 'user_login')
        username_entry.send_keys(username)
        password_entry = self.driver.find_element(By.ID, 'user_pass')
        password_entry.send_keys(password)
        signin_button = self.driver.find_element(By.ID, 'wp-submit')
        signin_button.click()
        time.sleep(5)
        self.driver.get(self.base_url + '/wp-admin/post-new.php')

    def enter_article_title(self, title):
        self.driver.switch_to.active_element.send_keys(title)
        time.sleep(2)

    def read_article_content(self, prompt):
        article = GPT.generate_articlegenerate_article(prompt)
        return article

    def enter_article_content(self, content):
        pyautogui.press('tab')
        self.driver.switch_to.active_element.send_keys(content)
        time.sleep(2)
        post_button = self.driver.find_element(By.XPATH, '//*[@id="editor"]/div/div[1]/div[1]/div[2]/div[3]/div/div[2]/ul/li[1]/button')
        post_button.click()
        time.sleep(2)

    def select_categories(self, categories):
        time.sleep(5)
        selected_categories = []
        category_search_bar = self.driver.find_element(By.CLASS_NAME, 'components-text-control__input')
        category_search_bar.click()
        for category in categories:
            category_search_bar.send_keys(category)
            time.sleep(5)

            actions = ActionChains(self.driver)
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.TAB)
            actions.send_keys(Keys.SPACE)
            actions.perform()
            selected_categories.append(category)
            category_search_bar.clear()
            time.sleep(1)
        return selected_categories

    def enter_tags(self, selected_categories):
        tags_input = self.driver.find_element(By.CSS_SELECTOR, 'input.components-form-token-field__input')
        for category in selected_categories:
            tags_input.send_keys(category)
            tags_input.send_keys(Keys.ENTER)
        time.sleep(5)

    def click_set_featured_image(self):
        set_image_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Set featured image")]')
        set_image_button.click()
        upload_file_button = self.driver.find_element(By.XPATH, '//*[@id="menu-item-upload"]')
        upload_file_button.click()
        time.sleep(5)

    def select_file_for_featured_image(self, image_file):
        select_files_button = self.driver.find_element(By.XPATH, '//button[contains(text(), "Select Files")]')
        action = ActionChains(self.driver)
        action.move_to_element(select_files_button).click().perform()
        time.sleep(2)
        pyautogui.write(image_file)
        pyautogui.press('enter')
        time.sleep(25)

    def finalize_featured_image_selection(self):
        set_image_button = self.driver.find_element(By.XPATH, '//button[@class="button media-button button-primary button-large media-button-select" and contains(text(), "Set featured image")]')
        set_image_button.click()
        time.sleep(15)

    def get_recommendation(self, tag):
        with open("C:\\E partician\\Projects\\Excel_Template_Automation\\FreeExcelTemplate.json", 'r') as file:
            articles = json.load(file)
        matching_articles = [article for article in articles if tag in article['tags']]

        if not matching_articles:
            matching_articles.append(random.choice(articles))

        return matching_articles[0] 

    def create_button(self, link, current_tags):
        template_1 = """ 
        
        <div class="wp-block-buttons"><!-- wp:button {"align":"center"} --> <div class="wp-block-button aligncenter"><a class="wp-block-button__link wp-element-button" href="
        """
        template_2 = """ "  rel="noreferrer noopener">Download</a></div>"""
        button = template_1 + link + template_2

        # Switch to code editor
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).key_down(Keys.ALT).send_keys('m').perform()
        actions.key_up(Keys.CONTROL).key_up(Keys.SHIFT).key_up(Keys.ALT).perform()

        # Find the textarea container
        textarea = self.driver.find_element(By.ID, 'post-content-0')

        # Cut the existing content and save it to a variable
        self.driver.execute_script("arguments[0].select(); document.execCommand('cut');", textarea)
        existing_content = pyperclip.paste()

        tag_to_search = current_tags[2] if len(current_tags) > 2 else None
        if tag_to_search:
            recommended_article = self.get_recommendation(tag_to_search)

        related_topics = f"""
        <!-- wp:heading {"level":4} -->
        <h4 class="wp-block-heading">Related Topics</h4>
        <!-- /wp:heading -->

        <!-- wp:list -->
        <ul>
            <!-- wp:list-item -->
            <li><a href="{recommended_article['href']}">{recommended_article['text']}</a></li>
            <!-- /wp:list-item -->

            <!-- You can repeat the above line for more recommendations if needed -->

        </ul>

                <ul>
            <!-- wp:list-item -->
            <li><a href="{recommended_article['href']}">{recommended_article['text']}</a></li>
            <!-- /wp:list-item -->

            <!-- You can repeat the above line for more recommendations if needed -->

        </ul>

                <ul>
            <!-- wp:list-item -->
            <li><a href="{recommended_article['href']}">{recommended_article['text']}</a></li>
            <!-- /wp:list-item -->

            <!-- You can repeat the above line for more recommendations if needed -->

        </ul>

                <ul>
            <!-- wp:list-item -->
            <li><a href="{recommended_article['href']}">{recommended_article['text']}</a></li>
            <!-- /wp:list-item -->

            <!-- You can repeat the above line for more recommendations if needed -->

        </ul>
        <!-- /wp:list -->
        """

        # Create the modified content with related topics, button, and existing content
        modified_content = existing_content + related_topics + button

        # Clear the textarea and write the modified content
        self.driver.execute_script("arguments[0].value = '';", textarea)
        textarea.send_keys(modified_content)

        # Switch back to normal mode for the next post
        actions = ActionChains(self.driver)
        actions.key_down(Keys.CONTROL).key_down(Keys.SHIFT).key_down(Keys.ALT).send_keys('m').perform()
        actions.key_up(Keys.CONTROL).key_up(Keys.SHIFT).key_up(Keys.ALT).perform()
        time.sleep(10)

    def Save_article(self):
        save_button = self.driver.find_element(By.XPATH, ' //*[@id="editor"]/div/div[1]/div[1]/div[1]/div/div[3]/button[1] ')
        save_button.click()
        time.sleep(10)
        

    def create_post(self, username, password, excel_folder_path, image_folder_path, categories):
        excel_files = glob.glob(os.path.join(excel_folder_path, '*.xlsx')) + glob.glob(os.path.join(excel_folder_path, '*.xls')) + glob.glob(os.path.join(excel_folder_path, '*.csv'))
        for excel_file in excel_files:
            file_name = os.path.splitext(os.path.basename(excel_file))[0]
            text_file = os.path.join(excel_folder_path, file_name + '.txt')
            image_file = os.path.join(image_folder_path, file_name + '.png')

            title = self.extract_title_from_excel(excel_file)
            link = self.upload_file(excel_file)

            # Generate the article content using OpenAI API
            #content = self.read_article_content(prompt)

            with open("content.txt", "r") as file:
                content = file.read()


            # Perform the login and create the post using the extracted title, generated content, and image file
            self.login(username, password)
            self.enter_article_title(title)
            self.enter_article_content(content)
            selected_categories = self.select_categories(categories)
            self.enter_tags(selected_categories)
            self.click_set_featured_image()
            self.select_file_for_featured_image(image_file)
            self.finalize_featured_image_selection()
            self.create_button(link, selected_categories)
            self.Save_article()
            #self.close()

    def close(self):
        self.driver.quit()