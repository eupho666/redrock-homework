#!/usr/bin/env python3
import socket,requests
import re
import requests.exceptions as exceptions
class mywhois():
	re_express_1 = re.compile('<pre style="border:0px;">[\w.\s\W]*(e-mail:)+[\w.\s\W]*(address:)+[\w.\s\W]*</pre>')
	not_exist = {"ru":"No entries found","nl":"is free",\
	"name":"No match for ","pl":"No information available about domain name",\
	"ca":"Domain status:         available","me":"NOT FOUND",\
	"uk":"No match for","fr":"No entries found","fi":"Domain not ",\
	"jp":"No match!!","au":"No Data Found","eu":"Status: AVAILABLE",\
	"ee":"Domain not found","br":"Not found:","kr":" no match",\
	"pt":"No entries found","bg":"does not exist in database!",\
	"de":"Status: free","at":"Status: free","be":"Status: AVAILABLE",\
	"info":"NOT FOUND","io":"is available for purchase",\
	"kg":"Data not found. This domain is available for registration",\
	"ch":"We do not have an entry in our database matching your query.",\
	"li":"We do not have an entry in our database matching your query.",\
	"id":"NOT FOUND","sk":"Not found","se":"not found.","is":"No entries found"}	
	def check(self,text,tld,is_second=False):
		text_ = text
		flag = 2
		if is_second:
			if "address:" in text_ or "registrar:" in text_ or "phone:" in text_ or "country:" in text_:
				flag = 0
				return flag
			else:
				flag = 1
				return flag
		elif tld in mywhois.not_exist:
			m = re.search(mywhois.not_exist[tld], text_, re.IGNORECASE)
			if m:
				flag = 1
				return flag
			if 'address:' in text_.lower():
				flag = 0
				return flag
		else:
			if "address:" or "e-mail:" in text_.lower():
				flag = 0
				return flag
			else:
				for i in mywhois.not_exist:
					m = re.search(mywhois.not_exist[i], text_,re.IGNORECASE)
					if m:
						flag = 1
						return flag
		return flag


	#WHOIS SERVER
	HOST_1 = "whois.nic."
	HOST_2 = "https://who.is/whois/"

	def mywhois(self,domain):
		aaa = domain
		tld = aaa.split(".")[-1]
		whois_host = mywhois.HOST_1 + tld
		response = b''
		try:
			s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
			s.settimeout(3)
			s.connect((whois_host,43))
			try:
				domain_1 = domain.encode('idna')
			except AttributeError:
				pass
			s.send(domain_1 + b'\r\n')

			while True:
				d = s.recv(4096)
				response += d
				if not d:
					break

			s.close()
		except socket.error as socketerror:
			print('Socket Error:',socketerror)
		response = response.decode('utf-8',errors='replace')
		flag = self.check(response,tld,False)
		if flag != 2:
			return flag
		else:
			whois_host = mywhois.HOST_2 + aaa
			try:
				r = requests.get(whois_host,timeout=4)
				flag = self.check(r.text,tld,True)
			except exceptions.ConnectionError:
				raise("can't connect! ")
			except exceptions.ConnectTimeout:
				raise("timeout! " )
			except exceptions.ReadTimeout:
				raise("readtimeout! " )
		return flag

		
			

