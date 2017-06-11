#!/usr/bin/env python
# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# -*- coding: UTF-8 -*-
import scrapy
from ..items import ReferralItem
from ..dbhelper import DBhelper
import datetime
from datetime import datetime
from w3lib.html import remove_tags, remove_tags_with_content


class QuotesSpider(scrapy.Spider):
    name = "referral"    

    def start_requests(self):
        urls = [
            'http://www.1point3acres.com/bbs/forum.php?mod=forumdisplay&fid=198&filter=author&orderby=dateline&sortid=192',
            'http://www.meetqun.net/forum.php?mod=forumdisplay&fid=37&filter=author&orderby=dateline&typeid=13'
        ]
        
        heads = ['http://www.1point3acres.com/bbs/', 'http://www.meetqun.net/' ]
        
        forums = ['1point3acres', 'meetqun']
       
        for i in range(len(urls)):
            request =  scrapy.Request(url=urls[i], callback=self.parse)
            request.meta['head'] = heads[i]
            request.meta['forum'] = forums[i]
            yield request

        yield scrapy.FormRequest(url="https://www.mitbbs.com/mitbbs_bbsbfind.php?board=JobHunting",
                    formdata={'board': 'JobHunting', 'dt': '10','og' : 'on', 'opflag' : '0', 'submit' :'%B5%DD%BD%BB%B2%E9%D1%AF%BD%E1%B9%FB'},
                    callback=self.parseMitBBS)

    def parse(self, response):
        allthread = response.css('tbody[id*=normalthread_]')
        titles = allthread.css('a.s.xst::text').extract()
        urls = allthread.css('a.s.xst::attr(href)').extract()
        dates = None
        isMeetQun = False
        if response.meta['forum'].startswith('meetqun'):
	    isMeetQun = True
        dates = allthread.css('td.by').css('em').css('span::text').extract()
        for i in range(len(titles)):
            title = titles[i]
            if not u'求' in title:
                item = ReferralItem()
                item['title'] = title
                item['url'] = urls[i]
                if urls[i].startswith('forum'):
                    item['url'] = response.meta['head'] + urls[i]
                item['hashCode'] = hash(title + item['url'])
                if isMeetQun == True:
                    item['date'] = str(datetime.strptime(dates[i],'%m-%d-%Y %I:%M %p').date())
                print ""
                yield(item)

    def parseMitBBS(self, response):
        rows = response.css('body').css('tr[bgcolor*="#FFFFF"]')[1:]
        dates = rows.css('td.black4::text').extract()
        topics = rows.css('a[href*="/article"]')
        titles = topics.css('a[href*="/article"]').extract()
        urls = topics.css('a[href*="/article"]::attr(href)').extract()
        for i in range(len(titles)):
            title = titles[i]
            if u'内推' in title:
                if u'求' in title or u'?' in title or u'？' in title or u'问' in title:
                    continue
                item = {}
                item['title'] = remove_tags(remove_tags_with_content(titles[i], ('script', )))
                item['url'] = urls[i]
                if urls[i].startswith('/'):
                    item['url'] = 'http://www.mitbbs.com' + urls[i]
                item['hashCode'] = hash(title + item['url'])
                dates[i] = dates[i].replace(u'\xa0', ' ')
                now = datetime.now()
                date = datetime.strptime(dates[i],'%b %d').date().replace(year=now.year)
                item['date'] = str(date)
                yield item
