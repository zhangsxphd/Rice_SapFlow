#!/usr/bin/env python3
"""Script to complete power rail connections and test points on Main_Controller_V01."""
import subprocess
import time

doc_uuid = "52caa9452ee66dee"

tracks = [
    # +5V rail
    # C1 (4293.3, -4173.2) -> C2 (4429.1, -4173.2) -> U1_L pin 1 (4571.3, -4173.2)
    (4293.3, -4173.2, 4571.3, -4173.2, 1, 15.0, "+5V"),
    # U1_L pin 1 -> branch to SJ1 pin 3 (5523.6, -4330.7)
    (4571.3, -4173.2, 5523.6, -4173.2, 1, 15.0, "+5V"),
    (5523.6, -4173.2, 5523.6, -4330.7, 1, 15.0, "+5V"),
    # TP1 (5728.3, -4212.6) stub to +5V branch
    (5523.6, -4212.6, 5728.3, -4212.6, 1, 12.0, "+5V"),

    # +3V3 rail
    # C3 (4293.3, -4370.1) -> C4 (4398.6, -4370.1) -> U1_L pin 3 (4571.3, -4373.2)
    (4293.3, -4370.1, 4429.1, -4370.1, 1, 15.0, "+3V3"),
    (4429.1, -4370.1, 4571.3, -4373.2, 1, 15.0, "+3V3"),
    # C3 to R1 pin 1 (4317.9, -4566.9)
    (4317.9, -4370.1, 4317.9, -4566.9, 1, 12.0, "+3V3"),
    # U1_L pin 3 -> SJ1 pin 1 (5421.3, -4330.7)
    (4571.3, -4373.2, 5421.3, -4373.2, 1, 15.0, "+3V3"),
    (5421.3, -4373.2, 5421.3, -4330.7, 1, 15.0, "+3V3"),
    # TP2 (5728.3, -4350.4) stub to SJ1 pin 1 / 3V3 branch
    (5421.3, -4350.4, 5728.3, -4350.4, 1, 12.0, "+3V3"),
    # J1 pin 1 (4970.5, -5151.6) to +3V3 via Bottom layer
    (4970.5, -5151.6, 4970.5, -5050.0, 1, 12.0, "+3V3"),

    # Test point stubs
    # TP6 (5728.3, -4901.6) to HEATER_RETURN trunk at (5629.92, -4901.6)
    (5629.92, -4901.6, 5728.3, -4901.6, 1, 12.0, "HEATER_RETURN"),
    # TP4 (5728.3, -4626.0) to SDA branch
    (4571.26, -4473.23, 5000.0, -4473.23, 1, 10.0, "SDA"),
    (5000.0, -4473.23, 5000.0, -4626.0, 1, 10.0, "SDA"),
    (5000.0, -4626.0, 5728.3, -4626.0, 1, 10.0, "SDA"),
    # TP5 (5728.3, -4763.8) to SCL branch
    (4571.26, -4573.23, 5050.0, -4573.23, 1, 10.0, "SCL"),
    (5050.0, -4573.23, 5050.0, -4763.8, 1, 10.0, "SCL"),
    (5050.0, -4763.8, 5728.3, -4763.8, 1, 10.0, "SCL"),
]

# GND Vias to tie top GND pads to bottom solid pour
gnd_vias = [
    # Near C1/C2 GND pads
    (4368.1, -4120.0),
    # Near C3/C4 GND pads
    (4368.1, -4420.0),
    # Near U1_L pin 2 GND
    (4650.0, -4273.2),
    # Near Q1 pin 2 & R4 pin 2 GND
    (5500.0, -4663.4),
    (5620.0, -4822.8),
    # Near J1 pin 2 GND
    (4950.8, -5080.0),
    # Near TP3 GND
    (5680.0, -4488.2),
]

def main():
    print("Adding power and signal tracks...")
    for i, (x1, y1, x2, y2, layer, w, net) in enumerate(tracks):
        cmd = [
            "easyeda", "pcb", "track",
            "--doc", doc_uuid,
            "--x1", str(x1), "--y1", str(y1),
            "--x2", str(x2), "--y2", str(y2),
            "--layer", str(layer), "--width", str(w),
            "--net", net
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Track {i+1}: {net} ({layer}) ok")
        else:
            print(f"Track {i+1} err: {res.stderr or res.stdout}")
        time.sleep(0.04)

    print("\nAdding GND stitching vias...")
    for i, (vx, vy) in enumerate(gnd_vias):
        cmd = [
            "easyeda", "pcb", "via",
            "--doc", doc_uuid,
            "--x", str(vx), "--y", str(vy),
            "--hole", "12", "--diameter", "24",
            "--net", "GND"
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            print(f"Via {i+1}: GND at ({vx}, {vy}) ok")
        else:
            print(f"Via {i+1} err: {res.stderr or res.stdout}")
        time.sleep(0.04)

if __name__ == "__main__":
    main()
