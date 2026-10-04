#!/usr/bin/env python3
"""Check retained EasyEDA readback against the required circuit, without editing CAD.

Run after capturing fresh, saved-state readback. This checks electrical identities
and real pin/pad numbers, rather than assuming that a native DRC proves intent.
"""
import csv
import hashlib
import json
import math
import re
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'verification/optimization'


def read(name):
    x = json.loads((OUT / name).read_text())
    if not isinstance(x, dict):
        return x
    if x.get('ok') is False:
        raise ValueError(f'Failed source response: {name}')
    return x.get('result', x)


def parts(x):
    return {c['designator']: c for c in x['components'] if c.get('designator')}


def connector():
    return {'1': '+3V3', '2': 'GND', '3': 'SDA', '4': 'SCL',
            '5': 'HEATER_VCC', '6': 'HEATER_RETURN', '7': None, '8': None}


def main():
    errors, counts, bom, source_hashes = [], {}, [], {}

    def check(condition, message):
        if not condition:
            errors.append(message)

    expected = {
        'main': {
            'J1': connector(),
            'J2': {'1': '+5V', '2': 'GND', '3': '+3V3', '4': 'SDA',
                   '5': 'SCL', '6': None, '7': 'HEATER_EN', '8': None},
            'J3': {str(i): 'GPIO10_RES' if i == 6 else None for i in range(1, 9)},
            'U4': {'1': '+5V', '2': 'GND', '3': 'HEATER_GATE', '4': None, '5': 'HEATER_VCC'},
            'Q1': {'1': 'HEATER_GATE', '2': 'GND', '3': 'HEATER_RETURN'},
            'R1': {'1': '+3V3', '2': 'SDA'}, 'R2': {'1': '+3V3', '2': 'SCL'},
            'R3': {'1': 'HEATER_EN', '2': 'HEATER_GATE'},
            'R4': {'1': 'HEATER_GATE', '2': 'GND'},
        },
        'sensor': {
            'J4': connector(), 'R5': {'1': 'HEATER_VCC', '2': 'HEATER_RETURN'},
            'U2': {'1': 'SCL', '2': 'GND', '3': None, '4': 'GND', '5': '+3V3', '6': 'SDA', '7': None},
            'U3': {'1': 'SCL', '2': 'GND', '3': None, '4': '+3V3', '5': '+3V3', '6': 'SDA', '7': None},
            'C5': {'1': '+3V3', '2': 'GND'}, 'C6': {'1': '+3V3', '2': 'GND'},
        },
    }
    for ref in ['C1', 'C2', 'C7', 'C9']:
        expected['main'][ref] = {'1': '+5V', '2': 'GND'}
    for ref in ['C3', 'C4']:
        expected['main'][ref] = {'1': '+3V3', '2': 'GND'}
    for ref in ['C8', 'C10']:
        expected['main'][ref] = {'1': 'HEATER_VCC', '2': 'GND'}
    for i, net in enumerate(['+5V', '+3V3', 'GND', 'SDA', 'SCL', 'HEATER_RETURN'], 1):
        expected['main']['TP' + str(i)] = {'1': net}

    required_ids = {
        'J1': 'C202118', 'J4': 'C202118', 'J2': 'C27438', 'J3': 'C27438',
        'U4': 'C259866', 'R5': 'C227500', 'U2': 'C2803242', 'U3': 'C2803242',
        'C5': 'C1525', 'C6': 'C1525',
        **{r: 'C440198' for r in ['C1', 'C3', 'C7', 'C8']},
        **{r: 'C14663' for r in ['C2', 'C4', 'C9', 'C10']},
    }
    for tag in ['main', 'sensor']:
        sch = parts(read(tag + '_sch_read_final.json'))
        pcb = parts(read(tag + '_pcb_list_final.json'))
        attrs = parts(read(tag + '_sch_list_final.json'))
        check(set(sch) == set(expected[tag]), f'{tag}: unexpected/missing schematic parts')
        check(set(pcb) == set(sch), f'{tag}: schematic/PCB part inventory mismatch')
        uid_s, uid_p = set(), set()
        for ref, c in sch.items():
            if ref not in pcb:
                continue
            a = {p['number']: p.get('net') or None for p in c['pins']}
            b = {str(p['padNumber']): p.get('net') or None for p in pcb[ref]['pads']}
            check(a == expected[tag].get(ref), f'{tag}/{ref}: circuit intent mismatch')
            check(a == b, f'{tag}/{ref}: physical pin-to-pad net mismatch')
            check(bool(c.get('uniqueId')) and c.get('uniqueId') == pcb[ref].get('uniqueId'),
                  f'{tag}/{ref}: schematic/PCB identity mismatch')
            check(c.get('uniqueId') not in uid_s, f'{tag}/{ref}: duplicate schematic identity')
            check(pcb[ref].get('uniqueId') not in uid_p, f'{tag}/{ref}: duplicate PCB identity')
            uid_s.add(c.get('uniqueId')); uid_p.add(pcb[ref].get('uniqueId'))
            if ref in required_ids:
                check(c.get('supplierId') == required_ids[ref], f'{tag}/{ref}: wrong supplier identity')
                check(pcb[ref].get('supplierId') == required_ids[ref], f'{tag}/{ref}: wrong PCB identity')
            attr = attrs[ref]
            if ref.startswith('TP'):
                check(len(b) == 1 and attr.get('addIntoBom') is False,
                      f'{tag}/{ref}: test pad must be single-pad and DNP')
            elif attr.get('addIntoBom'):
                check(bool(attr.get('supplierId')) and bool(attr.get('manufacturerId')),
                      f'{tag}/{ref}: missing procurement identity')
                bom.append({'board': tag, 'designator': ref, 'manufacturer': attr.get('manufacturer', ''),
                            'part': attr.get('manufacturerId', ''), 'lcsc': attr.get('supplierId', ''),
                            'value': attr.get('otherProperty', {}).get('Value', ''),
                            'footprint': attr.get('footprint', {}).get('name', ''), 'quantity': 1})
        gate, drc, dfm = (read(tag + n) for n in [
            '_schematic_gate_final.json', '_pcb_drc_final.json', '_pcb_dfm_final.json'])
        check(gate['verdict'] == 'pass', f'{tag}: schematic gate failed or blocked')
        check(drc.get('passed') is True and drc.get('total') == 0, f'{tag}: native PCB DRC not clear')
        check(dfm['summary']['errors'] == 0, f'{tag}: DFM errors remain')
        for rule in ['danglingEnds', 'viaInPad', 'silkOverPad', 'silkscreenFlipped']:
            check(dfm['summary'][rule] == 0, f'{tag}: unresolved {rule}')
        counts[tag] = {'parts': len(sch), 'pads': sum(len(c['pads']) for c in pcb.values()),
                       'nativePcbDrc': drc, 'dfmSummary': dfm['summary'],
                       'schematicStages': [{k: s[k] for k in ['name', 'status', 'errors', 'warnings']} for s in gate['stages']]}
        for name in [tag + suffix for suffix in ['_sch_read_final.json', '_sch_list_final.json',
            '_pcb_list_final.json', '_pcb_final.json', '_pcb_drc_final.json', '_schematic_gate_final.json']]:
            source_hashes[name] = hashlib.sha256((OUT / name).read_bytes()).hexdigest()
        if tag == 'sensor':
            center = pcb['R5']
            for ref in ['U2', 'U3']:
                dist = math.hypot(center['x'] - pcb[ref]['x'], center['y'] - pcb[ref]['y']) * 0.0254
                check(abs(dist - 3.0) < .03 and center['x'] == pcb[ref]['x'], f'{ref}: wrong heater spacing')
                counts[tag][ref + 'HeaterDistanceMm'] = round(dist, 4)

    paths = read('copper_paths_final.json')
    # Native net-path reports must establish actual copper, not merely equal net labels.
    for p in paths:
        r = p['report'].get('result', p['report'])
        check(r.get('connected') is True, f"{p['board']}: copper path unproven {p['from']} -> {p['to']}")
    ino = ROOT / 'firmware/RiceSapFlow/RiceSapFlow.ino'
    text = ino.read_text()
    check(re.search(r'PIN_SDA\s*=\s*4,\s*PIN_SCL\s*=\s*3,\s*PIN_HEATER\s*=\s*1', text) is not None,
          'Firmware GPIO mismatch against provisional SuperMini mapping')
    grouped = defaultdict(list)
    for row in bom:
        key = tuple(row[k] for k in ['board', 'manufacturer', 'part', 'lcsc', 'value', 'footprint'])
        grouped[key].append(row['designator'])
    with (ROOT / 'Rice_SapFlow_Optimized_BOM.csv').open('w', newline='', encoding='utf-8-sig') as f:
        writer = csv.writer(f)
        writer.writerow(['Board', 'Manufacturer', 'Manufacturer Part', 'LCSC', 'Value', 'Footprint', 'Designators', 'Quantity'])
        for key, refs in sorted(grouped.items()):
            writer.writerow([*key, ','.join(sorted(refs)), len(refs)])
    result = {'digitalChecksPassed': not errors, 'manufacturingReleased': False,
              'physicalTestingPerformed': False, 'sapFlowCalibrated': False,
              'partCount': sum(c['parts'] for c in counts.values()), 'bomPositionCount': len(bom),
              'copperPathProofCount': len(paths), 'boards': counts, 'errors': errors,
              'limitations': ['SuperMini exact identity and physical pinout pending',
                              'Main native ERC has 2 warning counts without item details',
                              'DFM advisory findings require documented review',
                              'FFC mapping, TMP117 stencil/EP, power and pulse timing require physical acceptance',
                              'Thermal coupling and sap-flow calibration require measurements'],
              'sourceSha256': source_hashes,
              'firmwareSha256': hashlib.sha256(ino.read_bytes()).hexdigest()}
    (OUT / 'intent_validation_final.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({k: result[k] for k in ['digitalChecksPassed', 'partCount', 'bomPositionCount', 'copperPathProofCount', 'errors']}, ensure_ascii=False))
    if errors:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
