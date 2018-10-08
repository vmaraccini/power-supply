from Utilities.Waveform.waveform_assertions import *

def assert_components(waveforms):
    assert_regulator(waveforms)

def assert_regulator(waveforms):
    # Max power, assuming I(R2) == I(OUT) from the regulator
    I_reg = waveforms['I(R2)']
    assert_bound(I_reg, 0, 1.1)

    V_drop = waveforms['V(out)'] - waveforms['V(n002)']
    P_reg = I_reg * V_drop

    # Approximate power limitation taken from Current limit vs In-out differential
    assert_bound(abs(P_reg), 0, 9)
