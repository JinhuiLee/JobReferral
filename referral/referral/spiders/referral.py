#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import scrapy
from ..items import ReferralItem
from ..dbhelper import DBhelper
import datetime
class QuotesSpider(scrapy.Spider):
    name = "referral"    

    def start_requests(self):
        urls = [
            'http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=198&filter=author&orderby=dateline&sortid=192',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        allthread = response.css('tbody[id*=normalthread_]')
        titles = allthread.css('a.s.xst::text').extract()
        urls = allthread.css('a.s.xst::attr(href)').extract()
        for i in range(len(titles)):
            title = titles[i]
            if not u'求' in title:
                item = ReferralItem()
                item['title'] = title
                item['url'] = urls[i]
                item['hashCode'] = hash(title + urls[i])
                print ""
                yield(item)
