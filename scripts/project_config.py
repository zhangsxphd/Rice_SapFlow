"""Shared project parameters. Physical prototype approval is still pending."""
from pathlib import Path

PROJECT_DIR = Path(__file__).resolve().parents[1]
OUTPUT_DIR = PROJECT_DIR
VARIANTS = (
    ("Sensor_FPC_2MM", 2.0, 36.0, 3.2),
    ("Sensor_FPC_3MM", 3.0, 40.0, 3.5),
    ("Sensor_FPC_4MM", 4.0, 45.0, 3.8),
)
TMP117_PINS = {"1": "SCL", "2": "GND", "3": None,
               "4": "ADD0", "5": "+3V3", "6": "SDA", "7": None}
FPC_PINS = {"1": "+3V3", "2": "GND", "3": "SDA", "4": "SCL",
            "5": "HEATER_VCC", "6": "HEATER_RETURN"}

# The existing SuperMini board identity and header orientation were not provided.
# Do not silently substitute a different clone's pinout or antenna keepout.
PHYSICAL_REVIEW_REQUIRED = (
    "Confirm the actual SuperMini model, 17.78 mm header spacing and pin order; "
    "the reference 18 mm wide module uses a different header arrangement.",
    "Confirm FH12 bottom-contact orientation, FPC mating width, contact length "
    "and total inserted thickness against the supplier drawing.",
    "Validate heater power, pulse duration and plant temperature rise with a "
    "calibrated prototype; PRF18 is a sensing thermistor, not a qualified heater.",
    "Finish routing and supply return paths; obtain schematic/PCB parity and "
    "native EasyEDA save/reload/readback/ERC/DRC evidence.",
)
