# rev200

## Description
Think you can reverse engineer the password…

http://44.197.231.105:3006

## Solve
The file http://44.197.231.105:3006/rev200 shows up in the directory listing. I'll download this to my machine and take a look...

The program takes a command line argument `PASSWORD`. This is doing a string comparison against the password.

I will use a program called `ltrace` to run the program and it will show me library calls the application is making:
```bash
user@arch:~/cyber/ctf/mitre-2022/rev/rev200$ ltrace ./rev200 AAAAAAAAAAAA
__libc_start_main(0x80487d8, 2, 0xff84bb14, 0x8049ba0 <unfinished ...>
strcmp("AAAAAAAAAAAA", "23_15_fun")                                                                                               = 1
puts("Wrong :("Wrong :(
)                                                                                                                  = 9
+++ exited (status 0) +++
```

Ok so we see our input is being compared to the string `23_15_fun` via the `strcmp()` function. Lets run the program normally with this password:
```bash
user@arch:~/cyber/ctf/mitre-2022/rev/rev200$ ./rev200 23_15_fun
Correct :)
Here is your flag: MCA{f677992ef948fbdcb542012db93c3c6b8ad6ec26}
```

## Flag
```
MCA{f677992ef948fbdcb542012db93c3c6b8ad6ec26}
```