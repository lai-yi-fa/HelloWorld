#!coding=utf8
import sys
reload(sys)
sys.setdefaultencoding('utf8')
import scrapy
#from scrapy_redis.spiders import RedisSpider
from scrapy.loader import ItemLoader
from scrapy.http import Request
from tv_Spider.items import TvSpiderItem
import requests
import bs4
from scrapy.loader.processors import MapCompose
from bs4 import BeautifulSoup
import lxml
import re
from urllib2 import URLError
import json
import time
import signal
from pybloomfilter import BloomFilter
import os
from scrapy.exceptions import CloseSpider
from urllib import quote_plus
import datetime
from scrapy.item import Item,Field
import hashlib
from tv_Spider.Path_translate import Relative_to_Absolute,Get_Valid_Url,get_HeadUrl
from tv_Spider.Total_page_circulate import Total_page_circulate,Turn_True_Page


class tvSpider(scrapy.Spider):
	name ='mangguo_tv'
	allowed_domain = []
		
	def __init__(self,*args,**kwargs):
		super(tvSpider,self).__init__(*args,**kwargs)
		self.now = time.time()
		self.config = []
		self.Index_Url = ""
			
	
	def start_requests(self):
		with open('config.json','r') as f:
			data = json.load(f)
			for i in data.iteritems():
				if i[0].encode('utf-8') == self.name:
					self.config.append(i)
			f.close()
		
		for v in self.config:
			if len(v[1]) == 2:
				self.Index_Url = v[1][0]['Index_Url']
				Is_Json = v[1][0]['Is_Json']
				Max_Page = v[1][0]['Max_Page']
				Final_Xpath = v[1][1]['Final_Xpath']
				if Is_Json == 1:
						for url in self.Index_Url:
								request = Request(url,self.parse_json)
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request
				else:
						for url in  self.Index_Url:
								request = Request(url,self.parse_splash,meta={
										'splash':{
										'endpoint':'render.html',
										'args':{
												'wait':0.5,
												'images':0,
												'render_all':1
												}
										}
								})				
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request	
			
			if len(v[1]) == 3:
				self.Index_Url = v[1][0]['Index_Url']
				Is_Json = v[1][0]['Is_Json']
				Max_Page = v[1][0]['Max_Page']
				All_Detail_Page = v[1][1]['All_Detail_Page']
				Final_Xpath = v[1][2]['Final_Xpath']
				if Is_Json == 1:
						for url in self.Index_Url:
								request = Request(url,self.parse_json)
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['All_Detail_Page'] = All_Detail_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request
				else:
						for url in  self.Index_Url:
								request = Request(url,self.parse_splash,meta={
										'splash':{
										'endpoint':'render.html',
										'args':{
												'wait':0.5,
												'images':0,
												'render_all':1
												}
										}
								})				
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['All_Detail_Page'] = All_Detail_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request	
				
			if len(v[1]) == 4:
				self.Index_Url = v[1][0]['Index_Url']
				Is_Json = v[1][0]['Is_Json']
				Max_Page = v[1][0]['Max_Page']
				All_Detail_Page = v[1][1]['All_Detail_Page']
				Signal_Detail_Page = v[1][2]['Signal_Detail_Page']
				Final_Xpath = v[1][3]['Final_Xpath']
				if Is_Json == 1:
						for url in self.Index_Url:
								request = Request(url,callback = self.parse_json)
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['All_Detail_Page'] = All_Detail_Page
								request.meta['Signal_Detail_Page'] = Signal_Detail_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request
				else:
						for url in self.Index_Url:
								request = Request(url,callback = self.parse_splash,dont_filter=True,meta={
											'splash':{
													'endpoint':'render.html',
													'args':{
															'wait':0.5,
															'images':0,
															'render_all':1
														}
													}
												})
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['All_Detail_Page'] = All_Detail_Page
								request.meta['Signal_Detail_Page'] = Signal_Detail_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request

			if len(v[1]) == 5:
				self.Index_Url = v[1][0]['Index_Url']
				Is_Json = v[1][0]['Is_Json']
				Max_Page = v[1][0]['Max_Page']
				All_Detail_Page = v[1][1]['All_Detail_Page']
				Signal_Detail_Page = v[1][2]['Signal_Detail_Page']
				Target_Detail_Page = v[1][3]['Target_Detail_Page']
				Final_Xpath = v[1][4]['Final_Xpath']
				if Is_Json == 1:
						for url in self.Index_Url:
								request = Request(url,callback = self.parse_json)
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['All_Detail_Page'] = All_Detail_Page
								request.meta['Signal_Detail_Page'] = Signal_Detail_Page
								request.meta['Target_Detail_Page'] = Target_Detail_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request
				else:
						for url in self.Index_Url:
								request = Request(url,callback = self.parse_splash,meta={
											'splash':{
													'endpoint':'render.html',
													'args':{
															'wait':0.5,
															'images':0,
															'render_all':1
														}
													}
												})
								request.meta['Index_Url'] = url
								request.meta['Max_Page'] = Max_Page
								request.meta['All_Detail_Page'] = All_Detail_Page
								request.meta['Signal_Detail_Page'] = Signal_Detail_Page
								request.meta['Target_Detail_Page'] = Target_Detail_Page
								request.meta['Final_Xpath'] = Final_Xpath
								yield request
				

	def parse_splash(self,response):
		#????????????????????????????????????????????????????????????????????????????????????????????????????????????final_parse???
		Index_Url = response.meta.get('Index_Url',None)
		Max_Page = response.meta.get('Max_Page',None)
		All_Detail_Page = response.meta.get('All_Detail_Page',None)
		Signal_Detail_Page = response.meta.get('Signal_Detail_Page',None)
		Target_Detail_Page = response.meta.get('Target_Detail_Page',None)
		Final_Xpath = response.meta.get('Final_Xpath',None)
		max_pages = 2
		try:
				max_pages = re.search(Max_Page['re'],''.join(response.xpath(Max_Page['xpath']).extract())).group()
		except Exception,e:
				print Exception,":",e
		#????????????????????????\d+????????????????????????????????????????????????get_HeadUrl()
		urls = get_HeadUrl(Index_Url,self.name)
		try:
				max_pages = Total_page_circulate(self.name,int(max_pages))
		except Exception,e:
				print Exception,":",e
		
		print "???????????????:%d"%max_pages
		if All_Detail_Page is None:
				for i in range(1,max_pages+1):
						i = Turn_True_Page(i,self.name)
						url = urls.format(page=str(i))
						request = Request(url,callback = self.parse_final,dont_filter=True,meta={
											'splash':{
											'endpoint':'render.html',
											'args':{
													'wait':0.5,
													'images':0,
													'render_all':1
													}
											}
								})
						request.meta['Final_Xpath'] = Final_Xpath
						yield request
		else:
				for i in range(1,int(max_pages)+1):
						try:
								i = Turn_True_Page(i,self.name)
								url = urls.format(page=str(i))
						except Exception,e:
								print Exception,":",e
						request = Request(url,callback = self.parse_first,dont_filter=True,meta={
										'splash':{
										'endpoint':'render.html',
										'args':{
												'wait':0.5,
												'images':0,
												'render_all':1
												}
										}
								})
						request.meta['Index_Url'] = Index_Url
						request.meta['All_Detail_Page'] = All_Detail_Page
						request.meta['Signal_Detail_Page'] = Signal_Detail_Page
						request.meta['Target_Detail_Page'] = Target_Detail_Page
						request.meta['Final_Xpath'] = Final_Xpath
						yield request

	def parse_json(self,response):
		Index_Url = response.meta.get('Index_Url',None)
		Max_Page = response.meta.get('Max_Page',None)
		All_Detail_Page = response.meta.get('All_Detail_Page',None)
		Signal_Detail_Page = response.meta.get('Signal_Detail_Page',None)
		Target_Detail_Page = response.meta.get('Target_Detail_Page',None)
		Final_Xpath = response.meta.get('Final_Xpath',None)
		res_json = json.loads(response.body_as_unicode())
		
		depth = 0
		try:
				while depth < len(Max_Page['index']):
						res_json = res_json.get(Max_Page['index'][depth])
						depth += 1
		except Exception,e:
				print Exception,":",e
		urls = get_HeadUrl(Index_Url,self.name)	
		
		print "now the res_json is %s"%res_json
		max_pages = Total_page_circulate(self.name,int(res_json))
		print "???????????????:%d"%max_pages
		if All_Detail_Page is None:
				for i in range(1,max_pages+1):
						i = Turn_True_Page(i,self.name)
						url = urls.format(page=str(i))
						request = Request(url,callback = self.parse_final,dont_filter=True,meta={
											'splash':{
											'endpoint':'render.html',
											'args':{
													'wait':0.5,
													'images':0,
													'render_all':1
													}
											}
								})
						request.meta['Final_Xpath'] = Final_Xpath
						yield request
		else:
				for i in range(1,int(max_pages)+1):
						try:
								i = Turn_True_Page(i,self.name)
								url = urls.format(page=str(i))
						except Exception,e:
								print Exception,":",e
						request = Request(url,callback = self.parse_json2,dont_filter=True)
						request.meta['Index_Url'] = Index_Url
						request.meta['All_Detail_Page'] = All_Detail_Page
						request.meta['Signal_Detail_Page'] = Signal_Detail_Page
						request.meta['Target_Detail_Page'] = Target_Detail_Page
						request.meta['Final_Xpath'] = Final_Xpath
						yield request

		
	def parse_json2(self,response):
		Index_Url = response.meta.get('Index_Url',None)
		All_Detail_Page = response.meta.get('All_Detail_Page',None)
		Signal_Detail_Page = response.meta.get('Signal_Detail_Page',None)
		Target_Detail_Page = response.meta.get('Target_Detail_Page',None)
		Final_Xpath = response.meta.get('Final_Xpath',None)
		detail_url = []
		res_json = json.loads(response.body_as_unicode())
		#????????????????????????key?????????value?????????????????????????????????[????????????for??????????????????list??????????????????len-1?????????????????????detail_url]
		depth = 0
		length = len(All_Detail_Page['index'])
		while depth < length - 1:
				res_json = res_json.get(All_Detail_Page['index'][depth])
				depth += 1
		#print "now the res_json is %s"%res_json
		for i in res_json:
				detail_url.append(i.get(All_Detail_Page['index'][length-1]))
		try:
				detail_url = Relative_to_Absolute(Index_Url,detail_url,self.name)
		except Exception,e:
				print Exception,":",e
		
		
		for url in detail_url:
				if Signal_Detail_Page is None:
						request = Request(url,callback = self.parse_final,meta={
											'splash':{
											'endpoint':'render.html',
											'args':{
													'wait':0.5,
													'images':0,
													'render_all':1
													}
											}
									})
						request.meta['Final_Xpath'] = Final_Xpath
						yield request
				else:
						request = Request(url,callback = self.parse_second)
						request.meta['Index_Url'] = Index_Url
						request.meta['Signal_Detail_Page'] = Signal_Detail_Page
						request.meta['Target_Detail_Page'] = Target_Detail_Page
						request.meta['Final_Xpath'] = Final_Xpath
						yield request

			
	def parse_first(self,response):
		Index_Url = response.meta.get('Index_Url',None)
		All_Detail_Page = response.meta.get('All_Detail_Page',None)
		Signal_Detail_Page = response.meta.get('Signal_Detail_Page',None)
		Target_Detail_Page = response.meta.get('Target_Detail_Page',None)
		Final_Xpath = response.meta.get('Final_Xpath',None)
		Some_Info = {}
		if 'Some_Info' in All_Detail_Page.keys():
				keys = All_Detail_Page['Some_Info'].keys()
				for key in keys:
						try:
								Some_Info[key] = response.xpath(All_Detail_Page['Some_Info'][key]).extract()[0]
						except Exception,e:
								print Exception,":",e
		#??????????????????????????????????????????xpath???????????????????????????list???
		detail_url = []
		
		for xpath in All_Detail_Page['xpath']:
				for url in Relative_to_Absolute(Index_Url,response.xpath(xpath).extract(),self.name):
						detail_url.append(url)
		#??????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????????final_parse?????????????????????final_parse???????????????????????????????????????????????????????????????????????????????????????????????????config.json???Final_Xpath?????????flag???1?????????????????????0??????????????????
		if Signal_Detail_Page is None:
				for url in detail_url:
						request = Request(url,callback = self.parse_final,dont_filter=True,meta={
											'splash':{
											'endpoint':'render.html',
											'args':{
													#??????aiyiyi??????load 10s????????????????????????
													'wait':0.5,
													'images':0,
													'render_all':1
													}
											}
									})
						request.meta['Some_Info'] = Some_Info
						request.meta['Final_Xpath'] = Final_Xpath
						yield request
		else:
				for url in detail_url:
						#???????????????????????????????????????????????????????????????????????????link
						request = Request(url,callback = self.parse_second,dont_filter=True,meta={
											'splash':{
											'endpoint':'render.html',
											'args':{
													'wait':0.5,
													'images':0,
													'render_all':1
													}
											}
									})
						#??????????????????????????????www.xxxx.com/xxx/xxx????????????????????????????????????list.mangguo.com/.... ????????????????????????url????????????????????????url??????????????????????????????url??????????????????Index_Url????????????
						request.meta['Index_Url'] = url
						request.meta['Signal_Detail_Page'] = Signal_Detail_Page
						request.meta['Target_Detail_Page'] = Target_Detail_Page
						request.meta['Final_Xpath'] = Final_Xpath
						yield request
	
	def parse_second(self,response):
		Index_Url = response.meta.get('Index_Url',None)
		Signal_Detail_Page = response.meta.get('Signal_Detail_Page',None)
		Target_Detail_Page = response.meta.get('Target_Detail_Page',None)
		Final_Xpath = response.meta.get('Final_Xpath',None)
		Some_Info = {}
		if 'Some_Info' in Signal_Detail_Page.keys():
				keys = Signal_Detail_Page['Some_Info'].keys()
				for key in keys:
						try:
								Some_Info[key] = response.xpath(Signal_Detail_Page['Some_Info'][key]).extract()[0]
						except Exception,e:
								print Exception,":",e
		detail_url = Relative_to_Absolute(Index_Url,response.xpath(Signal_Detail_Page['xpath']).extract(),self.name)
		if Target_Detail_Page is None:
				for url in detail_url:
						request = Request(url,callback = self.parse_final,dont_filter=True,meta={
												'splash':{
												'endpoint':'render.html',
												'args':{
														'wait':0.5,
														'images':0,
														'render_all':1
													}
												}
											})
						request.meta['Some_Info'] = Some_Info
						request.meta['Final_Xpath'] = Final_Xpath
						yield request
		else:
				for url in detail_url:
						#print "now the url is %s"%url
						request = Request(url,callback = self.parse_third,dont_filter=True)
						request.meta['Index_Url'] = Index_Url
						request.meta['Target_Detail_Page'] = Target_Detail_Page
						request.meta['Final_Xpath'] = Final_Xpath
						yield request
		

	def parse_third(self,response):
		Index_Url = response.meta['Index_Url']
		Target_Detail_Page = response.meta.get('Target_Detail_Page',None)
		Final_Xpath = response.meta.get('Final_Xpath',None)
		detail_url = Relative_to_Absolute(Index_Url,response.xpath(Target_Detail_Page['xpath']).extract(),self.name)	
		Some_Info = {}
		if 'Some_Info' in Target_Detail_Page.keys():
				keys = Target_Detail_Page['Some_Info'].keys()
				for key in keys:
						try:
								Some_Info[key] = response.xpath(Target_Detail_Page['Some_Info'][key]).extract()[0]
						except Exception,e:
								print Exception,":",e
		for url in detail_url:
				request = scrapy.Request(url,callback = self.parse_final,meta = {
										'splash':{
										'endpoint':'render.html',
										'args':{
												'wait':0.5,
												'images':0,
												'render_all':1
												}
										}
								})				
				request.meta['Some_Info'] = Some_Info
				request.meta['Final_Xpath'] = Final_Xpath
				#print "??????????????????????????????Some_Info???%s,?????????????????????url???%s"%(Some_Info['artist_name'],url)
				yield request


	def parse_final(self,response):
		#???????????????Final_Xpath????????????????????????......?????????????????????Final_Xpath??????????????????????????????
		Final_Xpath = response.meta.get('Final_Xpath',None)
		Some_Info = response.meta.get('Some_Info',None)
		
		if 'All_Xpath' not in Final_Xpath.keys():
				item = TvSpiderItem()
				l = ItemLoader(item=item, response=response)
				for key in Final_Xpath.keys():
						item.fields[key] = Field()
						try:
								#itemloader???add_xxx?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????("")
								if map(lambda x:1 if x else 0, map(lambda x:response.xpath(x).extract() if x != "/" else "",Final_Xpath[key])) in [[0,0],[0]] and key != "site_name":		
										map(lambda x:l.add_value(key , ""),["just_one"])
								elif key == "site_name":
										map(lambda x:l.add_value(key , x),Final_Xpath[key])
								else:
										map(lambda x:l.add_xpath(key , x) if response.xpath(x).extract() != [] else "",Final_Xpath[key])
						except Exception,e:
								print Exception,":",e
				if Some_Info:
						for key in Some_Info.keys():
								item.fields[key] = Field()
								l.add_value(key , Some_Info[key])
				yield l.load_item()
		else:
		#?????????????????????itemloader???add_xxx???????????????????????????????????????????????????????????????item?????????????????????????????????????????????item???itemloader????????????????????????????????????add_xpath??????????????????;;?????????add_value??????
				my_Final_Xpath = Final_Xpath.copy()
				All_Xpath = my_Final_Xpath['All_Xpath'].copy()
				del my_Final_Xpath['All_Xpath']
				all_xpath = All_Xpath['all_xpath']
				del All_Xpath['all_xpath']
				for i in response.xpath(all_xpath[0]):
						item = TvSpiderItem()
						l = ItemLoader(item=item, response=response)
						#???All_Xpath????????????????????????
						for key in All_Xpath.keys():
								item.fields[key] = Field()
								try:
										#itemloader???add_xxx?????????????????????????????????????????????????????????????????????????????????????????????????????????????????????("")
										if map(lambda x:1 if x else 0, map(lambda x:response.xpath(x).extract() if x != "/" else "",Final_Xpath[key])) in [[0,0],[0]]:
												map(lambda x:l.add_value(key , ""),["just_one"])
										else:
												map(lambda x:l.add_value(key, i.xpath(x).extract()) if i.xpath(x).extract() != [] else "",Final_Xpath[key])
								except Exception,e:
										print Exception,",",e
						#?????????All_Xpath???????????????????????????????????????????????????????????????????????????????????????????????????????????????All_Xpath??????????????????????????????
						for key in my_Final_Xpath.keys():
								item.fields[key] = Field()
								try:
										if map(lambda x:1 if x else 0, map(lambda x:response.xpath(x).extract() if x != "/" else "",Final_Xpath[key])) in [[0,0],[0]] and key != "site_name":
												map(lambda x:l.add_value(key , ""),["just_one"])
										elif key == "site_name":
												map(lambda x:l.add_value(key , x),my_Final_Xpath[key])
										else:
												map(lambda x:l.add_xpath(key , x) if response.xpath(x).extract() != [] else "",Final_Xpath[key])
								except Exception,e:
											print Exception,":",e
					
						if Some_Info:
								for key in Some_Info.keys():
									item.fields[key] = Field()
									l.add_value(key , Some_Info[key])
						yield l.load_item()
				
										#'splash':{
								#		'endpoint':'render.html',
								#		'args':{
								#				'wait':5,
								#				'images':0,
								#				'render_all':1
								#				}
								#		}
								#})				

