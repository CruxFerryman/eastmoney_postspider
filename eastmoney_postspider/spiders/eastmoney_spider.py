import scrapy
from eastmoney_postspider.items import EastmoneyPostspiderItem
import xlrd
import requests

year_check = 2016
month_now = 10
month_max = 9
month_min = 1


class EastmoneySpider(scrapy.Spider):
    # Get Constituent Codes in a workbook
    xlsname = "000300cons.xls"
    bk = xlrd.open_workbook(xlsname)
    shxrange = range(bk.nsheets)
    try:
        sh = bk.sheet_by_name("20160613")
    except:
        print("No sheet in %s named 20160613") % xlsname
    nrows = sh.nrows
    ncols = sh.ncols
    codes = []
    for i in range(1, nrows):
        code = sh.row_values(i, start_colx=0, end_colx=1)
        codes.append(code)

    # Configure a scrapy spider
    name = "eastmoney_test"
    allowed_domains = ["guba.eastmoney.com"]
    url_prefix = "http://guba.eastmoney.com/list,"
    url_suffix = ",f_1.html"
    start_urls = []
    for code in codes:
        start_url = url_prefix + str(code)[3:-2] + url_suffix
        start_urls.append(start_url)

    # Scrap websites and save useful values to items
    def parse(self, response):
        item = EastmoneyPostspiderItem()
        pagenum = response.url.split('f_')[1][:-5]
        res = response.status
        pagenum = int(pagenum) + 1
        baseurl = 'http://guba.eastmoney.com'
        newurl = response.url.split('f_')[0] + 'f_' + str(pagenum) + '.html'
        for sel in response.xpath('//div[@id="articlelistnew"]'):
            code_tmp = response.xpath('//span[@id="stockif"]/span/@data-popstock').extract()
            title_tmp = sel.xpath('div[starts-with(@class,"articleh")]/span[@class="l3"]/a[1]/text()').extract()
            writer_tmp = sel.xpath('div[starts-with(@class,"articleh")]/span[@class="l4"]/a[1]/text()').extract()
            read_tmp = sel.xpath('div[starts-with(@class,"articleh")]/span[@class="l1"]/text()').extract()
            comment_tmp = sel.xpath('div[starts-with(@class,"articleh")]/span[@class="l2"]/text()').extract()
            date_tmp = sel.xpath('div[starts-with(@class,"articleh")]/span[@class="l6"]/text()').extract()

            href_tmp = sel.xpath('div[starts-with(@class,"articleh")]/span[@class="l3"]/a[1]/@href').extract()
            postpages_url = []
            for href in href_tmp:
                if href[:1] == '/':
                    postpage_url = baseurl + href
                else:
                    postpage_url = baseurl + '/' + href
                postpages_url.append(postpage_url)

            # Get post dates in their detail pages
            years = []
            key1 = '<div class="zwfbtime">'
            key2 = '<div id="zwconttbtns">'
            for url in postpages_url:
                # index = postpages_url.index(url)
                r = requests.get(url)
                cont = r.content
                fa = cont.find(key1)
                fb = cont.find(key2)
                year = cont[fa:fb].split('-')[0][-4:]
                month = cont[fa:fb].split('-')[1]
                years.append(year)

            item['year'] = years
            item['code'] = code_tmp
            item['title'] = title_tmp
            item['writer'] = writer_tmp
            item['read'] = read_tmp
            item['comment'] = comment_tmp
            item['date'] = date_tmp
            item['url'] = postpages_url

            # Check the most recent post date in a page, double check when insert into sql table
            if int(years[1]) == year_check:
                if (int(month) <= month_max) and (int(month) >= month_min):
                    yield item
                yield scrapy.Request(newurl, self.parse, dont_filter=True)

