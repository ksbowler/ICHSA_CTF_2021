from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib
import base64

# --- common funcs ---
def sock(remoteip, remoteport):
	s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	s.connect((remoteip, remoteport))
	return s, s.makefile('rw')

def read_until(f, delim='\n'):
	data = ''
	while not data.endswith(delim):
		data += f.read(1)
	return data

	
#HOSTはIPアドレスでも可
HOST, PORT = "crime.ichsa.ctf.today", 8008
s, f = sock(HOST, PORT)
for _ in range(3): read_until(f)
#flag = "ICHSA_CTF{compressinh"
#flag = "ICHSA_CTF{compressing_sec"
flag = "ICHSA_CTF{compressing_secret_with_inp"
candi = "abcdefghijklmnopqrstuvwxyz_}"
while True:
	"""
	read_until(f,"Your input: ")
	#mes = flag + "??"
	mes = flag + "?"
	s.send(mes.encode()+b"\n")
	m = read_until(f).strip()
	read_until(f)
	m = base64.b64decode(m.encode())
	print("?",len(m))
	ans = "?"
	ans_len = len(m)
	"""
	ans = ""
	for c1 in candi:
		#for c2 in candi:
		read_until(f,"Your input: ")
		#mes = flag + c1 + c2
		mes = flag + c1
		s.send(mes.encode()+b"\n")
		m = read_until(f).strip()
		read_until(f)
		print(c1)
		print("before:",m)
		m = base64.b64decode(m.encode())
		print(" after:",m)
		#print(c1+c2,len(m))
		print(len(m))
		print()
		if len(m) == 95:
			print("update!")
			ans_len = len(m)
			ans = c1
	print("flag update!!")
	flag += ans
	print(flag)
	if "}" in ans: break
		

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

