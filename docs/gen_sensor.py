import os
from pathlib import Path

def generate_sensor_fpc_svg(filepath):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1400 900" width="1400" height="900" style="background:#ffffff; font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f0f2f5" stroke-width="1"/>
    </pattern>
    <filter id="shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="2" stdDeviation="3" flood-opacity="0.08"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff"/>
  <rect width="100%" height="100%" fill="url(#grid)"/>

  <!-- Frame -->
  <rect x="25" y="25" width="1350" height="850" fill="none" stroke="#334155" stroke-width="2"/>
  <rect x="27" y="27" width="1346" height="846" fill="none" stroke="#cbd5e1" stroke-width="1"/>

  <!-- Title Box -->
  <rect x="950" y="785" width="425" height="90" fill="#f8fafc" stroke="#334155" stroke-width="1.5"/>
  <line x1="950" y1="815" x2="1375" y2="815" stroke="#cbd5e1" stroke-width="1"/>
  <line x1="950" y1="845" x2="1375" y2="845" stroke="#cbd5e1" stroke-width="1"/>
  <line x1="1160" y1="815" x2="1160" y2="875" stroke="#cbd5e1" stroke-width="1"/>
  <text x="965" y="805" font-size="14" font-weight="bold" fill="#0f172a">PROJECT: Rice_SapFlow_V01</text>
  <text x="965" y="833" font-size="12" fill="#475569">TITLE: Sensor_FPC_V01 Schematic</text>
  <text x="1175" y="833" font-size="12" fill="#475569">REV: V1.0</text>
  <text x="965" y="863" font-size="11" fill="#64748b">STAGE: Concept only; native ERC pending</text>
  <text x="1175" y="863" font-size="11" fill="#64748b">DATE: 2026-10-02</text>

  <!-- Flow Direction Banner -->
  <rect x="50" y="45" width="870" height="40" rx="6" fill="#f0fdf4" stroke="#16a34a" stroke-width="1.5"/>
  <text x="70" y="70" font-size="13" font-weight="bold" fill="#15803d">PLANT SAP FLOW VECTOR (植物蒸腾液流方向):</text>
  <path d="M 420 65 L 820 65" stroke="#16a34a" stroke-width="3" stroke-linecap="round"/>
  <polygon points="830,65 815,58 815,72" fill="#16a34a"/>
  <text x="560" y="60" text-anchor="middle" font-size="11" font-weight="bold" fill="#16a34a">TMP117_UP (Upstream) ➔ PTC Heater ➔ TMP117_DOWN (Downstream)</text>

  <!-- Module 1: 6P 0.5mm Gold Finger Interface -->
  <rect x="50" y="110" width="260" height="640" rx="8" fill="#ffffff" stroke="#047857" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)"/>
  <rect x="50" y="110" width="260" height="35" rx="8" fill="#ecfdf5"/>
  <text x="65" y="134" font-size="13" font-weight="bold" fill="#065f46">J1: 6P 0.5mm Gold Finger</text>

  <rect x="80" y="165" width="200" height="560" rx="6" fill="#f8fafc" stroke="#047857" stroke-width="2"/>
  <text x="180" y="195" text-anchor="middle" font-size="14" font-weight="bold" fill="#065f46">FPC ZIF Tail (6P)</text>
  <text x="180" y="215" text-anchor="middle" font-size="11" fill="#047857">0.5 mm Pitch Gold Fingers</text>
  <text x="180" y="235" text-anchor="middle" font-size="10" fill="#64748b">Candidate thickness 0.30mm; fit UNVERIFIED</text>

  <!-- Pins 1 to 6 -->
  <!-- Pin 1: 3V3 -->
  <line x1="280" y1="270" x2="350" y2="270" stroke="#2563eb" stroke-width="2"/>
  <circle cx="280" cy="270" r="4" fill="#2563eb"/>
  <text x="265" y="275" text-anchor="end" font-size="11" font-weight="bold" fill="#2563eb">1: 3V3</text>
  <text x="360" y="275" font-size="11" font-weight="bold" fill="#2563eb">3V3</text>

  <!-- Pin 2: GND -->
  <line x1="280" y1="340" x2="350" y2="340" stroke="#1e293b" stroke-width="2"/>
  <circle cx="280" cy="340" r="4" fill="#1e293b"/>
  <text x="265" y="345" text-anchor="end" font-size="11" font-weight="bold" fill="#1e293b">2: GND</text>
  <text x="360" y="345" font-size="11" font-weight="bold" fill="#1e293b">GND</text>

  <!-- Pin 3: SDA -->
  <line x1="280" y1="410" x2="350" y2="410" stroke="#0891b2" stroke-width="2"/>
  <circle cx="280" cy="410" r="4" fill="#0891b2"/>
  <text x="265" y="415" text-anchor="end" font-size="11" font-weight="bold" fill="#0891b2">3: SDA</text>
  <text x="360" y="415" font-size="11" font-weight="bold" fill="#0891b2">I2C_SDA</text>

  <!-- Pin 4: SCL -->
  <line x1="280" y1="480" x2="350" y2="480" stroke="#0891b2" stroke-width="2"/>
  <circle cx="280" cy="480" r="4" fill="#0891b2"/>
  <text x="265" y="485" text-anchor="end" font-size="11" font-weight="bold" fill="#0891b2">4: SCL</text>
  <text x="360" y="485" font-size="11" font-weight="bold" fill="#0891b2">I2C_SCL</text>

  <!-- Pin 5: HEATER_VCC -->
  <line x1="280" y1="560" x2="350" y2="560" stroke="#dc2626" stroke-width="2.5"/>
  <circle cx="280" cy="560" r="4" fill="#dc2626"/>
  <text x="265" y="565" text-anchor="end" font-size="11" font-weight="bold" fill="#dc2626">5: HEATER_VCC</text>
  <text x="360" y="565" font-size="11" font-weight="bold" fill="#dc2626">HEATER_VCC</text>

  <!-- Pin 6: HEATER_RETURN -->
  <line x1="280" y1="640" x2="350" y2="640" stroke="#ea580c" stroke-width="2.5"/>
  <circle cx="280" cy="640" r="4" fill="#ea580c"/>
  <text x="265" y="645" text-anchor="end" font-size="11" font-weight="bold" fill="#ea580c">6: HEATER_RETURN</text>
  <text x="360" y="645" font-size="11" font-weight="bold" fill="#ea580c">HEATER_RETURN</text>


  <!-- Module 2: TMP117_UP (Upstream Temperature Sensor, Addr: 0x48) -->
  <rect x="340" y="110" width="310" height="640" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)"/>
  <rect x="340" y="110" width="310" height="35" rx="8" fill="#eff6ff"/>
  <text x="355" y="134" font-size="13" font-weight="bold" fill="#1d4ed8">U1: TMP117_UP (Addr 0x48)</text>

  <!-- U1 Body WSON-6 -->
  <rect x="400" y="180" width="200" height="380" rx="6" fill="#f8fafc" stroke="#1e293b" stroke-width="2"/>
  <text x="500" y="210" text-anchor="middle" font-size="14" font-weight="bold" fill="#0f172a">TMP117MAIDRVR</text>
  <text x="500" y="230" text-anchor="middle" font-size="11" fill="#2563eb">WSON-6 (2x2 mm)</text>
  <rect x="430" y="245" width="140" height="30" rx="4" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="500" y="265" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">I²C Addr: 0x48 (ADD0=GND)</text>

  <!-- Pins -->
  <!-- Pin 1: SCL -->
  <line x1="360" y1="310" x2="400" y2="310" stroke="#0891b2" stroke-width="2"/>
  <circle cx="400" cy="310" r="3.5" fill="#0891b2"/>
  <text x="410" y="315" font-size="11" font-weight="bold" fill="#0891b2">1: SCL</text>

  <!-- Pin 2: GND -->
  <line x1="360" y1="360" x2="400" y2="360" stroke="#1e293b" stroke-width="2"/>
  <circle cx="400" cy="360" r="3.5" fill="#1e293b"/>
  <text x="410" y="365" font-size="11" font-weight="bold" fill="#1e293b">2: GND</text>

  <!-- Pin 3: ALERT (NC) -->
  <line x1="400" y1="410" x2="370" y2="410" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="410" y="415" font-size="11" fill="#64748b">3: ALERT (NC)</text>
  <line x1="365" y1="405" x2="375" y2="415" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="365" y1="415" x2="375" y2="405" stroke="#94a3b8" stroke-width="1.5"/>

  <!-- Pin 4: ADD0 (address strap) -->
  <line x1="600" y1="410" x2="630" y2="410" stroke="#2563eb" stroke-width="2"/>
  <circle cx="600" cy="410" r="3.5" fill="#2563eb"/>
  <text x="590" y="415" text-anchor="end" font-size="11" font-weight="bold" fill="#2563eb">4: ADD0 ➔ GND</text>

  <!-- Pin 5: V+ (3V3) -->
  <line x1="600" y1="360" x2="630" y2="360" stroke="#2563eb" stroke-width="2"/>
  <circle cx="600" cy="360" r="3.5" fill="#2563eb"/>
  <text x="590" y="365" text-anchor="end" font-size="11" font-weight="bold" fill="#2563eb">5: V+ (3V3)</text>

  <!-- Pin 6: SDA -->
  <line x1="600" y1="310" x2="630" y2="310" stroke="#0891b2" stroke-width="2"/>
  <circle cx="600" cy="310" r="3.5" fill="#0891b2"/>
  <text x="590" y="315" text-anchor="end" font-size="11" font-weight="bold" fill="#0891b2">6: SDA</text>

  <!-- Thermal Pad 7 -->
  <rect x="460" y="460" width="80" height="50" rx="3" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="500" y="482" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Thermal Pad</text>
  <text x="500" y="498" text-anchor="middle" font-size="9" fill="#b45309">FLOATING (No Paste)</text>

  <!-- Decoupling Cap C1 (100nF) for U1 -->
  <rect x="420" y="585" width="160" height="90" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>
  <text x="500" y="605" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">C1: 100 nF (0402/0603)</text>
  <line x1="460" y1="620" x2="460" y2="640" stroke="#2563eb" stroke-width="1.5"/>
  <line x1="450" y1="640" x2="470" y2="640" stroke="#0f172a" stroke-width="2"/>
  <line x1="450" y1="646" x2="470" y2="646" stroke="#0f172a" stroke-width="2"/>
  <line x1="460" y1="646" x2="460" y2="665" stroke="#1e293b" stroke-width="1.5"/>
  <text x="440" y="650" font-size="9" text-anchor="end" fill="#2563eb">3V3</text>
  <text x="480" y="650" font-size="9" fill="#1e293b">GND</text>
  <text x="500" y="665" text-anchor="middle" font-size="9" fill="#64748b">Decoupling across V+ &amp; GND</text>


  <!-- Module 3: PTC Heater (PRF18BC471QB5RB) -->
  <rect x="670" y="110" width="280" height="640" rx="8" fill="#ffffff" stroke="#ea580c" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)"/>
  <rect x="670" y="110" width="280" height="35" rx="8" fill="#fff7ed"/>
  <text x="685" y="134" font-size="13" font-weight="bold" fill="#c2410c">HEATER: PRF18BC471QB5RB</text>

  <!-- Heater Box -->
  <rect x="700" y="240" width="220" height="280" rx="6" fill="#f8fafc" stroke="#ea580c" stroke-width="2"/>
  <text x="810" y="275" text-anchor="middle" font-size="15" font-weight="bold" fill="#9a3412">PTC HEATER</text>
  <text x="810" y="295" text-anchor="middle" font-size="11" fill="#ea580c">PRF18BC471QB5RB (0603)</text>
  <text x="810" y="315" text-anchor="middle" font-size="10" fill="#64748b">R25 = 470 Ω ±50% | POSISTOR</text>

  <!-- Resistor symbol -->
  <line x1="810" y1="330" x2="810" y2="350" stroke="#dc2626" stroke-width="2.5"/>
  <circle cx="810" cy="330" r="4" fill="#dc2626"/>
  <text x="825" y="335" font-size="11" font-weight="bold" fill="#dc2626">1: HEATER_VCC</text>

  <rect x="790" y="350" width="40" height="80" fill="#ffffff" stroke="#0f172a" stroke-width="2"/>
  <path d="M 780 410 L 840 370" stroke="#ea580c" stroke-width="2"/>
  <line x1="840" y1="370" x2="845" y2="370" stroke="#ea580c" stroke-width="2"/>
  <text x="810" y="395" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">PTC</text>

  <line x1="810" y1="430" x2="810" y2="470" stroke="#ea580c" stroke-width="2.5"/>
  <circle cx="810" cy="470" r="4" fill="#ea580c"/>
  <text x="825" y="475" font-size="11" font-weight="bold" fill="#ea580c">2: HEATER_RETURN</text>

  <!-- Thermal Isolation Constraint Box -->
  <rect x="690" y="550" width="240" height="150" rx="6" fill="#fef2f2" stroke="#ef4444" stroke-width="1.5"/>
  <text x="810" y="575" text-anchor="middle" font-size="11" font-weight="bold" fill="#b91c1c">THERMAL ISOLATION RULES</text>
  <text x="705" y="598" font-size="10" fill="#991b1b">• 严格对称布线 (上下走线对称)</text>
  <text x="705" y="618" font-size="10" fill="#991b1b">• 严禁在PTC与TMP117间大面积铺铜</text>
  <text x="705" y="638" font-size="10" fill="#991b1b">• 禁止连续 GND/PWR 平面横向导热</text>
  <text x="705" y="658" font-size="10" fill="#991b1b">• 保留PI基材热阻以保证温差敏感度</text>
  <text x="705" y="678" font-size="10" fill="#991b1b">• 间距规格: 2 mm / 3 mm / 4 mm</text>


  <!-- Module 4: TMP117_DOWN (Downstream Temperature Sensor, Addr: 0x49) -->
  <rect x="970" y="110" width="310" height="640" rx="8" fill="#ffffff" stroke="#2563eb" stroke-width="1.5" stroke-dasharray="6,4" filter="url(#shadow)"/>
  <rect x="970" y="110" width="310" height="35" rx="8" fill="#eff6ff"/>
  <text x="985" y="134" font-size="13" font-weight="bold" fill="#1d4ed8">U2: TMP117_DOWN (Addr 0x49)</text>

  <!-- U2 Body WSON-6 -->
  <rect x="1030" y="180" width="200" height="380" rx="6" fill="#f8fafc" stroke="#1e293b" stroke-width="2"/>
  <text x="1130" y="210" text-anchor="middle" font-size="14" font-weight="bold" fill="#0f172a">TMP117MAIDRVR</text>
  <text x="1130" y="230" text-anchor="middle" font-size="11" fill="#2563eb">WSON-6 (2x2 mm)</text>
  <rect x="1060" y="245" width="140" height="30" rx="4" fill="#dbeafe" stroke="#93c5fd"/>
  <text x="1130" y="265" text-anchor="middle" font-size="11" font-weight="bold" fill="#1e40af">I²C Addr: 0x49 (ADD0=3V3)</text>

  <!-- Pins -->
  <!-- Pin 1: SCL -->
  <line x1="990" y1="310" x2="1030" y2="310" stroke="#0891b2" stroke-width="2"/>
  <circle cx="1030" cy="310" r="3.5" fill="#0891b2"/>
  <text x="1040" y="315" font-size="11" font-weight="bold" fill="#0891b2">1: SCL</text>

  <!-- Pin 2: GND -->
  <line x1="990" y1="360" x2="1030" y2="360" stroke="#2563eb" stroke-width="2"/>
  <circle cx="1030" cy="360" r="3.5" fill="#2563eb"/>
  <text x="1040" y="365" font-size="11" font-weight="bold" fill="#2563eb">2: GND</text>

  <!-- Pin 3: ALERT (NC) -->
  <line x1="1030" y1="410" x2="1000" y2="410" stroke="#94a3b8" stroke-width="1.5"/>
  <text x="1040" y="415" font-size="11" fill="#64748b">3: ALERT (NC)</text>
  <line x1="995" y1="405" x2="1005" y2="415" stroke="#94a3b8" stroke-width="1.5"/>
  <line x1="995" y1="415" x2="1005" y2="405" stroke="#94a3b8" stroke-width="1.5"/>

  <!-- Pin 4: ADD0 (address strap) -->
  <line x1="1230" y1="410" x2="1260" y2="410" stroke="#1e293b" stroke-width="2"/>
  <circle cx="1230" cy="410" r="3.5" fill="#1e293b"/>
  <text x="1220" y="415" text-anchor="end" font-size="11" font-weight="bold" fill="#1e293b">4: ADD0 ➔ 3V3</text>

  <!-- Pin 5: V+ (3V3) -->
  <line x1="1230" y1="360" x2="1260" y2="360" stroke="#2563eb" stroke-width="2"/>
  <circle cx="1230" cy="360" r="3.5" fill="#2563eb"/>
  <text x="1220" y="365" text-anchor="end" font-size="11" font-weight="bold" fill="#2563eb">5: V+ (3V3)</text>

  <!-- Pin 6: SDA -->
  <line x1="1230" y1="310" x2="1260" y2="310" stroke="#0891b2" stroke-width="2"/>
  <circle cx="1230" cy="310" r="3.5" fill="#0891b2"/>
  <text x="1220" y="315" text-anchor="end" font-size="11" font-weight="bold" fill="#0891b2">6: SDA</text>

  <!-- Thermal Pad 7 -->
  <rect x="1090" y="460" width="80" height="50" rx="3" fill="#fef3c7" stroke="#d97706" stroke-width="1.5" stroke-dasharray="4,2"/>
  <text x="1130" y="482" text-anchor="middle" font-size="10" font-weight="bold" fill="#92400e">Thermal Pad</text>
  <text x="1130" y="498" text-anchor="middle" font-size="9" fill="#b45309">FLOATING (No Paste)</text>

  <!-- Decoupling Cap C2 (100nF) for U2 -->
  <rect x="1050" y="585" width="160" height="90" rx="6" fill="#f1f5f9" stroke="#94a3b8" stroke-width="1"/>
  <text x="1130" y="605" text-anchor="middle" font-size="11" font-weight="bold" fill="#0f172a">C2: 100 nF (0402/0603)</text>
  <line x1="1090" y1="620" x2="1090" y2="640" stroke="#2563eb" stroke-width="1.5"/>
  <line x1="1080" y1="640" x2="1100" y2="640" stroke="#0f172a" stroke-width="2"/>
  <line x1="1080" y1="646" x2="1100" y2="646" stroke="#0f172a" stroke-width="2"/>
  <line x1="1090" y1="646" x2="1090" y2="665" stroke="#1e293b" stroke-width="1.5"/>
  <text x="1070" y="650" font-size="9" text-anchor="end" fill="#2563eb">3V3</text>
  <text x="1110" y="650" font-size="9" fill="#1e293b">GND</text>
  <text x="1130" y="665" text-anchor="middle" font-size="9" fill="#64748b">Decoupling across V+ &amp; GND</text>

