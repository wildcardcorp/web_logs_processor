#!/usr/bin/python
#easy_install pygeoip argparse csv
#Copywright 2016 Wildcard Corp. www.wildcardcorp.com
#MIT Licensed
#Use as is where is


import re
from random import choice
import argparse
import urllib2
import urllib
import collections
import time
import requests
import json
import itertools
import cStringIO
import gzip
import sys
import datetime
import ast
from tendo import singleton

GREYLOGSERVER = 'http://x.x.x.x:20002/gelf'
argparser = argparse.ArgumentParser(description='Pull and Count Cloudflare logs')
argparser.add_argument('-e', '--authemail', dest="xauthemail", default='',	help="email associated to api key")
argparser.add_argument('-k', '--apikey', dest="authkey", default='',	help="api key")
argparser.add_argument('-z', '--zoneid', dest="zoneid", default='',	help="Zone ID")
argparser.add_argument('-c', '--country', dest="countrytarget", default='',	help="country to count")
argparser.add_argument('-m', '--minsago', dest="start", default=5,	help="start X minutes ago ")
argparser.add_argument('-u', '--showurls', dest="showurls", default=0,	help="show urls counts ")
argparser.add_argument('-i', '--showips', dest="showips", default=0,	help="show ip counts ")
argparser.add_argument('-t', '--topcount', dest="topcount", default=20,	help="number of top results")
argparser.add_argument('-r', '--ray', dest="rayid", default='',	help="ray id to pull")
argparser.add_argument('-rl', '--rawlogs', dest="rawlogs", default=0,	help="raw log")
argparser.add_argument('-cl', '--commonlogs', dest="commonlogs", default=0,	help="common log to stdout")
argparser.add_argument('-ef', '--epochfile', dest="epochfile", default=0,	help="use since epoch file")
argparser.add_argument('-pg', '--pushgraylog', dest="pushgraylog", default=0,	help="push to graylog")


def getrayid():
		url = 'https://api.cloudflare.com/client/v4/zones/' + args.zoneid + '/logs/requests/' + args.rayid
		headers = {'X-Auth-Key': args.authkey, 'X-Auth-Email': args.xauthemail }
		try:
			response = requests.get(url, headers=headers)

		except urllib2.HTTPError as e:
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code, e.reason
		except urllib2.URLError as e:
			print 'We failed to reach a server.'
			print 'Reason: ', e.code, e.reason
		else:
			print response.text
		return

def top10():
		outfile = str(time_now) + '.json.gz'
		url = 'https://api.cloudflare.com/client/v4/zones/' + args.zoneid + '/logs/requests'
		headers = {'X-Auth-Key': args.authkey, 'X-Auth-Email': args.xauthemail }

		params = {'start' : int(time_now)-(int(args.start)*60), 'end' : time_now}
		try:
			response = requests.get(url, params=params, headers=headers, stream=True)

		except urllib2.HTTPError as e:
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code, e.reason
		except urllib2.URLError as e:
			print 'We failed to reach a server.'
			print 'Reason: ', e.code, e.reason
		else:
			if response.status_code == 200:
				log_data = []
				for line in response.iter_lines():
					if line:
						log_data.append(json.loads(line))
				ipset =[]
				urlset=[]
				if len(log_data) == 0:
					for logline in log_data:
						ipset.append(logline['client']['ip'])
						urlset.append(logline['clientRequest']['httpHost']+logline['clientRequest']['uri'])
					ipset_counter=collections.Counter(ipset).most_common(args.topcount)
					urlset_counter=collections.Counter(urlset).most_common(args.topcount)

					if int(args.showips) == 1:
						for value, count in ipset_counter:
							print(value, count)
					if int(args.showurls) == 1:
						for value, count in urlset_counter:
							print(value, count)
				else:
					print "NO DATA!"
			else:
				print "bad api request"

		return

def raw_logs():
		fgz = cStringIO.StringIO()
		outfile = str(time_now) + '.json.gz'
		url = 'https://api.cloudflare.com/client/v4/zones/' + args.zoneid + '/logs/requests'
		headers = {'X-Auth-Key': args.authkey, 'X-Auth-Email': args.xauthemail }

		if int(args.epochfile) == 1:
			try:
				with open('epochfile.tmp', 'r+') as epochfile:
					lastepoch=epochfile.readline()
			except:
				lastepoch = int(time_now)-(3*60)
			params = {'start' : lastepoch, 'end' : time_now}
		else:
			params = {'start' : int(time_now)-(int(args.start)*60), 'end' : time_now}
		try:
			response = requests.get(url, params=params, headers=headers, stream=True)

		except urllib2.HTTPError as e:
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code, e.reason
		except urllib2.URLError as e:
			print 'We failed to reach a server.'
			print 'Reason: ', e.code, e.reason
		else:
			if response.status_code == 200:
				log_data = []
				with gzip.GzipFile(filename=outfile, mode='w', fileobj=fgz) as gzip_obj:
					for line in response.iter_lines():
						if line:
							log_data.append(json.loads(line))
						gzip_obj.write(json.dumps(log_data) )
						if int(args.epochfile) == 1:
							with open('epochfile.tmp', 'w+') as epochfile:
								epochfile.seek(0)
								epochfile.write(str(time_now))
			else:
				print "bad api request"

		return

