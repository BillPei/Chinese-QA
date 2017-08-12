# create by zhijing 2017-08-11
# translate SQuAD from english to chinese
# refactor the answers' indexs

# encoding='utf-8'
import os
from tqdm import tqdm
import argparse
import requests
import urllib
import json


def get_args():
	parser = argparse.ArgumentParser()
	BASE_PATH = 'D:/wuzhijing/resp/QA_demo'
	source_dir = os.path.join(BASE_PATH, "data", "squad")
	target_dir = os.path.join(BASE_PATH, "zhijing_test", "translate")
	chinese_dir = os.path.join(BASE_PATH, "zhijing_test", "translate")
	parser.add_argument('-s', "--source_dir", default=source_dir)
	parser.add_argument('-t', "--target_dir", default=target_dir)
	parser.add_argument('-ch', "--chinese_dir", default=chinese_dir)
	# TODO : put more args here
	return parser.parse_args()


def md5(str):
	import hashlib
	m = hashlib.md5()
	m.update(str)
	return m.hexdigest()
	
def translate_to_chinese(origin):
	q = origin
	trans=''
	salt = '1435660288'
#	appid = '20170328000043661'
#	key = '3Lp28tN3wuavY4K8LET2'
	appid = '20170812000072029'
	key = 'vpNWx2eK4HT5w27RbxP9'
	sign = (appid+q+salt+key).encode('utf-8')
	sign = md5(sign)
	# print('translating:q=',q)
	q = urllib.parse.quote(q)
	url = 'http://api.fanyi.baidu.com/api/trans/vip/translate?q='+q+'&from=en&to=zh&appid='+appid+'&salt='+salt+'&sign='+sign
	url = url.encode('utf-8')
	req = requests.get(url=url)
	trans = req.text
#	print(trans)
	return json.loads(trans)
#{"from":"en","to":"zh","trans_result":[{"src":"HI, HOW ARE YOU","dst":"嗨，你好吗？"}]}

def save(args, data, data_type):
	data_path = os.path.join(args.target_dir, "{}-v1.1.json".format(data_type))
	json.dump(data, open(data_path, 'w'))

def prepro(args):
	if not os.path.exists(args.target_dir):
		os.makedirs(args.target_dir)
#	prepro_each(args, 'dev', 0.0, 1.0, out_name='dev')
	prepro_each(args, 'train', 0.0, 1.0, out_name='train')

def prepro_each(args, data_type, start_ratio=0.0, stop_ratio=1.0, out_name="default"):
	source_path = os.path.join(args.source_dir, "{}-v1.1.json".format(data_type))
	chinese_path = os.path.join(args.chinese_dir, "{}-v1.1-chinese.json".format(data_type))
	source_data = json.load(open(source_path, 'r', encoding='utf-8'))
#	chinese_data = json.load(open(chinese_path, 'r', encoding='utf-8'))
	target_data = source_data
	start_ai = int(round(len(source_data['data']) * start_ratio))
	stop_ai = int(round(len(source_data['data']) * stop_ratio))
#	stop_ai = min(50, stop_ai)
	
	len_chinese = 22  # 已经翻译好的样本
	for ai, article in enumerate(tqdm(source_data['data'][start_ai:stop_ai], total=stop_ai-start_ai)):
		if ai < len_chinese:
			print(ai)
			target_data['data'][ai] = chinese_data['data'][ai]
			continue
		for pi, para in tqdm(enumerate(article['paragraphs']),total=len(article['paragraphs'])):
			context = para['context']
			context = translate_to_chinese(context)['trans_result'][0]['dst']
			target_data['data'][ai]['paragraphs'][pi]['context'] = context
			
			for qi, qa in enumerate(para['qas']):
				question = qa['question']
				question = translate_to_chinese(question)['trans_result'][0]['dst']
				target_data['data'][ai]['paragraphs'][pi]['qas'][qi]['question'] = question
				
				for ani, answer in enumerate(qa['answers']):
					answer_text = answer['text']
					answer_text = translate_to_chinese(answer_text)['trans_result'][0]['dst']
					target_data['data'][ai]['paragraphs'][pi]['qas'][qi]['answers'][ani]['text'] = answer_text
					
		print('saving ...' + "{}-v1.1.json".format(data_type))
		save(args, target_data, out_name)
	
# something wrong with conbine
def conbine():
	x = json.load(open('dev-v1.1-before.json', encoding='utf-8'))
	y = json.load(open('dev-v1.1-after.json', encoding='utf-8'))
	target_data = y
	for i in range(0, 33):
		if i < 33:
			target_data['data'][i] = x['data'][i]
	json.dump(target_data, open('dev-v1.1.json', 'w'))

def main():
	args = get_args()
#	args.source_dir = 'D:/wuzhijing/resp/QA_demo/zhijing_test/data'
	prepro(args)
	
	
if __name__ == '__main__':
#	conbine()
	main()
#	file_path = 'D:/wuzhijing/resp/QA_demo/zhijing_test/data/dev-v1.1.json'
#	txt = "HI, HOW ARE YOU"
#	txt = open(file_path,'r',encoding='utf-8').read()
#	translate_to_chinese(txt)
	