# rev300

## Description
Think you can reverse engineer the password this time…

http://44.197.231.105:3007

## Solve
Our binary is at the url http://44.197.231.105:3007/rev300
```bash
user@arch:~/cyber/ctf/mitre-2022/rev/rev300$ ./rev300 
Usage ././rev300 INPUT
user@arch:~/cyber/ctf/mitre-2022/rev/rev300$ ./rev300 letmein
Error: Wrong input string size!
user@arch:~/cyber/ctf/mitre-2022/rev/rev300$ 
```

I'll open the file in GDB to start debugging:
```bash
gdb ./rev300
```

We also need to set an argument before we run the program
```bash
gef➤  set args ABCDEF
```

Now let's take a look at available functions:
```as
gef➤  info func
All defined functions:

File decode.c:
22:	unsigned char *b64_decode(const char *, size_t);
27:	unsigned char *b64_decode_ex(const char *, size_t, size_t *);

File encode.c:
21:	char *b64_encode(const unsigned char *, size_t);

File rev300.c:
12:	int bytes2hexstr(uint8_t *, size_t, uint8_t *, size_t);
28:	int challenge(char *);
46:	int main(int, char **);
...
```
Only these 3 functions look relevant to the challenge, the rest is standard parts of a binary.

First I will look into the `main()` function:
```as
gef➤  disassemble main
Dump of assembler code for function main:
   0x08048778 <+0>:	lea    ecx,[esp+0x4]
   0x0804877c <+4>:	and    esp,0xfffffff0
   0x0804877f <+7>:	push   DWORD PTR [ecx-0x4]
   0x08048782 <+10>:	push   ebp
   0x08048783 <+11>:	mov    ebp,esp
   0x08048785 <+13>:	push   ebx
   0x08048786 <+14>:	push   ecx
   0x08048787 <+15>:	mov    ebx,ecx
   0x08048789 <+17>:	cmp    DWORD PTR [ebx],0x2 // Making sure we have an argument
   0x0804878c <+20>:	jne    0x80487cf <main+87> // If we do not give an argument jump to the error message
   0x0804878e <+22>:	mov    eax,DWORD PTR [ebx+0x4] // Load address our arguments into eax
   0x08048791 <+25>:	add    eax,0x4 // Add 4 to the address to get the second argument (the password)
   0x08048794 <+28>:	mov    eax,DWORD PTR [eax] // Move the actual value of this password into eax
   0x08048796 <+30>:	sub    esp,0xc
   0x08048799 <+33>:	push   eax // Push eax onto the stack for the strlen() function
   0x0804879a <+34>:	call   0x80484f0 <strlen@plt>
   0x0804879f <+39>:	add    esp,0x10
   0x080487a2 <+42>:	cmp    eax,0x2d // Compare the string length to 0x2d (45 in denary)
   0x080487a5 <+45>:	jne    0x80487bd <main+69> // Jump to an error message if the length is wrong
   0x080487a7 <+47>:	mov    eax,DWORD PTR [ebx+0x4] // Load address our arguments into eax
   0x080487aa <+50>:	add    eax,0x4 // Add 4 to the address to get the second argument (the password)
   0x080487ad <+53>:	mov    eax,DWORD PTR [eax] // Move the actual value of this password into eax
   0x080487af <+55>:	sub    esp,0xc
   0x080487b2 <+58>:	push   eax // Loading the argument onto the stack for the challenge() function
   0x080487b3 <+59>:	call   0x80486e4 <challenge> // Calls the challenge() function
   0x080487b8 <+64>:	add    esp,0x10
   0x080487bb <+67>:	jmp    0x80487ef <main+119>
   0x080487bd <+69>:	sub    esp,0xc // From here until <main+85> prints the "Error: Wrong input string size!" and exits
   0x080487c0 <+72>:	push   0x8048f38
   0x080487c5 <+77>:	call   0x80484d0 <puts@plt>
   0x080487ca <+82>:	add    esp,0x10
   0x080487cd <+85>:	jmp    0x80487ef <main+119>
   0x080487cf <+87>:	mov    eax,DWORD PTR [ebx+0x4] // From here until <main+114> the program will print the error for no argument and exit
   0x080487d2 <+90>:	mov    eax,DWORD PTR [eax]
   0x080487d4 <+92>:	sub    esp,0x8
   0x080487d7 <+95>:	push   eax
   0x080487d8 <+96>:	push   0x8048f58
   0x080487dd <+101>:	call   0x80484a0 <printf@plt>
   0x080487e2 <+106>:	add    esp,0x10
   0x080487e5 <+109>:	sub    esp,0xc
   0x080487e8 <+112>:	push   0x1
   0x080487ea <+114>:	call   0x80484e0 <exit@plt> // Exit the program
   0x080487ef <+119>:	mov    eax,0x0
   0x080487f4 <+124>:	lea    esp,[ebp-0x8]
   0x080487f7 <+127>:	pop    ecx
   0x080487f8 <+128>:	pop    ebx
   0x080487f9 <+129>:	pop    ebp
   0x080487fa <+130>:	lea    esp,[ecx-0x4]
   0x080487fd <+133>:	ret    
End of assembler dump.
```

