# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import re

total = 0

class Post():
	title = ''
	summary = ''
	link = ''
	"""docstring for Post"""
	def __init__(self):
		pass


class WxParser:
	def __init__(self):
		pass

	##处理单个TAB的热门文章
	def swTab(self, tabKey):

		print "\n\n\n" + tabKey + "\n============================================="
		url = "http://weixin.sogou.com/pcindex/pc/" + tabKey + "/" + tabKey + ".html"
		self.parsePostList(url, tabKey)
		for x in xrange(1,100):
			moreUrl = "http://weixin.sogou.com/pcindex/pc/" + tabKey + "/" + str(x) + ".html"
			print "================================>>>>>>>>"
			print moreUrl
			try:
				if self.parsePostList(moreUrl, tabKey) is False:
					break
			except Exception,ex:
				print "Over"
				break
			pass

	def parsePostList(self, url, tabKey):
		doc = urllib2.urlopen(url)
		if doc is None:
			return False
		soup = BeautifulSoup(doc)
		newInfos = soup.findAll(attrs={'class' : re.compile("wx-news-info2$")})
		for new in newInfos:
			tuigs = tabKey + '_tit_' #title
			iuigs = tabKey + "_img_" #image
			suigs = tabKey + '_summary_' #summary
			ta = new.find(attrs={'uigs' : re.compile(tuigs + "[0-9]{1,}$")})
			sa = new.find(attrs={'uigs' : re.compile(suigs + "[0-9]{1,}$")})
			if ta is None:
				continue
			index = ta.attrs.get('uigs').split("_tit_", 1)[1]

			ia = soup.find(attrs={'uigs' : re.compile(iuigs + index + "$")})
			imghref = ia.find('img').attrs.get('src')
			title = ta.text
			link = ta.attrs.get('href')
			summary = sa.text
			print "-----------------------------"
			print "title:" + title
			print "summary:" + summary
			print 'image=' + imghref
			print 'link=' + link
			global total
			total = total + 1
		return True

	#处理所有TAB的热门文章
	def dealTabNews(self, soup):
		print "\n\n\nHot News\n============================================="
		tab = soup.find(attrs={'class' : re.compile("wx-tabbox")}).findAll("a")

		for x in tab:
			ctabkey = x.attrs.get('uigs')
			if str(ctabkey).startswith('pc'):
				self.swTab(ctabkey)
			pass

	#处理右上角热词
	def dealHotWords(self, soup):
		hotwordsLabels = soup.find(attrs={'class' : re.compile("wx-ph$")}).findAll("a")
		print "HOT WORDS"
		print "============================================="
		for label in hotwordsLabels:
			print label.attrs.get('title')
			print label.attrs.get('href')
		pass

	#处理顶部导航热门文章
	def dealTopNews(self, soup):
		news = soup.findAll(attrs={'class' : re.compile("wx-news$")})
		for new in news:
			title = new.find(attrs={'uigs' : re.compile("toptitle_\d$")}).text
			summary = new.find(attrs={'uigs' : re.compile("topsummary_\d$")}).text
			link = new.find(attrs={'uigs' : re.compile("toptitle_\d$")}).attrs.get('href')
			print title
			print summary
			print link

	def parse(self):
		doc = urllib2.urlopen("http://weixin.sogou.com/")
		soup = BeautifulSoup(doc)
		soup.originalEncoding
		#self.dealHotWords(soup)
		#self.dealTopNews(soup)
		self.dealTabNews(soup)


parser = WxParser()
parser.parse()
print "total=" + total

 

