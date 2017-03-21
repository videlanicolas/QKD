# QKD
Python simulation of protocol BB84 for QKD.

## Usage
./qkd.py number_of_bits

## Example
### Without EVE
```
./qkd.py 1000 
Key Length: 490
True: 1
False: 0
```

### With EVE
```
./qkd.py 1000 
True: 0
False: 1
```
## Explanation

One can Iterate over a number of times to get a key by chainging the range in the script:
```
for i in range(10000):
		ret.append(QKD(int(sys.argv[1]),silent=True,eve_present=False))
```

The funciton QKD makes a QKD exchange between Alice and Bob, with or without Eve (as specified by the input variable). The funciton returns True if they achived the same key and False if they didn't. If they achived the same key it ouputs the key size.
One can see that the Key size will average to half the length of the random bits N that Alice and Bob agreed before.
If Eve is present, then Alice and Bob will not have matching keys, therefore their communication will fail. If one generates enough iterations (say 10000) then sometimes Alice and Bob will agree upon a key, but that is just random luck for Eve.

Test with key size 50 and iterating 10000 times with Eve present:
```
./qkd.py 50
Key Length: 20
Key Length: 26
Key Length: 22
Key Length: 15
Key Length: 27
Key Length: 20
Key Length: 17
Key Length: 20
Key Length: 27
Key Length: 20
Key Length: 25
Key Length: 18
Key Length: 20
Key Length: 23
Key Length: 21
Key Length: 21
Key Length: 22
Key Length: 26
Key Length: 20
True: 19
False: 9981
```

Not only the probability of not having the same key will rise (of 10000 iterations, Alice and Bob could not agree 9981 times), but the 19 times they could agree upon a key the size of that key is on average lower than 50/2 = 25. This should alert them that Eve is present.
