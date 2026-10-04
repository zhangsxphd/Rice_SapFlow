#!/usr/bin/env python3
"""Script to build the full schematic for Main_Controller_V01 in EasyEDA Pro."""
import subprocess
import time

doc = "P1"
LIB_UUID = "0819f05c4eef4c71ace90d822a990e87"

# Components to place: (designator, deviceUuid, x, y)
parts = [
    # SuperMini Sockets
    ("U1_L", "fd554b15b6eb4d6f90f5fd338a8ff700", 300, 350),
    ("U1_R", "fd554b15b6eb4d6f90f5fd338a8ff700", 440, 350),
    # Power Decoupling
    ("C1", "10d64c167f5444958d3df43138306622", 220, 160),
    ("C2", "811c5a69fad14dfa85c1af699a12c275", 300, 160),
    ("C3", "10d64c167f5444958d3df43138306622", 400, 160),
    ("C4", "811c5a69fad14dfa85c1af699a12c275", 480, 160),
    # I2C Pullups
    ("R1", "dbf34257462145a8b9c176dda48ee0d3", 240, 560),
    ("R2", "dbf34257462145a8b9c176dda48ee0d3", 340, 560),
    # Heater Driver Circuit
    ("R3", "05d0a77e155a4444af700530d20b7037", 660, 320),
    ("Q1", "ce3bf8afe66241198c3f6478c6919622", 780, 340),
    ("R4", "ef1ead21c2cf41919cef1cee41664859", 740, 440),
    ("SJ1", "acd188b15a9c406bb9cb83c474d5327e", 720, 170),
    # FPC Connector
    ("J1", "eef1104d332248b18b1071e84caa5472", 700, 580),
    # Test Points
    ("TP1", "ef0e3a4b3bc942b1af34075e46c8eda8", 960, 180),
    ("TP2", "ef0e3a4b3bc942b1af34075e46c8eda8", 960, 250),
    ("TP3", "ef0e3a4b3bc942b1af34075e46c8eda8", 960, 320),
    ("TP4", "ef0e3a4b3bc942b1af34075e46c8eda8", 960, 390),
    ("TP5", "ef0e3a4b3bc942b1af34075e46c8eda8", 960, 460),
    ("TP6", "ef0e3a4b3bc942b1af34075e46c8eda8", 960, 530),
]

def main():
    print("Clearing page P1...")
    subprocess.run(["easyeda", "sch", "clear", "--doc", doc])
    time.sleep(0.1)

    print(f"Placing {len(parts)} schematic components...")
    for des, uuid, x, y in parts:
        cmd = [
            "easyeda", "sch", "place",
            "--doc", doc,
            "--lib", LIB_UUID,
            "--uuid", uuid,
            "--x", str(x), "--y", str(y),
            "--designator", des
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Placed {des} at ({x},{y}) ok")
        else:
            print(f"Err placing {des}: {res.stderr or res.stdout}")
        time.sleep(0.04)

if __name__ == "__main__":
    main()
