import pwn
import hashlib
import string

hash_addresses = [0x0804b060, 0x0804b0a1, 0x0804b0e2, 0x0804b123, 0x0804b164, 0x0804b1a5, 0x0804b1e6, 0x0804b227, 0x0804b268, 0x0804b2a9, 0x0804b2ea, 0x0804b32b, 0x0804b36c, 0x0804b3ad, 0x0804b3ee, 0x0804b42f, 0x0804b470, 0x0804b4b1, 0x0804b4f2, 0x0804b533, 0x0804b574, 0x0804b5b5, 0x0804b5f6, 0x0804b637, 0x0804b678, 0x0804b6b9, 0x0804b6fa, 0x0804b73b, 0x0804b77c, 0x0804b7bd, 0x0804b7fe, 0x0804b83f, 0x0804b880, 0x0804b8c1, 0x0804b902, 0x0804b943, 0x0804b984, 0x0804b9c5, 0x0804ba06, 0x0804ba47, 0x0804ba88, 0x0804bac9, 0x0804bb0a, 0x0804bb4b, 0x0804bb8c, 0x0804bbcd, 0x0804bc0e, 0x0804bc4f, 0x0804bc90]
hash_keys = []
chars = string.ascii_letters + string.digits + "{" + "}"
flag = ""

def sha256(pt):
	m = hashlib.sha256()
	m.update(pt.encode())
	return m.hexdigest()


e = pwn.ELF("./rev400_2")
p = pwn.process("./rev400_2")

for address in hash_addresses:
	hash_ = e.read(address, 64).decode()
	if hash_ != "\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00":
		hash_keys.append(hash_)

for h in hash_keys:
	for c in chars:
		if sha256(flag + c) == h:
			flag += c
print(flag)