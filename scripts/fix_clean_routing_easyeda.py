#!/usr/bin/env python3
"""Script to remove colliding tracks across U1_R and re-route with verified DRC clearance."""
import subprocess
import time

doc_uuid = "52caa9452ee66dee"

# Track IDs to delete (colliding segments)
to_delete = [
    # +5V colliding segment
    "b7247203aacd7182",
    # +3V3 colliding segments
    "a937bc3e8ff37ac9", "aa55683dda214d9d", "8cdb64f7a0759df6",
    # HEATER_EN colliding segments
    "ef36fe156230844d", "52358cfdc8000a4f", "993cb7539d298629",
    # SDA / SCL test point colliding branches
    "ea3dc1a9229bb31a", "2f100c79065b4bca", "32e747bc71df1943",
    "a7d9a23f3571671d", "9fd757dd6790d4a0", "f399ed770fa440d0",
]

# New clean tracks:
# 1. +5V north route (completely north of U1_R)
# from U1_L pin 1 (4571.3, -4173.2) -> (4571.3, -4080.0) -> (5523.6, -4080.0) -> (5523.6, -4212.6)
new_tracks = [
    (4571.3, -4173.2, 4571.3, -4080.0, 1, 15.0, "+5V"),
    (4571.3, -4080.0, 5523.6, -4080.0, 1, 15.0, "+5V"),
    (5523.6, -4080.0, 5523.6, -4212.6, 1, 15.0, "+5V"),
    (5523.6, -4212.6, 5523.6, -4330.7, 1, 15.0, "+5V"), # connects to SJ1 pin 3

    # 2. +3V3 route through channel between pin 2 and pin 3 (y = -4323.2)
    (4571.3, -4373.2, 4650.0, -4373.2, 1, 15.0, "+3V3"),
    (4650.0, -4373.2, 4650.0, -4323.2, 1, 15.0, "+3V3"),
    (4650.0, -4323.2, 5421.3, -4323.2, 1, 15.0, "+3V3"),
    (5421.3, -4323.2, 5421.3, -4330.7, 1, 15.0, "+3V3"), # connects to SJ1 pin 1

    # 3. HEATER_EN south route (completely south of U1_R, y = -4940)
    (4689.37, -4773.23, 4689.37, -4940.0, 1, 12.0, "HEATER_EN"),
    (4689.37, -4940.0, 5380.91, -4940.0, 1, 12.0, "HEATER_EN"),
    (5380.91, -4940.0, 5380.91, -4822.83, 1, 12.0, "HEATER_EN"), # connects to R3 pin 1

    # 4. SDA to TP4 through channel between pin 4 and pin 5 (y = -4523.2)
    (4571.26, -4473.23, 4650.0, -4473.23, 1, 10.0, "SDA"),
    (4650.0, -4473.23, 4650.0, -4523.2, 1, 10.0, "SDA"),
    (4650.0, -4523.2, 5650.0, -4523.2, 1, 10.0, "SDA"),
    (5650.0, -4523.2, 5650.0, -4626.0, 1, 10.0, "SDA"),
    (5650.0, -4626.0, 5728.3, -4626.0, 1, 10.0, "SDA"), # connects to TP4

    # 5. SCL to TP5 south route (y = -4960)
    (4571.26, -4573.23, 4620.0, -4573.23, 1, 10.0, "SCL"),
    (4620.0, -4573.23, 4620.0, -4965.0, 1, 10.0, "SCL"),
    (4620.0, -4965.0, 5680.0, -4965.0, 1, 10.0, "SCL"),
    (5680.0, -4965.0, 5680.0, -4763.8, 1, 10.0, "SCL"),
    (5680.0, -4763.8, 5728.3, -4763.8, 1, 10.0, "SCL"), # connects to TP5
]

def main():
    print("Deleting colliding tracks...")
    del_cmd = ["easyeda", "pcb", "track-delete", "--doc", doc_uuid, "--ids", ",".join(to_delete)]
    subprocess.run(del_cmd)
    time.sleep(0.1)

    print("\nAdding clean routes...")
    for i, (x1, y1, x2, y2, layer, w, net) in enumerate(new_tracks):
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
            print(f"[{i+1}/{len(new_tracks)}] {net} ok")
        else:
            print(f"[{i+1}/{len(new_tracks)}] err {net}: {res.stderr or res.stdout}")
        time.sleep(0.04)

if __name__ == "__main__":
    main()
