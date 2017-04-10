# -*- coding: utf-8 -*-
# ChemTools is a collection of interpretive chemical tools for
# analyzing outputs of the quantum chemistry calculations.
#
# Copyright (C) 2014-2015 The ChemTools Development Team
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
"""Test chemtools.toolbox.conceptualglobal."""

import math
import numpy as np
import sympy as sp
from chemtools.toolbox.conceptualglobal import (QuadraticGlobalTool, ExponentialGlobalTool,
                                                RationalGlobalTool, GeneralGlobalTool)


def test_global_quadratic1():
    # E(N) = -9.0 + (-25.0)*N + N^2, N0=15
    model = QuadraticGlobalTool(-159.0, -153.0, -163.0, 15)
    # check parameters
    np.testing.assert_almost_equal(model.params[0], -9.0, decimal=6)
    np.testing.assert_almost_equal(model.params[1], -25.0, decimal=6)
    np.testing.assert_almost_equal(model.params[2], 1.0, decimal=6)
    np.testing.assert_almost_equal(model.n0, 15, decimal=6)
    np.testing.assert_almost_equal(model.n_max, 12.5, decimal=6)
    # check E(N)
    energy = lambda n: -9.0 - 25.0 * n + n * n
    np.testing.assert_almost_equal(model.energy(20), energy(20), decimal=6)
    np.testing.assert_almost_equal(model.energy(10), energy(10), decimal=6)
    np.testing.assert_almost_equal(model.energy(16.5), energy(16.5), decimal=6)
    # check dE(N)
    deriv = lambda n: -25.0 + 2 * n
    np.testing.assert_almost_equal(model.energy_derivative(20), deriv(20), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10), deriv(10), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5), deriv(16.5), decimal=6)
    # check d2E(N)
    np.testing.assert_almost_equal(model.energy_derivative(20, 2), 2.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 2), 2.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5, 2), 2.0, decimal=6)
    # check d^nE(N) for n > 2
    np.testing.assert_almost_equal(model.energy_derivative(20, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5, 5), 0.0, decimal=6)
    # check ionization potential and electron affinity
    ip = energy(14) - energy(15)
    ea = energy(15) - energy(16)
    np.testing.assert_almost_equal(model.ionization_potential, ip, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, ea, decimal=6)
    np.testing.assert_almost_equal(model.ip, ip, decimal=6)
    np.testing.assert_almost_equal(model.ea, ea, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, 0.5 * (ip + ea), decimal=6)
    electrophil = (-0.5 * (ip + ea))**2 / (2 * (ip - ea))
    np.testing.assert_almost_equal(model.electrophilicity, -electrophil, decimal=6)
    nucleofugal = (ip - 3 * ea)**2 / (8 * (ip - ea))
    np.testing.assert_almost_equal(model.nucleofugality, nucleofugal, decimal=6)
    electrofugal = (3 * ip - ea)**2 / (8 * (ip - ea))
    np.testing.assert_almost_equal(model.electrofugality, -electrofugal, decimal=6)
    # check chemical potential, chemical hardness, and related tools
    np.testing.assert_almost_equal(model.chemical_potential, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.mu, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.eta, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.softness, 1.0 / (ip - ea), decimal=6)
    # check grand potential (as a function of N)
    grand = lambda n: energy(n) - deriv(n) * n
    np.testing.assert_almost_equal(model.grand_potential(15), grand(15), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(14), grand(14), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(16.), grand(16.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(15.2), grand(15.2), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(14.62), grand(14.62), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(11.5), grand(11.5), decimal=6)
    # check grand potential derivative (as a function of N)
    np.testing.assert_almost_equal(model.grand_potential_derivative(14.), -14, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(15.), -15, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(16.), -16, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(15.001), -15.001, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(14.67), -14.67, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(16.91), -16.91, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(model.n0, 1), -15, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(16., 1), -16., decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(17.125, 1), -17.125, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(model.n0, 2), -0.5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(15.89, 2), -0.5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(14.03, 2), -0.5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(16.51, 2), -0.5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(model.n0, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(15, 4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(17.5, 5), 0.0, decimal=6)
    # check mu to N conversion
    np.testing.assert_almost_equal(model.convert_mu_to_n(5.0), 15., decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(5.004), 15.002, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(3.472), 14.236, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(8.962), 16.981, decimal=6)
    # check grand potential (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(15)), grand(15), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(14)), grand(14), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(16)), grand(16), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(13.7)), grand(13.7), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(14.8)), grand(14.8), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(12.3)), grand(12.3), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(11.4)), grand(11.4), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(15.05)), grand(15.05), decimal=6)
    # check grand potential derivative (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(15.05)), -15.05,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(16.34), 1), -16.34,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(15.61), 2), -0.5,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(16.67), 2), -0.5,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(14.31), 3), 0.0,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(12.67), 4), 0.0,
                                   decimal=6)
    # check hyper-softnesses
    np.testing.assert_almost_equal(model.hyper_softness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(4), 0.0, decimal=6)


def test_global_quadratic2():
    # E(N) = 30.0 + (-6.0)*N + 3*N^2, N0=10
    model = QuadraticGlobalTool(75.0, 102.0, 54.0, 5)
    # check parameters
    np.testing.assert_almost_equal(model.params[0], 30.0, decimal=6)
    np.testing.assert_almost_equal(model.params[1], -6.0, decimal=6)
    np.testing.assert_almost_equal(model.params[2], 3.0, decimal=6)
    np.testing.assert_almost_equal(model.n0, 5, decimal=6)
    np.testing.assert_almost_equal(model.n_max, 1, decimal=6)
    # check E(N)
    energy = lambda n: 30.0 - 6.0 * n + 3 * n * n
    np.testing.assert_almost_equal(model.energy(20), energy(20), decimal=6)
    np.testing.assert_almost_equal(model.energy(10), energy(10), decimal=6)
    np.testing.assert_almost_equal(model.energy(16.5), energy(16.5), decimal=6)
    # check dE(N)
    deriv = lambda n: -6.0 + 6 * n
    np.testing.assert_almost_equal(model.energy_derivative(20), deriv(20), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10), deriv(10), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5), deriv(16.5), decimal=6)
    # check d2E(N)
    np.testing.assert_almost_equal(model.energy_derivative(20, 2), 6.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 2), 6.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5, 2), 6.0, decimal=6)
    # check d^nE(N) for n > 2
    np.testing.assert_almost_equal(model.energy_derivative(20, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5, 5), 0.0, decimal=6)
    # check ionization potential and electron affinity
    ip = energy(4) - energy(5)
    ea = energy(5) - energy(6)
    np.testing.assert_almost_equal(model.ionization_potential, ip, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, ea, decimal=6)
    np.testing.assert_almost_equal(model.ip, ip, decimal=6)
    np.testing.assert_almost_equal(model.ea, ea, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, 0.5 * (ip + ea), decimal=6)
    electrophil = (-0.5 * (ip + ea))**2 / (2 * (ip - ea))
    np.testing.assert_almost_equal(model.electrophilicity, -electrophil, decimal=6)
    nucleofugal = (ip - 3 * ea)**2 / (8 * (ip - ea))
    np.testing.assert_almost_equal(model.nucleofugality, nucleofugal, decimal=6)
    electrofugal = (3 * ip - ea)**2 / (8 * (ip - ea))
    np.testing.assert_almost_equal(model.electrofugality, -electrofugal, decimal=6)
    # check chemical potential, chemical hardness, and related tools
    np.testing.assert_almost_equal(model.chemical_potential, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.mu, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.eta, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.softness, 1.0 / (ip - ea), decimal=6)
    # check grand potential (as a function of N)
    grand = lambda n: energy(n) - deriv(n) * n
    np.testing.assert_almost_equal(model.grand_potential(5.), grand(5.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(5.75), grand(5.75), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(6.3), grand(6.3), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(4.21), grand(4.21), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(10.), grand(10.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(15.6), grand(15.6), decimal=6)
    # check grand potential derivative (as a function of N)
    np.testing.assert_almost_equal(model.grand_potential_derivative(4.), -4, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(5.), -5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6., 1), -6, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(3.0123), -3.0123, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(7.2, 1), -7.2, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(8.1, 2), -1 / 6., decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6.12, 2), -1 / 6., decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(5.1, 3), 0., decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6.3, 4), 0., decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(7.45, 5), 0., decimal=6)
    # check mu to N conversion
    np.testing.assert_almost_equal(model.convert_mu_to_n(24.0), 5., decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(30.06), 6.01, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(20.16), 4.36, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(24.15), 5.025, decimal=6)
    # check grand potential (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(5.15)), grand(5.15), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(3.2)), grand(3.2), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(7.67)), grand(7.67), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(5.15)), grand(5.15), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(6.31)), grand(6.31), decimal=6)
    # check grand potential derivative (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(5.81)), -5.81,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(4.2), 1), -4.2,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(5.81), 2), -1/6.,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(4.89), 2), -1/6.,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(6.79), 3), 0.,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(3.12), 4), 0.,
                                   decimal=6)
    # check hyper-softnesses
    np.testing.assert_almost_equal(model.hyper_softness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(4), 0.0, decimal=6)


