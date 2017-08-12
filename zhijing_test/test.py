table = {ord(f):ord(t) for f,t in zip('，。！？（）％＃＠＆１２３４５６７８９０',',.!?()%#@&1234567890')}
context = 'aaa'
print('beforre: ' + context)

context = context.translate(table)
print('after: ' + context)