Now we know the input must be 45 characters long. The rest of the validation is done in `challenge()` so lets dissasemble this function:
```as
gef➤  disassemble challenge
Dump of assembler code for function challenge:
   0x080486e4 <+0>:		push   ebp
   0x080486e5 <+1>:		mov    ebp,esp
   0x080486e7 <+3>:		sub    esp,0x78
   0x080486ea <+6>:		sub    esp,0x4
   0x080486ed <+9>:		push   0x64
   0x080486ef <+11>:	push   0x0
   0x080486f1 <+13>:	lea    eax,[ebp-0x6c]
   0x080486f4 <+16>:	push   eax
   0x080486f5 <+17>:	call   0x8048510 <memset@plt>
   0x080486fa <+22>:	add    esp,0x10
   0x080486fd <+25>:	push   0x5a
   0x080486ff <+27>:	lea    eax,[ebp-0x6c]
   0x08048702 <+30>:	push   eax
   0x08048703 <+31>:	push   0x2d
   0x08048705 <+33>:	push   DWORD PTR [ebp+0x8]
   0x08048708 <+36>:	call   0x804867d <bytes2hexstr>
   0x0804870d <+41>:	add    esp,0x10
   0x08048710 <+44>:	sub    esp,0xc
   0x08048713 <+47>:	lea    eax,[ebp-0x6c]
   0x08048716 <+50>:	push   eax
   0x08048717 <+51>:	call   0x80484f0 <strlen@plt>
   0x0804871c <+56>:	add    esp,0x10
   0x0804871f <+59>:	sub    esp,0x8
   0x08048722 <+62>:	push   eax
   0x08048723 <+63>:	lea    eax,[ebp-0x6c]
   0x08048726 <+66>:	push   eax
   0x08048727 <+67>:	call   0x8048b7c <b64_encode>
   0x0804872c <+72>:	add    esp,0x10
   0x0804872f <+75>:	sub    esp,0x8
   0x08048732 <+78>:	push   eax
   0x08048733 <+79>:	push   0x8048ea8
   0x08048738 <+84>:	call   0x8048490 <strcmp@plt>
   0x0804873d <+89>:	add    esp,0x10
   0x08048740 <+92>:	test   eax,eax
   0x08048742 <+94>:	jne    0x804875e <challenge+122>
   0x08048744 <+96>:	sub    esp,0xc
   0x08048747 <+99>:	push   0x8048f21
   0x0804874c <+104>:	call   0x80484d0 <puts@plt>
   0x08048751 <+109>:	add    esp,0x10
   0x08048754 <+112>:	sub    esp,0xc
   0x08048757 <+115>:	push   0x0
   0x08048759 <+117>:	call   0x80484e0 <exit@plt>
   0x0804875e <+122>:	sub    esp,0xc
   0x08048761 <+125>:	push   0x8048f2c
   0x08048766 <+130>:	call   0x80484d0 <puts@plt>
   0x0804876b <+135>:	add    esp,0x10
   0x0804876e <+138>:	sub    esp,0xc
   0x08048771 <+141>:	push   0x1
   0x08048773 <+143>:	call   0x80484e0 <exit@plt>
End of assembler dump.
```
There is a string comparison at `0x08048738` so I will set a breakpoint here and run the code:
```as
gef➤  b *challenge+84
Note: breakpoint 1 also set at pc 0x8048738.
Breakpoint 2 at 0x8048738: file rev300.c, line 35.
gef➤  r
[ Legend: Modified register | Code | Heap | Stack | String ]
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── registers ────
$eax   : 0x804c1a0  →  "NDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxND[...]"
$ebx   : 0xffffd790  →  0x00000002
$ecx   : 0x0       
$edx   : 0x804c1a0  →  "NDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxND[...]"
$esp   : 0xffffd6d0  →  0x8048ea8  →  "NGQ0MzQxN2I2MTM2MzEzMDY0NjI2MzM0NjUzNDYyMzYzMTM2Mz[...]"
$ebp   : 0xffffd758  →  0xffffd778  →  0x00000000
$esi   : 0x8048dc0  →  <__libc_csu_init+0> endbr32 
$edi   : 0xf7ffcb80  →  0x00000000
$eip   : 0x8048738  →  <challenge+84> call 0x8048490 <strcmp@plt>
$eflags: [zero carry PARITY ADJUST SIGN trap INTERRUPT direction overflow resume virtualx86 identification]
$cs: 0x23 $ss: 0x2b $ds: 0x2b $es: 0x2b $fs: 0x00 $gs: 0x63 
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── stack ────
0xffffd6d0│+0x0000: 0x8048ea8  →  "NGQ0MzQxN2I2MTM2MzEzMDY0NjI2MzM0NjUzNDYyMzYzMTM2Mz[...]"	 ← $esp
0xffffd6d4│+0x0004: 0x804c1a0  →  "NDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxND[...]"
0xffffd6d8│+0x0008: 0xffffd6ec  →  "41414141414141414141414141414141414141414141414141[...]"
0xffffd6dc│+0x000c: 0x00005a ("Z"?)
0xffffd6e0│+0x0010: 0xffffd720  →  "4141414141414141414141414141414141414"
0xffffd6e4│+0x0014: 0xf7ffdbf8  →  0xf7ffdb8c  →  0xf7fc06d0  →  0xf7ffda20  →  0x00000000
0xffffd6e8│+0x0018: 0xf7fc0700  →  0x8048347  →  "GLIBC_2.0"
0xffffd6ec│+0x001c: "41414141414141414141414141414141414141414141414141[...]"
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── code:x86:32 ────
    0x804872f <challenge+75>   sub    esp, 0x8
    0x8048732 <challenge+78>   push   eax
    0x8048733 <challenge+79>   push   0x8048ea8
 →  0x8048738 <challenge+84>   call   0x8048490 <strcmp@plt>
   ↳   0x8048490 <strcmp@plt+0>   jmp    DWORD PTR ds:0x804b00c
       0x8048496 <strcmp@plt+6>   push   0x0
       0x804849b <strcmp@plt+11>  jmp    0x8048480
       0x80484a0 <printf@plt+0>   jmp    DWORD PTR ds:0x804b010
       0x80484a6 <printf@plt+6>   push   0x8
       0x80484ab <printf@plt+11>  jmp    0x8048480
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────── arguments (guessed) ────
strcmp@plt (
   [sp + 0x0] = 0x8048ea8 → "NGQ0MzQxN2I2MTM2MzEzMDY0NjI2MzM0NjUzNDYyMzYzMTM2Mz[...]",
   [sp + 0x4] = 0x804c1a0 → "NDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxNDE0MTQxND[...]",
   [sp + 0x8] = 0xffffd6ec → "41414141414141414141414141414141414141414141414141[...]",
   [sp + 0xc] = 0x00005a,
   [sp + 0x10] = 0xffffd720 → "4141414141414141414141414141414141414",
   [sp + 0x14] = 0xf7ffdbf8 → 0xf7ffdb8c → 0xf7fc06d0 → 0xf7ffda20 → 0x00000000,
   [sp + 0x18] = 0xf7fc0700 → 0x8048347 → "GLIBC_2.0",
   [sp + 0x1c] = 0x31343134,
   [sp + 0x20] = 0x31343134,
   [sp + 0x24] = 0x31343134,
   [sp + 0x28] = 0x31343134,
   [sp + 0x2c] = 0x31343134,
   [sp + 0x30] = 0x31343134,
   [sp + 0x34] = 0x31343134,
   [sp + 0x38] = 0x31343134
)
───────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── threads ────
[#0] Id 1, Name: "rev300", stopped 0x8048738 in challenge (), reason: BREAKPOINT
─────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────── trace ────
[#0] 0x8048738 → challenge(input_str=0xffffda11 'A' <repeats 45 times>)
[#1] 0x80487b8 → main(argc=0x2, argv=0xffffd844)
──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────────
gef➤  
```
The address `0x8048ea8` is storing an interesting base64 string... lets output its value
```as
gef➤  x/s 0x8048ea8
0x8048ea8:	"NGQ0MzQxN2I2MTM2MzEzMDY0NjI2MzM0NjUzNDYyMzYzMTM2Mzk2NTYzMzkzNTYxNjQzNTY1NjYzMjYxNjY2NTYxMzIzMTMwMzkzNzM0MzQzNzMyMzIzNjc="
gef➤  
```
I'll decode this in the command line to see what it's value is
```bash
user@arch:~$ echo "NGQ0MzQxN2I2MTM2MzEzMDY0NjI2MzM0NjUzNDYyMzYzMTM2Mzk2NTYzMzkzNTYxNjQzNTY1NjYzMjYxNjY2NTYxMzIzMTMwMzkzNzM0MzQzNzMyMzIzNjc=" | base64 -d
4d43417b613631306462633465346236313639656339356164356566326166656132313039373434373232367user@arch:~$
```
From reading the function names we know the input is being turned into hex -> base64 and then compared to the string. So all that's left is to decode this hex.
```
user@arch:~$ python -c "print(bytes.fromhex('4d43417b613631306462633465346236313639656339356164356566326166656132313039373434373232367d'))"
b'MCA{a610dbc4e4b6169ec95ad5ef2afea21097447226}'
```
*I had to add `d` to the end of the hex since it was missing the last hex character*

## Flag
```
MCA{a610dbc4e4b6169ec95ad5ef2afea21097447226}
```