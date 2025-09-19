"""
Module for quantum measurement bases.
"""

from argparse import ArgumentTypeError
import numpy
from numpy import pi
from quantum.gate import Gate
from quantum.state import One, Zero, Plus, Minus

__all__ = ["Basis"]


class Basis:
    r"""Class to obtain a measurement basis."""

    @classmethod
    def X(cls) -> numpy.ndarray:
        r"""Return X basis.

        Returns:
            numpy.ndarray: X basis
        """
        return numpy.array([Plus.SV, Minus.SV])

    @classmethod
    def Y(cls) -> numpy.ndarray:
        r"""Return Y basis.

        Returns:
            numpy.ndarray: Y basis
        """
        return numpy.array([Gate.Rz(pi / 2) @ Plus.SV, Gate.Rz(pi / 2) @ Minus.SV])

    @classmethod
    def Z(cls) -> numpy.ndarray:
        r"""Return Z basis.

        Returns:
            numpy.ndarray: Z basis
        """
        return numpy.array([Zero.SV, One.SV])

    @classmethod
    def Plane(cls, plane: str, theta: float) -> numpy.ndarray:
        r"""Single-qubit measurement basis on a given plane.

        .. math::

            M^{XY}(\theta) = \{R_{z}(\theta)|+\rangle, R_{z}(\theta)|-\rangle\}

            M^{YZ}(\theta) = \{R_{x}(\theta)|0\rangle, R_{x}(\theta)|1\rangle\}

            M^{XZ}(\theta) = \{R_{y}(\theta)|0\rangle, R_{y}(\theta) |1\rangle\}

        Args:
            plane (str): measurement plane, can be 'XY', 'YZ' or 'XZ'
            theta (float): measurement angle

        Returns:
            numpy.ndarray: measurement basis
        """
        if plane == "XY":  # XY plane measurement basis
            return numpy.array([Gate.Rz(theta) @ Plus.SV, Gate.Rz(theta) @ Minus.SV])

        elif plane == "YZ":  # YZ plane measurement basis
            return numpy.array([Gate.Rx(theta) @ Zero.SV, Gate.Rx(theta) @ One.SV])

        elif plane == "XZ":  # XZ plane measurement basis
            return numpy.array([Gate.Ry(theta) @ Zero.SV, Gate.Ry(theta) @ One.SV])

        else:
            raise ArgumentTypeError(f"Input {plane} should be 'XY', 'YZ' or 'XZ'.")
