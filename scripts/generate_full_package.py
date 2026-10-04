import os
import sys
import subprocess
import zipfile
import csv
import json
import argparse
from pathlib import Path
from project_config import OUTPUT_DIR, VARIANTS, PHYSICAL_REVIEW_REQUIRED
import pcbnew
import wx
_WX_APP = None

FOOTPRINT_BASE = os.environ.get('KICAD_FOOTPRINT_DIR', '/Applications/KiCad/KiCad.app/Contents/SharedSupport/footprints/')
ROOT_DIR = str(OUTPUT_DIR)
KICAD_CLI = os.environ.get('KICAD_CLI', '/Applications/KiCad/KiCad.app/Contents/MacOS/kicad-cli')

def add_edge_cuts_rect(board, x0, y0, x1, y1, radius=1.0):
    x0_i = pcbnew.FromMM(x0)
    y0_i = pcbnew.FromMM(y0)
    x1_i = pcbnew.FromMM(x1)
    y1_i = pcbnew.FromMM(y1)
    r_i = pcbnew.FromMM(radius)

    pts = [
        # Top edge
        (pcbnew.VECTOR2I(x0_i + r_i, y0_i), pcbnew.VECTOR2I(x1_i - r_i, y0_i)),
        # Right edge
        (pcbnew.VECTOR2I(x1_i, y0_i + r_i), pcbnew.VECTOR2I(x1_i, y1_i - r_i)),
        # Bottom edge
        (pcbnew.VECTOR2I(x1_i - r_i, y1_i), pcbnew.VECTOR2I(x0_i + r_i, y1_i)),
        # Left edge
        (pcbnew.VECTOR2I(x0_i, y1_i - r_i), pcbnew.VECTOR2I(x0_i, y0_i + r_i)),
        # Corners (clean 45-deg chamfer)
        (pcbnew.VECTOR2I(x1_i - r_i, y0_i), pcbnew.VECTOR2I(x1_i, y0_i + r_i)),
        (pcbnew.VECTOR2I(x1_i, y1_i - r_i), pcbnew.VECTOR2I(x1_i - r_i, y1_i)),
        (pcbnew.VECTOR2I(x0_i + r_i, y1_i), pcbnew.VECTOR2I(x0_i, y1_i - r_i)),
        (pcbnew.VECTOR2I(x0_i, y0_i + r_i), pcbnew.VECTOR2I(x0_i + r_i, y0_i)),
    ]
    for p_start, p_end in pts:
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetStart(p_start)
        seg.SetEnd(p_end)
        seg.SetWidth(pcbnew.FromMM(0.1))
        board.Add(seg)

def get_or_create_net(board, net_name):
    net = board.FindNet(net_name)
    if net is None:
        net = pcbnew.NETINFO_ITEM(board, net_name)
        board.Add(net)
    return net

def add_track(board, start_pos, end_pos, layer, width_mm, net=None):
    t = pcbnew.PCB_TRACK(board)
    t.SetStart(start_pos)
    t.SetEnd(end_pos)
    t.SetLayer(layer)
    t.SetWidth(pcbnew.FromMM(width_mm))
    if net:
        t.SetNet(net)
    board.Add(t)
    return t

def add_silkscreen_text(board, text, x_mm, y_mm, size_mm=1.0, layer=pcbnew.F_SilkS):
    t = pcbnew.PCB_TEXT(board)
    t.SetText(text)
    t.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_mm), pcbnew.FromMM(y_mm)))
    t.SetLayer(layer)
    t.SetTextSize(pcbnew.VECTOR2I(pcbnew.FromMM(size_mm), pcbnew.FromMM(size_mm)))
    t.SetTextThickness(pcbnew.FromMM(0.15))
    board.Add(t)
    return t

