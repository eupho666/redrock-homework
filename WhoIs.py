#!/usr/bin/env python3
import requests,re

class mywhois():
	reg_freshkey = r'(?<=refresh = ")[a-z0-9]+(?=")'
	reg_regis_info = r'<div class="col-md-12 queryResponseBodyValue"><div class="rawWhois">'
	HOST = "https://who.is/whois/"
	fresh_key = ''
	def mywhois(self,domain):
		r = requests.get(mywhois.HOST + domain,timeout=5)
		html = r.text
		key = re.search(mywhois.reg_freshkey,html)
		text = ''

		if key:
			mywhois.fresh_key = key.group(0)
			host = mywhois.HOST + domain + '?forceRefresh=' + mywhois.fresh_key + '+'
			r_fresh = requests.get(host,timeout=5)
			html = r.text

		return self.check(html)

	def check(self,text):
		flag = 1
		if mywhois.reg_regis_info in text:
			flag = 0
		return flag
