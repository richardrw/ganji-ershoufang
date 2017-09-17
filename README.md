# ganji-ershoufang
ganji-ershoufang是一个用于爬取赶集网上广州二手房信息的项目

## 文件说明：
* 1.cataSpider.py：用于爬取二手房页面下的所有类目，如租房／商铺等。  
* 2.fangUrlParsing.py：分析二手房类目下的页面结构，提取房源链接。
* 3.fangUrlSpider.py：执行后将爬取房源链接。
* 4.fangInfoSpider.py：分析房源的页面结构，从房源详情中提取户型、面积、价格等信息。
* 5.fangInfoSpider.py：执行后从数据库中提取房源url用来爬取房源信息。
* 6.sqlHlper.py：封装了部分数据库操作。
* 7.getIPProxy.py：以[IPProxyPool](https://github.com/richardrw/IPProxyPool "IPProxyPool")项目为基础，获取可用的代理IP。
* 8.config.py：设置User-Agent、IPProxy信息。IPProxy的信息可以从[IPProxyPool](https://github.com/richardrw/IPProxyPool "IPProxyPool")中获取。
* 9.counting.py：爬取数量统计。
* 10.show_huxing_fenbu.ipynb：清洗数据，并得出广州二手房各户型数量分布图。结果如下：
![广州二手房各户型数量分布图](/huxing.png)
* 11.show_yearAvgPrice_fenbu.ipynb：清洗数据，并得出广州各户型二手房在特定年份的平均价格分布图。结果如下：
![广州各户型二手房在1990-2017年的平均价格分布图](/avgPrice.png)
