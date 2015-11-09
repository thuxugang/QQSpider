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
from pyquery import PyQuery as pq
import httplib, urllib,urllib2
import json
global browser


SLEEP_TIME = 1
    
def getGroupNames():
    
    print u"开始.." 
    groupNames = []
    groupId = []
    browser.switch_to_window(browser.window_handles[-1])
    group = browser.find_elements_by_css_selector(".my-all-group li")
    
    
    
    for i in group:
        
        groupNames.append(i.text)
        groupId.append(i.get_attribute("data-id"))
    

    return groupNames, groupId

    
def getInfomation(searchName, searchId):
    

    browser.switch_to_window(browser.window_handles[-1])
    
    results = []

    j = 0
    while(j < len(searchName)):
        
        name = searchName[j]
        id = searchId[j]
        
        
        
        cookie = browser.get_cookies()
    
        skey = ""
        for i in cookie:
            
            name = i.get('name')
            if(name == "skey"):
                skey = i.get('value')
                break

        js = "var string = document.cookie;return string;"        
        string = browser.execute_script(js)
    
    #gtk 算法

        js2 = "var hash = 5381;  for(var i = 0, len ='" + skey + "'.length; i < len; ++i){ hash += (hash << 5) + '" + skey + "'.charAt(i).charCodeAt();  }  return hash"  

        gtk = browser.execute_script(js2)
        bkn = gtk & 0x7fffffff
        
        
        url = "http://qun.qq.com/cgi-bin/qun_mgr/search_group_members"
        
        params = {
            "gc":int(id),
            "st":0,
            "end":500,
            "sort":0,
            "bkn":bkn,
        }
        headers = {
            'Content-Type':"application/x-www-form-urlencoded; charset=UTF-8", 
            "Accept": "text/plain",
            'Referer':"http://qun.qq.com/member.html",
            'Host':"qun.qq.com",
            "Cookie":string,
            
            }    

        postData = urllib.urlencode(params)

        req=urllib2.Request(url, postData, headers)
      
        resp = urllib2.urlopen(req).read()
        result = json.loads(resp)

    
        
        results.append(result)
        j = j + 1 
        
    return results

def output(infomations, searchName, searchId):
    file = open("log.txt","w")    

    j = 0
    while(j < len(infomations)):    
        file.writelines(searchName[j] + ',' + searchId[j]) 
        file.writelines("\n") 
    
        for indiv in infomations[j]['mems']:
            
            string = ""
            
            g_temp = indiv['g']
            if((int)(g_temp) == 1):
                g = "女"
            elif((int)(g_temp) == 0):
                g = "男"
            else:
                g = "未填写"
            join_time_temp = indiv['join_time']
            join_time_temp2 = time.localtime(join_time_temp)
            join_time = time.strftime('%Y-%m-%d',join_time_temp2)
    
            last_speak_time_temp = indiv['last_speak_time']
            last_speak_time_temp2 = time.localtime(last_speak_time_temp)
            last_speak_time = time.strftime('%Y-%m-%d',last_speak_time_temp2)
#特殊字符处理            
            name = ""
            try:
                name = str(indiv['nick'])
            except:
                arr = list(indiv['nick'])
                temp = ""
                for i in arr:
                    try:
                        temp = temp + str(i)
                    except:
                        temp = temp + '*'
                name = temp

            card = ""
            try:
                card = str(indiv['card'])
            except:
                arr = list(indiv['card'])
                temp = ""
                for i in arr:
                    try:
                        temp = temp + str(i)
                    except:
                        temp = temp + '*'
                card = temp
                
            try:
                string = string + str(indiv['uin']) + ',' + name + ',' + card + ',' + g.decode('utf-8') + ',' + join_time + ',' + last_speak_time
                string = re.sub('&nbsp;', ' ', string)                 
                file.writelines(string)
                file.writelines("\n") 
            except:
                print indiv['uin']
                file.writelines("\n") 
                continue
            sum_peple = u"总人数：" + str(infomations[j]['count'])
        file.writelines(sum_peple)
        file.writelines("\n")
        file.writelines("\n")
        j = j + 1 

    file.writelines("\n") 


    
    

    
    
    
    file.close()  
    


        
if __name__ == '__main__':
    
    url = "http://qun.qq.com/"
#    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    chromedriver = "C:\Program Files\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    
    print u"正在打开网页，请稍后.."


    
    browser = webdriver.Chrome(chromedriver)
    
    browser.get(url)
    
    print u"请登录至群管理->成员管理,在'input.txt'中输入所要统计的群,每个群单独一行，然后按回车开始.."
    useless = raw_input('')
    
    searchName = []
    f = open('.\input.txt','r')  
    for line in open('.\input.txt'):  
        line = f.readline().strip('\n')

        searchName.append(line)
    
    

    groupNames, groupId = getGroupNames()
    
    searchId = []
    for name in searchName:
        indiv_id = groupNames.index(name)
        indiv = groupId[indiv_id]
        searchId.append(indiv)
    
    infomations = getInfomation(searchName, searchId)

    
    output(infomations, searchName, searchId)

    print u"已完成，详见log.txt..\n"

browser.quit()