def test_global_quadratic3():
    # E(N) = -100 + 5*N^2, N0=5
    model = QuadraticGlobalTool(25.0, 80.0, -20.0, 5)
    # check parameters
    np.testing.assert_almost_equal(model.params[0], -100.0, decimal=6)
    np.testing.assert_almost_equal(model.params[1], 0.0, decimal=6)
    np.testing.assert_almost_equal(model.params[2], 5.0, decimal=6)
    np.testing.assert_almost_equal(model.n0, 5, decimal=6)
    np.testing.assert_almost_equal(model.n_max, 0.0, decimal=6)
    # check E(N)
    energy = lambda n: -100.0 + 5 * n * n
    np.testing.assert_almost_equal(model.energy(20), energy(20), decimal=6)
    np.testing.assert_almost_equal(model.energy(10), energy(10), decimal=6)
    np.testing.assert_almost_equal(model.energy(16.5), energy(16.5), decimal=6)
    # check dE(N)
    deriv = lambda n: 10 * n
    np.testing.assert_almost_equal(model.energy_derivative(20), deriv(20), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10), deriv(10), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5), deriv(16.5), decimal=6)
    # check d2E(N)
    np.testing.assert_almost_equal(model.energy_derivative(20, 2), 10.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 2), 10.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5, 2), 10.0, decimal=6)
    # check d^nE(N) for n > 2
    np.testing.assert_almost_equal(model.energy_derivative(20, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5, 5), 0.0, decimal=6)
    # check ionization potential and electron affinity
    ip = energy(4) - energy(5)
    ea = energy(5) - energy(6)
    np.testing.assert_almost_equal(model.ionization_potential, ip, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, ea, decimal=6)
    np.testing.assert_almost_equal(model.ip, ip, decimal=6)
    np.testing.assert_almost_equal(model.ea, ea, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, 0.5 * (ip + ea), decimal=6)
    electrophil = (-0.5 * (ip + ea))**2 / (2 * (ip - ea))
    np.testing.assert_almost_equal(model.electrophilicity, -electrophil, decimal=6)
    nucleofugal = (ip - 3 * ea)**2 / (8 * (ip - ea))
    np.testing.assert_almost_equal(model.nucleofugality, nucleofugal, decimal=6)
    electrofugal = (3 * ip - ea)**2 / (8 * (ip - ea))
    np.testing.assert_almost_equal(model.electrofugality, -electrofugal, decimal=6)
    # check chemical potential, chemical hardness, and related tools
    np.testing.assert_almost_equal(model.chemical_potential, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.mu, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.eta, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.softness, 1.0 / (ip - ea), decimal=6)
    # check grand potential (as a function of N)
    grand = lambda n: energy(n) - deriv(n) * n
    np.testing.assert_almost_equal(model.grand_potential(5.), grand(5.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(4.), grand(4.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(6.), grand(6.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(4.678), grand(4.678), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(6.123), grand(6.123), decimal=6)
    # check grand potential derivative (as a function of N)
    np.testing.assert_almost_equal(model.grand_potential_derivative(5.), -5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(4., 1), -4, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6.), -6, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(5.6001), -5.6001, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(4.145, 1), -4.145, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(5., 2), -0.1, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(7.001, 2), -0.1, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(5., 3), 0., decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(1.25, 4), 0., decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6.5, 5), 0., decimal=6)
    # check mu to N conversion
    np.testing.assert_almost_equal(model.convert_mu_to_n(50), 5., decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(34.6), 3.46, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(69.8), 6.98, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(100.0), 10., decimal=6)
    # check grand potential (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(5.)), grand(5.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(5.641)), grand(5.641), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(4.56)), grand(4.56), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(deriv(3.905)), grand(3.905), decimal=6)
    # check grand potential derivative (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(5.81)), -5.81,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(4.341)), -4.341,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(6.452), 1), -6.452,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(3.678), 2), -0.1,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(4.341), 2), -0.1,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(2.001), 3), 0.,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(deriv(5.456), 4), 0.,
                                   decimal=6)
    # check hyper-softnesses
    np.testing.assert_almost_equal(model.hyper_softness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(4), 0.0, decimal=6)


