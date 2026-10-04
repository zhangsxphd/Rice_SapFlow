#!/usr/bin/env python3
"""Apply parameter data using typed EasyEDA CLI calls, with a retained journal.

Imported legacy devices cannot pass the standard replacement rollback guard.
Create and read back a candidate before disconnecting/deleting the old instance.
Never rerun this script blindly after a failure; reconcile its journal and live page.
"""
import json
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PROJECT = 'a422d704ace24952ae3d8c1eb5094d0b'
LIB = '0819f05c4eef4c71ace90d822a990e87'
PRIVATE = '9e05c206bff14f5b91e051328bc4efe6'
OUT = ROOT / 'verification/optimization'
sequence = 0
run_id = time.strftime('%H%M%S')

def run(args, doc, label):
    global sequence
    sequence += 1
    command = ['easyeda'] + [str(a) for a in args] + ['--project', PROJECT, '--doc', doc]
    r = subprocess.run(command, cwd=ROOT, text=True, capture_output=True, timeout=90)
    path = OUT / ('edit_%s_%03d_%s.json' % (run_id, sequence, label))
    path.write_text(r.stdout)
    if r.stderr:
        path.with_suffix('.stderr.txt').write_text(r.stderr)
    try:
        data = json.loads(r.stdout)
    except ValueError:
        raise RuntimeError('%s: non-JSON response: %s' % (label, r.stdout[-500:]))
    if r.returncode or data.get('ok') is False:
        raise RuntimeError('%s: %s' % (label, data.get('error', r.stdout[-500:])))
    result = data.get('result', data)
    if result.get('partial') or result.get('verified') is False:
        raise RuntimeError('%s: partial/unverified change; inspect %s' % (label, path))
    print('%03d %s' % (sequence, label), flush=True)
    return result

def read(doc, label):
    return run(['sch', 'read', '--no-check', '--page', doc], doc, label)

def replace_candidate(doc, old, uuid, nets, nc=(), library=LIB):
    ref = old['designator']
    candidate = 'J901'
    current = read(doc,'candidate_preflight_'+ref)
    existing = [c for c in current['components'] if c.get('designator') == candidate]
    if existing:
        if ref != 'U1_L' or existing[0].get('supplierId') != 'C27438':
            raise RuntimeError('Unexpected retained candidate; reconcile before proceeding')
        candidate_id = existing[0]['primitiveId']
    else:
        # Native creation at an occupied coordinate can return a non-persisted ID.
        # Use a blank measured area, then move only after the old part is removed.
        r = run(['sch','place','--lib',library,'--uuid',uuid,'--designator',candidate,
                 '--x',1800,'--y',1000],doc,'candidate_'+ref)
        candidate_id = r['primitiveId']
    snapshot = read(doc,'candidate_read_'+ref)
    new = next(c for c in snapshot['components'] if c['primitiveId'] == candidate_id)
    actual = {p['number'] for p in new['pins']}
    if not set(nets).issubset(actual):
        raise RuntimeError('Candidate %s lacks expected physical pin numbers' % ref)
    # Disconnect only the old instance's labelled stubs, leaving other parts intact.
    for p in old['pins']:
        if p.get('net'):
            run(['sch','disconnect','--pin',ref+':'+p['number']],doc,'detach_'+ref+'_'+p['number'])
    run(['sch','prim-delete','--ids',old['primitiveId']],doc,'delete_old_'+ref)
    uid = old.get('uniqueId') or 'rice-opt-'+ref
    run(['sch','modify','--id',candidate_id,'--designator',ref,'--x',old['x'],'--y',old['y'],
         '--patch',json.dumps({'uniqueId':uid})],doc,'adopt_'+ref)
    for pin,net in nets.items():
        kind = 'gnd' if net == 'GND' else 'power' if net in ['+5V','+3V3','HEATER_VCC'] else 'netport'
        run(['sch','autoconnect','--pin',ref+':'+pin,'--net',net,'--kind',kind,
             '--offset-max',40,'--json'],doc,'connect_'+ref+'_'+pin)
    if nc:
        run(['sch','no-connect','--designator',ref,'--pin',','.join(nc)],doc,'nc_'+ref)

