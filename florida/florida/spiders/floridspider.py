# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest

class FloridspiderSpider(scrapy.Spider):
    name = 'floridspider'
    allowed_domains = ['https://www.floridabar.org']
    start_urls = ['https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=&eligible=N&deceased=N&firm=&locValue=&locType=C&pracAreas=F01&lawSchool=&services=&langs=&certValue=&pageNumber=1&pageSize=50']

    def parse(self, response):
        profiles = response.xpath("//li[@class='profile-compact']")
        for profile in profiles:
            name = profile.xpath(".//div[@class='profile-identity']//p[1]/a/text()").get()
            company = profile.xpath(".//div[@class='profile-contact']/p[1]/text()[1]").get()
            add = ""
            a1= profile.xpath(".//div[@class='profile-contact']/p[1]/text()[2]").get()
            a2= profile.xpath(".//div[@class='profile-contact']/p[1]/text()[3]").get()
            a3 = profile.xpath(".//div[@class='profile-contact']/p[1]/text()[4]").get()
            a4 = profile.xpath(".//div[@class='profile-contact']/p[1]/text()[5]").get()
            if company[0].isdigit() or company.upper().startswith("PO BOX"):
                company = "Not available"
            l= []
            ins1 = isinstance(a1, str)
            ins2 = isinstance(a2, str)
            ins3 = isinstance(a3, str)
            ins4 = isinstance(a4, str)
            if ins1 == True:
                l.append(a1)
            if ins2 == True:
                l.append(a2)
            if ins3 == True:
                l.append(a3)
            if ins4 == True:
                l.append(a4)
            address = "".join(l)
            phone = response.xpath("//div[@class='profile-contact']//a[2]/text()").get()
            if phone == None:
                phone = "Not available"
            email = response.xpath("//div[@class='profile-contact']//a[2]/@href").get()
            email_clean = email.replace("mailto:", "")

            yield {
                'Name': name,
                'Company_Name': company,
                'Address': address,
                'Phone#': phone,
                'Email_id': email_clean
                }