# -*- coding: utf-8 -*-
"""
Created on Fri Oct 09 17:16:56 2015

@author: XuGang
"""
#import sys
#reload(sys)
#sys.setdefaultencoding('utf-8')

import re
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
import os


global browser


SLEEP_TIME = 1
    
def getGroupNames():
    
    print u"开始.." 
    result = []

    browser.switch_to_window(browser.window_handles[-1])
    groupNames = browser.find_elements_by_css_selector(".my-all-group li")
    
    for i in groupNames:
        result.append(i.text)
    

    return result

def action(string, groupnames, groupnumbers, last = False):
    
    webElement = browser.find_element_by_css_selector(string)
    
    if(last == False):
        print webElement.text
    
    groupnames.append(webElement.text)

    ActionChains(browser).double_click(webElement).perform()
    indiv = browser.find_element_by_xpath("//div[@class='group-members']")
    
    pattern = re.compile(r'([0-9]+)/[0-9]+')
    number = pattern.findall(indiv.text)[0]
    groupnumbers.append(number)
    
    time.sleep(SLEEP_TIME)
  
    change = browser.find_element_by_id("changeGroup")
    ActionChains(browser).double_click(change).perform()

    time.sleep(SLEEP_TIME)
    
    return groupnames, groupnumbers
    
def getNumbers(groupNames):
    
    groupnames = []
    groupnumbers = []
    last = ""
    for i in groupNames:
        
        string = "li[title=" + "'" + i + "'" + "]"

        name = re.sub(' ', '&nbsp;', i) 
        string = "li[title=" + "'" + name + "'" + "]"
        
        last = string
        
        groupnames, groupnumbers = action(string, groupnames, groupnumbers)
        
    groupnames, groupnumbers = action(last, groupnames, groupnumbers, last = True)


    return groupnames, groupnumbers

def getTotalNumbers(groupnumbers):
    total = 0
    for i in groupnumbers:        
        number = int(i)
        total = total + number
    return total

def output(groupnames, groupnumbers, totalgroups, totalnumbers):
    file = open("log.txt","w")    
       
    for i in groupnames:
        file.writelines(i)
  	file.writelines("\n")
    file.writelines("\n") 

    for j in groupnumbers:
        file.writelines(j)
	file.writelines("\n")
    file.writelines("\n") 
        
    sum_group = u"总群数：" + str(totalgroups)
    sum_peple = u"总人数：" + str(totalnumbers)
    
    file.writelines(sum_group)
    file.writelines("\n")
    file.writelines(sum_peple)
    file.writelines("\n")
    
    file.close()  
    
    return sum_group,sum_peple

        
if __name__ == '__main__':
    
    url = "http://qun.qq.com/"
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    
    print u"正在打开网页，请稍后.."

    print u"请给网速打分，good:1-5:bad"
    
    SLEEP_TIME = raw_input('')
    SLEEP_TIME = float(SLEEP_TIME)
    
    browser = webdriver.Chrome(chromedriver)
    
    browser.get(url)
    
    print u"请登录至群管理->成员管理,然后按任意键继续.."
    
    PRICE = raw_input('')
    
    groupNames = getGroupNames()    
    groupnames, groupnumbers = getNumbers(groupNames)
    
    groupnames = groupnames[:-1]
    groupnumbers = groupnumbers[1:]
    
    totalnumbers = getTotalNumbers(groupnumbers)        
    totalgroups= len(groupnames)
    
    output(groupnames, groupnumbers, totalgroups, totalnumbers)
    
    print u"总群数：" + str(totalgroups)
    print u"总人数：" + str(totalnumbers)
    print u"已完成，详见log.txt.."


browser.quit()


