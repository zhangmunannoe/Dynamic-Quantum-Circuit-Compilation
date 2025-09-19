"""
Module for quantum gates.
"""

import numpy

__all__ = ["Gate"]


class Gate:
    r"""Class to obtain the matrix of a quantum gate."""

    @classmethod
    def I(cls) -> numpy.ndarray:
        r"""Return the matrix of identity gate.

        Returns:
            numpy.ndarray: identity gate
        """
        return numpy.array([[1, 0], [0, 1]], dtype=complex)

    @classmethod
    def X(cls) -> numpy.ndarray:
        r"""Return the matrix of Pauli-X gate.

        Returns:
            numpy.ndarray: Pauli-X gate
        """
        return numpy.array([[0, 1], [1, 0]], dtype=complex)

    @classmethod
    def Y(cls) -> numpy.ndarray:
        r"""Return the matrix of Pauli-Y gate.

        Returns:
            numpy.ndarray: Pauli-Y gate
        """
        return numpy.array([[0, -1j], [1j, 0]], dtype=complex)

    @classmethod
    def Z(cls) -> numpy.ndarray:
        r"""Return the matrix of Pauli-Z gate.

        Returns:
            numpy.ndarray: Pauli-Z gate
        """
        return numpy.array([[1, 0], [0, -1]], dtype=complex)

    @classmethod
    def H(cls) -> numpy.ndarray:
        r"""Return the matrix of Hadamard gate.

        Returns:
            numpy.ndarray: Hadamard gate
        """
        return numpy.array([[1, 1], [1, -1]], dtype=complex) / numpy.sqrt(2.0)

    @classmethod
    def S(cls) -> numpy.ndarray:
        r"""Return the matrix of phase gate.

        Returns:
            numpy.ndarray: phase gate
        """
        return numpy.array([[1, 0], [0, 1j]], dtype=complex)

    @classmethod
    def T(cls) -> numpy.ndarray:
        r"""Return the matrix of T gate.

        Returns:
            numpy.ndarray: T gate
        """
        return numpy.array([[1, 0], [0, numpy.exp(1j * numpy.pi / 4)]], dtype=complex)

    @classmethod
    def Rx(cls, theta: float) -> numpy.ndarray:
        r"""Return the matrix of Rx gate.

        Args:
            theta (float): rotation angle

        Returns:
            numpy.ndarray: Rx gate
        """
        return numpy.array(
            [[numpy.cos(theta / 2), -1j * numpy.sin(theta / 2)], [-1j * numpy.sin(theta / 2), numpy.cos(theta / 2)]],
            dtype=complex,
        )

    @classmethod
    def Ry(cls, theta: float) -> numpy.ndarray:
        r"""Return the matrix of Ry gate.

        Args:
            theta (float): rotation angle

        Returns:
            numpy.ndarray: Ry gate
        """
        return numpy.array(
            [[numpy.cos(theta / 2), -numpy.sin(theta / 2)], [numpy.sin(theta / 2), numpy.cos(theta / 2)]], dtype=complex
        )

    @classmethod
    def Rz(cls, theta: float) -> numpy.ndarray:
        r"""Return the matrix of Rz gate.

        Args:
            theta (float): rotation angle

        Returns:
            numpy.ndarray: Rz gate
        """
        return numpy.array([[numpy.exp(-1j * theta / 2), 0], [0, numpy.exp(1j * theta / 2)]], dtype=complex)

    @classmethod
    def U(cls, theta: float, phi: float, gamma: float) -> numpy.ndarray:
        r"""Return the matrix of U gate.

        .. math::

            U (\theta, \phi, \gamma) = Rz(\phi) Rx(\theta) Rz(\gamma)

        Args:
            theta (float): Rx rotation angle
            phi (float): left Rz rotation angle
            gamma (float): right Rz rotation angle

        Returns:
            numpy.ndarray: U gate
        """
        return Gate.Rz(phi) @ Gate.Rx(theta) @ Gate.Rz(gamma)

    @classmethod
    def U3(cls, theta: float, phi: float, gamma: float) -> numpy.ndarray:
        r"""Return the matrix of U3 gate.

        .. math::

            U3 (\theta, \phi, \gamma) = Rz(\phi) Ry(\theta) Rz(\gamma)

        Args:
            theta (float): Ry rotation angle
            phi (float): left Rz rotation angle
            gamma (float): right Rz rotation angle

        Returns:
            numpy.ndarray: U3 gate
        """
        return Gate.Rz(phi) @ Gate.Ry(theta) @ Gate.Rz(gamma)

    @classmethod
    def CZ(cls) -> numpy.ndarray:
        r"""Return the matrix of controlled-Z gate.

        Returns:
            numpy.ndarray: controlled-Z gate
        """
        return numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, -1]], dtype=complex)

    @classmethod
    def CNOT(cls) -> numpy.ndarray:
        r"""Return the matrix of controlled-NOT gate.

        Returns:
            numpy.ndarray: controlled-NOT gate
        """
        return numpy.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 0, 1], [0, 0, 1, 0]], dtype=complex)

    @classmethod
    def SWAP(cls) -> numpy.ndarray:
        r"""Return the matrix of SWAP gate.

        Returns:
            numpy.ndarray: SWAP gate
        """
        return numpy.array([[1, 0, 0, 0], [0, 0, 1, 0], [0, 1, 0, 0], [0, 0, 0, 1]], dtype=complex)