</svg>'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)

def generate_sensor_geometry_svg(filepath):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1450 820" width="1450" height="820" style="background:#ffffff; font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;">
  <defs>
    <pattern id="grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#f1f5f9" stroke-width="1"/>
    </pattern>
    <marker id="arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 1.5 L 10 5 L 0 8.5 z" fill="#16a34a"/>
    </marker>
    <marker id="dim-arrow" viewBox="0 0 10 10" refX="5" refY="5" markerWidth="6" markerHeight="6" orient="auto-start-reverse">
      <path d="M 0 2 L 10 5 L 0 8 z" fill="#2563eb"/>
    </marker>
  </defs>

  <rect width="100%" height="100%" fill="#ffffff"/>
  <rect width="100%" height="100%" fill="url(#grid)"/>

  <!-- Frame -->
  <rect x="20" y="20" width="1410" height="780" fill="none" stroke="#334155" stroke-width="2"/>
  <text x="50" y="60" font-size="18" font-weight="bold" fill="#0f172a">Sensor_FPC_V01: Probe Geometry, Spacing Variants &amp; Thermal Symmetry</text>
  <text x="50" y="85" font-size="12" fill="#475569">Physical Layout Strategy for Sap Flow Measurement (Heat Pulse / Constant Heat / Heat Ratio Method)</text>

  <!-- Flow Direction Vector -->
  <g transform="translate(50, 110)">
    <rect x="0" y="0" width="1350" height="40" rx="6" fill="#f0fdf4" stroke="#86efac" stroke-width="1.5"/>
    <text x="20" y="25" font-size="13" font-weight="bold" fill="#15803d">PLANT TRANSPIRATION STREAM (水稻茎流方向):</text>
    <line x1="380" y1="20" x2="1280" y2="20" stroke="#16a34a" stroke-width="3" marker-end="url(#arrow)"/>
    <text x="830" y="15" text-anchor="middle" font-size="11" font-weight="bold" fill="#16a34a">UPSTREAM (基部/下部) ➔➔➔ HEATER (热脉冲施加点) ➔➔➔ DOWNSTREAM (穗部/上部)</text>
  </g>

  <!-- Physical Comparison of 3 Pitch Versions: 2mm, 3mm, 4mm -->
  <!-- Variant A: 2 mm Spacing -->
  <g transform="translate(60, 190)">
    <!-- FPC Substrate Outline -->
    <path d="M 0 35 L 20 10 L 320 10 L 340 35 L 320 60 L 20 60 Z" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <text x="15" y="-10" font-size="14" font-weight="bold" fill="#b45309">Variant 1: 2.0 mm Center-to-Center Spacing (微细茎秆适用)</text>
    <!-- Components -->
    <!-- TMP117 UP -->
    <rect x="70" y="23" width="24" height="24" rx="2" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
    <text x="82" y="39" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">UP</text>
    <!-- PTC Heater -->
    <rect x="160" y="26" width="20" height="18" rx="2" fill="#ea580c" stroke="#9a3412" stroke-width="1.5"/>
    <text x="170" y="39" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">PTC</text>
    <!-- TMP117 DOWN -->
    <rect x="246" y="23" width="24" height="24" rx="2" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
    <text x="258" y="39" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">DN</text>

    <!-- Dimension lines -->
    <!-- d1: UP to PTC -->
    <line x1="82" y1="75" x2="170" y2="75" stroke="#2563eb" stroke-width="1.5" marker-start="url(#dim-arrow)" marker-end="url(#dim-arrow)"/>
    <line x1="82" y1="50" x2="82" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="170" y1="46" x2="170" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="126" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#2563eb">d = 2.0 mm</text>

    <!-- d2: PTC to DN -->
    <line x1="170" y1="75" x2="258" y2="75" stroke="#2563eb" stroke-width="1.5" marker-start="url(#dim-arrow)" marker-end="url(#dim-arrow)"/>
    <line x1="258" y1="50" x2="258" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="214" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#2563eb">d = 2.0 mm</text>

    <!-- Description -->
    <text x="360" y="38" font-size="11" fill="#475569">总探测跨距: 4.0 mm | 候选间距，灵敏度与响应时间待实测</text>
  </g>

  <!-- Variant B: 3 mm Spacing -->
  <g transform="translate(60, 320)">
    <path d="M 0 35 L 20 10 L 400 10 L 420 35 L 400 60 L 20 60 Z" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <text x="15" y="-10" font-size="14" font-weight="bold" fill="#b45309">Variant 2: 3.0 mm Center-to-Center Spacing (标准水稻基部适用)</text>
    <!-- TMP117 UP -->
    <rect x="70" y="23" width="24" height="24" rx="2" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
    <text x="82" y="39" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">UP</text>
    <!-- PTC Heater -->
    <rect x="205" y="26" width="20" height="18" rx="2" fill="#ea580c" stroke="#9a3412" stroke-width="1.5"/>
    <text x="215" y="39" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">PTC</text>
    <!-- TMP117 DOWN -->
    <rect x="336" y="23" width="24" height="24" rx="2" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
    <text x="348" y="39" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">DN</text>

    <!-- Dimension lines -->
    <line x1="82" y1="75" x2="215" y2="75" stroke="#2563eb" stroke-width="1.5" marker-start="url(#dim-arrow)" marker-end="url(#dim-arrow)"/>
    <line x1="82" y1="50" x2="82" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="215" y1="46" x2="215" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="148" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#2563eb">d = 3.0 mm</text>

    <line x1="215" y1="75" x2="348" y2="75" stroke="#2563eb" stroke-width="1.5" marker-start="url(#dim-arrow)" marker-end="url(#dim-arrow)"/>
    <line x1="348" y1="50" x2="348" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="281" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#2563eb">d = 3.0 mm</text>

    <text x="440" y="38" font-size="11" fill="#475569">总探测跨距: 6.0 mm | 候选间距，热传导与对流比例待标定</text>
  </g>

  <!-- Variant C: 4 mm Spacing -->
  <g transform="translate(60, 450)">
    <path d="M 0 35 L 20 10 L 480 10 L 500 35 L 480 60 L 20 60 Z" fill="#fef3c7" stroke="#d97706" stroke-width="2"/>
    <text x="15" y="-10" font-size="14" font-weight="bold" fill="#b45309">Variant 3: 4.0 mm Center-to-Center Spacing (粗节茎秆/灌浆期适用)</text>
    <!-- TMP117 UP -->
    <rect x="70" y="23" width="24" height="24" rx="2" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
    <text x="82" y="39" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">UP</text>
    <!-- PTC Heater -->
    <rect x="250" y="26" width="20" height="18" rx="2" fill="#ea580c" stroke="#9a3412" stroke-width="1.5"/>
    <text x="260" y="39" text-anchor="middle" font-size="8" font-weight="bold" fill="#ffffff">PTC</text>
    <!-- TMP117 DOWN -->
    <rect x="426" y="23" width="24" height="24" rx="2" fill="#3b82f6" stroke="#1d4ed8" stroke-width="1.5"/>
    <text x="438" y="39" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">DN</text>

    <!-- Dimension lines -->
    <line x1="82" y1="75" x2="260" y2="75" stroke="#2563eb" stroke-width="1.5" marker-start="url(#dim-arrow)" marker-end="url(#dim-arrow)"/>
    <line x1="82" y1="50" x2="82" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <line x1="260" y1="46" x2="260" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="171" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#2563eb">d = 4.0 mm</text>

    <line x1="260" y1="75" x2="438" y2="75" stroke="#2563eb" stroke-width="1.5" marker-start="url(#dim-arrow)" marker-end="url(#dim-arrow)"/>
    <line x1="438" y1="50" x2="438" y2="82" stroke="#94a3b8" stroke-width="1" stroke-dasharray="2,2"/>
    <text x="349" y="90" text-anchor="middle" font-size="11" font-weight="bold" fill="#2563eb">d = 4.0 mm</text>

    <text x="520" y="38" font-size="11" fill="#475569">总探测跨距: 8.0 mm | 候选间距，量程与热响应待标定</text>
  </g>

  <!-- Cross-sectional Stackup & Thermal Routing Rules -->
  <g transform="translate(850, 190)">
    <rect x="0" y="0" width="550" height="370" rx="8" fill="#f8fafc" stroke="#cbd5e1" stroke-width="1.5"/>
    <text x="20" y="30" font-size="14" font-weight="bold" fill="#0f172a">FPC 叠层结构与热传导物理边界控制</text>

    <!-- Exploded Layers Visualization -->
    <!-- Layer 1: Coverlay -->
    <rect x="25" y="55" width="500" height="18" rx="2" fill="#fef08a" stroke="#ca8a04"/>
    <text x="275" y="68" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">Top Coverlay (聚酰亚胺 PI 覆盖膜 + 胶层: 12.5µm + 15µm)</text>

    <!-- Layer 2: Copper Traces -->
    <rect x="25" y="85" width="500" height="14" rx="2" fill="#fed7aa" stroke="#ea580c"/>
    <text x="275" y="96" text-anchor="middle" font-size="10" font-weight="bold" fill="#9a3412">Top Copper (18µm 压延铜 RA Cu) — 严格细线上下对称走线</text>

    <!-- Layer 3: Base PI Core -->
    <rect x="25" y="110" width="500" height="24" rx="2" fill="#fef9c3" stroke="#eab308"/>
    <text x="275" y="126" text-anchor="middle" font-size="10" font-weight="bold" fill="#713f12">PI Substrate Core (聚酰亚胺基材: 25µm) — 低热导率基底 (k ≈ 0.12 W/m·K)</text>

    <!-- Layer 4: Bottom Coverlay -->
    <rect x="25" y="145" width="500" height="18" rx="2" fill="#fef08a" stroke="#ca8a04"/>
    <text x="275" y="158" text-anchor="middle" font-size="10" font-weight="bold" fill="#854d0e">Bottom Coverlay (底层 PI 覆盖膜: 12.5µm + 15µm)</text>

    <!-- Thermal Pad & Keepout Highlights -->
    <rect x="20" y="180" width="510" height="175" rx="6" fill="#ffffff" stroke="#ef4444" stroke-width="1.2"/>
    <text x="35" y="202" font-size="11" font-weight="bold" fill="#dc2626">核心工艺与布局禁忌 (Design Rule Highlights):</text>
    <text x="35" y="222" font-size="10" fill="#334155">1. <tspan font-weight="bold">铜箔禁铺 (Copper Keepout):</tspan> PTC 与两颗 TMP117 之间严禁铺设 GND 或电源铜皮！</text>
    <text x="35" y="242" font-size="10" fill="#334155">2. <tspan font-weight="bold">横向热隔离:</tspan> 铜导热系数高达 398 W/m·K，大面积铺铜会造成严重横向热短路；</text>
    <text x="35" y="262" font-size="10" fill="#334155">3. <tspan font-weight="bold">走线对称性:</tspan> I2C 与电源走线沿两侧边缘对称延伸，线宽保持一致 (4~6 mil)；</text>
    <text x="35" y="282" font-size="10" fill="#334155">4. <tspan font-weight="bold">Thermal Pad 工艺:</tspan> TMP117 底部散热焊盘保留铜，但第一版严禁开钢网 (No Paste Mask)；</text>
    <text x="35" y="302" font-size="10" fill="#334155">5. <tspan font-weight="bold">焊盘电气悬空:</tspan> Thermal Pad 保持电气 Floating，避免引入杂散地电位与热串扰；</text>
    <text x="35" y="322" font-size="10" fill="#334155">6. <tspan font-weight="bold">微热电势抑制:</tspan> 采用对称差分温度测量，同温环境下两传感器零位对齐标定。</text>
  </g>

  <!-- Bottom Spec Summary -->
  <g transform="translate(50, 610)">
    <rect x="0" y="0" width="1350" height="150" rx="8" fill="#f1f5f9" stroke="#cbd5e1" stroke-width="1"/>
    <text x="25" y="30" font-size="13" font-weight="bold" fill="#0f172a">FPC 尾部金手指与补强板工程参数 (FPC ZIF Tail &amp; Stiffener Specs):</text>
    <text x="25" y="55" font-size="11" fill="#334155">• 引脚定义: 1=3V3, 2=GND, 3=SDA, 4=SCL, 5=HEATER_VCC, 6=HEATER_RETURN</text>
    <text x="25" y="78" font-size="11" fill="#334155">• 金手指间距: 0.50 mm Pitch | 导体宽度: 0.30 mm | 裸铜表面处理: ENIG (化学镍金 / 沉金 ≥ 2u")</text>
    <text x="25" y="101" font-size="11" fill="#334155">• 补强板材质: PI 补强 (Polyimide Stiffener) 或 FR-4 补强，金手指插入端总厚度严格匹配 ZIF 规范为 0.30 mm（公差与配合待验证）</text>
    <text x="25" y="124" font-size="11" fill="#334155">• 翻盖插拔锁紧方向: 配合主控板水平翻盖式 0.5mm 6P 连接器 (C202118) 严密锁合，防脱拔抗拉扯</text>
  </g>

</svg>'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)

if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    generate_sensor_fpc_svg(out / "Sensor_FPC_V01_Schematic.svg")
    generate_sensor_geometry_svg(out / "Rice_SapFlow_Sensor_Geometry_Layout.svg")
    print("Sensor SVGs generated.")
