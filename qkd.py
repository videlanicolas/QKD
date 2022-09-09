#!/usr/bin/python
import argparse
from random import randint

from models import QuantumUser

SEPARATOR = "############################"


def generate_random_bits(N):
    aux = list()
    for i in range(N):
        aux.append(randint(0, 1))
    return aux


def QKD(N, verbose=False, eve_present=False):
    alice_basis = generate_random_bits(N)
    alice_bits = generate_random_bits(N)
    alice = QuantumUser("Alice")
    alice_qubits = alice.send(data=alice_bits, basis=alice_basis)
    if eve_present:
        eve_basis = generate_random_bits(N)
        eve = QuantumUser("Eve")
        eve_bits = eve.receive(data=alice_qubits, basis=eve_basis)
        alice_qubits = eve.send(data=eve_bits, basis=eve_basis)
    bob_basis = generate_random_bits(N)
    bob = QuantumUser("Bob")
    bob_bits = bob.receive(data=alice_qubits, basis=bob_basis)
    alice_key = list()
    bob_key = list()
    for i in range(N):
        if alice_basis[i] == bob_basis[i]:
            alice_key.append(alice_bits[i])
            bob_key.append(bob_bits[i])
    if alice_key != bob_key:
        key = False
        length = None
        print("Encryption key mismatch, eve is present.")
    else:
        key = True
        length = len(bob_key)
        print("Successfully exchanged key!")
        print("Key Length: " + str(length))
    if verbose:
        print(f"Alice generates {N} random basis.")
        input()
        print("".join(str(e) for e in alice_basis))
        input()
        print(f"Alice generates {N} random bits.")
        input()
        print("".join(str(e) for e in alice_bits))
        input()
        print(f"Alice sends to Bob {N} encoded Qubits.")
        input()
        aux = ""
        for q in alice_qubits:
            aux += f"{q}   "
        print(aux)
        input()
        if eve_present:
            print("Eve intercepts Qubits!")
            input()
            print("".join(str(e) for e in eve_basis))
            input()
            print("Eve's bits.")
            input()
            print("".join(str(e) for e in eve_bits))
            input()
        print(f"Bob generates {N} random basis.")
        input()
        print("".join(str(e) for e in bob_basis))
        input()
        print("Bob receives and decodes Alice's Qubits.")
        input()
        print("".join(str(e) for e in bob_bits))
        input()
        print(
            "Alice and Bob interchange basis through Internet and compare their basis."
        )
        input()
    # print("Key obtained: " + ''.join(str(e) for e in bob_bits))
    # print(f"Efficiency: {round((float(len(key))/float(len(alice_bits)))*100.0)}%")
    return key


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="BB84 QKD demonstration with Python.")
    req_named = parser.add_argument_group("Required arguments")
    opt_named = parser.add_argument_group("Optional arguments")
    req_named.add_argument(
        "-q", "--qubits", required=True, help="Number of Qubits."
    )
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
