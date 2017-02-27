#!/usr/bin/env python3
from WhoIs import mywhois
import string
import gevent
from gevent.pool import Pool
from gevent import monkey
monkey.patch_all()

letters = string.ascii_lowercase
digits = string.digits
def make_domains_list(tld):
	domians_list = []
	digits_list = [x + y for x in digits for y in digits]
	list_1 = [x + y + tld for x in letters for y in letters]
	list_2 = [x + y + z + tld for x in letters for y in letters for z in letters]
	list_3 = {}




#for test
#domians_list = [x + y + z + 'gs' for x in letters for y in letters for z in letters]
def whois(domain):
	temp = mywhois()
	flag = temp.mywhois(domain)
	if flag == 1:
		with open("domain.txt","w+") as f:
			f.write("%s\n" % domain) 
		print("%s:yes\n" % domain)
	else:
		print("%s:no\n" % domain)
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
			tld = '.' + input("pleas input a tld:")
			list = [x + y + z + tld for x in letters for y in letters for z in letters]
			pool = Pool(1000)
			pool.map(whois,list)
			print('finished,go to see the domain.txt\n')
	except ValueError:
		raise('invalid input')