def build_main_controller(output_path):
    print("Generating Main_Controller_V01 PCB...")
    board = pcbnew.BOARD()

    # Nets
    net_gnd = get_or_create_net(board, "GND")
    net_5v = get_or_create_net(board, "+5V")
    net_3v3 = get_or_create_net(board, "+3V3")
    net_sda = get_or_create_net(board, "SDA")
    net_scl = get_or_create_net(board, "SCL")
    net_htr_en = get_or_create_net(board, "HEATER_EN")
    net_htr_gate = get_or_create_net(board, "HEATER_GATE")
    net_htr_vcc = get_or_create_net(board, "HEATER_VCC")
    net_htr_ret = get_or_create_net(board, "HEATER_RETURN")
    net_gpio10 = get_or_create_net(board, "GPIO10_RES")

    # Board Outline (50.0 x 32.0 mm)
    x0, y0 = 100.0, 100.0
    x1, y1 = 150.0, 132.0
    add_edge_cuts_rect(board, x0, y0, x1, y1, radius=1.0)

    # Silkscreen text (Centered at top edge, clear of all parts)
    add_silkscreen_text(board, "Rice_SapFlow_V01", 117.0, 102.5, size_mm=1.0)
    add_silkscreen_text(board, "Main_Controller_V1.0", 117.0, 104.0, size_mm=0.75)

    # Mounting Holes M3
    hole_lib = os.path.join(FOOTPRINT_BASE, 'MountingHole.pretty')
    holes_pos = [(104.0, 104.0), (146.0, 104.0), (104.0, 128.0), (146.0, 128.0)]
    for i, (hx, hy) in enumerate(holes_pos):
        h = pcbnew.FootprintLoad(hole_lib, 'MountingHole_3.2mm_M3')
        h.SetReference(f"H{i+1}")
        h.SetValue("M3")
        h.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(hx), pcbnew.FromMM(hy)))
        board.Add(h)

    # ESP32-C3 Super Mini Socket (2x 1x8 2.54mm female header socket)
    sock_lib = os.path.join(FOOTPRINT_BASE, 'Connector_PinSocket_2.54mm.pretty')
    u1_left = pcbnew.FootprintLoad(sock_lib, 'PinSocket_1x08_P2.54mm_Vertical')
    u1_left.SetReference("U1_L")
    u1_left.SetValue("SuperMini_L")
    u1_left.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(116.11), pcbnew.FromMM(106.0)))
    u1_left.Reference().SetVisible(False)
    u1_left.Value().SetVisible(False)
    board.Add(u1_left)

    u1_right = pcbnew.FootprintLoad(sock_lib, 'PinSocket_1x08_P2.54mm_Vertical')
    u1_right.SetReference("U1_R")
    u1_right.SetValue("SuperMini_R")
    u1_right.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(133.89), pcbnew.FromMM(106.0)))
    u1_right.Reference().SetVisible(False)
    u1_right.Value().SetVisible(False)
    board.Add(u1_right)
    add_silkscreen_text(board, "ESP32-C3 SuperMini", 117.5, 107.0, size_mm=0.8)

    u1_l_nets = {'1': net_5v, '2': net_gnd, '3': net_3v3, '4': net_sda, '5': net_scl, '7': net_htr_en}
    for p in u1_left.Pads():
        if p.GetNumber() in u1_l_nets:
            p.SetNet(u1_l_nets[p.GetNumber()])

    for p in u1_right.Pads():
        if p.GetNumber() == '6':  # Pin 14 of Super Mini is IO10 Reserved
            p.SetNet(net_gpio10)

    # Decoupling Capacitors
    c_lib = os.path.join(FOOTPRINT_BASE, 'Capacitor_SMD.pretty')
    c1 = pcbnew.FootprintLoad(c_lib, 'C_0805_2012Metric')
    c1.SetReference("C1")
    c1.SetValue("10uF")
    c1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(110.0), pcbnew.FromMM(106.0)))
    for p in c1.Pads():
        if p.GetNumber() == '1': p.SetNet(net_5v)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
    board.Add(c1)

    c2 = pcbnew.FootprintLoad(c_lib, 'C_0603_1608Metric')
    c2.SetReference("C2")
    c2.SetValue("100nF")
    c2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(112.5), pcbnew.FromMM(108.5)))
    for p in c2.Pads():
        if p.GetNumber() == '1': p.SetNet(net_5v)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
    board.Add(c2)

    c3 = pcbnew.FootprintLoad(c_lib, 'C_0805_2012Metric')
    c3.SetReference("C3")
    c3.SetValue("10uF")
    c3.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(110.0), pcbnew.FromMM(111.0)))
    for p in c3.Pads():
        if p.GetNumber() == '1': p.SetNet(net_3v3)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
    board.Add(c3)

    c4 = pcbnew.FootprintLoad(c_lib, 'C_0603_1608Metric')
    c4.SetReference("C4")
    c4.SetValue("100nF")
    c4.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(112.5), pcbnew.FromMM(113.5)))
    for p in c4.Pads():
        if p.GetNumber() == '1': p.SetNet(net_3v3)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
    board.Add(c4)

    # I2C Pull-Up Resistors R1 & R2 (4.7k 0603 to 3.3V)
    r_lib = os.path.join(FOOTPRINT_BASE, 'Resistor_SMD.pretty')
    r1 = pcbnew.FootprintLoad(r_lib, 'R_0603_1608Metric')
    r1.SetReference("R1")
    r1.SetValue("4.7k")
    r1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(110.5), pcbnew.FromMM(116.0)))
    for p in r1.Pads():
        if p.GetNumber() == '1': p.SetNet(net_3v3)
        elif p.GetNumber() == '2': p.SetNet(net_sda)
    board.Add(r1)

    r2 = pcbnew.FootprintLoad(r_lib, 'R_0603_1608Metric')
    r2.SetReference("R2")
    r2.SetValue("4.7k")
    r2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(110.5), pcbnew.FromMM(119.0)))
    for p in r2.Pads():
        if p.GetNumber() == '1': p.SetNet(net_3v3)
        elif p.GetNumber() == '2': p.SetNet(net_scl)
    board.Add(r2)

    # Solder Jumper SJ1 (3-pad: 1=3.3V, 2=HEATER_VCC, 3=5V)
    jmp_lib = os.path.join(FOOTPRINT_BASE, 'Jumper.pretty')
    sj1 = pcbnew.FootprintLoad(jmp_lib, 'SolderJumper-3_P1.3mm_Open_Pad1.0x1.5mm_NumberLabels')
    sj1.SetReference("SJ1")
    sj1.SetValue("3V3/5V")
    sj1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(139.0), pcbnew.FromMM(110.0)))
    for p in sj1.Pads():
        if p.GetNumber() == '1': p.SetNet(net_3v3)
        elif p.GetNumber() == '2': p.SetNet(net_htr_vcc)
        elif p.GetNumber() == '3': p.SetNet(net_5v)
    board.Add(sj1)
    add_silkscreen_text(board, "SJ1: 1=3V3 2=VCC 3=5V", 132.5, 107.2, size_mm=0.65)

    # AO3400A Low-Side Switch Circuit
    sot_lib = os.path.join(FOOTPRINT_BASE, 'Package_TO_SOT_SMD.pretty')
    q1 = pcbnew.FootprintLoad(sot_lib, 'SOT-23')
    q1.SetReference("Q1")
    q1.SetValue("AO3400A")
    q1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(139.0), pcbnew.FromMM(117.5)))
    for p in q1.Pads():
        if p.GetNumber() == '1': p.SetNet(net_htr_gate)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
        elif p.GetNumber() == '3': p.SetNet(net_htr_ret)
    board.Add(q1)

    r3 = pcbnew.FootprintLoad(r_lib, 'R_0603_1608Metric')
    r3.SetReference("R3")
    r3.SetValue("100R")
    r3.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(137.5), pcbnew.FromMM(122.5)))
    for p in r3.Pads():
        if p.GetNumber() == '1': p.SetNet(net_htr_en)
        elif p.GetNumber() == '2': p.SetNet(net_htr_gate)
    board.Add(r3)

    r4 = pcbnew.FootprintLoad(r_lib, 'R_0603_1608Metric')
    r4.SetReference("R4")
    r4.SetValue("100k")
    r4.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(141.0), pcbnew.FromMM(122.5)))
    for p in r4.Pads():
        if p.GetNumber() == '1': p.SetNet(net_htr_gate)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
    board.Add(r4)

    # FPC Connector J1 (6P 0.5mm Horizontal Flip-Lock)
    fpc_lib = os.path.join(FOOTPRINT_BASE, 'Connector_FFC-FPC.pretty')
    j1 = pcbnew.FootprintLoad(fpc_lib, 'Hirose_FH12-6S-0.5SH_1x06-1MP_P0.50mm_Horizontal')
    j1.SetReference("J1")
    j1.SetValue("FPC-0.5-6P")
    j1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(125.0), pcbnew.FromMM(129.0)))
    j1.SetOrientationDegrees(180)
    j1_nets = {
        '1': net_3v3, '2': net_gnd, '3': net_sda, '4': net_scl, '5': net_htr_vcc, '6': net_htr_ret, 'MP': net_gnd
    }
    for p in j1.Pads():
        if p.GetNumber() in j1_nets:
            p.SetNet(j1_nets[p.GetNumber()])
    board.Add(j1)
    add_silkscreen_text(board, "J1: 1=3V3 2=GND 3=SDA 4=SCL 5=VCC 6=RET", 108.5, 126.5, size_mm=0.65)

    # Test Points TP1 to TP6
    tp_lib = os.path.join(FOOTPRINT_BASE, 'TestPoint.pretty')
    tps = [
        ("TP1", "5V", net_5v, 145.5, 108.5),
        ("TP2", "3V3", net_3v3, 145.5, 110.5),
        ("TP3", "GND", net_gnd, 145.5, 114.0),
        ("TP4", "SDA", net_sda, 145.5, 117.5),
        ("TP5", "SCL", net_scl, 145.5, 121.0),
        ("TP6", "HTR_RET", net_htr_ret, 145.5, 123.5),
    ]
    for ref, val, net, tpx, tpy in tps:
        tp = pcbnew.FootprintLoad(tp_lib, 'TestPoint_Pad_D1.0mm')
        tp.SetReference(ref)
        tp.SetValue(val)
        tp.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(tpx), pcbnew.FromMM(tpy)))
        for p in tp.Pads():
            p.SetNet(net)
        board.Add(tp)
        add_silkscreen_text(board, val, tpx - 3.2, tpy - 0.4, size_mm=0.7)

    # Traces & Routing
    p_3v3_r1 = r1.FindPadByNumber('1').GetPosition()
    p_3v3_r2 = r2.FindPadByNumber('1').GetPosition()
    add_track(board, p_3v3_r1, p_3v3_r2, pcbnew.F_Cu, 0.25, net_3v3)

    p_sda_r1 = r1.FindPadByNumber('2').GetPosition()
    p_u1_sda = u1_left.FindPadByNumber('4').GetPosition()
    add_track(board, p_sda_r1, pcbnew.VECTOR2I(p_u1_sda.x - pcbnew.FromMM(2.0), p_sda_r1.y), pcbnew.F_Cu, 0.25, net_sda)
    add_track(board, pcbnew.VECTOR2I(p_u1_sda.x - pcbnew.FromMM(2.0), p_sda_r1.y), p_u1_sda, pcbnew.F_Cu, 0.25, net_sda)

    p_scl_r2 = r2.FindPadByNumber('2').GetPosition()
    p_u1_scl = u1_left.FindPadByNumber('5').GetPosition()
    add_track(board, p_scl_r2, pcbnew.VECTOR2I(p_u1_scl.x - pcbnew.FromMM(2.0), p_scl_r2.y), pcbnew.F_Cu, 0.25, net_scl)
    add_track(board, pcbnew.VECTOR2I(p_u1_scl.x - pcbnew.FromMM(2.0), p_scl_r2.y), p_u1_scl, pcbnew.F_Cu, 0.25, net_scl)

    # Heater Gate
    p_u1_htr_en = u1_left.FindPadByNumber('7').GetPosition()
    p_r3_in = r3.FindPadByNumber('1').GetPosition()
    add_track(board, p_u1_htr_en, pcbnew.VECTOR2I(p_u1_htr_en.x + pcbnew.FromMM(3.0), p_u1_htr_en.y), pcbnew.F_Cu, 0.25, net_htr_en)
    add_track(board, pcbnew.VECTOR2I(p_u1_htr_en.x + pcbnew.FromMM(3.0), p_u1_htr_en.y), pcbnew.VECTOR2I(p_r3_in.x - pcbnew.FromMM(2.0), p_r3_in.y), pcbnew.F_Cu, 0.25, net_htr_en)
    add_track(board, pcbnew.VECTOR2I(p_r3_in.x - pcbnew.FromMM(2.0), p_r3_in.y), p_r3_in, pcbnew.F_Cu, 0.25, net_htr_en)

    p_r3_out = r3.FindPadByNumber('2').GetPosition()
    p_r4_gate = r4.FindPadByNumber('1').GetPosition()
    p_q1_gate = q1.FindPadByNumber('1').GetPosition()
    add_track(board, p_r3_out, p_r4_gate, pcbnew.F_Cu, 0.25, net_htr_gate)
    gate_path = [p_r3_out,
                 pcbnew.VECTOR2I(p_r3_out.x, pcbnew.FromMM(121.0)),
                 pcbnew.VECTOR2I(pcbnew.FromMM(136.6), pcbnew.FromMM(121.0)),
                 pcbnew.VECTOR2I(pcbnew.FromMM(136.6), p_q1_gate.y), p_q1_gate]
    for a, b in zip(gate_path, gate_path[1:]):
        add_track(board, a, b, pcbnew.F_Cu, 0.25, net_htr_gate)

    # Real pad fanout: the 0.5 mm connector cannot accept 0.635 mm traces.
    # A 470 ohm heater draws nominally 10.6 mA at 5 V; 0.25 mm trunks
    # and 0.15 mm connector fanout are adequate electrically (thermal test pending).
    p_sj1_vcc = sj1.FindPadByNumber('2').GetPosition()
    p_j1_vcc = j1.FindPadByNumber('5').GetPosition()
    vcc_via = pcbnew.VECTOR2I(p_sj1_vcc.x, pcbnew.FromMM(112.0))
    j1_via = pcbnew.VECTOR2I(p_j1_vcc.x + pcbnew.FromMM(0.3), pcbnew.FromMM(129.5))
    for pos in (vcc_via, j1_via):
        via = pcbnew.PCB_VIA(board)
        via.SetPosition(pos)
        via.SetWidth(pcbnew.FromMM(0.6))
        via.SetDrill(pcbnew.FromMM(0.3))
        via.SetLayerPair(pcbnew.F_Cu, pcbnew.B_Cu)
        via.SetNet(net_htr_vcc)
        board.Add(via)
    add_track(board, p_sj1_vcc, vcc_via, pcbnew.F_Cu, 0.25, net_htr_vcc)
    vcc_path = [vcc_via,
                pcbnew.VECTOR2I(pcbnew.FromMM(136.0), vcc_via.y),
                pcbnew.VECTOR2I(pcbnew.FromMM(136.0), pcbnew.FromMM(125.9)),
                pcbnew.VECTOR2I(j1_via.x, pcbnew.FromMM(125.9)), j1_via]
    for a, b in zip(vcc_path, vcc_path[1:]):
        add_track(board, a, b, pcbnew.B_Cu, 0.25, net_htr_vcc)
    escape = pcbnew.VECTOR2I(p_j1_vcc.x, pcbnew.FromMM(129.9))
    add_track(board, j1_via, escape, pcbnew.F_Cu, 0.15, net_htr_vcc)
    add_track(board, escape, p_j1_vcc, pcbnew.F_Cu, 0.15, net_htr_vcc)

    p_q1_drain = q1.FindPadByNumber('3').GetPosition()
    p_j1_ret = j1.FindPadByNumber('6').GetPosition()
    return_path = [p_q1_drain,
                   pcbnew.VECTOR2I(pcbnew.FromMM(143.0), p_q1_drain.y),
                   pcbnew.VECTOR2I(pcbnew.FromMM(143.0), pcbnew.FromMM(125.2)),
                   pcbnew.VECTOR2I(p_j1_ret.x, pcbnew.FromMM(125.2)),
                   p_j1_ret]
    for a, b in zip(return_path, return_path[1:]):
        add_track(board, a, b, pcbnew.F_Cu, 0.15, net_htr_ret)

    # Bottom GND Plane
    zone_gnd = pcbnew.ZONE(board)
    zone_gnd.SetNet(net_gnd)
    zone_gnd.SetLayer(pcbnew.B_Cu)
    chain = pcbnew.SHAPE_LINE_CHAIN()
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x0 + 0.5), pcbnew.FromMM(y0 + 0.5)))
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x1 - 0.5), pcbnew.FromMM(y0 + 0.5)))
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x1 - 0.5), pcbnew.FromMM(y1 - 0.5)))
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x0 + 0.5), pcbnew.FromMM(y1 - 0.5)))
    chain.SetClosed(True)
    poly = pcbnew.SHAPE_POLY_SET()
    poly.AddOutline(chain)
    zone_gnd.SetOutline(poly)
    board.Add(zone_gnd)

    pcbnew.SaveBoard(output_path, board)
    print(f"Main_Controller_V01 saved to {output_path}")

