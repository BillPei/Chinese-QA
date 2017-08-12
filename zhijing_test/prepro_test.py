import json
from tqdm import tqdm
from collections import Counter
import nltk
import re
import jieba

#source_path = "D:/wuzhijing/resp/QA_demo/data/squad/dev-v1.1.json"
source_path = "D:/wuzhijing/resp/QA_demo/zhijing_test/data/train-v1.1.json"
source_data = json.load(open(source_path,'r',encoding='utf-8'))

q, cq, y, rx, rcx, ids, idxs = [], [], [], [], [], [], []
cy = []
x, cx = [], []
answerss = []
p = []
word_counter, char_counter, lower_word_counter = Counter(), Counter(), Counter()

start_ratio=0.0
stop_ratio=1.0
start_ai = int(round(len(source_data['data']) * start_ratio))
stop_ai = int(round(len(source_data['data']) * stop_ratio))

sent_tokenize = nltk.sent_tokenize
def word_tokenize(tokens):
#	return [token.replace("''", '"').replace("``", '"') for token in jieba.lcut(tokens, cut_all=False)]
	return [token.replace("''", '"').replace("``", '"') for token in nltk.word_tokenize(tokens)]

#from my.corenlp_interface import CoreNLPInterface
#url = 'vision-server2.corp.ai2'
#port = 8000
#interface = CoreNLPInterface(url, port)
#sent_tokenize = interface.split_doc
#word_tokenize = interface.split_sent


def process_tokens(temp_tokens):
    tokens = []
    for token in temp_tokens:
        flag = False
        l = ("-", "\u2212", "\u2014", "\u2013", "/", "~", '"', "'", "\u201C", "\u2019", "\u201D", "\u2018", "\u00B0")
        # \u2013 is en-dash. Used for number to nubmer
        # l = ("-", "\u2212", "\u2014", "\u2013")
        # l = ("\u2013",)
        tokens.extend(re.split("([{}])".format("".join(l)), token))
    return tokens

def get_2d_spans(text, tokenss):
    spanss = []
    cur_idx = 0
    for tokens in tokenss:
        spans = []
        for token in tokens:
            if text.find(token, cur_idx) < 0:
                print(tokens)
                print("{} {} {}".format(token, cur_idx, text))
                raise Exception()
            cur_idx = text.find(token, cur_idx)
            spans.append((cur_idx, cur_idx + len(token)))
            cur_idx += len(token)
        spanss.append(spans)
#    print('spanss')
 #   print(spanss)
    return spanss

def get_word_span(context, wordss, start, stop):
    spanss = get_2d_spans(context, wordss)
    idxs = []
    for sent_idx, spans in enumerate(spanss):
        for word_idx, span in enumerate(spans):
            if not (stop <= span[0] or start >= span[1]):
                idxs.append((sent_idx, word_idx))
                print('here')
                print(spanss[sent_idx][word_idx])

    assert len(idxs) > 0, "{} {} {} {}".format(context, spanss, start, stop)
    return idxs[0], (idxs[-1][0], idxs[-1][1] + 1)

def get_word_idx(context, wordss, idx):
    spanss = get_2d_spans(context, wordss)
    return spanss[idx[0]][idx[1]][0]

for ai, article in enumerate(tqdm(source_data['data'][start_ai:1])):
	print(ai)

	xp, cxp = [], []
	pp = []
	x.append(xp)
	cx.append(cxp)
	p.append(pp)
	for pi, para in enumerate(article['paragraphs']):
		# wordss
		print(pi)
		context = para['context']
		context = context.replace("''", '" ')
		context = context.replace("``", '" ')
		# context = context.encode('utf-8')
		
		table = {ord(f):ord(t) for f,t in zip(
		'，。！？【】（）％＃＠＆１２３４５６７８９０',
		',.!?[]()%#@&1234567890')}
		context = context.translate(table)
		
		print(context)
		xi = list(map(word_tokenize, sent_tokenize(context)))
		print('xi')
		print(xi)
		xi = [process_tokens(tokens) for tokens in xi]  # process tokens
		print('xi')
		print(xi)
		# given xi, add chars
		cxi = [[list(xijk) for xijk in xij] for xij in xi]
		print(cxi)
		print(context)
		xp.append(xi)
		cxp.append(cxi)
		pp.append(context)


		for xij in xi:
			for xijk in xij:
				word_counter[xijk] += len(para['qas'])
				lower_word_counter[xijk.lower()] += len(para['qas'])
				for xijkl in xijk:
					char_counter[xijkl] += len(para['qas'])


		rxi = [ai, pi]
		assert len(x) - 1 == ai
		assert len(x[ai]) - 1 == pi
		for qa in para['qas']:
# get words
			qi = word_tokenize(qa['question'])
			cqi = [list(qij) for qij in qi]
#			print(qi)     ###################333333
#			print(cqi) #############3333333333333333333
			yi = []
			cyi = []
			answers = []
#			print(len(qa['answers']))
			for answer in qa['answers']:
				answer_text = answer['text']
				answers.append(answer_text)
				answer_start = answer['answer_start']
				answer_stop = answer_start + len(answer_text)
# TODO : put some function that gives word_start, word_stop here
				print('abcde@@@@@@@@@@@@@')
				yi0, yi1 = get_word_span(context, xi, answer_start, answer_stop)
#				print(yi0) ########################
#				print(yi1) ######################
                    # yi0 = answer['answer_word_start'] or [0, 0]
                    # yi1 = answer['answer_word_stop'] or [0, 1]
				assert len(xi[yi0[0]]) > yi0[1]
				assert len(xi[yi1[0]]) >= yi1[1]
				w0 = xi[yi0[0]][yi0[1]]
				w1 = xi[yi1[0]][yi1[1]-1]
				i0 = get_word_idx(context, xi, yi0)
				i1 = get_word_idx(context, xi, (yi1[0], yi1[1]-1))
				cyi0 = answer_start - i0
				cyi1 = answer_stop - i1 - 1
#				print('w0 ' + w0)
#				print('w1 ' + w1)
#				print('i0 ' + str(i0))
#				print('i1 ' + str(i1))
#				print(cyi0)
#				print(cyi1)
                    # print(answer_text, w0[cyi0:], w1[:cyi1+1])
				assert answer_text[0] == w0[cyi0], (answer_text, w0, cyi0)
				assert answer_text[-1] == w1[cyi1]
				assert cyi0 < 32, (answer_text, w0)
				assert cyi1 < 32, (answer_text, w1)

				yi.append([yi0, yi1])
				cyi.append([cyi0, cyi1])

			for qij in qi:
				word_counter[qij] += 1
				lower_word_counter[qij.lower()] += 1
				for qijk in qij:
					char_counter[qijk] += 1

			q.append(qi)
			cq.append(cqi)
			y.append(yi)
			cy.append(cyi)
			rx.append(rxi)
			rcx.append(rxi)
			ids.append(qa['id'])
			idxs.append(len(idxs))
			answerss.append(answers)

