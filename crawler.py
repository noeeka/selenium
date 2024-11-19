import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import pyautogui
import pyperclip 
import sys
import pymysql
import uuid

pyautogui.FAILSAFE=False
# 导入pymysql模块
import pymysql
RETRIES=3
# 建立数据库连接
conn = pymysql.connect(
    host='192.168.58.131',		# 主机名（或IP地址）
    port=3306,				# 端口号，默认为3306
    user='root',			# 用户名
    password='root',	# 密码
    charset='utf8mb4'  		# 设置字符编码
)
# 创建游标对象
cursor = conn.cursor()
# 选择数据库
conn.select_db("buondua")
end=260
start=0
for i in range(start, end, 20):
    options_hot = webdriver.EdgeOptions()
    options_hot.headless = True
    # options_hot.add_argument("--window-size=1920,1080")  # set window size to native GUI size
    options_hot.add_argument("start-maximized")  # ensure window is full-screen
    options_hot.add_argument("--disable-features=EdgeSignIn")
    driver_chot = webdriver.Edge(options=options_hot)
    driver_chot.get("https://buondua.com/tag/%E7%A5%9E%E6%A5%BD%E5%9D%82%E7%9C%9F%E5%86%AC-11189?start="+str(i))
    elements_collection=driver_chot.find_elements(By.XPATH, "//div[@class='item-thumb']/a")
    print(elements_collection)
    for element_collection in elements_collection:
        options_tag_inner = webdriver.EdgeOptions()
        options_tag_inner.headless = True
        # options_tag_inner.add_argument("--window-size=1920,1080")
        options_tag_inner.add_argument("start-maximized")  # ensure window is full-screen
        options_tag_inner.add_argument("--disable-features=EdgeSignIn")
        driver_tag_inner = webdriver.Edge(options=options_tag_inner)
        driver_tag_inner.maximize_window()
        driver_tag_inner.implicitly_wait(10)
        driver_tag_inner.get(element_collection.get_attribute("href"))
        elements_tags_pages=driver_tag_inner.find_elements(By.XPATH, "//div[@class='pagination-list']/span/a")
        k_page=1
        k_image=1
        half_length = len(elements_tags_pages) // 2
        half_elements_tags_pages = elements_tags_pages[:half_length]

        for element_page in half_elements_tags_pages:
            options_inner = webdriver.EdgeOptions()
            options_inner.headless = True  # hide GUI
            # options_inner.add_argument("--window-size=1920,1080")
            options_inner.add_argument("start-maximized")
            options_inner.add_argument("disable-infobars")
            options_inner.add_argument("--disable-features=EdgeSignIn")
            driver_inner = webdriver.Edge(options=options_inner)
            print(element_page.get_attribute("href"))
            driver_inner.maximize_window()
            # driver_inner.implicitly_wait(20)
            driver_inner.get(element_page.get_attribute("href"))
            elements_images = WebDriverWait(driver_inner, 10).until(EC.visibility_of_all_elements_located((By.XPATH, "//div[@class='article-fulltext']/p/img")))
            
            # elements_images=driver_inner.find_elements(By.XPATH, "//div[@class='article-fulltext']/p/img")
            for element_images in elements_images:
                pyautogui.scroll(10)
                image_url_list=element_images.get_attribute("src").split("?")
                image_url=image_url_list[0]
                image_name=image_url.split("/")[-1]
                cursor.execute('SELECT count(id) FROM `post` where `image_url`="%s" and `image_name`="%s"' % (image_url,image_name))
                result : tuple = cursor.fetchall()
                # check_flag=result[0][0]
                check_flag=0
                if check_flag==0:
                    action = ActionChains(driver_inner).move_to_element(element_images)
                    action.context_click(element_images).perform()
                    time.sleep(2)
                    pyautogui.typewrite(['v'])
                    time.sleep(1)
                    pyautogui.press('enter')
                    time.sleep(1)
                    checker_images=os.path.exists("C:\\Users\\James\\Downloads\\"+image_name)
                    if checker_images:
                        unique_id = uuid.uuid4()
                        cursor.execute('INSERT INTO  `post` SET `uuid`="%s", `image_url`="%s",`category`="%s",`module_name`="%s",`page_url`="%s",`image_name`="%s",`datetime`=%d' % (unique_id,image_url,"神楽坂真冬-11189","神楽坂真冬",element_page.get_attribute("href"),image_name,int(time.time())))
                        conn.commit()
                        k_image=k_image+1
                    else:
                        for retry in range(RETRIES+1):
                            action = ActionChains(driver_inner).move_to_element(element_images)
                            action.context_click(element_images).perform()
                            time.sleep(2)
                            pyautogui.typewrite(['v'])
                            time.sleep(1)
                            pyautogui.press('enter')
                            time.sleep(1)
                            checker_images=os.path.exists("C:\\Users\\James\\Downloads\\"+image_name)
                            if checker_images:
                                unique_id = uuid.uuid4()
                                cursor.execute('INSERT INTO  `post` SET `uuid`="%s", `image_url`="%s",`category`="%s",`module_name`="%s",`page_url`="%s",`image_name`="%s",`datetime`=%d' % (unique_id,image_url,"神楽坂真冬-11189","神楽坂真冬",element_page.get_attribute("href"),image_name,int(time.time())))
                                conn.commit()
                                k_image=k_image+1
                                break

            k_page=k_page+1
            driver_inner.quit()
        driver_tag_inner.quit()

# 关闭游标和连接
cursor.close()
conn.close()
