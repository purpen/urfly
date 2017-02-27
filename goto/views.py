# -*- coding: utf-8 -*-

from django.http import Http404
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.urls import reverse

from .models import Linklib
from .forms import LinkForm
# 哈希库
import hashlib

code_map = (
		'a' , 'b' , 'c' , 'd' , 'e' , 'f' , 'g' , 'h' ,
        'i' , 'j' , 'k' , 'l' , 'm' , 'n' , 'o' , 'p' ,
        'q' , 'r' , 's' , 't' , 'u' , 'v' , 'w' , 'x' ,
        'y' , 'z' , '0' , '1' , '2' , '3' , '4' , '5' ,
        '6' , '7' , '8' , '9' , 'A' , 'B' , 'C' , 'D' ,
        'E' , 'F' , 'G' , 'H' , 'I' , 'J' , 'K' , 'L' ,
        'M' , 'N' , 'O' , 'P' , 'Q' , 'R' , 'S' , 'T' ,
        'U' , 'V' , 'W' , 'X' , 'Y' , 'Z'
	)


def jump(request, skey):
	'''实现短链接中间跳转'''
	result = get_object_or_404(Linklib, skey=skey)

	return HttpResponse('跳转至： %s' % result.link)


def index(request):
	'''短链接生成页'''
	form = LinkForm()
	return render(request, 'index.html', {'form': form})


def build(request):
	'''生成唯一key,保存对应关系记录'''
	link = request.POST['link']
	skeys = get_hash_key(link)
	# 选择第一个元素作为key
	skey = skeys[0]
	# 保存记录
	linklib = Linklib(skey=skey,link=link)
	linklib.save()

	# 生成短链接
	short_url = 'http://urfly.cn/%s' % skey

	return render(request, 'index.html', {'short_url': short_url, 'link': link})


def get_hash_key(link):
	'''为了让结果更加随机，把每次循环没有使用的第二个bit保存到e里面，这样可以让结果冲突率更小'''
	skeys = []
	hex = get_md5(link)
	for i in range(0, 4):
		n = int(hex[i*8:(i+1)*8], 16)
		v = []
		e = 0
		for j in range(0, 5):
			x = 0x0000003D & n
			e |= ((0x00000002 & n) >> 1) << j
			v.insert(0, code_map[x])
			n = n >> 6
		e |= n << 5
		v.insert(0, code_map[e & 0x0000003D])
		skeys.append(''.join(v))

	return skeys


def get_md5(s):
	'''防止hash值被破解，在生成md5值 '''
	s = s.encode('utf8')

	m = hashlib.md5()
	m.update(s)

	return m.hexdigest()

