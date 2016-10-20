eastmoney_postspider
===
A web crawler based on python-scrapy
---


# 中文介绍 | (Chinese Version)
更新：2016年10月20日
## 用途
在[东方财富网股吧](http://guba.eastmoney.com/remenba.aspx?type=1)中寻找沪深300指数成分股表格(000300cons.xls)中提及的股票所涉及的2016年1月～9月的所有帖子，并将这些帖子的标题、作者、阅读量、评论数、发表日期和帖子的链接输出到Json文件和SQL数据库中
## 环境
* 操作系统：OS X 10.11 (EI Capitan)
* Python版本: 2.7.12
* Python包：scrapy, xlrd, codec, MySQLdb, requests等
* 数据库支持：本地MySQL（SQLite支持在建），需要MySQL-python, MySQL-connector-c, MySQL-connector-python
## 实现
### 目标特点
* 未对或几乎未对机器访问行为进行限
制
* 每支股票的股吧的链接中包含了股票代码和分页页码
* 每支股票的股吧的帖子列表中包含了除发表年份之外的所有待爬元素，需进入帖子页面才能确定发表年份
* 翻页等交互操作主要通过HTML的href来实现，未使用javascript
### 程序流程
1. 加载xls文件读取包xlrd，读取工作簿，得到所有需要的的成分券代码
2. 根据成分券代码和目标特点，得到初始链接池（列表）start_url[]
3. scrapy包对start_url[]中的链接进行HTTP GET请求，使用parse()对返回结果进行解析
  3.1. 使用XPath（XML路径语言），结合正则表达式(RegEx)得到各元素的值（为字符串列表），即建立scrapy的选择器（selector）
  3.2. 将元素存储入item[]中
  3.3. 初步判断该页面内元素的合法性，若合法则用生成器生成，进入pipeline准备输出
  3.4. 回调parse()，解析下一页
4. （实际上与3.3同时）根据settings.py中各pipeline的配置，建立pilelines.py中定义的pipeline
5. 转换unicode编码字符，统一使用UTF－8编码以解决中文显示的问题
6. 输出
  6.1. 直接将每次的输出结果写入output.json
  6.2. 将合法元素分行插入SQL数据库的表中
## 待优化
（正在补充）

# English Version
To be continued...