def test_global_exponential1():
    # E(N) = 5.0 * exp(-0.1 * (N - 10)) + 3.0
    model = ExponentialGlobalTool(8.0, 7.524187090179797, 8.525854590378238, 10)
    np.testing.assert_almost_equal(model.params[0], 5.0, decimal=6)
    np.testing.assert_almost_equal(model.params[2], 3.0, decimal=6)
    np.testing.assert_almost_equal(model.params[1], 0.1, decimal=6)
    np.testing.assert_almost_equal(model.n0, 10, decimal=6)
    # check E(N)
    energy = lambda n: 5.0 * math.exp(-0.1 * (n - 10)) + 3.0
    np.testing.assert_almost_equal(model.energy(20), energy(20), decimal=6)
    np.testing.assert_almost_equal(model.energy(10), energy(10), decimal=6)
    np.testing.assert_almost_equal(model.energy(8), energy(8), decimal=6)
    np.testing.assert_almost_equal(model.energy(16.5), energy(16.5), decimal=6)
    # check dE(N)
    dE = lambda n, r: 5.0 * math.pow(-0.1, r) * math.exp(-0.1 * (n - 10))
    np.testing.assert_almost_equal(model.energy_derivative(18.1), dE(18.1, 1), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10), dE(10, 1), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(8.5), dE(8.5, 1), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(12.25), dE(12.25, 1), decimal=6)
    # check d2E(N)
    np.testing.assert_almost_equal(model.energy_derivative(17.3, 2), dE(17.3, 2), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 2), dE(10, 2), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(9.1, 2), dE(9.1, 2), decimal=6)
    # check d^nE(N) for n > 2
    np.testing.assert_almost_equal(model.energy_derivative(13.7, 3), dE(13.7, 3), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 4), dE(10, 4), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(4.5, 5), dE(4.5, 5), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(6.5, 10), dE(6.5, 10), decimal=6)
    # check ionization potential and electron affinity
    ip = energy(9) - energy(10)
    ea = energy(10) - energy(11)
    np.testing.assert_almost_equal(model.ionization_potential, ip, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, ea, decimal=6)
    np.testing.assert_almost_equal(model.ip, ip, decimal=6)
    np.testing.assert_almost_equal(model.ea, ea, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, -dE(10, 1), decimal=6)
    # check chemical potential, chemical hardness, and related tools
    np.testing.assert_almost_equal(model.chemical_potential, dE(10, 1), decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, dE(10, 2), decimal=6)
    np.testing.assert_almost_equal(model.mu, dE(10, 1), decimal=6)
    np.testing.assert_almost_equal(model.eta, dE(10, 2), decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), dE(10, 3), decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), dE(10, 4), decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), dE(10, 5), decimal=6)
    np.testing.assert_almost_equal(model.softness, 1.0 / dE(10, 2), decimal=6)
    np.testing.assert_almost_equal(model.softness, 1.0 / (5. * 0.1**2), decimal=6)
    # check n_max and related descriptors (expected values are computed symbolically)
    np.testing.assert_equal(model.n_max, float('inf'))
    np.testing.assert_almost_equal(model.energy(model.n_max), 3.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max, 2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.electrophilicity, 5.0, decimal=6)
    np.testing.assert_almost_equal(model.nucleofugality, -4.52418709, decimal=6)
    np.testing.assert_almost_equal(model.electrofugality, 5.52585459, decimal=6)
    # np.testing.assert_almost_equal(model.hyper_softness(2), 0.0, decimal=6)
    # check grand potential (as a function of N)
    grand = lambda n: energy(n) - dE(n, 1) * n
    np.testing.assert_almost_equal(model.grand_potential(9.), grand(9.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(10), grand(10), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(11.), grand(11.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(9.123), grand(9.123), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(8.5), grand(8.5), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(10.001), grand(10.001), decimal=6)
    # check grand potential derivative (as a function of N)
    np.testing.assert_almost_equal(model.grand_potential_derivative(9.), -9, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(10.5), -10.5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(11.001, 1), -11.001, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(9.15, 1), -9.15, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(model.n0, 1), -10, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(10., 2), -1/(5. * 0.1**2),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(10., 3), -1/(5.**2 * 0.1**3),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(10., 4), -2/(5.**3 * 0.1**4),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(9.6, 2), -1./dE(9.6, 2),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(10.76, 2), -1./dE(10.76, 2),
                                   decimal=6)
    d3omega = lambda n: dE(n, 3) / dE(n, 2)**3
    d4omega = lambda n: dE(n, 4) / dE(n, 2)**4 - (3 * dE(n, 3)**2) / dE(n, 2)**5
    d5omega = lambda n: (dE(n, 5)/dE(n, 2)**5 - (10 * dE(n, 3) * dE(n, 4))/dE(n, 2)**6 +
                         (15 * dE(n, 3)**3)/dE(n, 2)**7)
    np.testing.assert_almost_equal(model.grand_potential_derivative(9.23, 3), d3omega(9.23),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(11.56, 3), d3omega(11.56),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(9.23, 3), d3omega(9.23),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(8.67, 4), d4omega(8.67),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(10.4, 4), d4omega(10.4),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(12.6, 4), d4omega(12.6),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(11.5, 5), d5omega(11.5),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(13., 5), d5omega(13.),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(10.02, 5), d5omega(10.02),
                                   decimal=6)
    # check mu to N conversion
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.5), 10., decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.5476345026), 9.09, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.4230574978), 11.671, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.6086285202), 8.034, decimal=6)
    # check grand potential derivative (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(5.81, 1)), -5.81,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(10.5, 1)), -10.5,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(11.2, 1), 2),
                                   -1./dE(11.2, 2), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(11.2, 1), 3),
                                   d3omega(11.2), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(9.34, 1), 4),
                                   d4omega(9.34), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(10.7, 1), 5),
                                   d5omega(10.7), decimal=6)
    # check grand potential (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu(dE(9., 1)), grand(9.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(dE(10.001, 1)), grand(10.001),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(dE(11., 1)), grand(11.), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(dE(12.3, 1)), grand(12.3), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(dE(20.4, 1)), grand(20.4), decimal=6)
    # check hyper-softnesses
    np.testing.assert_almost_equal(model.hyper_softness(2), 1.0 / (5.**2 * 0.1**3), decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(3), 2.0 / (5.**3 * 0.1**4), decimal=6)


