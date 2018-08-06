# -*- coding: utf-8 -*-
import urllib3
import time
from bs4 import BeautifulSoup
import smtplib

c = 0
memos = []
while True:
    url = 'http://phillippowers.com/redirects/get.php?file=https://memo.cash/posts/new'
    http = urllib3.PoolManager()
    response = http.request('GET', url)
    soup = BeautifulSoup(response.data,'html.parser')
    c += 1
    mention_dict = {'@tracyspacy':'tracyspacygo@gmail.com','@memo':'gubkin.valentin@gmail.com'}
    for big_post in soup.find_all('div', 'post rounded box-shadow'):
        for post in big_post.find_all('div','message'):
            for user_link in big_post.find_all('a', 'profile profile-link'):
                if post.text.encode('utf-8') not in memos:
                    for name in mention_dict:
                        if name in post.text:
                            memos.append(post.text.encode('utf-8'))
                            posttext = post.text.encode('utf-8')
                            userlink = str(user_link.get('href')).encode('utf-8')
                            user_sent = ('https://memo.cash/' + str(userlink)).encode('utf-8')
                            basic_text =('\nYou was mentioned by ').encode('utf-8')
                            signaturetext = ('\n \n Made by tracyspacy \n  topic -> https://memo.cash/topic/%40mention+Email+Notifier+').encode('utf-8')
                            try:
                                server = smtplib.SMTP('mail.inbox.lv​', 587)
                                server.starttls()
                                server.login("memo-mention@inbox.lv", "nSyJT9GL")
                                message = (str(basic_text) + str(user_sent) + str(posttext) + str(signaturetext))
                                sendto = str(mention_dict[name])
                                server.sendmail("memo-mention@inbox.lv", sendto, message)
                            except smtplib.SMTPException:
                                print ("Error: unable to send email")
                        else:
                            continue
                else:
                    continue
    print ('round', c)
    time.sleep(200)