# File Name : GoogleTranslate_3
# @date : 2020-02-10  16:15

import threading
from tkinter import *
from PIL import Image, ImageTk
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver_path1 = 'chrome_driver for 80-version.exe'    # 80版本
driver_path2 = "chrome_driver for 79-version.exe"    # 79版本
def changeRgb(*rgb):
    RGB = []
    for r in rgb:
        RGB.append(r)
    return '#%02x%02x%02x' % (RGB[0], RGB[1], RGB[2])


def switch(language='Auto'):
    Language = {
        "Auto": "auto",
        "English": "en",
        "Chinese": "zh-CN",
        "German": "de",
        "Russian": "ru",
        "Japanese": "ja",
        "French": 'fr',
        "Korea": "ko",
    }
    if language in Language.keys():
        return Language[language]

print("Please wait while the program is starting ...")
class MainForm(object):
    def __init__(self):

        self.winWidth = 800
        self.winHeight = 600
        self.url = "https://translate.google.cn/#view=home&op=translate&sl=auto&tl=en"  # "http://www.baidu.com"
        self.winX = int((1920 - self.winWidth) / 2)
        self.winY = int((1080 - self.winHeight) / 2)
        self.background1 = changeRgb(132, 188, 80)
        self.background2 = changeRgb(178, 224, 223)

        self.driver = None
        self.flag = None
        self.dft_language1 = 'Auto'
        self.dft_language2 = 'English'
        self.result = ''
        self.tip = ''
        self.translate_data = ''
        self.error_version = None


        # open Chrome
    def openChrome(self):
        self.flag = 1
        options = webdriver.ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('disable-infobars')
        try:
            self.driver = webdriver.Chrome(executable_path=driver_path2, options=options, desired_capabilities=None)
        except:
            self.error_version = 1
            self.driver = webdriver.Chrome(executable_path=driver_path1, options=options,desired_capabilities=None)  # chrome_options=options
        self.driver.get(self.url)
        self.flag += 1

    def new_url(self, words, SourceLanguage="auto", TranslateLanguage='en'):
        default_url = "https://translate.google.cn/#view=home&op=translate&sl=auto&tl=en"
        self.url = default_url + "{}&tl={}&text={}".format(SourceLanguage, TranslateLanguage, words)
        return self.url

    def operatingWeb(self, left_flag=False, right_flag=False):
        # switch language
        l_box = ["Auto", "English", "Chinese", "German", "Russian", "Japanese", "French", "Korea"]
        left_lang, right_lang = '', ''
        # print('Language = [Auto / English / Chinese / German / Russian / Japanese / French / Korea]')
        # print("default: %s → %s" % (self.dft_language1, self.dft_language2))
        if left_flag is True:
            while 1:
                left_lang = input('Input Current language category: ')
                if left_lang in l_box:
                    self.dft_language1 = left_lang
                    break
                else:
                    print("InputError Current language No \"%s\",Please try again!" % left_lang)

        if right_flag is True:
            while 1:
                right_lang = input('Input Translate language category: ')
                if right_lang == self.dft_language1:
                    print("Duplicate input is invalid")
                elif right_lang in l_box:
                    self.dft_language2 = right_lang
                    break
                else:
                    print("InputError Translate language No \"%s\",Please try again!" % right_lang)
        # l_format = switch(self.dft_language1)     # create url private
        # r_format = switch(self.dft_language2)

        # Mock request
        if self.flag == 1:
            sleep(3)  # Wait Chrome start
        if self.error_version == 1:
            print("Version Error wait 2s")
            sleep(2)
        while 1:
            words = input('Input you need translate words[%s --> %s](:quit or exit): ' % (self.dft_language1, self.dft_language2))

            if words in [":quit", ":exit"]:
                print("The program is about to exit!!")
                self.driver.quit()
                sys.exit()
            else:
                source_text = ''
                try:
                    source_text = self.driver.find_element(By.CSS_SELECTOR, '#source').text
                    if source_text is not None:
                        self.driver.find_element(By.CSS_SELECTOR, '#source').clear()
                except:
                    print("First Enter, source_text = ''")

                self.driver.find_element(By.CSS_SELECTOR, '#source').send_keys(words)   # request web info

            try:
                while 1:
                    sleep(0.6)
                    self.translate_data = self.driver.find_element(By.CSS_SELECTOR,"span.tlid-translation.translation").text
                    break
            except:
                pass
            self.tip = self.driver.find_element(By.CSS_SELECTOR, "div.gt-cc-l div.gt-cc-l-i").text
            print("翻译结果: {}\n其他提示: {}".format(self.translate_data, self.tip))

            # get translate category(L/R)
            L_lang_box_ele = '.sl-sugg .sl-sugg-button-container'      # div[role="button"]
            R_lang_box_ele = '.tl-sugg .sl-sugg-button-container'
            L = len(self.driver.find_element(By.CSS_SELECTOR, L_lang_box_ele).find_elements(By.TAG_NAME, 'div'))
            R = len(self.driver.find_element(By.CSS_SELECTOR, R_lang_box_ele).find_elements(By.TAG_NAME, 'div'))
            # _bs4 = BeautifulSoup('')
            L_category_box = []
            R_category_box = []
            L_selected = None  # used right clicked
            R_selected = None
            for i in range(1, L+1):
                L_category = self.driver.find_element(By.CSS_SELECTOR,'.sl-sugg .sl-sugg-button-container div[role="button"]:nth-child({})'.format(i)).text
                L_category_box.append(L_category)

                try:  # jg which is selected
                    L_ele = '.sl-sugg div[aria-pressed="true"]:nth-child({})'.format(i)
                    self.driver.find_element(By.CSS_SELECTOR, L_ele)
                    L_selected = i
                except:
                    pass

            for j in range(1, R+1):
                R_category = self.driver.find_element(By.CSS_SELECTOR,'.tl-sugg .sl-sugg-button-container div[role="button"]:nth-child({})'.format(j)).text
                R_category_box.append(R_category)

                try:  # jg which is selected
                    R_ele = '.tl-sugg div[aria-pressed="true"]:nth-child({})'.format(j)
                    self.driver.find_element(By.CSS_SELECTOR, R_ele)
                    R_selected = j
                except:
                    pass
            print("L_selected={} && R_selected={}".format(L_selected, R_selected))
            print("left select: {} right select: {}".format(L_category_box[L_selected-1], R_category_box[R_selected-1]))
            print('left category:{}\nright category:{}'.format(L_category_box, R_category_box))


def main():
    app = MainForm()
    threading.Thread(target=app.openChrome).start()
    threading.Thread(target=app.operatingWeb).start()

def application():
    app = MainForm()
    # app.screen()  //主窗体
    # app.operatingWeb(left_flag=True, right_flag=True)
    app.operatingWeb()

if __name__ == '__main__':
    # application()
    main()
