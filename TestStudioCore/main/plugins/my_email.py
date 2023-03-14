import smtplib
from email.mime.text import MIMEText
# 发送多种类型的邮件
from email.mime.multipart import MIMEMultipart
import datetime
from selenium import webdriver
import time
import base64
from selenium.webdriver.chrome.options import Options


def get_allure_report_screenshot():
    chrome_options = Options()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-dev-shm-usage')

    # driver = webdriver.Chrome()
    # driver = webdriver.Chrome('/home/<user>/chromedriver', chrome_options=chrome_options)
    driver = webdriver.Chrome(chrome_options=chrome_options)
    driver.get('http://192.168.0.106:8066/index.html')
    time.sleep(2)
    # 通过base64进行保存图片
    x = driver.get_screenshot_as_base64()
    image = base64.b64decode(x)
    file = open('allure_latest_report.jpg', "wb")
    file.write(image)


def send_email():
    msg_from = '1696746432@qq.com'  # 发送方邮箱
    passwd = 'hdpdxzcyuitbeeah'  # 就是上面的授权码

    to = ['1696746432@qq.com']  # 接受方邮箱

    # 设置邮件内容
    # MIMEMultipart类可以放任何内容
    msg = MIMEMultipart()
    # conntent="这个是字符串"
    # #把内容加进去
    # msg.attach(MIMEText(conntent,'plain','utf-8'))

    # 添加附件
    # att1 = MIMEText(open('result.xlsx', 'rb').read(), 'base64', 'utf-8')  # 打开附件
    # att1['Content-Type'] = 'application/octet-stream'  # 设置类型是流媒体格式
    # att1['Content-Disposition'] = 'attachment;filename=result.xlsx'  # 设置描述信息
    #
    att2 = MIMEText(open('allure_latest_report.jpg', 'rb').read(), 'base64', 'utf-8')
    att2['Content-Type'] = 'application/octet-stream'  # 设置类型是流媒体格式
    att2['Content-Disposition'] = 'attachment;filename=allure_latest_report.jpg'  # 设置描述信息
    #
    # msg.attach(att1)  # 加入到邮件中
    msg.attach(att2)

    now_time = datetime.datetime.now()
    year = now_time.year
    month = now_time.month
    day = now_time.day
    mytime = str(year) + " 年 " + str(month) + " 月 " + str(day) + " 日 "
    fayanren = "测试专家A"
    zhuchiren = "CTO"
    # 构造HTML
    content = '''
                    <html>
                    <body>
                        <h1 align="center">每日测试任务报告</h1>
                        <p><strong>您好：</strong></p>
                        <blockquote><p><strong>以下内容是本次会议的纪要,请查收！</strong></p></blockquote>

                        <blockquote><p><strong>发言人：{fayanren}</strong></p></blockquote>
                        <blockquote><p><strong>主持人：{zhuchiren}</strong></p></blockquote>
                        <a class="tag-link" href="http://192.168.0.106:8066/index.html" target="_blank" rel="noopener">点击查看allure测试报告</a>
                        <p align="right">{mytime}</p>
                    <body>
                    <html>
                    '''.format(fayanren=fayanren, zhuchiren=zhuchiren, mytime=mytime)

    msg.attach(MIMEText(content, 'html', 'utf-8'))

    # 设置邮件主题
    msg['Subject'] = "每日测试任务报告"

    # 发送方信息
    msg['From'] = msg_from

    # 开始发送

    # 通过SSL方式发送，服务器地址和端口
    s = smtplib.SMTP_SSL("smtp.qq.com", 465)
    # 登录邮箱
    s.login(msg_from, passwd)
    # 开始发送
    s.sendmail(msg_from, to, msg.as_string())
    print("邮件发送成功")

def get_allure_screenshot_and_send_mail():
    get_allure_report_screenshot()
    send_email()

if __name__ == '__main__':
    get_allure_report_screenshot()
    send_email()

# 参考地址 https://blog.csdn.net/MATLAB_matlab/article/details/106240424