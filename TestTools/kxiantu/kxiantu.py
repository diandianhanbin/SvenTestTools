# ecoding=utf-8
# Author: 翁彦彬 | Sven_Weng
# Email : diandianhanbin@gmail.com
import tushare as ts
data = ts.get_hist_data('sh', start='2016-06-01', end='2016-07-10')
# print data
print data
price = [x for x in data['open']]
print max(price)
print min(price)