def build_sensor_fpc(variant_name, spacing_mm, probe_len_mm, probe_w_mm, output_path):
    print(f"Generating {variant_name} (pitch={spacing_mm}mm, length={probe_len_mm}mm)...")
    board = pcbnew.BOARD()

    net_gnd = get_or_create_net(board, "GND")
    net_3v3 = get_or_create_net(board, "+3V3")
    net_sda = get_or_create_net(board, "SDA")
    net_scl = get_or_create_net(board, "SCL")
    net_htr_vcc = get_or_create_net(board, "HEATER_VCC")
    net_htr_ret = get_or_create_net(board, "HEATER_RETURN")

    # Board Outline (Lance Needle with Tapered Tip & Stiffened Tail)
    x_tail_start = 100.0
    x_tail_end = 108.0
    x_tip = x_tail_start + probe_len_mm
    x_probe_end = x_tip - 3.0
    half_w = probe_w_mm / 2.0
    y_center = 100.0
    y_top = y_center - half_w
    y_bot = y_center + half_w

    probe_pts = [
        # Tail
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_start), pcbnew.FromMM(y_center - 1.8)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end), pcbnew.FromMM(y_center - 1.8))),
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end), pcbnew.FromMM(y_center - 1.8)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end + 1.0), pcbnew.FromMM(y_top))),
        # Top lance edge
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end + 1.0), pcbnew.FromMM(y_top)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_probe_end), pcbnew.FromMM(y_top))),
        # Tapered needle tip
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_probe_end), pcbnew.FromMM(y_top)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_tip), pcbnew.FromMM(y_center))),
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_tip), pcbnew.FromMM(y_center)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_probe_end), pcbnew.FromMM(y_bot))),
        # Bottom lance edge
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_probe_end), pcbnew.FromMM(y_bot)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end + 1.0), pcbnew.FromMM(y_bot))),
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end + 1.0), pcbnew.FromMM(y_bot)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end), pcbnew.FromMM(y_center + 1.8))),
        # Tail bottom edge
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_end), pcbnew.FromMM(y_center + 1.8)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_start), pcbnew.FromMM(y_center + 1.8))),
        # Tail left edge
        (pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_start), pcbnew.FromMM(y_center + 1.8)),
         pcbnew.VECTOR2I(pcbnew.FromMM(x_tail_start), pcbnew.FromMM(y_center - 1.8))),
    ]
    for p_start, p_end in probe_pts:
        seg = pcbnew.PCB_SHAPE(board)
        seg.SetShape(pcbnew.SHAPE_T_SEGMENT)
        seg.SetLayer(pcbnew.Edge_Cuts)
        seg.SetStart(p_start)
        seg.SetEnd(p_end)
        seg.SetWidth(pcbnew.FromMM(0.1))
        board.Add(seg)

    # 1. Gold Finger Connector J1_FPC (6P 0.5mm)
    fp_tail = pcbnew.FOOTPRINT(board)
    fp_tail.SetReference("J1_FPC")
    fp_tail.SetValue("GoldFinger_6P")
    fp_tail.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(103.5), pcbnew.FromMM(y_center)))
    fp_tail.Reference().SetVisible(False)
    fp_tail.Value().SetVisible(False)

    pin_nets = [net_3v3, net_gnd, net_sda, net_scl, net_htr_vcc, net_htr_ret]
    for i in range(6):
        pad = pcbnew.PAD(fp_tail)
        pad.SetNumber(str(i + 1))
        pad.SetShape(pcbnew.PAD_SHAPE_RECT)
        pad.SetSize(pcbnew.VECTOR2I(pcbnew.FromMM(2.5), pcbnew.FromMM(0.30)))
        pad.SetAttribute(pcbnew.PAD_ATTRIB_SMD)
        lset = pcbnew.LSET()
        lset.AddLayer(pcbnew.F_Cu)
        lset.AddLayer(pcbnew.F_Mask)  # Exposed ENIG Gold Finger
        pad.SetLayerSet(lset)
        pad_y = (i - 2.5) * 0.50
        pad.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(103.5), pcbnew.FromMM(y_center + pad_y)))
        pad.SetNet(pin_nets[i])
        fp_tail.Add(pad)
    board.Add(fp_tail)

    add_silkscreen_text(board, "1", 101.5, y_center - 1.25, size_mm=0.8, layer=pcbnew.F_Fab)
    add_silkscreen_text(board, "6", 101.5, y_center + 1.25, size_mm=0.8, layer=pcbnew.F_Fab)

    # 2. Sensing Components Placement along plant sap flow:
    # Linear order: TMP117_UP (U1) -> PTC (R_HEAT) -> TMP117_DOWN (U2)
    # Center PTC at x = 122.0 mm
    x_ptc = 122.0
    x_up = x_ptc - spacing_mm
    x_down = x_ptc + spacing_mm

    son_lib = os.path.join(FOOTPRINT_BASE, 'Package_SON.pretty')
    r_lib = os.path.join(FOOTPRINT_BASE, 'Resistor_SMD.pretty')
    c_lib = os.path.join(FOOTPRINT_BASE, 'Capacitor_SMD.pretty')

    # A. TMP117_UP (U1, address 0x48, ADD0 -> GND)
    u1 = pcbnew.FootprintLoad(son_lib, 'WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm')
    u1.SetReference("U1")
    u1.SetValue("TMP117_UP")
    u1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_up), pcbnew.FromMM(y_center)))
    u1.SetOrientationDegrees(90)
    u1.Reference().SetVisible(False)
    u1.Value().SetVisible(False)

    # Remove paste apertures and retain floating thermal pad
    pads_to_remove = []
    for p in u1.Pads():
        p_num = p.GetNumber()
        if p_num == '':
            pads_to_remove.append(p)
        elif p_num == '1': p.SetNet(net_scl)
        elif p_num == '2': p.SetNet(net_gnd)
        elif p_num == '4': p.SetNet(net_gnd)  # ADD0 -> GND => 0x48
        elif p_num == '5': p.SetNet(net_3v3)
        elif p_num == '6': p.SetNet(net_sda)
        elif p_num == '7':
            # Exposed Thermal Pad: ensure NO paste, NO net (floating)
            lset = p.GetLayerSet()
            if lset.Contains(pcbnew.F_Paste):
                lset.RemoveLayer(pcbnew.F_Paste)
                p.SetLayerSet(lset)
    for p in pads_to_remove:
        u1.Remove(p)
    board.Add(u1)
    add_silkscreen_text(board, "UP", x_up - 0.5, y_center - 1.25, size_mm=0.8, layer=pcbnew.F_Fab)

    # Decoupling Cap C1 (100nF 0402) for U1
    c1 = pcbnew.FootprintLoad(c_lib, 'C_0402_1005Metric')
    c1.SetReference("C1")
    c1.SetValue("100nF")
    c1.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_up - 1.8), pcbnew.FromMM(y_center)))
    c1.SetOrientationDegrees(90)
    c1.Reference().SetVisible(False)
    c1.Value().SetVisible(False)
    for p in c1.Pads():
        if p.GetNumber() == '1': p.SetNet(net_3v3)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
    board.Add(c1)

    # B. PRF18BC471QB5RB PTC Heater (R_HEAT, 0603, 470 ohm)
    r_heat = pcbnew.FootprintLoad(r_lib, 'R_0603_1608Metric')
    r_heat.SetReference("R_HEAT")
    r_heat.SetValue("PTC_470R")
    r_heat.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_ptc), pcbnew.FromMM(y_center)))
    r_heat.SetOrientationDegrees(90)
    r_heat.Reference().SetVisible(False)
    r_heat.Value().SetVisible(False)
    for p in r_heat.Pads():
        if p.GetNumber() == '1': p.SetNet(net_htr_vcc)
        elif p.GetNumber() == '2': p.SetNet(net_htr_ret)
    board.Add(r_heat)
    add_silkscreen_text(board, "PTC", x_ptc - 0.7, y_center - 1.25, size_mm=0.8, layer=pcbnew.F_Fab)

    # C. TMP117_DOWN (U2, address 0x49, ADD0 -> 3.3V)
    u2 = pcbnew.FootprintLoad(son_lib, 'WSON-6-1EP_2x2mm_P0.65mm_EP1x1.6mm')
    u2.SetReference("U2")
    u2.SetValue("TMP117_DN")
    u2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_down), pcbnew.FromMM(y_center)))
    u2.SetOrientationDegrees(90)
    u2.Reference().SetVisible(False)
    u2.Value().SetVisible(False)

    pads_to_remove = []
    for p in u2.Pads():
        p_num = p.GetNumber()
        if p_num == '':
            pads_to_remove.append(p)
        elif p_num == '1': p.SetNet(net_scl)
        elif p_num == '2': p.SetNet(net_gnd)
        elif p_num == '4': p.SetNet(net_3v3)  # ADD0 -> 3.3V => 0x49
        elif p_num == '5': p.SetNet(net_3v3)
        elif p_num == '6': p.SetNet(net_sda)
        elif p_num == '7':
            # Exposed Thermal Pad: ensure NO paste, NO net (floating)
            lset = p.GetLayerSet()
            if lset.Contains(pcbnew.F_Paste):
                lset.RemoveLayer(pcbnew.F_Paste)
                p.SetLayerSet(lset)
    for p in pads_to_remove:
        u2.Remove(p)
    board.Add(u2)
    add_silkscreen_text(board, "DN", x_down - 0.5, y_center - 1.25, size_mm=0.8, layer=pcbnew.F_Fab)

    # Decoupling Cap C2 (100nF 0402) for U2
    c2 = pcbnew.FootprintLoad(c_lib, 'C_0402_1005Metric')
    c2.SetReference("C2")
    c2.SetValue("100nF")
    c2.SetPosition(pcbnew.VECTOR2I(pcbnew.FromMM(x_down + 1.8), pcbnew.FromMM(y_center)))
    c2.SetOrientationDegrees(90)
    c2.Reference().SetVisible(False)
    c2.Value().SetVisible(False)
    for p in c2.Pads():
        if p.GetNumber() == '1': p.SetNet(net_3v3)
        elif p.GetNumber() == '2': p.SetNet(net_gnd)
    board.Add(c2)

    # The old six horizontal lines did not touch the fingers or sensor pins
    # and crossed unrelated pads. Remove this invalid routing scaffold.
    # Preserve all intended pad nets; incomplete routes remain visible to DRC.
    add_track(board, u2.FindPadByNumber('4').GetPosition(),
              u2.FindPadByNumber('5').GetPosition(), pcbnew.F_Cu, 0.15, net_3v3)

    # Strict Thermal Keepout Zone (Rule Area preventing copper pour in sensing region)
    keepout_z = pcbnew.ZONE(board)
    keepout_z.SetIsRuleArea(True)
    keepout_z.SetDoNotAllowZoneFills(True)
    keepout_z.SetDoNotAllowTracks(False)
    keepout_z.SetDoNotAllowVias(False)
    keepout_z.SetDoNotAllowPads(False)
    keepout_z.SetDoNotAllowFootprints(False)
    chain = pcbnew.SHAPE_LINE_CHAIN()
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x_up - 2.5), pcbnew.FromMM(y_top)))
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x_down + 2.5), pcbnew.FromMM(y_top)))
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x_down + 2.5), pcbnew.FromMM(y_bot)))
    chain.Append(pcbnew.VECTOR2I(pcbnew.FromMM(x_up - 2.5), pcbnew.FromMM(y_bot)))
    chain.SetClosed(True)
    poly = pcbnew.SHAPE_POLY_SET()
    poly.AddOutline(chain)
    keepout_z.SetOutline(poly)
    lset = pcbnew.LSET()
    lset.AddLayer(pcbnew.F_Cu)
    lset.AddLayer(pcbnew.B_Cu)
    keepout_z.SetLayerSet(lset)
    board.Add(keepout_z)

    pcbnew.SaveBoard(output_path, board)
    print(f"{variant_name} saved to {output_path}")

