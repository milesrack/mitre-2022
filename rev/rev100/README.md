# rev100

## Description
Think you can find the password…

http://3.238.30.178:3005/

## Solve
Download the binary rev100

Run `strings` on the binary, this looks for all printable strings within the file:
```
$ strings rev100  
/lib/ld-linux.so.2  
libc.so.6  
_IO_stdin_used  
exit  
strncmp  
puts  
printf  
__libc_start_main  
GLIBC_2.0  
_ITM_deregisterTMCloneTable  
__gmon_start__  
_ITM_registerTMCloneTable  
UWVS  
[^_]  
MCA_CTF_2022  
Correct :)  
MCA{db346ae600417d8cbceb5c86914b627165635e77}  
Here is your flag: %s  
Wrong :(  
 Usage %s PASSWORD  
;*2$"  
...

```

## Flag
```
MCA{db346ae600417d8cbceb5c86914b627165635e77}
```
