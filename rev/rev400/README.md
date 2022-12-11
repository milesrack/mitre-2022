# rev400

## Description
Think you can reverse engineer the password…

http://44.197.231.105:3008

## Solve
Download the file at http://44.197.231.105:3008/rev400_2

First I opened the binary in ghidra and looked at the main function:
```c
int main(int argc,char **argv)

{
  size_t password_len;
  
  if (argc == 2) {
    password_len = strlen(argv[1]);
    if (password_len == 45) {
      challenge(argv[1]);
    }
    else {
      puts("Error: Wrong input string size!");
    }
    return 0;
  }
  printf("\n Usage %s INPUT\n",*argv);
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```

The program is checking that our program has two arguments (`argv[0]` is the program name and `argv[1]` is the argument we pass). Then it checks that the length of our argument is 45 characters and calls the `challenge()` function.

Now let's take a look at the `challenge()` function:
```c
int challenge(char *password)

{
  size_t password_len;
  int iVar1;
  char hash_string [65];
  uint8_t hash [32];
  uint8_t password_mem [46];
  int i;
  
  i = 0;
  while( true ) {
    if (0x2c < i) {
      puts("Correct :)");
                    /* WARNING: Subroutine does not return */
      exit(0);
    }
    memset(password_mem,0,0x2e);
    memcpy(password_mem,password,i + 1);
    password_len = strlen((char *)password_mem);
    calc_sha_256(hash,password_mem,password_len);
    hash_to_string(hash_string,hash);
    iVar1 = strcmp(hash_string,(char *)hash_keys[i]);
    if (iVar1 != 0) break;
    i = i + 1;
  }
  puts("Wrong :(");
                    /* WARNING: Subroutine does not return */
  exit(1);
}
```

This function initializes a counter: `i`. The function will run until 0x2c (44) is less than i (so 45 iterations). On each iteration, it copies `i` number of bytes from our input into memory. Then the `calc_sha_256()` function creates a SHA256 hash of the value in memory and copies it to `hash`. `hash_to_string()` will then store the string value of `hash` in `string_hash`. Finally, the `string_hash` is compared to `hash_keys[i]`.

The `hash_keys[]` array stores the correct hash for each iteration. We cannot brute force these hashes individually since the hash builds on the last iteration. Figuring out the correct input values at each iteration will ultimately give us the flag.

I wrote this python script to solve the challenge:
```python
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
```

## Flag
```
MCA{1ccb4978a9ec500fe1d4d2e6e6aa0a31f3fa6f97}
```