#!/usr/bin/env python3
import requests,string
from datetime import datetime
import gevent
import random
from homework import mywhois
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

str1 = string.ascii_lowercase
str2 = string.ascii_lowercase + string.digits

list1 = [x + y + '.' + 'fr' for x in str1 for y in str1]
def mkdomain():
	m = 0
	letters = string.ascii_lowercase
	#num_list = [x + y for x in digits for y in digits]
	letters_list = [x + y + z for x in letters for y in letters for z in letters]
	
	while m < len(letters_list):
		l = letters_list[m]
		yield l
		m = m + 1
		
url = 'http://panda.www.net.cn/cgi-bin/check.cgi?area_domain='
#url = 'https://who.is/whois/'		 

def whois(domain):
	u = url + domain
	r = requests.get(u,timeout=3)
	html = r.text
	flag = 2
	if '<original>211' in html:
		print("%s:no\n" % domain)
		flag = 0
	else:
		if 'is available' in html:
			print("%s:yes\n" % domain)
			flag = 1
			with open("domain.txt","w") as f:
				f.write("%s\n" % domain)
		elif 'unsupport tld type' in html:
			temp = mywhois()
			flag = temp.mywhois(domain)
			if flag == 1:
				with open("domain.txt","w") as f:
					f.write("%s\n" % domain)
				print("%s:yes\n" % domain)
			elif flag == 0:
				print("%s:no\n" % domain)
			else:
				print("%s:can't check!!!" % domain)


	return flag


if __name__ == '__main__':
#功能选择菜单
	answer = input('please choose a option:\n1:check a domain whether can be use.\n2:enter a tld to see any else domains haven\'t been register.\n\r')
	try:
		option = int(answer)

		if option == 1:
			domain = input('please enter a domain:\n')
			status = whois(domain)
			if status == 1:
				print('this domain haven\'t been registered,go now!')
			elif status == 0:
				print('can\'t be registered.')


		elif option == 2:
			pool = Pool(1000)
			pool.map(whois,list1)
			print('finished,go to see the domain.txt\n')
			now = datetime.now()
			print(now)
	except ValueError:
		raise('invalid input')