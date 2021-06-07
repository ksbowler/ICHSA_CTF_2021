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

def modifyXor(d):
	if len(d) == 0: return ""
	x = len(d)//2 + 1
	ret = ""
	for i in range(0,len(d),2):
		#print("xor",x,x-1-(i//2))
		t = int(d[i:i+2],16)^x^(x-1-(i//2))
		t = hex(t)[2:]
		if len(t) == 1: t = "0"+t
		ret += t
	#print("ret:",ret)
	return ret
		
	
#HOSTはIPアドレスでも可
HOST, PORT = "poodle1.ichsa.ctf.today", 8003
s, f = sock(HOST, PORT)
for _ in range(5): read_until(f)
enc = read_until(f).strip()
print("enc:",enc)
for _ in range(5): read_until(f)

d2 = ""
dec2 = ""

for j in range(16):
	print(j)
	#print(":",read_until(f))
	#read_until(f,">> ")
	hen = True
	for i in range(256):
		read_until(f)
		read_until(f,">> ")
		h = hex(i)[2:]
		#print("h:",h)
		if len(h) == 1: h = "0"+h
		print("h:",h)
		mes = enc[:32] + "00"*(15-j)+ h + modifyXor(d2) + enc[64:]
		#print("mes:",mes)
		assert len(mes) == 96
		s.send(mes.encode()+b"\n")
		recv_m = read_until(f).strip()
		print(recv_m)
		if "mmm" in recv_m:
			hen = False
			print("Find!")
			d2 = h + d2
			t = i^(j+1)
			t = hex(t)[2:]
			if len(t) == 1: t = "0"+t
			dec2 = t + dec2
			break
	if hen:
		print("okashii")
		break
			

p2 = long_to_bytes(int(dec2,16)^int(enc[32:64],16))
print(p2)
d1 = ""
dec1 = ""

for j in range(16):
	print(j)
	hen = True
	for i in range(256):
		read_until(f)
		read_until(f,">> ")
		h = hex(i)[2:]
		#print("h:",h)
		if len(h) == 1: h = "0"+h
		print("h:",h)
		mes = "00"*(15-j)+ h + modifyXor(d1) + enc[32:64]
		#print("mes:",mes)
		assert len(mes) == 64
		s.send(mes.encode()+b"\n")
		recv_m = read_until(f).strip()
		print(recv_m)
		if "mmm" in recv_m:
			hen = False
			print("Find!")
			d1 = h + d1
			t = i^(j+1)
			t = hex(t)[2:]
			if len(t) == 1: t = "0"+t
			dec1 = t + dec1
			break
	if hen:
		print("okashii")
		break
p1 = long_to_bytes(int(dec1,16)^int(enc[:32],16))
print(p1)
print(p1+p2)
 
#read_untilの使い方
#返り値があるのでprintするか、何かの変数に入れる
#1行読む：read_until(f)
#特定の文字まで読む：read_until(f,"input")
#配列に格納する：recv_m = read_until(f).split() or .strip()

#サーバーに何か送るとき
#s.send(b'1\n') : 1を送っている
#バイト列で送ること。str->bytesにするには、変数の後に.encode()
#必ず改行を入れること。終了ポイントが分からなくなる。ex) s.send(flag.encode() + b'\n')

