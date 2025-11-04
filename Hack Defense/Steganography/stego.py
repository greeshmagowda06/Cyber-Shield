# stego/stego.py
from PIL import Image
import sys

def encode(infile, outfile, message):
    img = Image.open(infile)
    data = list(img.getdata())
    bits = ''.join(f"{ord(c):08b}" for c in message) + "00000000"
    if len(bits) > len(data)*3:
        raise ValueError("Message too long")
    new=[]
    bi=0
    for pixel in data:
        r,g,b = pixel[:3]
        if bi < len(bits):
            r = (r & ~1) | int(bits[bi]); bi+=1
        if bi < len(bits):
            g = (g & ~1) | int(bits[bi]); bi+=1
        if bi < len(bits):
            b = (b & ~1) | int(bits[bi]); bi+=1
        new.append((r,g,b))
    img.putdata(new)
    img.save(outfile)
    print("Saved",outfile)

def decode(infile):
    img = Image.open(infile)
    data = list(img.getdata())
    bits=''
    for r,g,b in data:
        bits += str(r&1)+str(g&1)+str(b&1)
    chars = [bits[i:i+8] for i in range(0,len(bits),8)]
    msg=''
    for c in chars:
        ch = chr(int(c,2))
        if ch == '\x00': break
        msg+=ch
    print("Decoded:", msg)

if __name__=="__main__":
    if sys.argv[1]=="encode":
        encode(sys.argv[2], sys.argv[3], sys.argv[4])
    else:
        decode(sys.argv[2])