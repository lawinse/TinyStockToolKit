import urllib2,urllib,sys,re,time,json,sys
from stock import *

from PyQt4.QtCore import *
from PyQt4.QtGui import *
global stock2code,code2stock,stock_histdetail
stock2code = {}
code2stock = {}
stock_histdetail = {}
stock_daydetail = {}

app = QApplication([])
clipboard = QApplication.clipboard()


def get_json_from_api(clear_stock_code):
	global stock_histdetail,stock_daydetail
	Myapikey = "c13ebaeeb37da844497222a59c9b7ceb";
	# if (clear_stock_code in )
	# print time.localtime()[3],time.localtime()[4]

	if ((time.localtime()[3]>=15 and time.localtime()[4]>10 or time.localtime()[3]>15) and clear_stock_code in stock_daydetail.keys()):
		s = json.loads(stock_daydetail[clear_stock_code])

	else:
		print "api: daydetail"
		url = "http://apis.baidu.com/apistore/stockservice/stock?stockid="+clear_stock_code+"&list=1"
		req = urllib2.Request(url)
		req.add_header("apikey",Myapikey);
		resp = urllib2.urlopen(req)
		content = resp.read()
		stock_daydetail[clear_stock_code] = content
		s = json.loads(content)


	if (clear_stock_code in stock_histdetail.keys()):
		s1 = json.loads(stock_histdetail[clear_stock_code]);
	else:
		print "api: histdetail"
		mkt = clear_stock_code[0:2];

		# secID = (mkt=="sh")?
		if (mkt=="sh"):
			secID = clear_stock_code[2:]+".XSHG"
		else:
			secID = clear_stock_code[2:]+".XSHE"
		ticker = clear_stock_code[2:]
		ok = 0;
		for Type in ["A","B"]:
			url = 'http://apis.baidu.com/wxlink/getequ/getequ?secID='+secID+'&ticker='+ticker+'&equTypeCD='+Type+'&field=primeOperating,officeAddr,'+\
						'transCurrCD,totalShares,nonrestFloatShares,nonrestfloatA,listDate'
			# print url
			req = urllib2.Request(url)
			req.add_header("apikey",Myapikey)
			resp = urllib2.urlopen(req)
			content = resp.read()
			stock_histdetail[clear_stock_code] = content;
			# print content
			s1 = json.loads(content);

			if (s1["result"]["retCode"] == 1): break;
	print len(stock_histdetail),len(stock_daydetail)
	if (len(stock_histdetail) > 20):
		cnt = 0
		for item in stock_histdetail.keys():
			stock_histdetail.pop(item)
			++cnt
			if (cnt > 5): break
	if (len(stock_daydetail) > 20):
		cnt = 0
		for item in stock_daydetail.keys():
			stock_daydetail.pop(item)
			++cnt
			if (cnt > 5): break
	return s,s1

def isStockCode(str):
	return str.isdigit() and len(str) == 6


def on_clipboard_change():

    data = clipboard.mimeData()
    # if data.hasFormat('text/uri-list'):
    #     for path in data.urls():
    #         print path
    if data.hasText():
        # print "text"
        # print data.text()
        clear_text = str(data.text()).strip().decode("utf8")
        clear_text = "".join(clear_text.split())
        clear_stock_code = ""
        if (isStockCode(clear_text)):
        	if (clear_text in code2stock.keys()):
        		clear_stock_code = code2stock[clear_text].split("&")[0] + clear_text
        	else:
        		print "Not found!\n"
        else:
        	if (clear_text in stock2code.keys()):
        		clear_stock_code = stock2code[clear_text];
        	else:
        		print "Not found!\n"
        if (clear_stock_code==""): return
        json1,json2 = get_json_from_api(clear_stock_code);
        stk = Stock(json1["retData"]["stockinfo"][0],json2["result"]["data"][0])
        stk.printStock();




def load_stock_dic():
	global stock2code,code2stock,stock_histdetail
	f1 = open('stock2code.dat','r')
	stock2code = eval(f1.read());
	f1.close();
	f1 = open('code2stock.dat','r')
	code2stock = eval(f1.read());
	f1.close();
	# f1 = open('stock_histdetail.dat','r')
	# code2stock = eval(f1.read());
	# if (time.time()-code2stock["time"]>12*3600):
	# 	code2stock = {}
	# 	code2stock["time"] = time.time();
	# f1.close();


def get_stock_dic():
	curTime = time.time()
	timestamp = open("ts.dat","r");
	if (curTime < eval(timestamp.read())+24*3600):
		timestamp.close()
		return
	timestamp.close()
	url =str('http://quote.eastmoney.com/stocklist.html')
	header = { 'User-Agent':'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)' }
	request = urllib2.Request(url,headers = header)
	_stock2code = {}
	_code2stock = {}
	try:
		response = urllib2.urlopen(request,)
		content = response.read().decode("gbk")
		pattern = re.compile('<li><a.*?href=.*?html">(.*?)</a></li>',re.I)
		items = re.findall(pattern,content)
		reload(sys)
		sys.setdefaultencoding('utf-8')
		timestamp = open("ts.dat","w")
		f1 = open('stock2code.dat','w')
		f2 = open('code2stock.dat','w')
		market = "sh";
		for item in items:

			# print item
			tmp = re.split("[()]",item)
			if (tmp[1] == "000001"): market = "sz"
			_stock2code[tmp[0]] = market+tmp[1]
			_code2stock[tmp[1]] = market+"&"+tmp[0];
		f1.write(str(_stock2code))
		f2.write(str(_code2stock))
		timestamp.write(str(time.time()));
		f1.close()
		f2.close()
		timestamp.close();
	except urllib2.URLError, e:
		if hasattr(e,"code"):        
			print u"dsd",e.reason

def main():
	get_stock_dic();
	load_stock_dic();
	clipboard.dataChanged.connect(on_clipboard_change)
	sys.exit(app.exec_())
	



if __name__ == '__main__':
	main()

	# u'\u5e73\u5b89\u94f6\u884c'