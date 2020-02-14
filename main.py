# -*- coding: utf-8 -*-#

#-------------------------------------------------------------------------------
# Name:         main
# Description:  FuckWangda
# Author:       qpand
# Date:         2019/12/10
#-------------------------------------------------------------------------------

from selenium import webdriver
import time
from selenium.webdriver.common.keys import Keys
from lxml import etree

options = webdriver.ChromeOptions()

executable_path = r"E:\PycharmProjects\FuckWangda\webdriver\chromedriver.exe"

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

username = "38006067"
password = "!Q2w3e4r"
#username = "13608170940"
#password = "Linda@135"

# 登录
browser.find_element_by_id('D31username').send_keys(username)
browser.find_element_by_id('D31password').send_keys(password)
browser.find_element_by_id('D31login').click()

time.sleep(5)

html = browser.page_source
if html.find("退出账号"):
    realName = browser.find_element_by_xpath('//div[@class="user-info-top"]/div[2]/div[1]/div[1]').get_attribute("innerText")
    print("%s 登陆成功" % realName)

    # 专题ID
    subjectIDList = ["c4cbf55f-0490-412e-a13a-2fa456e38e11"]

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
        # //div[contains(@class,"catalog-state-info")]/div/div[2]/div[1]/text()
        # //div[contains(@class,"catalog-state-info")]/div/div[3]/a/div/text()
        # //div[contains(@class,"catalog-state-info")]/div/div[3]/a/@data-resource-id
        # 20200214 //a[contains(@class,\"btn small\")]/@data-resource-id
        # 课程标题
        classList = selector.xpath("//div[contains(@class,\"text-overflow title\")]/@title")
        # 课程状态
        classStatus = selector.xpath("//a[contains(@class,\"btn small\")]/text()")
        # 课程ID
        classIdList = selector.xpath("//a[contains(@class,\"btn small\")]/@data-resource-id")

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
            #print(browser.current_url)
            # 等待播放
            time.sleep(8)

            playS = ''
            while True:
                html = browser.page_source
                selector = etree.HTML(html)
                course_name = selector.xpath("//dt/div[contains(@class,\"text-overflow\")]/@title")
                course_status = selector.xpath("//div[contains(@class,\"item continue pointer\")]/span/text()")

                course_finish = True
                for name, status in zip(course_name, course_status):
                    # print("%s -- %s" % (name, status))
                    # 判断课程状态如果不为 重新学习，则修改课程状态为未完成，继续学习
                    if status != "重新学习":
                        current_time = selector.xpath("//div[contains(@class,\"vjs-current-time-display\")]/text()")
                        duration = selector.xpath("//div[contains(@class,\"vjs-duration-display\")]/text()")
                        print("%s -- %s  %s/%s" % (name, status, current_time, duration))
                        course_finish = False
                        time.sleep(10)
                        break

                # 课程已完成，则退出
                if course_finish:
                    print("\r已完成")
                    break

'''
                # 暂停检查，已暂停则跳出循环
                if html.find("vjs-paused") > 0:
                    print("\r已暂停")
                    # 暂停处理
                    time.sleep(2)
                    playButton = browser.find_element_by_xpath('//div[@class="vjs-control-bar"]/button[1]')
                    if playButton.text == "播放":
                        try:
                            playButton.send_keys(Keys.ENTER)
                            time.sleep(2)
                            print("\r%s 继续播放" % browser.title)
                        except Exception as re:
                            print("处理错误:%s" % str(re))
                            break

                # 检查学习进度及完成状态，完成则退出循环进入下一节
                selector = etree.HTML(html)
                playNewS = selector.xpath('//div[contains(@class,"chapter-list")]/ul/li/div/dl/dd/div/span[1]/text()')
                if len(playNewS) > 0:

                    # 检查是否已完成
                    if playNewS[0] == "重新学习":
                        print("\r%s 已完成" % browser.title)
                        break

                    if playS == "":
                        playS = playNewS[0]
                        print("\r%s" % playS)

                    if playS != playNewS[0]:
                        playS = playNewS[0]
                        print("\r%s" % playS)
                    else:
                        print("-", end='')

                    time.sleep(5)
'''
# 关闭浏览器
browser.close()

