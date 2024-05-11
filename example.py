#!/usr/bin/env python3
# example.py
# https://ww1.microchip.com/downloads/aemDocuments/documents/OTH/ProductDocuments/DataSheets/22187E.pdf

import math
import smbus
import time

# I2C channel 1 is connected to the GPIO pins
channel = 1

#  MCP4725 defaults to address 0x60
address = 0x60

# Register addresses (with "normal mode" power-down bits)
reg_write_dac = 0x40

# Initialize I2C (SMBus)
bus = smbus.SMBus(channel)

# FIGURE 5-9 Byte 2 = [0  1  0  1  0, DAC1, DAC0, ~UDAC]
#                      C2 C1 C0 W1 W2
SEQ_WRITE = 0x50

# Bytes 3,4 repeats for each channel [VREF PD1 PD0 Gx D11 D10 D9 D8] A [D7 D6 D5 D4 D3 D2 D1 D0]

VREF_VDD = 0x00
VREF_INTERNAL = 0x80

PD_NORMAL = 0x00


Vref = VREF_VDD
Pd = PD_NORMAL

# Create a sawtooth wave 16 times
for i in range(0x10000):

    # Create our 12-bit number representing relative voltage

    # Sawtooth
    voltage = ((i & 0xfff) << 7) & 0xfff

    # Create sin wave
    # voltage_f = (math.sin(2.0*math.pi*i/200) * (2**11 - 1)) + 2**11
    # voltage = int(voltage_f)

    # Shift everything left by 4 bits and separate bytes
    # msg = (voltage & 0xff0) >> 4
    # msg = [msg, (msg & 0xf) << 4]

    # Write out I2C command: address, reg_write_dac, msg[0], msg[1]
    # bus.write_i2c_block_data(address, reg_write_dac, msg)

    msg = [SEQ_WRITE]

    msg.append(Vref | Pd | ((voltage & 0xf00) >> 8))
    msg.append((voltage & 0xff))

    voltage = ~voltage # channel B and D will be opposite A and C

    msg.append(Vref | Pd | ((voltage & 0xf00) >> 8))
    msg.append((voltage & 0xff))

    voltage = ~voltage

    msg.append(Vref | Pd | ((voltage & 0xf00) >> 8))
    msg.append((voltage & 0xff))

    voltage = ~voltage

    msg.append(Vref | Pd | ((voltage & 0xf00) >> 8))
    msg.append((voltage & 0xff))

    bus.write_i2c_block_data(address, msg[0], msg[1:])

    print("writing {} {}".format(i, voltage))
    
    time.sleep(0.02)
