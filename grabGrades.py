import requests
from bs4 import BeautifulSoup as bs
import replit
replit.clear()

class grabGrades:
  def __init__(self, name, pswrd):
    uname = name
    psw = pswrd
    self.deGrades = []
    self.deName = ""
    s = requests.Session()
    site = s.get("https://aspen.cps.edu/aspen/logon.do")  

    bs_content = bs(site.content, "html.parser")
    token = bs_content.find("input", {"name":"org.apache.struts.taglib.html.TOKEN"})["value"]
    #login_data = {"username":"uname","psw": redacted, "org.apache.struts.taglib.html.TOKEN":token}
    #s.post("https://aspen.cps.edu/aspen/logon.do",login_data)
    #grades = s.get("https://aspen.cps.edu/aspen/home.do")

    headers = {
      'Connection': 'keep-alive',
      'Pragma': 'no-cache',
      'Cache-Control': 'no-cache',
      'Upgrade-Insecure-Requests': '1',
      'Origin': 'https://aspen.cps.edu',
      'Content-Type': 'application/x-www-form-urlencoded',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.0.0 Safari/537.36',
      'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'Sec-Fetch-Site': 'same-origin',
      'Sec-Fetch-Mode': 'navigate',
      'Sec-Fetch-User': '?1',
      'Sec-Fetch-Dest': 'document',
      'Referer': 'https://aspen.cps.edu/aspen/logon.do',
      'Accept-Language': 'en-US,en;q=0.9',
    }

    data = {
      'org.apache.struts.taglib.html.TOKEN': token,
      'userEvent': '930',
      'userParam': '',
      'operationId': '',
      'deploymentId': 'aspen',
      'scrollX': '0',
      'scrollY': '0',
      'formFocusField': 'username',
      'mobile': 'false',
      'SSOLoginDone': '',
      'username': uname,
      'password': psw
    }


    s.get("https://aspen.cps.edu/aspen/home.do")
    cookies = s.cookies
    sessionid = s.cookies['JSESSIONID']
    postURL = ("https://aspen.cps.edu/aspen/logon.do;%s" %sessionid)

    response = s.post(postURL, headers=headers, cookies=cookies, data=data)

    grades = s.get("https://aspen.cps.edu/aspen/portalClassList.do?navkey=academics.classes.list")

    getGrades =  bs(grades.content, "html.parser")

    for div in getGrades.find_all("div", {"id":"dataGrid"}):
      for table in div.find_all("table"):
        for tr in table.find_all("tr", {"class":"listCell"}):
          for td in tr.select("td[nowrap]"):
            count = 0
            Teacher = ""
            Grade = ""
            Class = ""

            for i in td.text:
              if(i.isspace()):
                count += 1

            if("." in td.text):
              Grade = td.text.strip()
              self.deGrades.append(Grade)
              print("Grade: " + Grade)

            if("," in td.text):
              Teacher = td.text.strip()
              self.deGrades.append(Teacher)
              print("Teacher: " + Teacher)

            if(count < 8 and td.text.strip() != "0" and td.text.strip() != "1" and td.text.strip() != ""):
              Class = td.text.strip()
              self.deGrades.append(Class)
              print("Class: " + Class)

    if(self.deGrades != []):
      Home = s.get("https://aspen.cps.edu/aspen/home.do")
      deHome = bs(Home.content, "html.parser")
      Name = deHome.find("div", {"id":"userPreferenceMenu"})
      x = Name.text.split()
      self.deName = x[1]