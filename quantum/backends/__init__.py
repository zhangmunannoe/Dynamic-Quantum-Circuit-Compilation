"""
Module for quantum computation backends.
"""

from enum import Enum

__all__ = ["mbqc", "Backend"]


class Backend(Enum):
    r"""QNET backends."""
    StateVector = "StateVector"
    DensityMatrix = "DensityMatrix"
    MBQC = "MBQC"
