from random import randint

from models.qubit import QuBit


class QuantumAgent:
    def __init__(self, name):
        self.name = name
        self.data = []
        self.basis = []
        self.last_sent = []

    def send(self):
        """
        Using computational base |0> y |1> for the horizontal and vertical states.
        Using Hadamard base |0> + |1> y |0> - |1> diagonal states.
        0 0 -> |0>
        0 1 -> |1>
        1 0 -> |0> + |1>
        1 1 -> |0> - |1>
        """
        assert len(self.data) == len(self.basis), "Basis and data must be the same length!"
        qubits = list()
        for i in range(len(self.data)):
            if not self.basis[i]:
                # Computational base
                if not self.data[i]:
                    qubits.append(QuBit(0))
                else:
                    qubits.append(QuBit(1))
            else:
                # Hadamard base
                if not self.data[i]:
                    aux = QuBit(0)
                else:
                    aux = QuBit(1)
                aux.hadamard()
                qubits.append(aux)
        self.last_sent = qubits
        return qubits

    def receive(self, data):
        assert len(data) == len(self.basis), "Basis and data must be the same length!"
        bits = list()
        for i in range(len(data)):
            if not self.basis[i]:
                bits.append(data[i].measure())
            else:
                data[i].hadamard()
                bits.append(data[i].measure())
        self.data = bits
        return bits


    def generate_basis(self, N):
        self.basis = generate_random_bits(N)
        return self.basis


    def generate_data(self, N):
        self.data = generate_random_bits(N)
        return self.data

def generate_random_bits(N):
    return [randint(0, 1) for _ in range(N)]
