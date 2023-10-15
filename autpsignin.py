"""
Name: 2cycd自动签到 
Author: Ripple
Author URI: https://hiripple.com/
Version: 1.0.0
License: GNU General Public License v3.0
License URI: https://www.gnu.org/licenses/gpl-3.0.html
description:
论坛官网：http://www.2cycd.com
每天签到领贡献～

使用浏览器登录之后, F12-网络选项卡-捉包把home.php/plugin.php请求里面的Cookie的值填到变量cycd_cookie里, 多账号换行或&或@隔开

cron: 0 8 * * *
"""
import requests
from bs4 import BeautifulSoup
import os
import time

def get_formhash(cookie):
  url_hash = "http://www.2cycd.com/plugin.php?id=dc_signin"
  headers_hash = {
    "Accept": "*/*",
    "Accept-Encoding": "gzip, deflate",
    "Accept-Language": "zh-CN,zh-Hans;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Cookie": cookie,
    "Host": "www.2cycd.com",
    "Pragma": "no-cache",
    "Proxy-Connection": "keep-alive",
    "Referer": "http://www.2cycd.com/plugin.php?id=dc_signin",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Safari/605.1.15"
}

  response_hash = requests.get(url_hash, headers=headers_hash)
  soup = BeautifulSoup(response_hash.content, 'html.parser')
  formhash_input = soup.find('input', {'name': 'formhash'})

  if formhash_input:
      return formhash_input['value']
  else:
      print("formhash not found!")
      return None

def sign_in(cookie, formhash_value):
  url_sign = "http://www.2cycd.com/plugin.php?id=dc_signin:sign&inajax=1"
  headers_sign = {
    "Host": "www.2cycd.com",
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/118.0",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
    "Accept-Language": "zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2",
    "Accept-Encoding": "gzip, deflate",
    "Content-Type": "application/x-www-form-urlencoded",
    "Content-Length": "203",
    "Origin": "http://www.2cycd.com",
    "Connection": "keep-alive",
    "Referer": "http://www.2cycd.com/plugin.php?id=dc_signin",
    "Cookie": cookie,
    "Upgrade-Insecure-Requests": "1",
    "Pragma": "no-cache",
    "Cache-Control": "no-cache"
}

  data = {
  "formhash": formhash_value,
  "signsubmit": "yes",
  "handlekey": "signin",
  "emotid": "11",
  "referer": "http://www.2cycd.com/plugin.php?id=dc_signin",
  "content": "%BC%C7%C9%CF%D2%BB%B1%CA%A3%AChold%D7%A1%CE%D2%B5%C4%BF%EC%C0%D6%A3%A1"
}

  response = requests.post(url_sign, headers=headers_sign, data=data)
  return response

def main():
    print("2cycd签到开始：")
    for i in range(3):  # 尝试3次
        if i > 0:
            print('重试第' + str(i) + '次')
        try:
            cookie = os.getenv("cycd_cookie")
            if not cookie :
              print("未检测到cookie，请添加cookie！")
              return None
            formhash_value = get_formhash(cookie)
            print('***************结果统计***************')
            if formhash_value:
                response = sign_in(cookie, formhash_value)
                if "您今日已经签过到" in response.text:
                    print("今日已签到!")
                    print('*************************************')
                    break
                elif "签到成功" in response.text:
                    print("恭喜，签到成功!")
                    print('*************************************')
                    break
                else:
                    print("出现未知错误，可能是cookie不正确或已过期，请重新填写。")
            else:
                print("Failed to sign in due to missing formhash value.可能是填写了错误的cookie。")
            print('*************************************')

        except Exception as e:
            print('line: ' + str(e.__traceback__.tb_lineno) + ' ' + repr(e))
            time.sleep(10)

if __name__ == "__main__":
    main()
