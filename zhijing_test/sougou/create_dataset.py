# create by zhijing 2017-08-10
# gernerate a words file from SouGou CA

#coding:utf-8
import sys
import os
import operator
from tqdm import tqdm
import time

dat_path = 'D:/wuzhijing/resp/QA_demo/zhijing_test/sougou'
dat = 'news_tensite_xml.dat'
dat = 'news.txt'
dat_dir = os.path.join(dat_path, dat)

out = 'sougou.txt'
out = 'sougou_test.txt'

def exact_content():
	contend = ''
	f_in = open(dat_dir, 'r', encoding='utf-8')
	total = len(f_in.readlines())
	f_in.close()
	if	os.path.exists(out):
		os.remove(out)
	f_out = open(out, 'w', encoding='utf-8')
	with open(dat_dir, 'r', encoding='utf-8') as f_in:
		for line in tqdm(f_in, total=total) :
#			time.sleep(1)
			x = '<content>'
			y = line[0:min(len(x),len(line))]
			if operator.eq(x, y) == True:
				contend = line[len(x):len(line)-len(x)] + '\n'
				f_out.write(contend)
#	print(contends)
	f_out.close()


				
if __name__ == '__main__':
	exact_content()