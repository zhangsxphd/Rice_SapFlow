"""Compatibility entry point; see generate_full_package.py for the canonical builder."""
import sys
from generate_full_package import (
    add_edge_cuts_rect, get_or_create_net, add_track, add_silkscreen_text,
    build_main_controller, build_sensor_fpc, generate_kicad_pro, main,
)

if __name__ == "__main__":
    sys.exit(main())
