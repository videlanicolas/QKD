#!/usr/bin/python
from numpy import matrix
from math import pow, sqrt
from random import randint
import sys

class qubit():
	def __init__(self,initial_state):
		if initial_state:
			self.__state = matrix([[0],[1]])
		else:
			self.__state = matrix([[1],[0]])
		self.__measured = False
		self.__H = (1/sqrt(2))*matrix([[1,1],[1,-1]])
		self.__X = matrix([[0,1],[1,0]])
	def show(self):
		aux = ""
		if round(matrix([1,0])*self.__state,2):
			aux += "{0}|0>".format(str(round(matrix([1,0])*self.__state,2)) if round(matrix([1,0])*self.__state,2) != 1.0 else '')
		if round(matrix([0,1])*self.__state,2):
			if aux:
				aux += " + "
			aux += "{0}|1>".format(str(round(matrix([0,1])*self.__state,2)) if round(matrix([0,1])*self.__state,2) != 1.0 else '')
		return aux
	def measure(self):
		if self.__measured:
			raise Exception("Qubit already measured!")
		M = 1000000
		m = randint(0,M)
		self.__measured = True
		if m < round(pow(matrix([1,0])*self.__state,2),2)*M:
			return 0
		else:
			return 1
	def hadamard(self):
		if self.__measured:
			raise Exception("Qubit already measured!")
		self.__state = self.__H*self.__state
	def X(self):
		if self.__measured:
			raise Exception("Qubit already measured!")
		self.__state = self.__X*self.__state

class quantum_user():
	def __init__(self,name):
		self.name = name
	def send(self,data,basis):
		"""
		Uso base computacional |0> y |1> para los estados horizontal y vertical.
		Uso base Hadamard |0> + |1> y |0> - |1> para los estados diagonales.
		0 0 -> |0>
		0 1 -> |1>
		1 0 -> |0> + |1>
		1 1 -> |0> - |1>
		"""
		assert len(data) == len(basis), "Basis and data must be the same length!"
		qubits = list()
		for i in range(len(data)):
			if not basis[i]:
				#Base computacional
				if not data[i]:
					qubits.append(qubit(0))
				else:
					qubits.append(qubit(1))
			else:
				#Base Hadamard
				if not data[i]:
					aux = qubit(0)
				else:
					aux = qubit(1)
				aux.hadamard()
				qubits.append(aux)
		return qubits
	def receive(self,data,basis):
		assert len(data) == len(basis), "Basis and data must be the same length!"
		bits = list()
		for i in range(len(data)):
			if not basis[i]:
				bits.append(data[i].measure())
			else:
				data[i].hadamard()
				bits.append(data[i].measure())
		return bits
def generate_random_bits(N):
	aux = list()
	for i in range(N):
		aux.append(randint(0,1))
	return aux

def QKD(N,silent=False,eve_present=False):
	alice_basis = generate_random_bits(N)
	alice_bits = generate_random_bits(N)
	alice = quantum_user("Alice")
	alice_qubits = alice.send(data=alice_bits,basis=alice_basis)
	if eve_present:
		eve_basis = generate_random_bits(N)
		eve = quantum_user("Eve")
		eve_bits = eve.receive(data=alice_qubits,basis=eve_basis)
		alice_qubits = eve.send(data=eve_bits,basis=eve_basis)
	bob_basis = generate_random_bits(N)
	bob = quantum_user("Bob")
	bob_bits = bob.receive(data=alice_qubits,basis=bob_basis)
	alice_key = list()
	bob_key = list()
	for i in range(N):
		if alice_basis[i] == bob_basis[i]:
			alice_key.append(alice_bits[i])
			bob_key.append(bob_bits[i])
	if alice_key != bob_key:
		key = False
		length = None
	else:
		key = True
		length = len(bob_key)
		print "Key Length: " + str(length)
	if not silent:
		print "Alice generates {0} random basis.".format(str(N))
		raw_input()
		print ''.join(str(e) for e in alice_basis)
		raw_input()
		print "Alice generates {0} random bits.".format(str(N))
		raw_input()
		print ''.join(str(e) for e in alice_bits)
		raw_input()
		print "Alice sends to Bob {0} encoded Qubits.".format(str(N))
		raw_input()
		aux = ""
		for q in alice_qubits:
			aux += q.show() + "   "
		print aux
		raw_input()
		if eve:
			print "Eve intercepts Qubits!"
			raw_input()
			print ''.join(str(e) for e in eve_basis)
			raw_input()
			print "Eve's bits."
			raw_input()
			print ''.join(str(e) for e in eve_bits)
			raw_input()
		print "Bob generates {0} random basis.".format(str(N))
		raw_input()
		print ''.join(str(e) for e in bob_basis)
		raw_input()
		print "Bob receives and decodes Alice's Qubits."
		raw_input()
		print ''.join(str(e) for e in bob_bits)
		raw_input()
		print "Alice and Bob interchange basis through Internet and compare their basis."
		raw_input()
	#print "Key obtained: " + ''.join(str(e) for e in bob_bits)
	#print "Efficiency: {0}%".format(str(round((float(len(key))/float(len(alice_bits)))*100.0)))
	return key

if __name__ == "__main__":
	ret = list()
	for i in range(10000):
		ret.append(QKD(int(sys.argv[1]),silent=True,eve_present=True))
	print "True: {0}".format(ret.count(True))
	print "False: {0}".format(ret.count(False))