def test_global_rational1():
    # E(N) = (0.5 - 2.2 N) / (1 + 0.7 N)
    model = RationalGlobalTool(-1.6250, -1.96774193, -1.0, 2.0)
    # check parameters
    np.testing.assert_almost_equal(model.n0, 2.0, decimal=6)
    np.testing.assert_almost_equal(model.params[0], 0.5, decimal=6)
    np.testing.assert_almost_equal(model.params[1], -2.2, decimal=6)
    np.testing.assert_almost_equal(model.params[2], 0.7, decimal=6)
    # check energy values (expected values are computed symbolically)
    np.testing.assert_almost_equal(model.energy(0), 0.5, decimal=6)
    np.testing.assert_almost_equal(model.energy(1), -1.0, decimal=6)
    np.testing.assert_almost_equal(model.energy(2), -1.6250, decimal=6)
    np.testing.assert_almost_equal(model.energy(3), -1.96774193, decimal=6)
    np.testing.assert_almost_equal(model.energy(4), -2.18421052, decimal=6)
    np.testing.assert_almost_equal(model.energy(5), -2.33333333, decimal=6)
    np.testing.assert_almost_equal(model.energy(6), -2.44230769, decimal=6)
    np.testing.assert_almost_equal(model.energy(1.5), -1.36585365, decimal=6)
    np.testing.assert_almost_equal(model.energy(0.8), -0.80769230, decimal=6)
    # check energy derivatives (expected values are computed symbolically)
    np.testing.assert_almost_equal(model.energy_derivative(0), -2.55, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(1), -0.88235294, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(2), -0.44270833, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(3), -0.26534859, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(4), -0.17659279, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(5), -0.12592592, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(6), -0.09430473, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(1.5), -0.60678167, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(0.8), -1.04783037, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(1.5, 2), 0.41438748, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(0.8, 2), 0.94036059, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(1.1, 3), -0.7638260, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(2.5, 4), 0.13346951, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(0.65, 5), -7.74347011, decimal=5)
    np.testing.assert_almost_equal(model.energy_derivative(1.90, 6), 0.827697092, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(3.20, 3), -0.06803109, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(4.05, 7), -0.03231737, decimal=6)
    # check global descriptors (expected values are computed symbolically)
    np.testing.assert_almost_equal(model.ip, 0.625, decimal=6)
    np.testing.assert_almost_equal(model.ea, 0.34274193, decimal=6)
    np.testing.assert_almost_equal(model.mu, -0.44270833, decimal=6)
    np.testing.assert_almost_equal(model.eta, 0.258246527, decimal=6)
    np.testing.assert_almost_equal(model.ionization_potential, 0.625, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, 0.34274193, decimal=6)
    np.testing.assert_almost_equal(model.chemical_potential, -0.44270833, decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, 0.258246527, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, 0.44270833, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), -0.22596571, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), 0.263626663, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), -0.38445555, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(5), 0.672797214, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(6), -1.37362764, decimal=6)
    np.testing.assert_almost_equal(model.softness, 3.87226890, decimal=6)
    # check n_max and related descriptors (expected values are computed symbolically)
    np.testing.assert_equal(model.n_max, float('inf'))
    np.testing.assert_almost_equal(model.energy(model.n_max), -3.14285714, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max, 2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.electrophilicity, 1.51785714, decimal=6)
    np.testing.assert_almost_equal(model.nucleofugality, -1.17511520, decimal=6)
    np.testing.assert_almost_equal(model.electrofugality, 2.14285714, decimal=6)
    # check grand potential (as a function of N)
    np.testing.assert_almost_equal(model.grand_potential(1.), -0.11764705, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(2.), -0.73958333, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(3.), -1.17169614, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(2.78), -1.08950656, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(5.2), -1.74186236, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(0.), 0.5, decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential(model.n_max), , decimal=6)
    # check grand potential derivative (as a function of N)
    np.testing.assert_almost_equal(model.grand_potential_derivative(2.), -2.0, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(1.4, 1), -1.4, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(2.86), -2.86, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(2., 2), -3.87226890, decimal=6)
    # expected values based on derived formulas
    n0, a0, a1, b1 = 2.0, 0.5, -2.2, 0.7
    dE = lambda n, r: (-b1)**(r-1) * (a1 - a0*b1) * math.factorial(r) / (1 + b1*n)**(r+1)
    d2omega = lambda n: -1. / dE(n, 2)
    d3omega = lambda n: dE(n, 3) / dE(n, 2)**3
    # d4omega = lambda n: dE(n, 4) / dE(n, 2)**4 - (3 * dE(n, 3)**2) / dE(n, 2)**5
    # d5omega = lambda n: (dE(n, 5)/dE(n, 2)**5 - (10 * dE(n, 3) * dE(n, 4))/dE(n, 2)**6 +
    #                      (15 * dE(n, 3)**3)/dE(n, 2)**7)
    np.testing.assert_almost_equal(model.grand_potential_derivative(4.1, 2), d2omega(4.1),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(3.5, 2), d2omega(3.5),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(2.9, 3), d3omega(2.9),
                                   decimal=5)
    np.testing.assert_almost_equal(model.grand_potential_derivative(4.67, 1), -4.67, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(4.67, 2), d2omega(4.67),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(4.67, 3), d3omega(4.67),
                                   decimal=4)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(1.6, 4), d4omega(1.6),
    #                                decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(2.92, 4), d4omega(2.92),
    #                                decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(5.01, 5), d5omega(5.01),
    #                                decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(4.101, 5), d5omega(4.101),
    #                                decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(model.n_max, 4), ,
    #                                decimal=6)
    # check mu to N conversion
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.4427083333), 2., decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.5799422391), 1.567, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.9515745573), 0.91, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.2641542934), 3.01, decimal=6)
    # check grand potential (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.125925925), -1.70370370, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.442708333), -0.73958333, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.232747054), -1.27423079, decimal=6)
    # check grand potential derivative (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(5.81, 1)), -5.81,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(4.67, 1), 2),
                                   d2omega(4.67), decimal=5)
    # np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(6.45, 1), 3),
    #                                d3omega(6.45), decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(5.12, 1), 4),
    #                                d4omega(5.12), decimal=6)
    # check hyper-softnesses
    expected = 3.0 * (1 + b1 * n0)**5 / (4 * b1 * (a1 - a0 * b1)**2)
    np.testing.assert_almost_equal(model.hyper_softness(2), expected, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(2.0, 3), -expected, decimal=6)
    expected = -15 * (1 + b1 * n0)**7 / (8 * b1 * (a1 - a0 * b1)**3)
    np.testing.assert_almost_equal(model.hyper_softness(3), expected, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(2.0, 4), -expected, decimal=6)


