# -*- coding: utf-8 -*-
class Stock:
	def __init__(self,_obj1,_obj2):
		self.__dict__.update(_obj1)
		self.__dict__.update(_obj2)
	def printStock_Debug(self):
		for item in self.__dict__.keys():
			print item + ":" , self.__dict__[item],"\n"
	def printStock(self):
		dic = self.__dict__
		print "股票名称:" , dic["name"]
		print "代码:" , dic["code"]
		print "更新时间:" , dic["date"] + " "+ dic["time"]
		print "今开盘:" , (dic["OpenningPrice"])
		print "昨收盘:" , (dic["closingPrice"])
		print "当前:" , (dic["currentPrice"])
		print "今最高:" , (dic["hPrice"])
		print "今最低:" , (dic["lPrice"])
		print "卖一:" , (dic["sellOnePrice"]),dic["sellOne"]
		print "买一:" , (dic["buyOnePrice"]), dic["buyOne"]
		print "------------------------"
		print "上市日期:" , (dic["listDate"])
		print "成交数:" , (dic["totalNumber"])
		print "成交额（元）:" , (dic["turnover"])
		print "总股本:" , (dic["totalShares"])
		print "公司无限售流通股份合计:" , (dic["nonrestFloatShares"])
		print "无限售流通股本:" , (dic["nonrestfloatA"])
		print "办公地址:" , (dic["officeAddr"])
		print "主营业务范围:" , (dic["primeOperating"])
		print "\n\n"



		
if __name__ == '__main__':
	stk = Stock({},{})
	stk = Stock(s["retData"]["stockinfo"][0],s1["result"]["data"][0])
	stk.printStock();