def common_logs():
		url = 'https://api.cloudflare.com/client/v4/zones/' + args.zoneid + '/logs/requests'
		headers = {'Accept-encoding': 'gzip', 'X-Auth-Key': args.authkey, 'X-Auth-Email': args.xauthemail }

		if int(args.epochfile) == 1:
			try:
				with open('epochfile.tmp', 'r+') as epochfile:
					lastepoch=epochfile.readline()
			except:
				lastepoch = int(time_now)-(3*60)
			params = {'start' : lastepoch, 'end' : time_now}
		else:
			params = {'start' : int(time_now)-(int(args.start)*60), 'end' : time_now}
		try:
			response = requests.get(url, params=params, headers=headers, stream=True)

		except urllib2.HTTPError as e:
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code, e.reason
		except urllib2.URLError as e:
			print 'We failed to reach a server.'
			print 'Reason: ', e.code, e.reason
		else:
			if response.status_code == 200:
				log_data = []

				for line in response.iter_lines():
					if line:
						logline = json.loads(line)
#						print logline
						print ('{} {} {} {} {} {} {}'.format(
							logline['client']['ip'],
							logline['client']['srcPort'],
							logline['clientRequest']['httpHost'],
							logline['clientRequest']['uri'],
							logline['edgeResponse']['status'],
							logline['edgeResponse']['bytes'],
		#					logline['clientRequest']['userAgent'],
							logline['rayId']))

					if int(args.epochfile) == 1:
						with open('epochfile.tmp', 'w+') as epochfile:
							epochfile.seek(0)
							epochfile.write(str(time_now))
				else:
					print "NO DATA!"
					return
			else:
				print "bad api request"
				return
		return


def push_graylog():
#curl -XPOST http://graylog.example.org:12202/gelf -p0 -d '{"short_message":"Hello there", "host":"example.org", "facility":"test", "_foo":"bar"}'
		ingest_url = GREYLOGSERVER
		url = 'https://api.cloudflare.com/client/v4/zones/' + args.zoneid + '/logs/requests'
		headers = {'Accept-encoding': 'gzip', 'X-Auth-Key': args.authkey, 'X-Auth-Email': args.xauthemail }

		if int(args.epochfile) == 1:
			try:
				with open('epochfile.tmp', 'r+') as epochfile:
					lastepoch=epochfile.readline()
			except:
				lastepoch = int(time_now)-(3*60)
			params = {'start' : lastepoch, 'end' : time_now}
		else:
			params = {'start' : int(time_now)-(int(args.start)*60), 'end' : time_now}
		try:
			response = requests.get(url, params=params, headers=headers, stream=True)

		except urllib2.HTTPError as e:
			print 'The server couldn\'t fulfill the request.'
			print 'Error code: ', e.code, e.reason
		except urllib2.URLError as e:
			print 'We failed to reach a server.'
			print 'Reason: ', e.code, e.reason
		else:
			if response.status_code == 200:
				log_data = []

				for line in response.iter_lines():
					if line:
						logline =[]
						logline = json.loads(line)
						json_data = json.dumps({ \
									  "version": "1.1", \
									  "host": "rest processor", \
									  "full_message": json.dumps(logline), \
									  "short_message": "CF from zone", \
									  "timestamp":  "{:.5f}".format((int(logline['timestamp']))/1000000000.0), \
									  "level": 1,\

									})
						push_r = requests.post(ingest_url, data=json_data)
					if int(args.epochfile) == 1:
						with open('epochfile.tmp', 'w+') as epochfile:
							epochfile.seek(0)
							epochfile.write(str(time_now))

			else:
				print "bad api request Code: " + str(response.status_code)
				return
		return




if __name__ == '__main__':
	args = argparser.parse_args()
	time_now = int(time.time())

	me = singleton.SingleInstance() # will sys.exit(-1) if other instance is running

	if args.rayid != '':
		getrayid()
	elif int(args.commonlogs) == 1:
		common_logs()
	elif int(args.rawlogs) == 1:
		raw_logs()
	elif int(args.pushgraylog) == 1:
		push_graylog()
	else:
		top10()

	sys.exit()





#	gi = pygeoip.GeoIP('GeoIP.dat')
