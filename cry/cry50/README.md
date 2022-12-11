# cry50

## Description
What could this mean?

http://3.238.30.178:3015

## Solve
Visiting the site gives us this cryptic text:
```
Pu jyfwavnyhwof, h Jhlzhy jpwoly pz jhalnvypglk hz h zbizapabapvu jpwoly pu dopjo aol hswohila pu aol wshpu alea pz zopmalk if h mpelk ubtily kvdu aol hswohila. Hkchuahnlz vm bzpun h Jhlzhy jpwoly pujsbkl: Vul vm aol lhzplza tlaovkz av bzl pu jyfwavnyhwof huk jhu wyvcpkl tpuptbt zljbypaf av aol pumvythapvu. Jhlzhy vujl zhpk aoha opz mhcvypal mshn dhz TJH{1i09hjl75jl6lkm1535289h740mh0i1hi331ml64} 
```
If we try to submit this flag we will see it is incorrect. Some decoding must be done. This looks like a simple ceasar cipher.

I put the text in [CyberChef](https://cyberchef.org) and selected the ROT13 module. Then I just increased the shift # until I saw legible text.

Shifting the text 19 letters decodes the message:
```
In cryptography, a Caesar cipher is categorized as a substitution cipher in which the alphabet in the plain text is shifted by a fixed number down the alphabet. Advantages of using a Caesar cipher include: One of the easiest methods to use in cryptography and can provide minimum security to the information. Caesar once said that his favorite flag was MCA{1b09ace75ce6edf1535289a740fa0b1ab331fe64} 
```
## Flag
```
MCA{1b09ace75ce6edf1535289a740fa0b1ab331fe64} 
```