def main_parts():
    doc = '2d01061a63b3efa0'
    parts = {c['designator']:c for c in read(doc,'start_main')['components'] if c.get('designator')}
    tp = json.loads((OUT/'tp_device.json').read_text())['result']['uuid']
    updates = [('U1_L','0a4d2569e740414d92321f53f6972245',('6','8')),
               ('U1_R','0a4d2569e740414d92321f53f6972245',('1','2','3','4','5','7','8')),
               ('C1','6e5726223dd84f70bc3b626fc7d1f72c',()),
               ('C3','6e5726223dd84f70bc3b626fc7d1f72c',()),
               ('C2','96b39256cc3f4d80bd3b503deb4f3328',()),
               ('C4','96b39256cc3f4d80bd3b503deb4f3328',())]
    for ref,uuid,nc in updates:
        old=parts[ref]; nets={p['number']:p['net'] for p in old['pins'] if p.get('net')}
        replace_candidate(doc,old,uuid,nets,nc)
    for i in range(1,7):
        ref='TP'+str(i); old=parts[ref]; net=next(p['net'] for p in old['pins'] if p.get('net'))
        replace_candidate(doc,old,tp,{'1':net},library=PRIVATE)
    for pin in ['1','2','3']:
        run(['sch','disconnect','--pin','SJ1:'+pin],doc,'detach_SJ1_'+pin)
    run(['sch','prim-delete','--ids',parts['SJ1']['primitiveId']],doc,'remove_voltage_selector')
    for ref,uuid,x,y in [('C7','6e5726223dd84f70bc3b626fc7d1f72c',1220,700),
                        ('C8','6e5726223dd84f70bc3b626fc7d1f72c',1220,550),
                        ('C9','96b39256cc3f4d80bd3b503deb4f3328',1360,700),
                        ('C10','96b39256cc3f4d80bd3b503deb4f3328',1360,550)]:
        r=run(['sch','place','--lib',LIB,'--uuid',uuid,'--designator',ref,'--x',x,'--y',y],doc,'place_'+ref)
        run(['sch','modify','--id',r['primitiveId'],'--patch',json.dumps({'uniqueId':'rice-opt-'+ref})],doc,'uid_'+ref)
    snapshot=read(doc,'heater_parts'); u4=next(c for c in snapshot['components'] if c['designator']=='U4')
    run(['sch','modify','--id',u4['primitiveId'],'--patch',json.dumps({'uniqueId':'rice-opt-U4'})],doc,'uid_U4')
    targets={'U4':{'1':'+5V','2':'GND','3':'HEATER_GATE','5':'HEATER_VCC'},
             'C7':{'1':'+5V','2':'GND'},'C9':{'1':'+5V','2':'GND'},
             'C8':{'1':'HEATER_VCC','2':'GND'},'C10':{'1':'HEATER_VCC','2':'GND'}}
    for ref,nets in targets.items():
        for pin,net in nets.items():
            kind='gnd' if net=='GND' else 'power' if net in ['+5V','HEATER_VCC'] else 'netport'
            run(['sch','autoconnect','--pin',ref+':'+pin,'--net',net,'--kind',kind,'--json'],doc,'wire_'+ref+'_'+pin)
    run(['sch','no-connect','--designator','U4','--pin','4'],doc,'nc_U4')
    run(['sch','save'],doc,'save_main')
    read(doc,'final_main')

if __name__ == '__main__':
    raise SystemExit(
        'This module retains the typed CLI helpers and the original staged plan for audit. '
        'The plan is obsolete after optimization and must not be replayed. '
        'Open Rice_SapFlow_Optimized.epro2 and inspect live state before further edits.'
    )
