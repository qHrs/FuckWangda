# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         main
# Description:  FuckWangda
# Author:       qpand
# Date:         2019/12/10
#-------------------------------------------------------------------------------

from selenium import webdriver
import time
from lxml import etree

options = webdriver.ChromeOptions()

executable_path = r"D:\PycharmProjects\FuckWangda\webdriver\chromedriver.exe"

options.add_argument('--no-sandbox')  # 解决DevToolsActivePort文件不存在的报错
options.add_argument('window-size=1920x1080')  # 指定浏览器分辨率
options.add_argument('--disable-gpu')  # 谷歌文档提到需要加上这个属性来规避bug
options.add_argument('--hide-scrollbars')  # 隐藏滚动条, 应对一些特殊页面
options.add_argument('blink-settings=imagesEnabled=false')  # 不加载图片, 提升速度
options.add_argument('--headless')  # 浏览器不提供可视化页面. linux下如果系统不支持可视化不加这条会启动失败
options.add_argument('log-level=3')  # 只输出失败信息
browser = webdriver.Chrome(executable_path=executable_path, options=options)

# 打开登陆页面
browser.get("https://wangda.andedu.net/")
time.sleep(5)

print(browser.title)

username = "13540098614"
password = "Fuckwangda2018"
#username = "13608170940"
#password = "Linda@135"

# 登录
browser.find_element_by_id('D23username').send_keys(username)
browser.find_element_by_id('D23password').send_keys(password)
browser.find_element_by_id('D23login').click()

time.sleep(5)

html = browser.page_source
if html.find("退出账号"):
    realName = browser.find_element_by_xpath('//div[@class="user-info-top"]/div[2]/div[1]/div[1]').get_attribute("innerText")
    print("%s 登陆成功" % realName)

    # 专题ID
    subjectIDList = ["85400297-7e8b-4dab-88a4-7959cfa0fd10",
            "33b5fe33-79ba-47dc-bec0-3b7a5ce7b2ce",
            "49060db8-fd8a-401e-aaf1-727281900af1",
            "73bfb6cd-ad81-4b9e-ac5d-c8694f49eb2d",
            "271080e4-0e39-4f7b-961c-cc0e5bffba2b",
            "46b0c273-0eb2-4cba-9117-af13f751813b",
            "1a7a41e5-6b7c-4074-b2d7-7c85a857280e",
            "e8b602bb-8731-4b5b-8d4d-67c0f1b2eba7",
            "a8dfcf08-a8fa-4963-9a6e-44448a540e28"]

    # 永远都学不完的bug
    #bugUrl = ["40f280e7-09f1-43e4-b7da-5e1edd70f1e1"]
    bugUrl = []

    for subjectID in subjectIDList:
        url = "https://wangda.andedu.net/#/study/subject/detail/{0}"
        browser.get(url.format(subjectID))
        time.sleep(5)
        html = browser.page_source
        # browser.find_element_by_xpath
        selector = etree.HTML(html)
        classList = selector.xpath('//div[contains(@class,"catalog-state-info")]/div/div[2]/div[1]/text()')
        classStatus = selector.xpath('//div[contains(@class,"catalog-state-info")]/div/div[3]/a/div/text()')
        classIdList = selector.xpath('//div[contains(@class,"catalog-state-info")]/div/div[3]/a/@data-resource-id')

        courseList = []
        for title, status, classId in zip(classList, classStatus, classIdList):
            if status in ["继续学习", "开始学习"]:
                if classId not in bugUrl:
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
            courseUrl = "https://wangda.andedu.net/#/study/course/detail/subject-course/{0}/6/{1}"
            browser.get(courseUrl.format(item["classId"], subjectID))
            print(browser.current_url)
            # 等待播放
            time.sleep(8)

            playS = ''
            while True:
                html = browser.page_source

                # 暂停检查，已暂停则跳出循环
                if html.find("vjs-paused") > 0:
                    print("\n已暂停")
                    # ($x('//div[@class="vjs-control-bar"]/button[1]')[0]).click()
                    playButton = browser.find_element_by_xpath('//div[@class="vjs-control-bar"]/button[1]')
                    if playButton:
                        print(playButton.text)
                    #browser.refresh()
                    #time.sleep(5)
                    break

                # 检查学习进度及完成状态，完成则退出循环进入下一节
                selector = etree.HTML(html)
                playNewS = selector.xpath('//div[contains(@class,"chapter-list")]/ul/li/div/dl/dd/div/span[1]/text()')
                if len(playNewS) > 0:

                    # 检查是否已完成
                    if playNewS[0] == "重新学习":
                        print("\r%s 已完成1" % (item["name"]))
                        break

                    if playS == "":
                        playS = playNewS[0]
                        print("\r%s" % playS)

                    if playS != playNewS[0]:
                        playS = playNewS[0]
                        print("\r%s" % playS)
                    else:
                        print("-", end='')

                    if playS == "重新学习" :
                        print("\r%s 已完成2" % (item["name"]))
                        break

                    time.sleep(5)

