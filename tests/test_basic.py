#!/usr/bin/env python
import ncarglow as glow
import pytest
from pytest import approx
from datetime import datetime
import numpy as np


def test_simple():
    time = datetime(2015, 12, 13, 10, 0, 0)
    glat = 65.1
    glon = -147.5
    # %% flux [erg cm-2 s-1 == mW m-2 s-1]
    Q = 1
    # %% characteristic energy [eV]
    Echar = 100e3
    # %% Number of energy bins
    Nbins = 250

    try:
        iono = glow.simple(time, glat, glon, Q, Echar, Nbins)
    except ConnectionError:
        pytest.xfail('CI internet FTP issue')

    assert iono['alt_km'].size == Nbins
    assert iono['Tn'][32] == approx(186.0)
    assert iono['A5577'][32] == approx(18.74)


def test_ebins():
    time = datetime(2015, 12, 13, 10, 0, 0)
    glat = 65.1
    glon = -147.5
    # %% Energy grid [eV]
    Emin = 0.1
    Emax = 1e6
    E0 = 100e3
    Nbins = 250
    # %% monoenergetic beam
    Ebins = np.logspace(np.log10(Emin), np.log10(Emax), Nbins).astype(np.float32)
    Phitop = np.zeros_like(Ebins)
    Phitop[abs(Ebins-E0).argmin()] = 1.
    Phitop = Phitop.astype(np.float32)
    # %% run glow
    try:
        iono = glow.ebins(time, glat, glon, Ebins, Phitop)
    except ConnectionError:
        pytest.xfail('CI internet FTP issue')

    assert iono['alt_km'].size == Nbins
    assert iono['Tn'][32] == approx(186.0)
    assert iono['A5577'][32] == approx(0.04)


if __name__ == '__main__':
    pytest.main(['-x', __file__])
