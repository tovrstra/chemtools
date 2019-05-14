# -*- coding: utf-8 -*-
# ChemTools is a collection of interpretive chemical tools for
# analyzing outputs of the quantum chemistry calculations.
#
# Copyright (C) 2016-2019 The ChemTools Development Team
#
# This file is part of ChemTools.
#
# ChemTools is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# ChemTools is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --
# pragma pylint: disable=invalid-name
"""Kinetic Energy Density Module."""


import numpy as np

from chemtools.utils.utils import doc_inherit
from chemtools.wrappers.molecule import Molecule
from chemtools.denstools.densbased import DensGradBasedTool


__all__ = ["KED"]


class KED(object):
    """Kinetic Energy Density Class."""

    def __init__(self, molecule, points, spin="ab", index=None):
        r"""Initialize class using instance of `Molecule` and grid points.

        Parameters
        ----------
        molecule : Molecule
            An instance of `Molecule` class.
        points : np.ndarray
            Cartesian coordinates, a 2D array with 3 columns, to calculate local properties.
        spin : str
            The type of occupied spin orbitals.
        index : sequence
            Sequence of integers representing the index of spin orbitals.

        """
        if points.ndim != 2 or points.shape[1] != 3:
            raise ValueError("Argument points should be a 2D array with 3 columns.")
        self._points = points
        # compute density, gradient, & kinetic energy density on grid
        dens = molecule.compute_density(self._points, spin, index)
        grad = molecule.compute_gradient(self._points, spin, index)
        self._ke = molecule.compute_kinetic_energy_density(self._points, spin, index)
        # initialize dens- & grad-based tools class
        self._denstools = DensGradBasedTool(dens, grad)

    @classmethod
    def from_file(cls, filename, points, spin="ab", index=None):
        """Initialize class from file.

        Parameters
        ----------
        filename : str
            Path to molecule's files.
        points : np.ndarray
            Cartesian coordinates, a 2D array with 3 columns, to calculate local properties.
        spin : str
            The type of occupied spin orbitals.
        index : sequence
            Sequence of integers representing the index of spin orbitals.
        """
        molecule = Molecule.from_file(filename)
        return cls(molecule, points, spin, index)

    @property
    def points(self):
        """Coordinates of grid points."""
        return self._points

    @property
    @doc_inherit(DensGradBasedTool, 'density')
    def density(self):
        return self._denstools.density

    @property
    def positive_definite(self):
        r"""Positive definite kinetic energy density.

        .. math::
           \tau \left(\mathbf{r}\right) =
           \sum_i^N n_i \frac{1}{2} \rvert \nabla \phi_i \left(\mathbf{r}\right) \lvert^2
        """
        return self._ke

    @property
    @doc_inherit(DensGradBasedTool, 'kinetic_energy_density_thomas_fermi')
    def thomas_fermi(self):
        return self._denstools.kinetic_energy_density_thomas_fermi

    @property
    @doc_inherit(DensGradBasedTool, 'kinetic_energy_density_weizsacker')
    def weizsacker(self):
        return self._denstools.kinetic_energy_density_weizsacker