def generate_kicad_pro(pro_path, proj_name):
    content = f'''{{
  "meta": {{
    "filename": "{proj_name}.kicad_pro",
    "version": 1
  }},
  "schematic": {{
    "annotate_start_num": 1,
    "drawing": {{
      "dashed_lines_dash_length_ratio": 12.0,
      "dashed_lines_gap_length_ratio": 3.0,
      "default_line_thickness": 0.1524,
      "default_text_size": 1.27,
      "field_names": [],
      "intersheets_ref_own_page": false,
      "intersheets_ref_prefix": "",
      "intersheets_ref_short": false,
      "intersheets_ref_show": false,
      "intersheets_ref_suffix": "",
      "junction_size_choice": 3,
      "pin_symbol_size": 0.0,
      "text_offset_ratio": 0.2
    }}
  }},
  "board": {{
    "design_settings": {{
      "rules": {{
        "min_clearance": 0.15,
        "min_track_width": 0.15
      }}
    }}
  }}
}}'''
    with open(pro_path, 'w', encoding='utf-8') as f:
        f.write(content)

def generate_bom_cpl(target_dir, board_name):
    print(f"Generating BOM & CPL for {board_name}...")
    if "Main_Controller" in board_name:
        bom_rows = [
            ("Comment", "Designator", "Footprint", "LCSC Part #"),
            ("ESP32-C3 Super Mini Socket (1x8 2.54mm Female Header)", "U1_L, U1_R", "PinSocket_1x08_P2.54mm_Vertical", "C42431840"),
            ("AO3400A N-MOSFET SOT-23 30V 5.7A", "Q1", "SOT-23", "C20917"),
            ("4.7kΩ ±1% 0603 SMD Resistor (I2C Pull-Up)", "R1, R2", "R_0603_1608Metric", "C23162"),
            ("100Ω ±1% 0603 SMD Resistor (Gate Damping)", "R3", "R_0603_1608Metric", "C22775"),
            ("100kΩ ±1% 0603 SMD Resistor (Gate Pull-Down)", "R4", "R_0603_1608Metric", "C25803"),
            ("10µF 50V X5R 0805 SMD Capacitor (GRM21BR61H106KE43L)", "C1, C3", "C_0805_2012Metric", "C440198"),
            ("100nF 50V X7R 0603 SMD Capacitor", "C2, C4", "C_0603_1608Metric", "C14663"),
            ("6P 0.5mm Horizontal Flip-Lock FPC Connector", "J1", "Hirose_FH12-6S-0.5SH_1x06-1MP_P0.50mm_Horizontal", "C202118"),
            ("3-Pad Solder Jumper (Default OPEN; manually select one voltage)", "SJ1", "SolderJumper-3_P1.3mm_Open_Pad1.0x1.5mm_NumberLabels", "CUSTOM_SMD"),
            ("Test Point SMD Pad D1.0mm", "TP1, TP2, TP3, TP4, TP5, TP6", "TestPoint_Pad_D1.0mm", "CUSTOM_TP"),
            ("M3 Mounting Hole Dia 3.2mm", "H1, H2, H3, H4", "MountingHole_3.2mm_M3", "MECHANICAL"),
        ]
    else:
        bom_rows = [
            ("Comment", "Designator", "Footprint", "LCSC Part #"),
            ("TMP117MAIDRVR ±0.1°C High-Accuracy Temp Sensor (ADD0=GND, 0x48)", "U1", "WSON-6-1EP_2x2mm_P0.65mm", "C2803242"),
            ("TMP117MAIDRVR ±0.1°C High-Accuracy Temp Sensor (ADD0=3V3, 0x49)", "U2", "WSON-6-1EP_2x2mm_P0.65mm", "C2803242"),
            ("PRF18BC471QB5RB PTC Thermistor Heater (470Ω 0603)", "R_HEAT", "R_0603_1608Metric", "C152572"),
            ("100nF 16V X7R 0402 SMD Capacitor (CL05B104KO5NNNC)", "C1, C2", "C_0402_1005Metric", "C1525"),
            ("6P 0.5mm Gold Fingers (ENIG); mating dimensions and total thickness UNVERIFIED", "J1_FPC", "FPC_GoldFinger_6P", "FPC_INTEGRATED"),
        ]

    bom_path = os.path.join(target_dir, f"BOM_{board_name}.csv")
    with open(bom_path, 'w', encoding='utf-8') as f:
        for r in bom_rows:
            f.write(','.join(f'"{col}"' for col in r) + '\n')

    pcb_path = os.path.join(target_dir, f"{board_name}.kicad_pcb")
    board = pcbnew.LoadBoard(pcb_path)
    cpl_path = os.path.join(target_dir, f"CPL_{board_name}.csv")
    with open(cpl_path, 'w', encoding='utf-8', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(["Designator", "Val", "Package", "Mid X", "Mid Y", "Rotation", "Layer"])
        for fp in sorted(board.GetFootprints(), key=lambda item: item.GetReference()):
            ref = fp.GetReference()
            if ref.startswith(('H', 'TP', 'SJ')) or ref == 'J1_FPC' or not (fp.GetAttributes() & pcbnew.FP_SMD):
                continue  # PCB features are not assembled components.
            pos = fp.GetPosition()
            writer.writerow([ref, fp.GetValue(), fp.GetFPID().GetLibItemName(),
                             f"{pcbnew.ToMM(pos.x):.4f}", f"{pcbnew.ToMM(pos.y):.4f}",
                             f"{fp.GetOrientationDegrees() % 360:.2f}",
                             "Bottom" if fp.IsFlipped() else "Top"])


def validate_board(pcb_path, output_dir, name):
    """Return fresh KiCad evidence; this does not assert schematic parity."""
    drc_path = Path(output_dir) / f"{name}_DRC.json"
    cmd = [KICAD_CLI, "pcb", "drc", "--refill-zones", "--save-board",
           "--format", "json", "--exit-code-violations", "--output", str(drc_path), str(pcb_path)]
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode not in (0, 5) or not drc_path.exists():
        raise RuntimeError(f"DRC could not run for {name}: {result.stderr[-800:]}")
    report = json.loads(drc_path.read_text())
    # A missing collection is missing evidence, not an empty/passing check.
    if any(key not in report or not isinstance(report[key], list)
           for key in ("violations", "unconnected_items", "schematic_parity")):
        raise RuntimeError(f"Incomplete DRC report: {drc_path}")
    passed = result.returncode == 0 and not any(report[key] for key in
                      ("violations", "unconnected_items", "schematic_parity"))
    status = {"board": name, "tool": "KiCad", "passed": passed,
              "violations": len(report["violations"]),
              "unconnected_items": len(report["unconnected_items"]),
              "schematic_parity_verified": False,
              "easyeda_live_verified": False,
              "fabrication_released": False,
              "physical_review_required": list(PHYSICAL_REVIEW_REQUIRED)}
    (Path(output_dir) / f"{name}_Status.json").write_text(json.dumps(status, indent=2) + "\n")
    print(f"{name}: DRC {'PASS' if passed else 'FAIL'}, "
          f"{status['violations']} violations, {status['unconnected_items']} unconnected")
    return status


def export_fabrication_files(pcb_path, output_dir, name):
    status = validate_board(pcb_path, output_dir, name)
    if not status["passed"]:
        raise RuntimeError(f"Fabrication refused: {name} failed DRC; see {name}_DRC.json")
    if status["physical_review_required"]:
        raise RuntimeError("Fabrication refused: physical design and native EasyEDA review incomplete")
    # CAM output is retained here for a reviewed future release. No files are
    # emitted before validation, including BOM/board consistency and native checks.
    gerber_dir = Path(output_dir) / "gerber"
    gerber_dir.mkdir(exist_ok=True)
    subprocess.run([KICAD_CLI, "pcb", "export", "gerbers", "-o", str(gerber_dir), str(pcb_path)], check=True)
    subprocess.run([KICAD_CLI, "pcb", "export", "drill", "-o", str(gerber_dir), str(pcb_path)], check=True)
    zip_path = Path(output_dir) / f"{name}_Gerber.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as zf:
        for source in sorted(gerber_dir.iterdir()):
            if source.is_file():
                zf.write(source, arcname=source.name)
    return zip_path


def main(argv=None):
    global _WX_APP
    _WX_APP = wx.App(False) if wx.GetApp() is None else wx.GetApp()
    parser = argparse.ArgumentParser(description="Build layout candidates and fail-closed validation reports")
    parser.add_argument('--output-dir', type=Path, default=Path(ROOT_DIR))
    parser.add_argument('--fabrication', action='store_true', help='Request release only after all validation gates')
    args = parser.parse_args(argv)
    statuses = []
    designs = [('Main_Controller_V01', None), *[(v[0], v[1:]) for v in VARIANTS]]
    for name, params in designs:
        subdir = args.output_dir / (name if params is None else f"Sensor_FPC_V01/{name}")
        subdir.mkdir(parents=True, exist_ok=True)
        pcb_path = subdir / f"{name}.kicad_pcb"
        if params is None:
            build_main_controller(str(pcb_path))
        else:
            build_sensor_fpc(name, *params, str(pcb_path))
        generate_kicad_pro(str(pcb_path.with_suffix('.kicad_pro')), name)
        generate_bom_cpl(str(subdir), name)
        statuses.append(validate_board(pcb_path, subdir, name))
    (args.output_dir / 'validation_summary.json').write_text(json.dumps(statuses, indent=2) + "\n")
    if args.fabrication:
        raise RuntimeError("Fabrication refused: see DRC and physical/native review blockers")
    print('Layout candidates and reports generated; fabrication has NOT been approved.')
    return 0 if all(status['passed'] for status in statuses) else 5


if __name__ == '__main__':
    sys.exit(main())
