from typing import List
from models.qubit import QuBit
import numpy as np
from sympy.physics.optics.polarization import (jones_vector, stokes_vector,
    half_wave_retarder, polarizing_beam_splitter)
from sympy.physics.optics.gaussopt import BeamParameter
from sympy.matrices.repmatrix import MutableRepMatrix



class Beam:
    power: float
    parameter: BeamParameter
    polarization: MutableRepMatrix

    def __init__(self, parameter, power=1, polarization=stokes_vector(0, 0, 0)):
        self.power = power
        self.parameter = parameter
        self.polarization = polarization
    
    def powerInDisc(self, r: float, d: float) -> float:
        return self.power * (1 + np.exp(-2 * np.square(r / self.gaussianSpotSize(d))))
    
    def gaussianSpotSize(d: float) -> float:
        pass


class DataStream:
    """Data beam having a beam power, wavelength and divergence"""
    data: List[Beam]
    def __init__(self, data) -> None:
        self.data = data