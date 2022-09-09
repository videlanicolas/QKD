from qubit import QuBit



class QuantumUser:
    def __init__(self, name):
        self.name = name

    def send(self, data, basis):
        """
        Using computational base |0> y |1> for the horizontal and vertical states.
        Using Hadamard base |0> + |1> y |0> - |1> diagonal states.
        0 0 -> |0>
        0 1 -> |1>
        1 0 -> |0> + |1>
        1 1 -> |0> - |1>
        """
        assert len(data) == len(basis), "Basis and data must be the same length!"
        qubits = list()
        for i in range(len(data)):
            if not basis[i]:
                # Computational base
                if not data[i]:
                    qubits.append(QuBit(0))
                else:
                    qubits.append(QuBit(1))
            else:
                # Hadamard base
                if not data[i]:
                    aux = QuBit(0)
                else:
                    aux = QuBit(1)
                aux.hadamard()
                qubits.append(aux)
        return qubits

    def receive(self, data, basis):
        assert len(data) == len(basis), "Basis and data must be the same length!"
        bits = list()
        for i in range(len(data)):
            if not basis[i]:
                bits.append(data[i].measure())
            else:
                data[i].hadamard()
                bits.append(data[i].measure())
        return bits
