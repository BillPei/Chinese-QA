# create by zhijing 2017-08-10
# this is a test code for using word2vec

#coding:utf-8
import jieba
import sys
import os
import word2vec as w2v
from tqdm import tqdm
import time

def preset(in_filepath, out_filepath):
	fin = open(in_filepath, 'r', encoding='utf-8')
	fout = open(out_filepath, 'w', encoding='utf-8')
	context = fin.read()
	
	#context = delete_punctuation(context)
	context = cut_word(context)

	fout.write(context)
	fin.close()
	fout.close()
	print('zhijing: the context has been deleted punctuation and word by word successfully...')

def delete_punctuation(context):
	table = {ord(f):ord(t) for f,t in zip('，。！？', '    ')}
	context = context.translate(table)
	return context
	
def cut_word(context):
	context = jieba.cut(context, cut_all=False)
	context = " ".join(context)
	return context
	
def create_dictionary():
	bin_file = 'text.bin'
	modle = w2v.load(bin_file)

if __name__ == '__main__':
	# 对原始段落进行 去标点 分词 操作
	if sys.argv[1] == 'preset':
		in_filepath = 'text.txt'
		out_filepath = 'test_words.txt'
		preset(in_filepath, out_filepath)
		
	# 训练词序列，得到word到vector的映射
	elif sys.argv[1] == 'train':
		in_origin = 'test_words.txt'
		out_phrase = 'phrases.txt'
		# larger and equal than preset action, addin g delete repeted white space
		w2v.word2phrase(in_origin, out_phrase, verbose=True)
		out_bin = 'text.bin'
		w2v.word2vec(out_phrase, out_bin, 100, verbose=True)
		out_cluster = 'clusters.txt'
		w2v.word2clusters(out_bin, out_cluster, 100, verbose=True)
	
	# 使用生成的bin文件，生成中文glove文件
	elif sys.argv[1] == 'create_glove':
		import word2vec as w2v
		bin_file = 'text.bin'
		model = w2v.load(bin_file)
		words = model.vocab
		num, size = model.vectors.shape
		
		glove = 'glove.{}.{}d.txt'.format(num-2,size)
		if(os.path.exists(glove)):
			os.remove(glove)
		with open(glove, 'a', encoding='utf-8') as fh:
			for word in tqdm(words[1:], total=num-1):
	#			time.sleep(0.5)
				vec = word + " " + " ".join(str(i) for i in list(model[word])) + '\n'
	#			print(vec)
				fh.write(vec)
		
		
		