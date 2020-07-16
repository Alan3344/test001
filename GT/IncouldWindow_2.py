# File Name : IncouldWindow
# @date : 2020-02-08  11:50

import _thread
import threading
from tkinter import *
from PIL import Image, ImageTk
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup

driver_path1 = 'chrome_driver for 80-version.exe'    # 80 version
driver_path2 = "chrome_driver for 79-version.exe"    # 79 version

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
    """Used url to restart request (start) browser"""
    def __init__(self):

        self.winWidth = 800
        self.winHeight = 600
        self.url = "https://translate.google.cn/#view=home&op=translate&sl="  # "http://www.baidu.com"
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

        # open Chrome

    def openChrome(self):
        self.flag = 1
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('disable-infobars')
        try:    # try error 79 version driver(my chrome current is 80 version)
            self.driver = webdriver.Chrome(executable_path=driver_path2, options=options, desired_capabilities=None)
        except:
            self.driver = webdriver.Chrome(executable_path=driver_path1, options=options,desired_capabilities=None)  # chrome_options=options

        self.driver.get(self.url)
        self.flag += 1


    def new_url(self, words, SourceLanguage="auto", TranslateLanguage='en'):
        default_url = "https://translate.google.cn/#view=home&op=translate&sl=auto&tl=en"
        self.url = default_url + "{}&tl={}&text={}".format(SourceLanguage, TranslateLanguage, words)
        return self.url

    def operatingWeb(self, left_flag=False, right_flag=False):
        # switch language
        # handle = 1
        l_box = ["Auto", "English", "Chinese", "German", "Russian", "Japanese", "French", "Korea"]

        print('Language = [Auto / English / Chinese / German / Russian / Japanese / French / Korea]')
        print("default: %s → %s" % (self.dft_language1, self.dft_language2))
        if left_flag is True:
            while 1:
                left_lang = input('Input Current language category: ')
                if left_lang in l_box:
                    # l_box.remove(left_lang)
                    self.dft_language1 = left_lang
                    break
                else:
                    print("InputError Current language No \"%s\",Please try again!" % left_lang)

        if right_flag is True:
            while 1:
                right_lang = input(
                    'Input Translate language category: ')
                if right_lang == self.dft_language1:
                    print("Duplicate input is invalid")
                elif right_lang in l_box:
                    self.dft_language2 = right_lang
                    break
                else:
                    print("InputError Translate language No \"%s\",Please try again!" % right_lang)
        l_format = switch(self.dft_language1)   # create url private
        r_format = switch(self.dft_language2)

        while 1:
            if self.flag == 1:
                sleep(3)    # wait Chrome start...
            words = input('Input you need translate words[%s --> %s](:quit or exit): ' % (self.dft_language1, self.dft_language2))
            if words in [":quit", ":exit"]:
                print("The program is about to exit!!")
                self.driver.quit()
                sys.exit()
            else:
                # send requests
                request_new_url = self.new_url(words=words, SourceLanguage=l_format, TranslateLanguage=r_format)
                self.driver.get(request_new_url)

            try:
                while 1:
                    sleep(0.4)
                    self.translate_data = self.driver.find_element(By.CSS_SELECTOR,"span.tlid-translation.translation").text
                    break
            except:
                pass
            self.tip = self.driver.find_element(By.CSS_SELECTOR, "div.gt-cc-l div.gt-cc-l-i").text
            print("翻译结果: {}\n其他提示: {}".format(self.translate_data, self.tip))


    def screen(self):
        """No use"""
        win = Tk()
        win.geometry("{}x{}+{}+{}".format(self.winWidth, self.winHeight, self.winX, self.winY))
        area_size = (640, 10)
        button_size = (6, 1)
        # for i in range(5):
        #     Button(win, width=button_size[0], height=button_size[1], bg='blue', text="这是字", fg="gray", bd=0).place(x=60*i,y=0)
        area1 = Label(win, width=area_size[0], height=area_size[1], bg=self.background1)
        area1.place(x=0, y=20)
        # Label(win, width=area_size[0], height=1).pack()
        area2 = Label(win, width=area_size[0], height=area_size[1], bg=self.background2)
        area2.place(x=0, y=210)

        # win.mainloop()  # current browser no use tk window

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
