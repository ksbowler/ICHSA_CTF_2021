from Crypto.Util.number import *
from functools import reduce
from operator import mul
from itertools import combinations
import sys
import socket, struct, telnetlib

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
HOST, PORT = "baby_homework.ichsa.ctf.today", 8010
flag = ""
"""
while True:
	#s, f = sock(HOST, PORT)
	for i in range(48,126):
		print(i,chr(i))
		s, f = sock(HOST, PORT)
		read_until(f)
		mes = "0"*(16-len(flag)-1) + flag+ chr(i) + "0"*(16-len(flag)-1) 
		s.send(mes.encode()+b"\n")
		m = read_until(f).strip()
		#print(m)
		#print(m[:32])
		#print(m[32:64])
		assert len(m) >= 64
		s.close()
		if m[:32] == m[32:64]:
			flag += chr(i)
			print(flag)
			break
"""
flag = "d0n7_7ruzt_DeF4u"
while True:
	isfin = True
	for i in range(48,126):
		print(i,chr(i))
		s, f = sock(HOST, PORT)
		read_until(f)
		mes = "0"*(16-(len(flag)%16)-1)	+ flag + chr(i) + "0"*(16-(len(flag)%16)-1)
		s.send(mes.encode()+b"\n")
		m = read_until(f).strip()
		s.close()
		if m[32:64] == m[96:128]:
			isfin = False
			flag += chr(i)
			print(flag,len(flag))
			break
	if isfin: break
print("ICHSA_CTF{"+flag+"}")

	

#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

