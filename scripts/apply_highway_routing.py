#!/usr/bin/env python3
"""Script to apply the zero-crossing, strictly ordered highway routing on Main_Controller_V01."""
import subprocess
import time

doc_uuid = "52caa9452ee66dee"

# First, clean up any existing SCL, SDA, and HEATER_EN test-branch tracks
# We can query all line IDs of SDA, SCL, HEATER_EN that we want to replace
def get_lines_to_delete():
    # Use easyeda CLI to list tracks and find those matching our nets
    res = subprocess.run(["easyeda", "pcb", "track-list", "--doc", doc_uuid], capture_output=True, text=True)
    import json
    data = json.loads(res.stdout)
    ids = []
    for line in data.get("result", {}).get("lines", []):
        net = line.get("net")
        if net in ["SCL", "SDA", "HEATER_EN"]:
            # Keep the local connections at R1/R2 and R3/R4/Q1, delete the inter-module highways
            sx, sy, ex, ey = line["startX"], line["startY"], line["endX"], line["endY"]
            # Delete if it reaches x > 4600 or crosses highway
            if max(sx, ex) > 4600 and min(sx, ex) < 5600:
                ids.append(line["primitiveId"])
            elif max(sx, ex) >= 5600:
                ids.append(line["primitiveId"])
    return ids

# Strictly ordered highways:
# 1. SDA highway at y = -4523.2
# connects U1_L pin 4 (4571.26, -4473.23) to TP4 (5728.3, -4626.0)
sda_tracks = [
    (4571.26, -4473.23, 4650.0, -4473.23, 1, 10.0, "SDA"),
    (4650.0, -4473.23, 4650.0, -4523.2, 1, 10.0, "SDA"),
    (4650.0, -4523.2, 5650.0, -4523.2, 1, 10.0, "SDA"),
    (5650.0, -4523.2, 5650.0, -4626.0, 1, 10.0, "SDA"),
    (5650.0, -4626.0, 5728.3, -4626.0, 1, 10.0, "SDA"),
]

# 2. SCL highway at y = -4623.2
# connects U1_L pin 5 (4571.26, -4573.23) to TP5 (5728.3, -4763.8)
scl_tracks = [
    (4571.26, -4573.23, 4680.0, -4573.23, 1, 10.0, "SCL"),
    (4680.0, -4573.23, 4680.0, -4623.2, 1, 10.0, "SCL"),
    (4680.0, -4623.2, 5620.0, -4623.2, 1, 10.0, "SCL"),
    (5620.0, -4623.2, 5620.0, -4763.8, 1, 10.0, "SCL"),
    (5620.0, -4763.8, 5728.3, -4763.8, 1, 10.0, "SCL"),
]

# 3. HEATER_EN highway at y = -4940.0
# connects U1_L pin 7 (4571.26, -4773.23) to R3 pin 1 (5380.91, -4822.83)
htr_en_tracks = [
    (4571.26, -4773.23, 4640.0, -4773.23, 1, 12.0, "HEATER_EN"),
    (4640.0, -4773.23, 4640.0, -4940.0, 1, 12.0, "HEATER_EN"),
    (4640.0, -4940.0, 5380.91, -4940.0, 1, 12.0, "HEATER_EN"),
    (5380.91, -4940.0, 5380.91, -4822.83, 1, 12.0, "HEATER_EN"),
]

def main():
    del_ids = get_lines_to_delete()
    print(f"Deleting {len(del_ids)} old track segments...")
    if del_ids:
        cmd = ["easyeda", "pcb", "track-delete", "--doc", doc_uuid, "--ids", ",".join(del_ids)]
        subprocess.run(cmd)
        time.sleep(0.1)

    all_new = sda_tracks + scl_tracks + htr_en_tracks
    print(f"Placing {len(all_new)} highway track segments...")
    for i, (x1, y1, x2, y2, layer, w, net) in enumerate(all_new):
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
            print(f"[{i+1}/{len(all_new)}] {net} ok")
        else:
            print(f"[{i+1}/{len(all_new)}] err: {res.stderr or res.stdout}")
        time.sleep(0.04)

if __name__ == "__main__":
    main()
