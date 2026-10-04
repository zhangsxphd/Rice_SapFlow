import os
from pathlib import Path

def generate_main_controller_pcb_svg(filepath):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1200 900" width="1200" height="900" style="background:#0f172a; font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;">
  <defs>
    <pattern id="pcb-grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    </pattern>
    <filter id="pcb-shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="8" stdDeviation="10" flood-opacity="0.3" flood-color="#000000"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#0b1120"/>
  <rect width="100%" height="100%" fill="url(#pcb-grid)"/>

  <!-- Title & Banner -->
  <text x="60" y="50" font-size="22" font-weight="bold" fill="#38bdf8">Main_Controller_V01: PCB Concept (Not a CAD Export)</text>
  <text x="60" y="78" font-size="13" fill="#94a3b8">2-Layer FR-4 (1.6 mm, 1 oz) | Dimensions: 50.0 mm × 32.0 mm | SMT + THT Mixed Assembly</text>

  <!-- PCB Board Body -->
  <!-- Origin at (150, 120), Width: 800px (50mm, 16px/mm), Height: 512px (32mm) -->
  <g transform="translate(180, 130)" filter="url(#pcb-shadow)">
    <!-- Board Substrate (FR4 Dark Green Solder Mask) -->
    <rect x="0" y="0" width="800" height="512" rx="24" fill="#064e3b" stroke="#047857" stroke-width="3"/>
    <!-- Copper Pour Simulation (Hatched/Darker Green) -->
    <rect x="12" y="12" width="776" height="488" rx="16" fill="#043828" opacity="0.8"/>

    <!-- 4x Mounting Holes (M3, Dia 3.2mm, Pad Dia 6.0mm) -->
    <!-- Top-Left -->
    <circle cx="35" cy="35" r="24" fill="#d97706" stroke="#b45309" stroke-width="2"/>
    <circle cx="35" cy="35" r="14" fill="#0b1120"/>
    <!-- Bottom-Left -->
    <circle cx="35" cy="477" r="24" fill="#d97706" stroke="#b45309" stroke-width="2"/>
    <circle cx="35" cy="477" r="14" fill="#0b1120"/>
    <!-- Top-Right -->
    <circle cx="765" cy="35" r="24" fill="#d97706" stroke="#b45309" stroke-width="2"/>
    <circle cx="765" cy="35" r="14" fill="#0b1120"/>
    <!-- Bottom-Right -->
    <circle cx="765" cy="477" r="24" fill="#d97706" stroke="#b45309" stroke-width="2"/>
    <circle cx="765" cy="477" r="14" fill="#0b1120"/>

    <!-- Silkscreen Border -->
    <rect x="18" y="18" width="764" height="476" rx="14" fill="none" stroke="#f8fafc" stroke-width="1.2" stroke-dasharray="8,6"/>
    <text x="35" y="90" font-size="14" font-weight="bold" fill="#f8fafc">Rice_SapFlow_V01</text>
    <text x="35" y="110" font-size="11" fill="#cbd5e1">Main_Controller_V1.0</text>

    <!-- Component 1: ESP32-C3 Super Mini Headers (U1) -->
    <!-- Centered horizontally, x = 160 to 500 (Width 340, Height 340) -->
    <rect x="160" y="80" width="340" height="340" rx="8" fill="#0f2b1d" stroke="#f8fafc" stroke-width="1.5"/>

    <!-- Super Mini USB-C / RF Antenna Keepout Zone (Overhanging top edge) -->
    <rect x="260" y="60" width="140" height="42" rx="4" fill="#1e293b" stroke="#cbd5e1" stroke-width="1.2"/>
    <text x="330" y="85" text-anchor="middle" font-size="10" font-weight="bold" fill="#f8fafc">USB-C Receptacle</text>

    <!-- Super Mini Label inside body -->
    <text x="330" y="125" text-anchor="middle" font-size="13" font-weight="bold" fill="#38bdf8">U1: ESP32-C3 Super Mini</text>
    <text x="330" y="143" text-anchor="middle" font-size="10" fill="#94a3b8">2×8 2.54mm Socket (Row Pitch: 17.78 mm / 700 mil)</text>

    <!-- PCB Antenna on top edge -->
    <path d="M 270 42 L 390 42" stroke="#f59e0b" stroke-width="3"/>
    <text x="330" y="35" text-anchor="middle" font-size="10" font-weight="bold" fill="#f59e0b">2.4GHz Antenna Keepout (Top Edge)</text>

    <!-- 1x8 Header Pin Left -->
    <g transform="translate(180, 160)">
      <!-- Pins 1 to 8: 5V, GND, 3V3, IO0, IO1, IO2, IO3, IO4 -->
      <!-- Pitch 2.54mm = ~30px -->
      <!-- Pin 1: 5V -->
      <circle cx="15" cy="15" r="10" fill="#dc2626" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="15" r="5" fill="#fef2f2"/>
      <text x="35" y="20" font-size="11" font-weight="bold" fill="#f8fafc">1: 5V</text>

      <!-- Pin 2: GND -->
      <circle cx="15" cy="45" r="10" fill="#334155" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="45" r="5" fill="#fef2f2"/>
      <text x="35" y="50" font-size="11" font-weight="bold" fill="#f8fafc">2: GND</text>

      <!-- Pin 3: 3V3 -->
      <circle cx="15" cy="75" r="10" fill="#2563eb" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="75" r="5" fill="#fef2f2"/>
      <text x="35" y="80" font-size="11" font-weight="bold" fill="#f8fafc">3: 3V3</text>

      <!-- Pin 4: IO0 (SDA) -->
      <circle cx="15" cy="105" r="10" fill="#0891b2" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="105" r="5" fill="#fef2f2"/>
      <text x="35" y="110" font-size="11" font-weight="bold" fill="#38bdf8">4: IO0 (SDA)</text>

      <!-- Pin 5: IO1 (SCL) -->
      <circle cx="15" cy="135" r="10" fill="#0891b2" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="135" r="5" fill="#fef2f2"/>
      <text x="35" y="140" font-size="11" font-weight="bold" fill="#38bdf8">5: IO1 (SCL)</text>

      <!-- Pin 6: IO2 -->
      <circle cx="15" cy="165" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="165" r="5" fill="#fef2f2"/>
      <text x="35" y="170" font-size="10" fill="#94a3b8">6: IO2</text>

      <!-- Pin 7: IO3 (HEATER_EN) -->
      <circle cx="15" cy="195" r="10" fill="#ea580c" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="195" r="5" fill="#fef2f2"/>
      <text x="35" y="200" font-size="11" font-weight="bold" fill="#fb923c">7: IO3 (HTR_EN)</text>

      <!-- Pin 8: IO4 -->
      <circle cx="15" cy="225" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="225" r="5" fill="#fef2f2"/>
      <text x="35" y="230" font-size="10" fill="#94a3b8">8: IO4</text>
    </g>

    <!-- 1x8 Header Pin Right -->
    <g transform="translate(465, 160)">
      <!-- Pins 9 to 16: IO5 to IO10, etc. -->
      <circle cx="15" cy="15" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="15" r="5" fill="#fef2f2"/>
      <text x="-10" y="20" text-anchor="end" font-size="10" fill="#94a3b8">IO5 :9</text>

      <circle cx="15" cy="45" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="45" r="5" fill="#fef2f2"/>
      <text x="-10" y="50" text-anchor="end" font-size="10" fill="#94a3b8">IO6 :10</text>

      <circle cx="15" cy="75" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="75" r="5" fill="#fef2f2"/>
      <text x="-10" y="80" text-anchor="end" font-size="10" fill="#94a3b8">IO7 :11</text>

      <circle cx="15" cy="105" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="105" r="5" fill="#fef2f2"/>
      <text x="-10" y="110" text-anchor="end" font-size="10" fill="#94a3b8">IO8 :12</text>

      <circle cx="15" cy="135" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="135" r="5" fill="#fef2f2"/>
      <text x="-10" y="140" text-anchor="end" font-size="10" fill="#94a3b8">IO9 :13</text>

      <!-- Pin 14: IO10 (RESERVED) -->
      <circle cx="15" cy="165" r="10" fill="#6366f1" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="165" r="5" fill="#fef2f2"/>
      <text x="-10" y="170" text-anchor="end" font-size="11" font-weight="bold" fill="#a5b4fc">IO10 (RES) :14</text>

      <circle cx="15" cy="195" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="195" r="5" fill="#fef2f2"/>
      <text x="-10" y="200" text-anchor="end" font-size="10" fill="#94a3b8">IO20 :15</text>

      <circle cx="15" cy="225" r="10" fill="#475569" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="15" cy="225" r="5" fill="#fef2f2"/>
      <text x="-10" y="230" text-anchor="end" font-size="10" fill="#94a3b8">IO21 :16</text>
    </g>


    <!-- Power Decoupling Area (Near Pin 1 & Pin 3) -->
    <!-- C1: 10uF (0805) + C2: 100nF (0603) for 5V -->
    <rect x="70" y="165" width="28" height="16" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
    <text x="84" y="196" text-anchor="middle" font-size="9" fill="#f8fafc">C1: 10uF</text>
    <rect x="110" y="165" width="22" height="14" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
    <text x="121" y="194" text-anchor="middle" font-size="8" fill="#f8fafc">C2: 100n</text>

    <!-- C3: 10uF (0805) + C4: 100nF (0603) for 3.3V -->
    <rect x="70" y="225" width="28" height="16" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
    <text x="84" y="256" text-anchor="middle" font-size="9" fill="#f8fafc">C3: 10uF</text>
    <rect x="110" y="225" width="22" height="14" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
    <text x="121" y="254" text-anchor="middle" font-size="8" fill="#f8fafc">C4: 100n</text>

    <!-- I2C Pullup Resistors R1 & R2 (0603) -->
    <rect x="110" y="280" width="22" height="14" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
    <text x="121" y="308" text-anchor="middle" font-size="9" fill="#38bdf8">R1: 4.7k</text>
    <rect x="110" y="320" width="22" height="14" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
    <text x="121" y="348" text-anchor="middle" font-size="9" fill="#38bdf8">R2: 4.7k</text>


    <!-- Component 2: MOSFET Switch & Gate Circuit (Q1, R3, R4) -->
    <g transform="translate(540, 260)">
      <rect x="0" y="0" width="110" height="120" rx="6" fill="#0f2b1d" stroke="#ea580c" stroke-width="1.2" stroke-dasharray="4,3"/>
      <text x="55" y="20" text-anchor="middle" font-size="10" font-weight="bold" fill="#ea580c">Heater Low-Side</text>

      <!-- Q1: AO3400A (SOT-23) -->
      <rect x="35" y="35" width="40" height="30" rx="3" fill="#1e293b" stroke="#f8fafc" stroke-width="1"/>
      <text x="55" y="53" text-anchor="middle" font-size="9" font-weight="bold" fill="#f8fafc">Q1</text>
      <!-- SOT-23 Pads (G, S, D) -->
      <rect x="25" y="40" width="8" height="6" fill="#f59e0b"/>
      <rect x="25" y="52" width="8" height="6" fill="#f59e0b"/>
      <rect x="77" y="46" width="8" height="8" fill="#f59e0b"/>
      <text x="18" y="45" font-size="8" fill="#fb923c">G</text>
      <text x="18" y="58" font-size="8" fill="#cbd5e1">S</text>
      <text x="90" y="53" font-size="8" fill="#fb923c">D</text>

      <!-- R3: 100R (0603) Gate Series -->
      <rect x="10" y="80" width="22" height="14" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
      <text x="21" y="105" text-anchor="middle" font-size="8" fill="#f8fafc">R3:100Ω</text>

      <!-- R4: 100k (0603) Gate Pull-down -->
      <rect x="55" y="80" width="22" height="14" rx="2" fill="#d97706" stroke="#f8fafc" stroke-width="1"/>
      <text x="66" y="105" text-anchor="middle" font-size="8" fill="#f8fafc">R4:100k</text>
    </g>


    <!-- Component 3: Solder Jumper SJ1 (3-Pad) -->
    <g transform="translate(540, 150)">
      <rect x="0" y="0" width="110" height="70" rx="6" fill="#0f2b1d" stroke="#f59e0b" stroke-width="1.2" stroke-dasharray="4,3"/>
      <text x="55" y="18" text-anchor="middle" font-size="10" font-weight="bold" fill="#f59e0b">SJ1 Voltage Select</text>

      <!-- 3 Pads -->
      <rect x="20" y="28" width="18" height="24" rx="2" fill="#2563eb" stroke="#f8fafc" stroke-width="1"/>
      <text x="29" y="44" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">1</text>
      <text x="29" y="62" text-anchor="middle" font-size="8" fill="#93c5fd">3.3V</text>

      <rect x="46" y="28" width="18" height="24" rx="2" fill="#ea580c" stroke="#f8fafc" stroke-width="1"/>
      <text x="55" y="44" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">2</text>
      <text x="55" y="62" text-anchor="middle" font-size="8" fill="#fdba74">VCC</text>

      <rect x="72" y="28" width="18" height="24" rx="2" fill="#dc2626" stroke="#f8fafc" stroke-width="1"/>
      <text x="81" y="44" text-anchor="middle" font-size="9" font-weight="bold" fill="#ffffff">3</text>
      <text x="81" y="62" text-anchor="middle" font-size="8" fill="#fca5a5">5V</text>

      <!-- Jumper is open by default -->
      
      <text x="68" y="25" text-anchor="middle" font-size="7" font-weight="bold" fill="#facc15">OPEN</text>
    </g>


    <!-- Component 4: J1 FPC Connector 6P 0.5mm Horizontal Flip-Lock -->
    <!-- Positioned at bottom center, opening facing downwards -->
    <g transform="translate(300, 425)">
      <rect x="0" y="0" width="200" height="75" rx="4" fill="#022c22" stroke="#10b981" stroke-width="2"/>
      <text x="100" y="22" text-anchor="middle" font-size="12" font-weight="bold" fill="#34d399">J1: FPC-0.5-6P (SMT Flip-Lock)</text>
      <text x="100" y="38" text-anchor="middle" font-size="9" fill="#a7f3d0">LCSC C202118 | Bottom Edge Insertion</text>

      <!-- 6 SMT Pins -->
      <!-- 1: 3V3, 2: GND, 3: SDA, 4: SCL, 5: HTR_VCC, 6: HTR_RETURN -->
      <g transform="translate(30, 48)">
        <!-- Pin 1 -->
        <rect x="0" y="0" width="10" height="20" rx="1" fill="#2563eb" stroke="#f8fafc" stroke-width="0.8"/>
        <text x="5" y="-4" text-anchor="middle" font-size="8" fill="#93c5fd">1</text>

        <!-- Pin 2 -->
        <rect x="25" y="0" width="10" height="20" rx="1" fill="#475569" stroke="#f8fafc" stroke-width="0.8"/>
        <text x="30" y="-4" text-anchor="middle" font-size="8" fill="#cbd5e1">2</text>

        <!-- Pin 3 -->
        <rect x="50" y="0" width="10" height="20" rx="1" fill="#0891b2" stroke="#f8fafc" stroke-width="0.8"/>
        <text x="55" y="-4" text-anchor="middle" font-size="8" fill="#67e8f9">3</text>

        <!-- Pin 4 -->
        <rect x="75" y="0" width="10" height="20" rx="1" fill="#0891b2" stroke="#f8fafc" stroke-width="0.8"/>
        <text x="80" y="-4" text-anchor="middle" font-size="8" fill="#67e8f9">4</text>

        <!-- Pin 5 -->
        <rect x="100" y="0" width="10" height="20" rx="1" fill="#dc2626" stroke="#f8fafc" stroke-width="0.8"/>
        <text x="105" y="-4" text-anchor="middle" font-size="8" fill="#fca5a5">5</text>

        <!-- Pin 6 -->
        <rect x="125" y="0" width="10" height="20" rx="1" fill="#ea580c" stroke="#f8fafc" stroke-width="0.8"/>
        <text x="130" y="-4" text-anchor="middle" font-size="8" fill="#fdba74">6</text>
      </g>
      <!-- Plug Direction Arrow -->
      <polygon points="100,78 95,70 105,70" fill="#34d399"/>
      <text x="100" y="68" text-anchor="middle" font-size="8" fill="#34d399">FPC Entry</text>
    </g>


    <!-- Test Points TP1 to TP6 (Arrayed along right board edge) -->
    <g transform="translate(680, 100)">
      <rect x="0" y="0" width="100" height="300" rx="6" fill="#0f2b1d" stroke="#8b5cf6" stroke-width="1.2" stroke-dasharray="4,3"/>
      <text x="50" y="20" text-anchor="middle" font-size="11" font-weight="bold" fill="#c084fc">Test Points</text>

      <!-- TP1: 5V -->
      <circle cx="50" cy="50" r="12" fill="#dc2626" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="50" cy="50" r="5" fill="#fef2f2"/>
      <text x="50" y="74" text-anchor="middle" font-size="9" font-weight="bold" fill="#fca5a5">TP1: 5V</text>

      <!-- TP2: 3V3 -->
      <circle cx="50" cy="95" r="12" fill="#2563eb" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="50" cy="95" r="5" fill="#fef2f2"/>
      <text x="50" y="119" text-anchor="middle" font-size="9" font-weight="bold" fill="#93c5fd">TP2: 3V3</text>

      <!-- TP3: GND -->
      <circle cx="50" cy="140" r="12" fill="#334155" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="50" cy="140" r="5" fill="#fef2f2"/>
      <text x="50" y="164" text-anchor="middle" font-size="9" font-weight="bold" fill="#cbd5e1">TP3: GND</text>

      <!-- TP4: SDA -->
      <circle cx="50" cy="185" r="12" fill="#0891b2" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="50" cy="185" r="5" fill="#fef2f2"/>
      <text x="50" y="209" text-anchor="middle" font-size="9" font-weight="bold" fill="#67e8f9">TP4: SDA</text>

      <!-- TP5: SCL -->
      <circle cx="50" cy="230" r="12" fill="#0891b2" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="50" cy="230" r="5" fill="#fef2f2"/>
      <text x="50" y="254" text-anchor="middle" font-size="9" font-weight="bold" fill="#67e8f9">TP5: SCL</text>

      <!-- TP6: HTR_RET -->
      <circle cx="50" cy="275" r="12" fill="#ea580c" stroke="#f8fafc" stroke-width="1.5"/>
      <circle cx="50" cy="275" r="5" fill="#fef2f2"/>
      <text x="50" y="299" text-anchor="middle" font-size="8" font-weight="bold" fill="#fdba74">TP6: HTR_RET</text>
    </g>

  </g>

  <!-- Technical Spec Legend at bottom -->
  <g transform="translate(180, 690)">
    <rect x="0" y="0" width="800" height="160" rx="8" fill="#1e293b" stroke="#334155" stroke-width="1"/>
    <text x="25" y="30" font-size="14" font-weight="bold" fill="#38bdf8">Main_Controller_V01 物理布线与层叠规范 (PCB Layout Guidelines):</text>
    <text x="25" y="55" font-size="11" fill="#cbd5e1">1. <tspan font-weight="bold">板框尺寸：</tspan>50.0 mm × 32.0 mm，四角带 M3 安装定位孔 (孔心距板边 4.0 mm)；</text>
    <text x="25" y="75" font-size="11" fill="#cbd5e1">2. <tspan font-weight="bold">天线净空：</tspan>ESP32-C3 Super Mini 顶部 PCB 天线外凸或区域正下方顶底层净空铺铜，严禁有铜箔覆盖天线区；</text>
    <text x="25" y="95" font-size="11" fill="#cbd5e1">3. <tspan font-weight="bold">大电流回路：</tspan>5V ➔ SJ1 ➔ J1.Pin5 (HEATER_VCC) 与 J1.Pin6 ➔ Q1.Drain ➔ Source ➔ GND 干线参考 0.25 mm；0.5 mm 间距连接器处细化至 0.15 mm；</text>
    <text x="25" y="115" font-size="11" fill="#cbd5e1">4. <tspan font-weight="bold">I²C 信号布线：</tspan>SDA 与 SCL 等长平行引出至 J1 插座，线宽 8 mil，间距 8 mil，底层敷设完整接地参考平面；</text>
    <text x="25" y="135" font-size="11" fill="#cbd5e1">5. <tspan font-weight="bold">去耦电容就近：</tspan>C1/C2 与 C3/C4 分别紧贴 5V 与 3.3V 排针引脚，过孔直接打入底层主地平面。</text>
  </g>

