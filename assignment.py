#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 11 01:43:31 2019

@author: manzars
"""

from selenium import webdriver
from bs4 import BeautifulSoup
import requests
import time

url = "http://team.org.my/members-directory/"

wb = webdriver.Chrome("/home/manzars/Downloads/chromedriver")
wb.get(url)
links = []
for i in range(23):
    html = wb.execute_script('return document.documentElement.outerHTML')
    soup = BeautifulSoup(html, 'lxml')
    links_page = soup.findAll('a', {'class': 'sabai-entity-bundle-type-directory-listing'})
    for link in links_page:
        links.append(link.attrs['href'])
    div = soup.findAll('div', {'class': 'sabai-pagination'})
    a = div[0].findAll('a')
    
    wb.find_element_by_xpath('//*[@id="sabai-embed-wordpress-shortcode-2"]/div[2]/div[3]/div[2]/div/a[' + str(len(a)) + ']').click()
    time.sleep(4)
html = wb.execute_script('return document.documentElement.outerHTML')
soup = BeautifulSoup(html, 'lxml')
links_page = soup.findAll('a', {'class': 'sabai-entity-bundle-type-directory-listing'})
for link in links_page:
    links.append(link.attrs['href'])

wb.close()    

header = "Company Name, Telephone, Fax, Email, Contact Person\n"
file = open('assignment.csv', 'w')
file.write(header)

for link in links:
    req = requests.get(link)
    soup = BeautifulSoup(req.text, 'lxml')
    
    name = soup.findAll('head')
    name = name[0].title.text.split(' – TEAM')[0]
    
    try:
        tel = soup.findAll('div', {'class': 'sabai-directory-contact-tel'})[0].a.text
    except:
        tel = 'NaN'
        
    try:
        fax = soup.findAll('div', {'class': 'sabai-directory-contact-fax'})[0].span.text
    except:
        fax = 'NaN'
        
    try:
        email = soup.findAll('div', {'class': 'sabai-directory-contact-email'})[0].a.attrs['href'].split('mailto:')[1]
    except:
        email = 'NaN'
    
    try:
        contact = soup.findAll('div', {'class': 'sabai-field-name-field-contact-person'})[0].findAll('div', {'class': 'sabai-field-value'})[0].text
    except:
        contact = 'NaN'
    
    print(name)
    file.write(name.replace(',', '') + ', ' + tel.replace(',', '|') + ', ' + fax.replace(',', '|') + ', ' + email + ', ' + contact.replace(',', '|') + '\n')
file.close() 
    
    
#//*[@id="sabai-embed-wordpress-shortcode-2"]/div[2]/div[3]/div[2]/div/a[8]
#//*[@id="sabai-embed-wordpress-shortcode-2"]/div[2]/div[3]/div[2]/div/a[9]