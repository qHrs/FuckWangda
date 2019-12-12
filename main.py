# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         main
# Description:  
# Author:       qpand
# Date:         2019/12/10
#-------------------------------------------------------------------------------

from selenium import webdriver
import time
from lxml import etree

options = webdriver.ChromeOptions()

executable_path = r"webdriver\chromedriver.exe"

options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
#options.add_argument('User-Agent=Mozilla/5.0 (Linux; U; Android 8.1.0; zh-cn; BLA-AL00 Build/HUAWEIBLA-AL00) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/57.0.2987.132 MQQBrowser/8.9 Mobile Safari/537.36')
browser = webdriver.Chrome(executable_path=executable_path, options=options)

#打开页面
browser.get("https://wangda.andedu.net/")
time.sleep(10)

print(browser.title)

username = "38006067"
password = "!Q2w3e4r"

# 登录
browser.find_element_by_id('D23username').send_keys(username)
browser.find_element_by_id('D23password').send_keys(password)
browser.find_element_by_id('D23login').click()

time.sleep(5)

html = browser.page_source
if html.find("退出账号"):
    print("登陆成功")

    surl = "https://wangda.andedu.net/#/study/subject/detail/e8b602bb-8731-4b5b-8d4d-67c0f1b2eba7"  # 揭秘云计算

    browser.get(surl)
    time.sleep(5)
    html = browser.page_source
    selector = etree.HTML(html)
    classList = selector.xpath('//div[contains(@class,"catalog-state-info")]/div/div[2]/div[1]/text()')
    classStatus = selector.xpath('//div[contains(@class,"catalog-state-info")]/div/div[3]/a/div/text()')
    classIdList = selector.xpath('//div[contains(@class,"catalog-state-info")]/div/div[3]/a/@data-resource-id')

    courseList = []
    for title, status, classId in zip(classList, classStatus, classIdList):
        if status in ["继续学习", "开始学习"]:
            course = {}
            course["name"] = title
            course["status"] = status
            course["classId"] = classId
            courseList.append(course)

    for item in courseList:
        print("%s - %s - %s" % (item["name"], item["status"], item["classId"]))

    for item in courseList:
        print("%s 开始学习" % (item["name"]))

        # 播放
        # 课程url 0-视频id 1-课程id
        subjectID = surl.split("/")[7]
        #browser.get("https://wangda.andedu.net/#/study/course/detail/subject-course/f62887c2-69f3-4e17-ac15-a5b186411ea5/6/73bfb6cd-ad81-4b9e-ac5d-c8694f49eb2d")
        courseUrl = "https://wangda.andedu.net/#/study/course/detail/subject-course/{0}/6/{1}"
        browser.get(courseUrl.format(item["classId"], subjectID))
        # '//div[contains(@class,"chapter-list")]/ul/li/div/dl/dd/div/span[1]/text()'

        playS = ''
        while True:
            html = browser.page_source
            selector = etree.HTML(html)
            playNewS = selector.xpath('//div[contains(@class,"chapter-list")]/ul/li/div/dl/dd/div/span[1]/text()')
            if len(playNewS) > 0:

                if playS == "":
                    playS = playNewS[0]
                    print(playS)

                if playS in ["重新学习", "学习中"] :
                    print("%s 已完成" % (item["name"]))
                    break

                if playS != playNewS[0]:
                    playS = playNewS[0]
                    print(playS)
                else:
                    print("-", end='')

                time.sleep(2)

    # https://wangda.andedu.net/#/study/course/detail/subject-course/f9a4a6c5-152d-4971-a420-e4416ffcf509/6/e8b602bb-8731-4b5b-8d4d-67c0f1b2eba7

    # print(html)   data-resource-id  $x('//div[contains(@class,"catalog-state-info")]/div/div[3]/a[contains(@data-resource-id)]')
    #//*[@id="D177studyBtn-67d0102f-8164-43cc-8d7a-01b2b94e4084"]
    # https://wangda.andedu.net/#/study/course/detail/subject-course/d42558f8-ba03-4d23-89ed-c6d8b3fe5fc7/6/e8b602bb-8731-4b5b-8d4d-67c0f1b2eba7
    # $x('//div[contains(@class,"chapter-list")]/ul/li/div/dl/dd/div/span[contains(@class,"progress")]/text()')

