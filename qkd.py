#!/usr/bin/python
import argparse
from random import randint

from models import QuantumAgent


SEPARATOR = "############################"


def generate_random_bits(N):
    aux = list()
    for _ in range(N):
        aux.append(randint(0, 1))
    return aux


def user_feedback(
    verbose: bool,
    alice: QuantumAgent,
    bob: QuantumAgent,
    alice_key,
    bob_key,
    eve: QuantumAgent = None,
    ):
    if verbose:
        print(f"Alice generates {N} random basis.")
        input()
        print("".join(str(e) for e in alice.basis))
        input()
        print(f"Alice generates {N} random bits.")
        input()
        print("".join(str(e) for e in alice.data))
        input()
        print(f"Alice sends to Bob {N} encoded Qubits.")
        input()
        aux = ""
        for q in alice.last_sent:
            aux += f"{q}   "
        print(aux)
        input()
        if eve:
            print("Eve intercepts Qubits!")
            input()
            print("".join(str(e) for e in eve.basis))
            input()
            print("Eve's bits.")
            input()
            print("".join(str(e) for e in eve.data))
            input()
        print(f"Bob generates {N} random basis.")
        input()
        print("".join(str(e) for e in bob.basis))
        input()
        print("Bob receives and decodes Alice's Qubits.")
        input()
        print("".join(str(e) for e in bob.bits))
        input()
        print(
            "Alice and Bob interchange basis through Internet and compare their basis."
        )
        input()

    if alice_key != bob_key:
        key = False
        print("Encryption key mismatch, eve is present.")
    else:
        key = True
        print("Successfully exchanged key!")
        print(f"Key Length: {len(bob_key)}")
    # print("Key obtained: " + ''.join(str(e) for e in bob_bits))
    # print(f"Efficiency: {round((float(len(key))/float(len(alice_bits)))*100.0)}%")


def QKD(N, verbose=False, eve_present=False):
    alice = QuantumAgent("Alice")
    alice.generate_basis(N)
    alice.generate_data(N)
    sent_qubits = alice.send()
    
    eve = None
    if eve_present:
        eve = QuantumAgent("Eve")
        eve.generate_basis(N)
        eve.receive(data=sent_qubits)
        sent_qubits = eve.send()
    
    bob = QuantumAgent("Bob")
    bob.generate_basis(N)
    bob.receive(data=sent_qubits)
    
    alice_key = list()
    bob_key = list()
    for i in range(N):
        if alice.basis[i] == bob.basis[i]:
            alice_key.append(alice.data[i])
            bob_key.append(bob.data[i])
    
    user_feedback(
        verbose=verbose,
        alice=alice,
        bob=bob,
        eve=eve,
        alice_key=alice_key,
        bob_key=bob_key,
    )

    return alice_key == bob_key


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BB84 QKD demonstration with Python.")
    req_named = parser.add_argument_group("Required arguments")
    opt_named = parser.add_argument_group("Optional arguments")
    req_named.add_argument("-q", "--qubits", required=True, help="Number of Qubits.")
    opt_named.add_argument(
        "-i", "--iterate", required=False, help="Number of iterations."
    )
    opt_named.add_argument(
        "-e",
        "--eve",
        action="store_true",
        default=False,
        required=False,
        help="Is EVE present?",
    )
    opt_named.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        default=False,
        required=False,
        help="Verbose logs.",
    )
    args = parser.parse_args()
    assert int(args.qubits)
    ret = list()

    N = 1
    if args.iterate:
        assert int(args.iterate)
        N = int(args.iterate)

    for i in range(N):
        print(f"############# {i} #############")
        ret.append(QKD(int(args.qubits), verbose=args.verbose, eve_present=args.eve))
        print(SEPARATOR)
    print(SEPARATOR)
    print(SEPARATOR)
    t = f"{float(ret.count(True)) * 100.0 / float(N):.2f}"
    u = f"{float(ret.count(False)) * 100.0 / float(N):.2f}"
    print(f"True: {ret.count(True)} <{t}%>")
    print(f"False: {ret.count(False)} <{u}%>")
