# -*- coding:utf-8 -*-  
import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from jinja2 import Template
import datetime



def send(today, old):
	# me == my email address
	# you == recipient's email address
	me = ""
	you = [""]
	# Create message container - the correct MIME type is multipart/alternative.
	msg = MIMEMultipart('alternative')
	msg['Subject'] = u"一亩三分地今日内推-" + str(datetime.date.today())
	msg['From'] = me
	msg['To'] = ", ".join(you)
	
	print "hello"
        print today , old

	# Create the body of the message (a plain-text and an HTML version).
	html = """\
	<ul class="list-group">
          <h2> Today's referal: </h2>
	  {% for n in today %} 
	  <li class="list-group-item"><a href={{n.url}}><font size="2" color="green">{{n.title}}</font></a></li>
	  {% endfor %}
          <h4> Previous: </h4>
	  {% for pack in old %}
	      <h4> {{ pack.date }} </h4>
	      {% for item in pack.jobData %}
	          <li class="list-group-item"><a href={{item.url}}><font size="2" color="blue">{{item.title}}</font></a></li>
              {% endfor %}
	  {% endfor %}
	</ul>
	"""

	t = Template(html)
	html = t.render(date = str(datetime.date.today()), today = today, old = old)

	part2 = MIMEText(html.encode('utf-8'), 'html',_charset='utf-8')

	msg.attach(part2)
	# Send the message via local SMTP server.
	mail = smtplib.SMTP('smtp.gmail.com', 587)

	mail.ehlo()

	mail.starttls()

	mail.login(,)
	mail.sendmail(me, you, msg.as_string())
	mail.quit()
