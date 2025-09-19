"""
Module for quantum noise.
"""

from typing import List
import numpy
from quantum.gate import Gate

__all__ = ["Noise"]


class Noise:
    r"""Class to obtain quantum noise models."""

    @classmethod
    def BitFlip(cls, prob: float) -> List[numpy.ndarray]:
        r"""Kraus operators of a quantum bit flip noise.

        Such a noise has Kraus operators:

        .. math::

            E_0 = \sqrt{1-p} I, \quad
            E_1 = \sqrt{p} X.

        Args:
            prob (float): probability of a bit flip

        Returns:
            List[numpy.ndarray]: a list of kraus operators for the noise
        """
        assert 0 <= prob <= 1, "`prob` should be between 0 and 1."
        return [numpy.sqrt(1 - prob) * Gate.I(), numpy.sqrt(prob) * Gate.X()]

    @classmethod
    def PhaseFlip(cls, prob: float) -> List[numpy.ndarray]:
        r"""Kraus operators of a quantum phase flip noise.

        Such a noise has Kraus operators:

        .. math::

            E_0 = \sqrt{1-p} I, \quad
            E_1 = \sqrt{p} Z.

        Args:
            prob (float): probability of a phase flip

        Returns:
            List[numpy.ndarray]: a list of kraus operators for the noise
        """
        assert 0 <= prob <= 1, "`prob` should be between 0 and 1."
        return [numpy.sqrt(1 - prob) * Gate.I(), numpy.sqrt(prob) * Gate.Z()]

    @classmethod
    def BitPhaseFlip(cls, prob: float) -> List[numpy.ndarray]:
        r"""Kraus operators of a quantum bit-phase flip noise.

        Such a noise has Kraus operators:

        .. math::

            E_0 = \sqrt{1-p} I, \quad
            E_1 = \sqrt{p} Y.

        Args:
            prob (float): probability of a bit-phase flip

        Returns:
            List[numpy.ndarray]: a list of kraus operators for the noise
        """
        assert 0 <= prob <= 1, "`prob` should be between 0 and 1."
        return [numpy.sqrt(1 - prob) * Gate.I(), numpy.sqrt(prob) * Gate.Y()]

    @classmethod
    def AmplitudeDamping(cls, prob: float) -> List[numpy.ndarray]:
        r"""Kraus operators of a quantum amplitude damping noise.

        Such a noise has Kraus operators:

        .. math::

            E_0 =
            \begin{bmatrix}
                1 & 0 \\
                0 & \sqrt{1-p}
            \end{bmatrix}, \quad
            E_1 =
            \begin{bmatrix}
                0 & \sqrt{p} \\
                0 & 0
            \end{bmatrix}.

        Args:
            prob (float): damping probability

        Returns:
            List[numpy.ndarray]: a list of kraus operators for the noise
        """
        assert 0 <= prob <= 1, "`prob` should be between 0 and 1."
        return [
            numpy.array([[1, 0], [0, numpy.sqrt(1 - prob)]], dtype=complex),
            numpy.array([[0, numpy.sqrt(prob)], [0, 0]], dtype=complex),
        ]

    @classmethod
    def PhaseDamping(cls, prob: float) -> List[numpy.ndarray]:
        r"""Kraus operators of a quantum phase damping noise.

        Such a noise has Kraus operators:

        .. math::

            E_0 =
            \begin{bmatrix}
                1 & 0 \\
                0 & \sqrt{1-p}
            \end{bmatrix}, \quad
            E_1 =
            \begin{bmatrix}
                0 & 0 \\
                0 & \sqrt{p}
            \end{bmatrix}.

        Args:
            prob (float): probability of a bit flip

        Returns:
            List[numpy.ndarray]: a list of kraus operators for the noise
        """
        assert 0 <= prob <= 1, "`prob` should be between 0 and 1."
        return [
            numpy.array([[1, 0], [0, numpy.sqrt(1 - prob)]], dtype=complex),
            numpy.array([[0, 0], [0, numpy.sqrt(prob)]], dtype=complex),
        ]

    @classmethod
    def Depolarizing(cls, prob: float) -> List[numpy.ndarray]:
        r"""Kraus operators of a quantum depolarizing noise.

        Such a noise has Kraus operators:

        .. math::

            E_0 = \sqrt{1-p} I, \quad
            E_1 = \sqrt{p/3} X, \quad
            E_2 = \sqrt{p/3} Y, \quad
            E_3 = \sqrt{p/3} Z.

        Args:
            prob (float): parameter of the depolarizing noise

        Returns:
            List[numpy.ndarray]: a list of kraus operators for the noise
        """
        assert 0 <= prob <= 1, "`prob` should be between 0 and 1."
        return [
            numpy.sqrt(1 - prob) * Gate.I(),
            numpy.sqrt(prob / 3) * Gate.X(),
            numpy.sqrt(prob / 3) * Gate.Y(),
            numpy.sqrt(prob / 3) * Gate.Z(),
        ]
