#!/usr/bin/env python
# coding: utf-8

#imports
import requests
import smtplib
from bs4 import BeautifulSoup
import re

#url
producturl = ' '
r = requests.get(producturl)
r.raise_for_status()

#email
toAddress = [' ', ' ']
fromAddress = ' '
appPassword = ' '

#product info
productinfo = BeautifulSoup(r.text, 'html.parser')
productname = productinfo.find('div', attrs={"itemprop":"name"}).text.strip()
productcolour = productinfo.find('p', class_='purchase-attributes__color-details__name').text.strip()
productsize = productinfo.find('span', class_='purchase-attribute-carousel-counter__label').text.strip()[6:]
addtobagbutton = productinfo.find('button', attrs={"data-lulu-track":"pdp-add-to-bag-regular-disabled", "class":"button-1xp0M lll-text-button add-to-bag buttonPrimary-2q4bX", "type":"button"})
notavailableheader = productinfo.find('h1', class_='oos__heading headline')

#case: not available online
if notavailableheader:
    print('The item is not available online at this time :(')

#case: sold out
elif addtobagbutton:
    print('The item is still out of stock :(')

#else: it's in stock!
else:
    conn = smtplib.SMTP('smtp.gmail.com', 587) # smtp address & port
    conn.ehlo() # start the connection
    conn.starttls() # start tls encryption - when password is sent, it will be encrypted
    conn.login(fromAddress, appPassword)
    conn.sendmail(fromAddress, toAddress,
                  'Subject: Lulu Alert!\n\nLululemon\'s ' + productname + ' are back in stock in ' \
                  + productcolour + ', size ' + productsize \
                  + '! Hurry and get them while you can! \n Happy shopping :) \nIn Stock Notifier V1.0')
    conn.quit()
    print('Sent notificaton e-mails for the following recipients:\n')
    for i in range(len(toAddress)):
        print(toAddress[i])
