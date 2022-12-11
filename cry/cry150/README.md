# cry150

## Description
Read the text with some charisma we need to be preparing for the play.

I need you to tip toe the line between your character and yourself.

Great, now that it’s clear, let’s take from your last lines.

Gandalf - “It is not despair, for despair is only for those who see the end beyond all doubt. We do not.”

Everyone in costumes, I think that is exactly what we were looking for.

Don’t lose this confidence during the play you are Gandalf after all; white beard up and big smiles the show is about to start.

R2FuZGFsZiAtIFdlIG11c3QgZVhPUmNpc2UgdGhlIGRlbW9uIG9mIEJhbHJvZ3Mgb3V0IG9mIHRoaXMgcGxhbmUgb2YgZXhpc3RlbmNlIGluIG9yZGVyIHRvIGdldCB0byBMb3RobMOzcmllbi4KCjFGIDBBIDA2IDNDIDI2IDdDIDM2IDcwIDczIDc1IDc3IDcxIDZBIDJEIDczIDc0IDIxIDc2IDY3IDdBIDc3IDcyIDcyIDIwIDMxIDJEIDIxIDc2IDc3IDczIDMxIDcwIDcwIDcyIDcyIDI3IDYxIDJGIDIzIDcyIDIzIDI2IDM3IDJEIDNBIA==

## Solve
The ciphertext here looks like some base64. Decoding it gives us another part of the challenge:
```
Gandalf - We must eXORcise the demon of Balrogs out of this plane of existence in order to get to Lothlórien.

1F 0A 06 3C 26 7C 36 70 73 75 77 71 6A 2D 73 74 21 76 67 7A 77 72 72 20 31 2D 21 76 77 73 31 70 70 72 72 27 61 2F 23 72 23 26 37 2D 3A
```

This challenge took me a while because I was solving it wrong (tried brute forcing XOR key, using "Balrogs", "Gandalf", etc.) Ultimiately my team found out we need to reverse the key.

We know the first 3 letters of the flag will be "MCA" and the 3 first bytes of the ciphertext are `0x1F, 0x0A, 0x06`. XORing each of these against eachother gives the first 3 letters of the key "RIG".

```python
ct = [0x1F, 0x0A, 0x06]
pt = "MCA"
print(''.join([chr(c^ord(pt[i])) for i,c in enumerate(ct)]))
```
```
RIG
```

Using some guesswork we can assume the key is "RIGGED". Let's write a script to solve this:
```python
ct = [0x1F, 0x0A, 0x06, 0x3C, 0x26, 0x7C, 0x36, 0x70, 0x73, 0x75, 0x77, 0x71, 0x6A, 0x2D, 0x73, 0x74, 0x21, 0x76, 0x67, 0x7A, 0x77, 0x72, 0x72, 0x20, 0x31, 0x2D, 0x21, 0x76, 0x77, 0x73, 0x31, 0x70, 0x70, 0x72, 0x72, 0x27, 0x61, 0x2F, 0x23, 0x72, 0x23, 0x26, 0x37, 0x2D, 0x3A]
key = "RIGGED"
print(''.join([chr(c^ord(key[i % len(key)])) for i,c in enumerate(ct)]))
```

## Flag
```
MCA{c8d942258d43d253057dcdf127c9757c3fd5fbed}
```