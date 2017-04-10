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
"""Test chemtools.utils.utils."""

from chemtools.utils.utils import doc_inherit


def test_cubegen_o2_uhf():
    class Foo(object):
        """Dummy class for testing doc inheritance."""

        def foo(self):
            """Frobber."""
            pass

    class Bar(Foo):
        """Dummy class for testing doc inheritance."""

        @doc_inherit(Foo)
        def foo(self):
            pass

    assert Bar.foo.__doc__ == Bar().foo.__doc__
    assert Bar.foo.__doc__ == Foo.foo.__doc__
