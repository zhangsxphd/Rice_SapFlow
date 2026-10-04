#!/usr/bin/env python3
"""Script to insert the validated KiCad routes into EasyEDA Pro."""
import json
import subprocess
import time

segs_mm = [
    # Already placed: (138.325, 122.5, 140.175, 122.5, 0.25, 1, "HEATER_GATE"),
    (136.6, 116.55, 138.0625, 116.55, 0.25, 1, "HEATER_GATE"),
    (136.6, 121.0, 136.6, 116.55, 0.25, 1, "HEATER_GATE"),
    (138.325, 121.0, 136.6, 121.0, 0.25, 1, "HEATER_GATE"),
    (138.325, 122.5, 138.325, 121.0, 0.25, 1, "HEATER_GATE"),
    (143.0, 125.2, 123.75, 125.2, 0.15, 1, "HEATER_RETURN"),
    (143.0, 117.5, 143.0, 125.2, 0.15, 1, "HEATER_RETURN"),
    (123.75, 125.2, 123.75, 130.85, 0.15, 1, "HEATER_RETURN"),
    (139.9375, 117.5, 143.0, 117.5, 0.15, 1, "HEATER_RETURN"),
    (109.675, 116.0, 109.675, 119.0, 0.25, 1, "+3V3"),
    (124.25, 129.9, 124.25, 130.85, 0.15, 1, "HEATER_VCC"),
    (139.0, 110.0, 139.0, 112.0, 0.25, 1, "HEATER_VCC"),
    (124.55, 129.5, 124.25, 129.9, 0.15, 1, "HEATER_VCC"),
    (139.0, 112.0, 136.0, 112.0, 0.25, 2, "HEATER_VCC"),  # B.Cu
    (136.0, 125.9, 124.55, 125.9, 0.25, 2, "HEATER_VCC"),  # B.Cu
    (136.0, 112.0, 136.0, 125.9, 0.25, 2, "HEATER_VCC"),  # B.Cu
    (124.55, 125.9, 124.55, 129.5, 0.25, 2, "HEATER_VCC"),  # B.Cu
    (111.325, 119.0, 114.11, 119.0, 0.25, 1, "SCL"),
    (114.11, 119.0, 116.11, 116.16, 0.25, 1, "SCL"),
    (111.325, 116.0, 114.11, 116.0, 0.25, 1, "SDA"),
    (114.11, 116.0, 116.11, 113.62, 0.25, 1, "SDA"),
    (134.675, 122.5, 136.675, 122.5, 0.25, 1, "HEATER_EN"),
    (119.11, 121.24, 134.675, 122.5, 0.25, 1, "HEATER_EN"),
    (116.11, 121.24, 119.11, 121.24, 0.25, 1, "HEATER_EN"),
]

def main():
    success = 0
    doc_uuid = "52caa9452ee66dee"
    for i, (x1, y1, x2, y2, w, layer, net) in enumerate(segs_mm):
        x1_mil = round(x1 / 25.4 * 1000, 2)
        y1_mil = round(-y1 / 25.4 * 1000, 2)
        x2_mil = round(x2 / 25.4 * 1000, 2)
        y2_mil = round(-y2 / 25.4 * 1000, 2)
        w_mil = round(w / 25.4 * 1000, 1)

        cmd = [
            "easyeda", "pcb", "track",
            "--doc", doc_uuid,
            "--x1", str(x1_mil),
            "--y1", str(y1_mil),
            "--x2", str(x2_mil),
            "--y2", str(y2_mil),
            "--layer", str(layer),
            "--width", str(w_mil),
            "--net", net
        ]
        res = subprocess.run(cmd, capture_output=True, text=True)
        if res.returncode == 0:
            success += 1
            print(f"[{i+1}/{len(segs_mm)}] Placed {net} ({layer}): ({x1_mil},{y1_mil}) -> ({x2_mil},{y2_mil})")
        else:
            print(f"[{i+1}/{len(segs_mm)}] FAILED {net}: {res.stderr or res.stdout}")
        time.sleep(0.05)

    print(f"\nDone: {success}/{len(segs_mm)} segments successfully routed.")

if __name__ == "__main__":
    main()
