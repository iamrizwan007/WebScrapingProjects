# -*- coding: utf-8 -*-
import scrapy
from scrapy_selenium import SeleniumRequest
from scrapy_cloudflare_middleware.middlewares import CloudFlareMiddleware
class FloridspiderSpider(scrapy.Spider):
    name = 'javaspider'
    # allowed_domains = ['https://www.floridabar.org']
    # start_urls = ['https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=&eligible=N&deceased=N&firm=&locValue=&locType=C&pracAreas=F01&lawSchool=&services=&langs=&certValue=&pageNumber=1&pageSize=50']

    def start_requests(self):
        yield SeleniumRequest(
            url= "https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=&eligible=N&deceased=N&firm=&locValue=&locType=C&pracAreas=F01&lawSchool=&services=&langs=&certValue=&pageNumber=1&pageSize=50",
            wait_time= 1,
            callback= self.parse,

        )

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
            phone = profile.xpath(".//div[@class='profile-contact']//a[contains(@href,'tel')]")
            office_num = ""
            if len(phone) == 0:
                office_num = "Not Available"
                phone = "Not Available"
            elif len(phone) == 1:
                office_num = office_num = profile.xpath("//li[@class='profile-compact']//div[@class='profile-contact']//a[contains(@href,'tel')][1]/text()").get()
                phone = "Not Available"
            elif len(phone) > 1:
                office_num = profile.xpath("//li[@class='profile-compact']//div[@class='profile-contact']//a[contains(@href,'tel')][1]/text()").get()
                phone = profile.xpath("//li[@class='profile-compact']//div[@class='profile-contact']//a[contains(@href,'tel')][2]/text()").get()
            email = profile.xpath(".//div[@class='profile-contact']//a[@class='icon-email']/@href").get()
            # driver = response.meta['driver']
            # email = driver.find_element_by_xpath("//a[@class='icon-email']").text
            email_clean = email.replace("mailto:", "")
            yield {
                'Name': name,
                'Company_Name': company,
                'Address': address,
                'Office#': office_num,
                'Cell#': phone,
                'Email_id': email_clean
            }
        for i in range(2,3):
            next_url = f"https://www.floridabar.org/directories/find-mbr/?lName=&sdx=N&fName=&eligible=N&deceased=N&firm=&locValue=&locType=C&pracAreas=F01&lawSchool=&services=&langs=&certValue=&pageNumber={i}&pageSize=50"
            yield SeleniumRequest(
                url= next_url,
                wait_time= 1,
                callback= self.parse
            )