def test_global_rational2():
    # E(N) = (-0.15 - 4.2 N) / (1 + 0.45 N)
    model = RationalGlobalTool(-6.99363057, -7.23428571, -6.69064748, 6.5)
    # check parameters
    np.testing.assert_almost_equal(model.n0, 6.5, decimal=6)
    np.testing.assert_almost_equal(model.params[0], -0.15, decimal=6)
    np.testing.assert_almost_equal(model.params[1], -4.2, decimal=6)
    np.testing.assert_almost_equal(model.params[2], 0.45, decimal=6)
    # check energy values (expected values are computed symbolically)
    np.testing.assert_almost_equal(model.energy(6.5), -6.99363057, decimal=6)
    np.testing.assert_almost_equal(model.energy(7.5), -7.23428571, decimal=6)
    np.testing.assert_almost_equal(model.energy(5.5), -6.69064748, decimal=6)
    np.testing.assert_almost_equal(model.energy(5.0), -6.507692307, decimal=6)
    np.testing.assert_almost_equal(model.energy(8.0), -7.336956521, decimal=6)
    # check energy derivatives (expected values are computed symbolically)
    np.testing.assert_almost_equal(model.energy_derivative(6.5), -0.26824617, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(7.5), -0.21590204, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(5.5), -0.34221831, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(4, 2), 0.16942647, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10., 3), -0.00548704, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(9.5, 4), 0.002212836, decimal=6)
    # check global descriptors (expected values are computed symbolically)
    np.testing.assert_almost_equal(model.ip, 0.30298309, decimal=6)
    np.testing.assert_almost_equal(model.ea, 0.24065514, decimal=6)
    np.testing.assert_almost_equal(model.mu, -0.26824617, decimal=6)
    np.testing.assert_almost_equal(model.eta, 0.06150867, decimal=6)
    np.testing.assert_almost_equal(model.ionization_potential, 0.30298309, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, 0.24065514, decimal=6)
    np.testing.assert_almost_equal(model.chemical_potential, -0.26824617, decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, 0.06150867, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, 0.26824617, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), -0.0211558, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), 0.00970204, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), -0.0055616, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(5), 0.00382587, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(6), -0.0030704, decimal=6)
    np.testing.assert_almost_equal(model.softness, 16.25786868, decimal=6)
    # check n_max and related descriptors (expected values are computed symbolically)
    np.testing.assert_equal(model.n_max, float('inf'))
    np.testing.assert_almost_equal(model.energy(model.n_max), -9.33333333, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max, 2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(model.n_max, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.electrophilicity, 2.33970276, decimal=6)
    np.testing.assert_almost_equal(model.nucleofugality, -2.099047619, decimal=6)
    np.testing.assert_almost_equal(model.electrofugality, 2.64268585, decimal=6)
    # check grand potential (as a function of N)
    np.testing.assert_almost_equal(model.grand_potential(6.5), -5.2500304, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(7.91), -5.7468530, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(0.), -0.15, decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential(model.n_max), , decimal=6)
    # check grand potential derivative (as a function of N)
    # expected values based on derived formulas
    n0, a0, a1, b1 = 6.5, -0.15, -4.2, 0.45
    dE = lambda n, r: (-b1)**(r-1) * (a1 - a0*b1) * math.factorial(r) / (1 + b1*n)**(r+1)
    d2omega = lambda n: -1. / dE(n, 2)
    d3omega = lambda n: dE(n, 3) / dE(n, 2)**3
    # d4omega = lambda n: dE(n, 4) / dE(n, 2)**4 - (3 * dE(n, 3)**2) / dE(n, 2)**5
    # d5omega = lambda n: (dE(n, 5)/dE(n, 2)**5 - (10 * dE(n, 3) * dE(n, 4))/dE(n, 2)**6 +
    #                      (15 * dE(n, 3)**3)/dE(n, 2)**7)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6.5), -6.5, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(7.1, 1), -7.1, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(5.8, 2), d2omega(5.8),
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_derivative(0.0, 3), d3omega(0.0),
                                   decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(8.01, 4), d4omega(8.01),
    #                                decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(6.901, 5), d5omega(6.901),
    #                                decimal=6)
    # check mu to N conversion
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.2682461763), 6.5, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.2345757894), 7.105, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.1956803972), 7.99, decimal=6)
    np.testing.assert_almost_equal(model.convert_mu_to_n(-0.3568526811), 5.34, decimal=6)
    # check grand potential (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.26824617), -5.2500304, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.19153203), -5.8048876, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.20521256), -5.6965107, decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_derivative(model.n_max, 4), , decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.268246176), -5.2500304, decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu(-0.198782625), -5.7468530, decimal=6)
    # check grand potential derivative (as a function of mu)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(6.301, 1)), -6.301,
                                   decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(5.55, 1), 2),
                                   d2omega(5.55), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(6.99, 1), 3),
                                   d3omega(6.99), decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(7.1, 1), 4),
    #                                d4omega(7.1), decimal=6)
    # np.testing.assert_almost_equal(model.grand_potential_mu_derivative(dE(7.6, 1), 5),
    #                                d5omega(7.6), decimal=6)
    # check hyper-softnesses
    expected = 3.0 * (1 + b1 * n0)**5 / (4 * b1 * (a1 - a0 * b1)**2)
    np.testing.assert_almost_equal(model.hyper_softness(2), expected, decimal=5)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6.5, 3), -expected, decimal=5)
    expected = -15 * (1 + b1 * n0)**7 / (8 * b1 * (a1 - a0 * b1)**3)
    np.testing.assert_almost_equal(model.hyper_softness(3), expected, decimal=4)
    np.testing.assert_almost_equal(model.grand_potential_derivative(6.5, 4), -expected, decimal=4)


