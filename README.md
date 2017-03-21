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

## Quantum Mechanics explanation

Quantum communication will be based on two quantum basis: the computational basis \|0\> and \|1\>, and the Hadamard basis 1/sqrt(2)\*(\|0\> + \|1\>) and 1/sqrt(2)\*(\|0\> - \|1\>). When a Quantum user generates a random bit associated with these basis we choose 0 as the computational basis and 1 as the Hadamard basis.

When measured, we apply Hadamard gate on the Hadamard basis Qubits and the Identity gate at the computational basis. |0> and 1/sqrt(2)\*(|0> + |1>) are interpretated as 

- Alice and Bob publicly agree upon a number N, this number should be at least 2 times the key length that they expect to get. They also agree who will be the sender and who will be the receiver.
- Alice generates N random bits (using a Quantum random generator, at the best scenario, but she can use a pseudo-random generator like /dev/random) and maps them to Quantum basis.
- Alice generates N random bits and creates the required states using the previous random basis. She then sends these Qubits through the quantum channel (i.e. Fibre Optic with polarized Photons) So:
	
-	Basis | Bits | State
	------| -----|-----
	0     | 0    | \|0\>
	0     | 1    | \|1\>
	1     | 1    | 1/sqrt(2)\*(\|0\> + \|1\>)
	1     | 1    | 1/sqrt(2)\*(\|0\> - \|1\>)
- Bob generates N random bits and maps them to their quantum basis.
- Bob measured the received Qubits from Alice with his basis, he then gets the measured bits.
- Alice and Bob exchange publicly their basis and compare them locally.
- Alice and Bob drop the bits where their basis doesn't match, the remaining bits will be the agreed key. If the key length is may below N/2 then they consider a MITM attack happened.
- Alice sends and encrypted "Hello" message to Bob with that key. If Bob can't decrypt the message with his key then a MITM ocurred (or decoherence), otherwise they have their key for encryption.
