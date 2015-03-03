# -*- coding: utf-8 -*-
import urllib2
from bs4 import BeautifulSoup
import re

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
		url = "http://weixin.sogou.com/pcindex/pc/" + tabKey + "/" + tabKey + ".html"
		doc = urllib2.urlopen(url)
		soup = BeautifulSoup(doc)
		#soup.originalEncoding
		for x in xrange(1,30):
			tuigs = tabKey + '_tit_' + str(x) #title
			iuigs = tabKey + "_img_" + str(x) #image
			suigs = tabKey + '_summary_' + str(x) #summary
			ta = soup.find(attrs={'uigs' : re.compile(tuigs + "$")})
			ia = soup.find(attrs={'uigs' : re.compile(iuigs + "$")})
			sa = soup.find(attrs={'uigs' : re.compile(suigs + "$")})
			if ia is None:
				continue
			imghref = ia.find('img').attrs.get('src')
			title = ta.text
			summary = sa.text
			print str(x) + ":"
			print title
			print summary
			print 'imageHref=' + imghref
			pass
		pass

	def unescape(self, s):
		if s is None:
			return 'None'
		s = s.replace("&lt;", "<")
		s = s.replace("&gt;", ">")
		# this has to be last:
		s = s.replace("&amp;", "&")
		return s

	#处理所有TAB的热门文章
	def dealTabNews(self, soup):
		print "\n\n\nHot News\n============================================="
		tab = soup.find(attrs={'class' : re.compile("wx-tabbox")}).findAll("a")

		for x in tab:
			ctabkey = x.attrs.get('uigs')
			if str(ctabkey).startswith('pc'):
				swTab(ctabkey)
			pass

	#处理右上角热词
	def dealHotWords(self, soup):
		hotwordsLabels = soup.find(attrs={'class' : re.compile("wx-ph$")}).findAll("a")
		print "HOT WORDS"
		print "============================================="
		for label in hotwordsLabels:
			print label.text
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
			pass

	def parse(self):
		doc = urllib2.urlopen("http://weixin.sogou.com/")
		soup = BeautifulSoup(doc)
		soup.originalEncoding
		self.dealTopNews(soup)


parser = WxParser()
parser.parse()

 

