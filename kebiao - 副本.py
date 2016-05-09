from urllib import parse,request
from http import cookiejar
from bs4 import BeautifulSoup
import requests
import re,os
import datetime
from ics import Calendar,Event
xh = "YouId"
mm = "PassWord"
#相关信息
st = "学生"
st = st.encode('gb2312')
date0 ={
    "__VIEWSTATE":"dDwtMTMxNjk0NzYxNTs7PtSNmeyDsvQQJ46rKmnP1/9Eh4rQ",
    "txtUserName":xh,
    "TextBox2":mm,
    "txtSecretCode" :"",
    "RadioButtonList1":st,
    "Button1":"",
    "lbLanguage":""
}
#登陆
#导入cookie信息
baseurl = "http://210.44.159.22"
filename = "cookie.txt"
try:
    cookie = cookiejar.MozillaCookieJar()
    cookie.load(filename,ignore_discard = True,ignore_expires = True)
    handler = request.HTTPCookieProcessor(cookie)
    opener = request.build_opener(handler)
    req = requests.get(baseurl+"/xs_main.aspx?xh="+xh,cookies = cookie)
    if req.history:
    	for each in req.history:
    		print(each,each.headers["Location"])
    	raise loginerror
    else:
    	print("登陆成功")
except Exception as e:
    print(e)
    cookie = cookiejar.MozillaCookieJar(filename)
    handler = request.HTTPCookieProcessor(cookie)
    opener  = request.build_opener(handler)
    checkcodeimg = opener.open(baseurl + "/CheckCode.aspx")
    with open("checkcodeimg.jpg","wb") as f:
        f.write(checkcodeimg.read())
    string = input("请输入验证码")
    date0["txtSecretCode"] = string
    date = parse.urlencode(date0).encode()
    r= request.Request(url=baseurl +"/default2.aspx",data=date)
    rec = opener.open(r)
    rec = rec.read().decode("GB2312")
    cookie.save(ignore_discard=True, ignore_expires=True)
def changeWeekday(day):
    if("一" in day):
        return 1
    elif("二" in day):
        return 2
    elif("三" in day):
        return 3
    elif("四" in day):
        return 4 
    elif("五" in day):
        return 5
    elif("六" in day):
        return 6
    elif("天" in day):
        return 7
    else:
        return 5
def changeTimeStart(time):
    if("1,2" in time):
        return "08:30:00"
    elif("3,4" in time):
        return "10:20:00"
    elif("5,6" in time):
        return "13:30:00"
    elif("7,8" in time):
        return "15:10:00"
    elif("9,10" in time):
        return "17:50:00"
    else:
        return "10:20:00"
def changeTimeEnd(time):
    if("1,2" in time):
        return "10:10:00"
    elif("3,4" in time):
        return "12:05:00"
    elif("5,6" in time):
        return "15:00:00"
    elif("7,8" in time):
        return "17:00:00"
    elif("9,10" in time):
        return "18:50:00"
    else:
        return "12:05:00"
def getcode(url,cookies):
	req = request.Request(url)
	req.add_header("Referer",url)
	text = opener.open(req).read().decode("gb2312")
	soup = BeautifulSoup(text,"html.parser")
	viewstate = soup.find(type = "hidden")['value']
	return viewstate
def myAlign(string, length=0):  
    if length == 0:  
        return string  
    slen = len(string)  
    re = string  
    if isinstance(string,str):  
        placeholder = '  '
    else:  
        placeholder = '　'  
    while slen < length:  
        re += placeholder  
        slen += 1  
    for each in string:
    	if ord(each) > 0x0020 and ord(each) < 0x7e:
    		re += " "

    return re  

opener.addheaders = [("User-Agent","Mozilla/5.0 (Windows NT 6.1; WOW64; rv:43.0) Gecko/20100101 Firefox/43.0")]
#信息查询
url = "http://210.44.159.22/xskbcx.aspx?xh=201503041048&xm=%C2%A6%CA%F7%B1%F3&gnmkdm=N121603"
req = request.Request(url = url)
req.add_header("Referer",url)

rec = opener.open(req).read().decode("gb2312")
soup = BeautifulSoup(rec,"html.parser")
num = 0
subject = soup.find_all(rowspan = "2")
n = re.compile(r'<.*?>')
while True:
    try:
        for each in range(len(subject)):
            subject[each] = str(subject[each])[:n.search(str(subject[each])).start()]+"/"+str(subject[each])[n.search(str(subject[each])).end():]
    except Exception as e:
        break;
for each in subject:
    subject[num] = each.split("/")
    num = num + 1
d = datetime.datetime.today()
today = datetime.date.today()
begindate = []
c = Calendar()
num = 0
for r in range(10):
    num = 0
    for i in range(1):
        for each in subject:
            e = Event()
            if(r == 0):
                juli = abs(int(changeWeekday(each[2]))-1)
                begindate.append(today + datetime.timedelta(days = juli))
            e.name = each[1]
            e.begin = str(begindate[num]).replace("-","") +" "+changeTimeStart(each[2])
            e.end = str(begindate[num]) +changeTimeEnd(each[2])
            begindate[num] = begindate[num]+datetime.timedelta(days = 7)
            num = num + 1
            e.location = each[4]
            c.events.append(e)
            

