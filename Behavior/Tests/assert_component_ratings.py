from Utilities.Waveform.waveform_assertions import *

def assert_components(waveforms):
    assert_regulator(waveforms)

def assert_regulator(waveforms):
    # Max power, assuming I(R2) == I(OUT) from the regulator
    I_reg = waveforms['I(R2)']
    assert_bound(I_reg, 0, 1.1, label="Max regulator current")

    V_out = waveforms['V(out)']
    V_in = waveforms['V(n002)']

    V_drop = V_out - V_in
    P_out = I_reg * V_drop
    P_drive = I_reg / 60 * V_drop
    P_reg = P_out + P_drive

    # Approximate power limitation taken from Current limit vs In-out differential
    assert_bound(abs(P_reg), 0, 9, label="Regulator power dissipation")
