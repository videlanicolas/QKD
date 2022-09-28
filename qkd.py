#!/usr/bin/python
import argparse
from random import randint

import numpy as np
from models import QuantumAgent
from models.databeam import DataStream, Beam
from sympy import pprint, symbols
from sympy.core.numbers import (I, pi)

from sympy.physics.optics.polarization import (mueller_matrix,
    linear_polarizer, half_wave_retarder, stokes_vector, phase_retarder, quarter_wave_retarder)
from sympy.physics.optics.gaussopt import (RayTransferMatrix, FreeSpace, FlatRefraction,
        CurvedRefraction, FlatMirror, CurvedMirror, ThinLens, GeometricRay,
        BeamParameter, waist2rayleigh, rayleigh2waist)

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
        print("".join(str(e) for e in bob.data))
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

def eom_transfer_matrix():
    return FlatRefraction(n_eom, n_air) * \
            FreeSpace(len_eom) * \
            FlatRefraction(n_air, n_eom)

def telescope_transfer_matrix():
    return 

def eom_mueller_matrix(theta):
    return mueller_matrix(phase_retarder(0, theta))

def alice_optical_path(base, bit):    
    bit_states = [0, pi, pi/2, 3*pi/2] # V, H, L, R
    eom = eom_mueller_matrix(bit_states[base << 1 | bit])
    vertical_polarizer = mueller_matrix(linear_polarizer(pi / 2))
    hwp = mueller_matrix(half_wave_retarder(pi / 8))
    return hwp * eom * hwp * vertical_polarizer


def issue_key(key, base_word):
    data = DataStream([0 for _ in range(len(key))])
    for i in range(len(key)):
        beam = Beam(parameter=BeamParameter(830e-9, 0, 1e-3))
        bit, base = int(key[i]), int(base_word[i])
        beam.polarization = alice_optical_path(bit, base) * beam.polarization
        data.data[i] = beam
        pprint(beam.polarization)
    
    return data


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
    t = f"{float(ret.count(True)) * 100.0 / float(N):.2f}"
    u = f"{float(ret.count(False)) * 100.0 / float(N):.2f}"
    print(f"True: {ret.count(True)} <{t}%>")
    print(f"False: {ret.count(False)} <{u}%>")