def test_global_general_energy_quadratic():
    # E(N) = 31.0 - 28.0 * N + 4.0 * N^2
    n, n0, a, b, c = sp.symbols('n, n0, a, b, c')
    expr = a + b * n + c * (n**2)
    model = GeneralGlobalTool(expr, 3.45, {2.1: -10.16, 2.5: -14.0, 4.3: -15.44}, n, n0)
    np.testing.assert_almost_equal(model.params[a], 31.0, decimal=6)
    np.testing.assert_almost_equal(model.params[b], -28.0, decimal=6)
    np.testing.assert_almost_equal(model.params[c], 4.0, decimal=6)
    np.testing.assert_almost_equal(model.n0, 3.45, decimal=6)
    np.testing.assert_almost_equal(model.n_max, 28. / (2 * 4.0), decimal=6)
    # check energy
    energy = lambda n: 31.0 - 28.0 * n + 4.0 * (n**2)
    np.testing.assert_almost_equal(model.energy(5.23), energy(5.23), decimal=6)
    np.testing.assert_almost_equal(model.energy(3.45), energy(3.45), decimal=6)
    np.testing.assert_almost_equal(model.energy(3.00), energy(3.0), decimal=6)
    # check energy derivatives
    deriv = lambda n: -28.0 + 8.0 * n
    np.testing.assert_almost_equal(model.energy_derivative(6.30), deriv(6.30), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(3.45), deriv(3.45), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(1.70), deriv(1.70), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(0.55, 2), 8.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(3.45, 2), 8.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(16.5, 2), 8.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(9.20, 3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(3.45, 4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(1.00, 5), 0.0, decimal=6)
    # check ionization potential and electron affinity
    ip = energy(2.45) - energy(3.45)
    ea = energy(3.45) - energy(4.45)
    np.testing.assert_almost_equal(model.ionization_potential, ip, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, ea, decimal=6)
    np.testing.assert_almost_equal(model.ip, ip, decimal=6)
    np.testing.assert_almost_equal(model.ea, ea, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, 0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.chemical_potential, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.mu, -0.5 * (ip + ea), decimal=6)
    np.testing.assert_almost_equal(model.eta, ip - ea, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.softness, 1.0 / (ip - ea), decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(2), 0.0, decimal=6)
    np.testing.assert_almost_equal(model.electrophilicity, (ip + ea)**2 / (8*(ip - ea)), decimal=6)
    np.testing.assert_almost_equal(model.nucleofugality, (ip - 3*ea)**2 / (8*(ip - ea)), decimal=6)
    np.testing.assert_almost_equal(model.electrofugality, (3*ip - ea)**2 / (8*(ip - ea)), decimal=6)
    # check grand potential
    grand = lambda n: energy(n) - deriv(n) * n
    np.testing.assert_almost_equal(model.grand_potential(15), grand(15), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(10), grand(10), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(20), grand(20), decimal=6)


def test_global_general_energy_exponential():
    # E(N) = 6.91 * exp(-0.25 * (N - 7.0)) + 2.74
    n, n0, a, b, gamma = sp.symbols('n, n0, A, B, gamma')
    expr = a * sp.exp(- gamma * (n - 7.0)) + b
    n_energies = {7.5: 8.838053596859556, 1.25: 31.832186639954763, 3.6: 18.906959746808596}
    model = GeneralGlobalTool(expr, 7.0, n_energies, n, n0)
    np.testing.assert_almost_equal(model.params[a], 6.91, decimal=6)
    np.testing.assert_almost_equal(model.params[b], 2.74, decimal=6)
    np.testing.assert_almost_equal(model.params[gamma], 0.25, decimal=6)
    np.testing.assert_almost_equal(model.n0, 7, decimal=6)
    np.testing.assert_almost_equal(model.n_max, float('inf'), decimal=6)
    # check energy
    energy = lambda n: 6.91 * math.exp(-0.25 * (n - 7.0)) + 2.74
    np.testing.assert_almost_equal(model.energy(20), energy(20), decimal=6)
    np.testing.assert_almost_equal(model.energy(10), energy(10), decimal=6)
    np.testing.assert_almost_equal(model.energy(8), energy(8), decimal=6)
    np.testing.assert_almost_equal(model.energy(16.5), energy(16.5), decimal=6)
    # check energy derivatives
    dE = lambda n, r: 6.91 * math.pow(-0.25, r) * math.exp(-0.25 * (n - 7))
    np.testing.assert_almost_equal(model.energy_derivative(18.1), dE(18.1, 1), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10), dE(10, 1), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(8.5), dE(8.5, 1), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(12.25), dE(12.25, 1), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(17.3, 2), dE(17.3, 2), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 2), dE(10, 2), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(9.1, 2), dE(9.1, 2), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(13.7, 3), dE(13.7, 3), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(10, 4), dE(10, 4), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(4.5, 5), dE(4.5, 5), decimal=6)
    np.testing.assert_almost_equal(model.energy_derivative(6.5, 10), dE(6.5, 10), decimal=6)
    # check ionization potential and electron affinity
    ip = energy(6) - energy(7)
    ea = energy(7) - energy(8)
    np.testing.assert_almost_equal(model.ionization_potential, ip, decimal=6)
    np.testing.assert_almost_equal(model.electron_affinity, ea, decimal=6)
    np.testing.assert_almost_equal(model.ip, ip, decimal=6)
    np.testing.assert_almost_equal(model.ea, ea, decimal=6)
    np.testing.assert_almost_equal(model.electronegativity, -dE(7, 1), decimal=6)
    np.testing.assert_almost_equal(model.electrophilicity, 6.91, decimal=6)
    np.testing.assert_almost_equal(model.nucleofugality, -(energy(8.0) - 2.74), decimal=6)
    np.testing.assert_almost_equal(model.electrofugality, energy(6.0) - 2.74, decimal=6)
    # check chemical potential, chemical hardness, and related tools
    np.testing.assert_almost_equal(model.chemical_potential, dE(7, 1), decimal=6)
    np.testing.assert_almost_equal(model.chemical_hardness, dE(7, 2), decimal=6)
    np.testing.assert_almost_equal(model.mu, dE(7, 1), decimal=6)
    np.testing.assert_almost_equal(model.eta, dE(7, 2), decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(2), dE(7, 3), decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(3), dE(7, 4), decimal=6)
    np.testing.assert_almost_equal(model.hyper_hardness(4), dE(7, 5), decimal=6)
    np.testing.assert_almost_equal(model.softness, 1.0/dE(7, 2), decimal=6)
    np.testing.assert_almost_equal(model.hyper_softness(2), -dE(7., 3)/dE(7, 2)**3, decimal=6)
    # check grand potential
    grand = lambda n: energy(n) - dE(n, 1) * n
    np.testing.assert_almost_equal(model.grand_potential(15), grand(15), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(10), grand(10), decimal=6)
    np.testing.assert_almost_equal(model.grand_potential(20), grand(20), decimal=6)


# def test_global_general_morse():
    # # E(N) = 4.01 * exp(-0.17 * (N - 17.0) + 0.32) + 6.95
    # n, n0, a, b, gamma, delta = sp.symbols('n, n0, A, B, gamma, delta')
    # expr = a * sp.exp(- gamma * (n - 4.0) + delta) + b
    # # energies = {1.0: 16.146208148459372, 4.0:12.472282334987188, 5.9:10.947988026968526,
    # #             7.7:9.894064887805316}
    # energies = {0.5:98.21717932504218, 4.2:55.606783873132294, 5.9:43.39452499661585,
    #             7.7:33.787260559941295}
    # model = GeneralGlobalTool(expr, 17.0, energies, n, n0)
    # print model._params
    # np.testing.assert_almost_equal(model._params[a], 4.01, decimal=6)
    # np.testing.assert_almost_equal(model._params[b], 6.95, decimal=6)
    # np.testing.assert_almost_equal(model._params[gamma], 0.17, decimal=6)
    # np.testing.assert_almost_equal(model._params[delta], 0.32, decimal=6)
    # np.testing.assert_almost_equal(model.n0, 7, decimal=6)
    # assert 5 == 6
    # pass