</svg>'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)

def generate_sensor_fpc_pcb_svg(filepath):
    svg = '''<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1450 950" width="1450" height="950" style="background:#0f172a; font-family:'Segoe UI',-apple-system,BlinkMacSystemFont,Roboto,Helvetica,Arial,sans-serif;">
  <defs>
    <pattern id="fpc-grid" width="20" height="20" patternUnits="userSpaceOnUse">
      <path d="M 20 0 L 0 0 0 20" fill="none" stroke="#1e293b" stroke-width="0.8"/>
    </pattern>
    <filter id="fpc-shadow" x="-5%" y="-5%" width="110%" height="110%">
      <feDropShadow dx="0" dy="6" stdDeviation="8" flood-opacity="0.3" flood-color="#000000"/>
    </filter>
  </defs>

  <rect width="100%" height="100%" fill="#0b1120"/>
  <rect width="100%" height="100%" fill="url(#fpc-grid)"/>

  <!-- Title & Banner -->
  <text x="60" y="50" font-size="22" font-weight="bold" fill="#fbbf24">Sensor_FPC_V01: Flexible PCB Layout &amp; Probe Array (2mm/3mm/4mm)</text>
  <text x="60" y="78" font-size="13" fill="#94a3b8">FPC concept only | Actual routing incomplete | Native DRC pending</text>

  <!-- Flow Direction Vector Banner -->
  <g transform="translate(60, 105)">
    <rect x="0" y="0" width="1330" height="40" rx="6" fill="#14532d" stroke="#22c55e" stroke-width="1.5"/>
    <text x="25" y="25" font-size="13" font-weight="bold" fill="#86efac">PLANT TRANSPIRATION FLOW VECTOR (水稻液流方向):</text>
    <line x1="380" y1="20" x2="1280" y2="20" stroke="#4ade80" stroke-width="3" stroke-linecap="round"/>
    <polygon points="1290,20 1275,13 1275,27" fill="#4ade80"/>
    <text x="830" y="15" text-anchor="middle" font-size="11" font-weight="bold" fill="#4ade80">TMP117_UP (上游测温) ➔➔➔ PTC HEATER (热脉冲激发) ➔➔➔ TMP117_DOWN (顺流峰值响应)</text>
  </g>

  <!-- Detailed PCB Layout View: 3 mm Standard Pitch Probe -->
  <!-- Probe Drawn Horizontally: Left is Gold Finger, Right is Probe Needle Tip -->
  <g transform="translate(60, 180)" filter="url(#fpc-shadow)">
    <rect x="0" y="0" width="1330" height="320" rx="10" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <text x="25" y="32" font-size="15" font-weight="bold" fill="#fde047">Detailed FPC Physical Trace &amp; Component Layout (3.0 mm Standard Pitch Variant)</text>

    <!-- FPC Probe Shape (Amber / Golden Polyimide Base) -->
    <!-- Tail (x=50 to 220, y=70 to 250), Probe Body (x=220 to 1180, y=100 to 220), Tip (x=1180 to 1250) -->
    <path d="M 50 80 L 220 80 L 250 110 L 1180 110 L 1260 160 L 1180 210 L 250 210 L 220 240 L 50 240 Z" fill="#78350f" stroke="#d97706" stroke-width="2.5"/>

    <!-- Gold Finger Area (Tail x=50 to 180) -->
    <rect x="50" y="80" width="130" height="160" fill="#92400e" stroke="#b45309" stroke-width="1"/>
    <text x="115" y="68" text-anchor="middle" font-size="11" font-weight="bold" fill="#fbbf24">ZIF Gold Finger (6P 0.5mm)</text>
    <text x="115" y="260" text-anchor="middle" font-size="9" fill="#fde68a">+ 0.2mm PI Stiffener (Back)</text>

    <!-- 6 Gold Fingers (Pin 1 to 6) -->
    <g transform="translate(55, 95)">
      <!-- 1: 3V3 -->
      <rect x="0" y="0" width="70" height="14" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
      <text x="75" y="11" font-size="9" font-weight="bold" fill="#60a5fa">1: 3V3</text>
      <!-- 2: GND -->
      <rect x="0" y="22" width="70" height="14" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
      <text x="75" y="33" font-size="9" font-weight="bold" fill="#cbd5e1">2: GND</text>
      <!-- 3: SDA -->
      <rect x="0" y="44" width="70" height="14" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
      <text x="75" y="55" font-size="9" font-weight="bold" fill="#38bdf8">3: SDA</text>
      <!-- 4: SCL -->
      <rect x="0" y="66" width="70" height="14" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
      <text x="75" y="77" font-size="9" font-weight="bold" fill="#38bdf8">4: SCL</text>
      <!-- 5: HTR_VCC -->
      <rect x="0" y="88" width="70" height="14" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
      <text x="75" y="99" font-size="9" font-weight="bold" fill="#f87171">5: HTR_VCC</text>
      <!-- 6: HTR_RET -->
      <rect x="0" y="110" width="70" height="14" rx="2" fill="#fbbf24" stroke="#d97706" stroke-width="1"/>
      <text x="75" y="121" font-size="9" font-weight="bold" fill="#fb923c">6: HTR_RET</text>
    </g>

    <!-- Symmetrical Traces Running along Top and Bottom Margins -->
    <!-- Top Margin Traces (3V3, SDA, HTR_VCC) -->
    <path d="M 180 102 L 250 118 L 1150 118" fill="none" stroke="#f87171" stroke-width="2"/>
    <path d="M 180 114 L 250 124 L 1150 124" fill="none" stroke="#60a5fa" stroke-width="2"/>
    <path d="M 180 126 L 250 130 L 1150 130" fill="none" stroke="#38bdf8" stroke-width="2"/>

    <!-- Bottom Margin Traces (GND, SCL, HTR_RET) -->
    <path d="M 180 190 L 250 190 L 1150 190" fill="none" stroke="#38bdf8" stroke-width="2"/>
    <path d="M 180 202 L 250 196 L 1150 196" fill="none" stroke="#cbd5e1" stroke-width="2"/>
    <path d="M 180 214 L 250 202 L 1150 202" fill="none" stroke="#fb923c" stroke-width="2"/>


    <!-- SENSING ZONE (x=450 to 1050) -->
    <!-- Thermal Keepout Zone Boundary (Red Dashed Box) -->
    <rect x="420" y="132" width="670" height="56" rx="4" fill="#450a0a" opacity="0.6" stroke="#ef4444" stroke-width="1.5" stroke-dasharray="4,4"/>
    <text x="755" y="146" text-anchor="middle" font-size="9" font-weight="bold" fill="#fca5a5">STRICT COPPER KEEPOUT ZONE (严禁大面积铺铜 / 仅保留微细对称引线)</text>

    <!-- Component 1: TMP117_UP (WSON-6, 2x2mm) -->
    <!-- Center at x = 500, y = 160 -->
    <g transform="translate(475, 138)">
      <rect x="0" y="0" width="45" height="45" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="22" y="16" text-anchor="middle" font-size="8" font-weight="bold" fill="#38bdf8">TMP117</text>
      <text x="22" y="27" text-anchor="middle" font-size="7" fill="#94a3b8">UP (0x48)</text>
      <!-- Exposed Thermal Pad (Copper with NO Paste Mask, Floating) -->
      <rect x="12" y="30" width="20" height="12" fill="#d97706" stroke="#fbbf24" stroke-width="0.8"/>
      <text x="22" y="39" text-anchor="middle" font-size="6" fill="#fef3c7">PAD:FLOAT</text>

      <!-- Decoupling Cap C1 (0402) Adjacent -->
      <rect x="-24" y="15" width="16" height="12" rx="1" fill="#f59e0b" stroke="#f8fafc" stroke-width="0.8"/>
      <text x="-16" y="38" text-anchor="middle" font-size="7" fill="#fef3c7">C1:100n</text>
    </g>

    <!-- Component 2: PTC Heater (PRF18BC471QB5RB, 0603) -->
    <!-- Center at x = 755, y = 160 (Distance = 255px = 3.0mm in display scale) -->
    <g transform="translate(735, 142)">
      <rect x="0" y="0" width="40" height="36" rx="2" fill="#7c2d12" stroke="#ea580c" stroke-width="2"/>
      <text x="20" y="16" text-anchor="middle" font-size="8" font-weight="bold" fill="#fb923c">PTC</text>
      <text x="20" y="28" text-anchor="middle" font-size="7" fill="#fed7aa">470Ω 0603</text>
      <!-- Two SMT End Electrodes -->
      <rect x="-6" y="8" width="8" height="20" fill="#f97316"/>
      <rect x="38" y="8" width="8" height="20" fill="#f97316"/>
    </g>

    <!-- Component 3: TMP117_DOWN (WSON-6, 2x2mm) -->
    <!-- Center at x = 1010, y = 160 (Distance = 255px = 3.0mm) -->
    <g transform="translate(985, 138)">
      <rect x="0" y="0" width="45" height="45" rx="3" fill="#1e293b" stroke="#38bdf8" stroke-width="1.5"/>
      <text x="22" y="16" text-anchor="middle" font-size="8" font-weight="bold" fill="#38bdf8">TMP117</text>
      <text x="22" y="27" text-anchor="middle" font-size="7" fill="#94a3b8">DN (0x49)</text>
      <!-- Exposed Thermal Pad (Copper with NO Paste Mask, Floating) -->
      <rect x="12" y="30" width="20" height="12" fill="#d97706" stroke="#fbbf24" stroke-width="0.8"/>
      <text x="22" y="39" text-anchor="middle" font-size="6" fill="#fef3c7">PAD:FLOAT</text>

      <!-- Decoupling Cap C2 (0402) Adjacent -->
      <rect x="52" y="15" width="16" height="12" rx="1" fill="#f59e0b" stroke="#f8fafc" stroke-width="0.8"/>
      <text x="60" y="38" text-anchor="middle" font-size="7" fill="#fef3c7">C2:100n</text>
    </g>

    <!-- Dimension Annotation (UP to PTC = 3.0mm, PTC to DN = 3.0mm) -->
    <g transform="translate(0, 75)">
      <!-- d1 -->
      <line x1="497" y1="140" x2="755" y2="140" stroke="#fde047" stroke-width="2"/>
      <polygon points="497,140 507,136 507,144" fill="#fde047"/>
      <polygon points="755,140 745,136 745,144" fill="#fde047"/>
      <line x1="497" y1="110" x2="497" y2="148" stroke="#fde047" stroke-width="1" stroke-dasharray="2,2"/>
      <line x1="755" y1="110" x2="755" y2="148" stroke="#fde047" stroke-width="1" stroke-dasharray="2,2"/>
      <text x="626" y="132" text-anchor="middle" font-size="12" font-weight="bold" fill="#fde047">d = 3.0 mm</text>

      <!-- d2 -->
      <line x1="755" y1="140" x2="1007" y2="140" stroke="#fde047" stroke-width="2"/>
      <polygon points="755,140 765,136 765,144" fill="#fde047"/>
      <polygon points="1007,140 997,136 997,144" fill="#fde047"/>
      <line x1="1007" y1="110" x2="1007" y2="148" stroke="#fde047" stroke-width="1" stroke-dasharray="2,2"/>
      <text x="881" y="132" text-anchor="middle" font-size="12" font-weight="bold" fill="#fde047">d = 3.0 mm</text>
    </g>

    <!-- Probe Tip Geometry Note -->
    <text x="1240" y="165" font-size="10" font-weight="bold" fill="#fbbf24">Tip Needle</text>
    <text x="1240" y="180" font-size="8" fill="#94a3b8">Non-invasive insertion</text>
  </g>


  <!-- Three Spacing Variants Architecture (2mm, 3mm, 4mm) -->
  <g transform="translate(60, 530)">
    <rect x="0" y="0" width="1330" height="370" rx="10" fill="#1e293b" stroke="#334155" stroke-width="1.5"/>
    <text x="25" y="30" font-size="15" font-weight="bold" fill="#38bdf8">三版本中心距尺寸规格与热物性参数对照 (Design Specifications for 2mm / 3mm / 4mm Variants)</text>

    <!-- Table Header -->
    <rect x="25" y="48" width="1280" height="30" fill="#0f172a" stroke="#475569" stroke-width="1"/>
    <text x="40" y="68" font-size="11" font-weight="bold" fill="#93c5fd">版本名称</text>
    <text x="200" y="68" font-size="11" font-weight="bold" fill="#93c5fd">间距 d</text>
    <text x="275" y="68" font-size="11" font-weight="bold" fill="#93c5fd">跨距 2d</text>
    <text x="360" y="68" font-size="11" font-weight="bold" fill="#93c5fd">探针长宽</text>
    <text x="475" y="68" font-size="11" font-weight="bold" fill="#93c5fd">适用作物生长阶段与茎秆直径</text>
    <text x="770" y="68" font-size="11" font-weight="bold" fill="#93c5fd">热脉冲测定算法与流速敏感区间</text>
    <text x="1120" y="68" font-size="11" font-weight="bold" fill="#93c5fd">特殊制造要求</text>

    <!-- Row 1: 2 mm -->
    <rect x="25" y="78" width="1280" height="42" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>
    <text x="40" y="104" font-size="11" font-weight="bold" fill="#fde047">Sensor_FPC_2MM</text>
    <text x="200" y="104" font-size="11" fill="#cbd5e1">2.0 mm</text>
    <text x="275" y="104" font-size="11" fill="#cbd5e1">4.0 mm</text>
    <text x="360" y="104" font-size="11" fill="#cbd5e1">36 × 3.2 mm</text>
    <text x="475" y="104" font-size="11" fill="#cbd5e1">水稻苗期/分蘖期分蘖（茎径 2.0 ~ 3.5 mm）</text>
    <text x="770" y="104" font-size="11" fill="#cbd5e1">热扩散时延极短（1~3s），微弱夜间液流及零流标定灵敏</text>
    <text x="1120" y="104" font-size="10" fill="#fca5a5">热隔离槽 0.15mm</text>

    <!-- Row 2: 3 mm -->
    <rect x="25" y="120" width="1280" height="42" fill="#0f172a" stroke="#334155" stroke-width="0.8"/>
    <text x="40" y="146" font-size="11" font-weight="bold" fill="#fde047">Sensor_FPC_3MM (标准)</text>
    <text x="200" y="146" font-size="11" fill="#cbd5e1">3.0 mm</text>
    <text x="275" y="146" font-size="11" fill="#cbd5e1">6.0 mm</text>
    <text x="360" y="146" font-size="11" fill="#cbd5e1">40 × 3.5 mm</text>
    <text x="475" y="146" font-size="11" fill="#cbd5e1">拔节初期/拔节中期主茎（茎径 3.5 ~ 6.0 mm）</text>
    <text x="770" y="146" font-size="11" fill="#cbd5e1">HRM 候选间距，线性区与蒸腾测量范围待实测</text>
    <text x="1120" y="146" font-size="10" fill="#fca5a5">基线零漂标定</text>

    <!-- Row 3: 4 mm -->
    <rect x="25" y="162" width="1280" height="42" fill="#1e293b" stroke="#334155" stroke-width="0.8"/>
    <text x="40" y="188" font-size="11" font-weight="bold" fill="#fde047">Sensor_FPC_4MM</text>
    <text x="200" y="188" font-size="11" fill="#cbd5e1">4.0 mm</text>
    <text x="275" y="188" font-size="11" fill="#cbd5e1">8.0 mm</text>
    <text x="360" y="188" font-size="11" fill="#cbd5e1">45 × 3.8 mm</text>
    <text x="475" y="188" font-size="11" fill="#cbd5e1">抽穗扬花期/灌浆成熟期粗茎（茎径 6.0 ~ 9.0 mm）</text>
    <text x="770" y="188" font-size="11" fill="#cbd5e1">大量程高蒸腾（>30 cm/h），防止强对流热脉冲过冲失真</text>
    <text x="1120" y="188" font-size="10" fill="#fca5a5">防折断倒角 R0.5</text>

    <!-- Key PCB Fabrication Notes -->
    <g transform="translate(25, 215)">
      <rect x="0" y="0" width="1280" height="135" rx="6" fill="#09182a" stroke="#2563eb" stroke-width="1"/>
      <text x="20" y="25" font-size="12" font-weight="bold" fill="#60a5fa">嘉立创 FPC 柔性板制造下单工艺指导 (LCEDA / JLCPCB Flex PCB Parameters):</text>
      <text x="20" y="48" font-size="11" fill="#cbd5e1">• <tspan font-weight="bold">板材与结构：</tspan>双层柔性板 (2-Layer FPC)，基材厚度选用 0.11 mm，铜箔厚度 0.5 oz (18 µm) 压延铜 (RA Cu)；</text>
      <text x="20" y="70" font-size="11" fill="#cbd5e1">• <tspan font-weight="bold">覆盖膜与颜色：</tspan>黄色聚酰亚胺 (Yellow Coverlay)，微阻焊对位精度要求 ±0.05 mm；</text>
      <text x="20" y="92" font-size="11" fill="#cbd5e1">• <tspan font-weight="bold">表面处理：</tspan>沉金工艺 (ENIG 2u")，金手指部位耐插拔，TMP117 细间距 WSON 焊盘平整度极佳；</text>
      <text x="20" y="114" font-size="11" fill="#cbd5e1">• <tspan font-weight="bold">补强工艺 (Stiffener)：</tspan>FPC 插入端金手指背面贴合 PI 补强板，指定插入端总厚度严格满足 0.30 ± 0.03 mm 匹配 ZIF 翻盖锁合。</text>
    </g>
  </g>

</svg>'''
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(svg)

if __name__ == "__main__":
    out = Path(__file__).resolve().parent
    generate_main_controller_pcb_svg(out / "Main_Controller_V01_PCB_Layout.svg")
    generate_sensor_fpc_pcb_svg(out / "Sensor_FPC_V01_PCB_Layout.svg")
    print("PCB Layout SVGs generated.")
