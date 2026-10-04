# Rice_SapFlow_V01 项目完整设计交接与工程交付文档

> **项目名称**：Rice_SapFlow (水稻茎流测量系统)  
> **所属平台**：嘉立创EDA专业版 (EasyEDA Pro Desktop)  
> **工程UUID**：`a422d704ace24952ae3d8c1eb5094d0b` (本地文稿同步工程)  
> **设计交付状态**：**原理图 100% 完成并验证通过，PCB 布局布线 100% 完成并通过原生 DRC 零错误零警告**  
> **交付日期**：2026-10-03  

---

## 一、 系统架构与子系统概述

本项目旨在实现高精度、微功耗的水稻茎流（Sap Flow）热脉冲与热比法测量系统，包含两大核心子系统：
1. **Main_Controller_V01 (主控板)**
   - **文档映射**：原理图 `Main_Controller` (`2d01061a63b3efa0`)，PCB `PCB1` (`82d38807b4b94fc9`)
   - **控制模块**：ESP32-C3 SuperMini 模块（2×8 Pin、2.54 mm 间距双排针插拔结构，17.78 mm 跨距）
   - **电源架构**：USB/外部 5V 主供电，ESP32-C3 SuperMini 板载高精度 LDO 输出 3.3V
   - **去耦网络**：5V 与 3.3V 轨各配置 10 µF (0805) + 100 nF (0603) 高频去耦电容
   - **I²C 通信总线**：GPIO0=SDA，GPIO1=SCL，配置 4.7 kΩ 上拉电阻至 3.3V
   - **加热驱动支路**：AO3400A N-MOSFET (SOT-23) 低边开关；Drain=HEATER_RETURN，Source=GND；栅极串联 100 Ω 驱动电阻至 GPIO3 (HEATER_EN)，并由 100 kΩ 电阻下拉至 GND
   - **电源跳线**：SJ1 3 焊盘焊锡跳线，可硬跳选择加热电源为 3.3V 或 5V，默认连接 5V
   - **引出接口**：J1 为 6P 0.5 mm 间距卧式翻盖 FPC 连接器（引脚定义：1=3V3, 2=GND, 3=SDA, 4=SCL, 5=HEATER_VCC, 6=HEATER_RETURN）
   - **测试点系统**：配置 TP1(5V), TP2(3V3), TP3(GND), TP4(SDA), TP5(SCL), TP6(HEATER_RETURN) 共 6 处测试焊盘

2. **Sensor_FPC_V01 (柔性传感器探针)**
   - **文档映射**：原理图 `Sensor_FPC` (`fda1ce33cb7e4c7a`)，PCB `PCB1_1` (`a35176e7ddcb0d7d`)
   - **测温芯片**：2 颗高精度数字温度计 TMP117MAIDRVR (WSON-6)
     - 上游传感器 U2：ADD0 接地 (GND)，I²C 地址固定为 `0x48`
     - 下游传感器 U3：ADD0 接 3.3V (+3V3)，I²C 地址固定为 `0x49`
     - 本地去耦：每颗 TMP117 电源端就近配置 100 nF (0402) 去耦电容 (C5, C6)
   - **热脉冲发生元件**：PRF18BC471RB5RB PTC 发热电阻 (R5)，阻值 470 Ω，置于两颗 TMP117 之间
   - **几何拓扑与热隔离**：
     - 严格沿水稻液流方向线性排列：`TMP117_UP (U2)` → `PTC (R5)` → `TMP117_DOWN (U3)`，间距 3 mm
     - **严禁大面积铺铜**：传感器区域与 PTC 周边绝对禁止铺设铜皮（零铜箔隔离区），走线严格沿双侧通道对称分布，避免横向热窜扰
     - **热焊盘工艺处理**：TMP117 底部裸焊盘保留铜皮以平整贴装，电气完全悬空，钢网层剔除开孔以防锡膏短路
   - **金手指接口**：尾部设计 6P 0.5 mm 金手指 (J4)，附带加强板（Stiffener）机械结构

---

## 二、 原理图设计与电气规则检查 (ERC) 报告

在进入 PCB 布局前，两张原理图已完成严格设计与原生检验：
1. **Main_Controller 原理图**：
   - 原生 DRC 校验：`nativePassed: true, error: 0, fatal: 0`
   - 网表与走线检查 (`schematic.check`)：`passed: true, total: 0` (0 悬空引脚、0 悬空网络、0 重叠导线)
   - 官方矢量导出：`Main_Controller_V01_Schematic_Final.svg` (及高分渲染 `Main_Controller_V01_Schematic_Final.png`)
2. **Sensor_FPC 原理图**：
   - 原生 DRC 校验：`nativePassed: true, error: 0, fatal: 0`
   - 网表与走线检查 (`schematic.check`)：`passed: true, total: 0`
   - 官方矢量导出：`Sensor_FPC_V01_Schematic_Final.svg` (及高分渲染 `Sensor_FPC_V01_Schematic_Final.png`)

---

## 三、 PCB 布局布线与制造设计检查 (DRC / DFM) 报告

两款 PCB 均采用嘉立创 EDA 专业版官方 API 进行精确参数化设计与验证：

### 1. Main_Controller_V01 (主控板 - 双层硬板 FR-4)
- **板框尺寸**：1180 mil × 1810 mil (约 30.0 mm × 46.0 mm)，带 60 mil 倒圆角
- **层叠与铺铜**：Top Layer 信号走线与器件贴装，Bottom Layer 全局大面积 GND 铺铜平面 (`a652e6f31835f8f4`)
- **布线指标**：共 63 条导线、17 颗标准过孔 (外径 24 mil / 内径 12 mil)，所有电源与地网络均实现低阻抗回流
- **DRC 验证**：
  - 嘉立创原生 DRC：`passed: true, violations: []` (**0 错误、0 警告**)
  - DFM 制造检查 (`easyeda pcb check`)：`ERROR=0`，无悬空线、无尖角走线、无间距冲突、无环孔隐患
- **丝印美化**：执行 `pcb.silk.align` 避让检查，Q1、TP4、TP5 等位号丝印均无压焊盘。

### 2. Sensor_FPC_V01 (柔性传感器板 - 双层聚酰亚胺 FPC)
- **外形尺寸**：320 mil × 1500 mil (约 8.1 mm × 38.1 mm)
- **热隔离布线拓扑 (Manhattan Orthogonal Architecture)**：
  - 西侧走线廊道 (`x = 1200..1250`)：承载 `HEATER_VCC` (8 mil), `SCL` (6 mil), `SDA` (6 mil)
  - 东侧走线廊道 (`x = 1400..1460`)：承载 `HEATER_RETURN` (8 mil), `+3V3` (8 mil), `GND` (8 mil)
  - 中心测温通道 (`x = 1260..1390`)：除 U2、U3、R5 极短出线短桩外，严禁任何铜箔与走线，完全杜绝轴向与横向热桥
- **连接性检查**：全板 6 个网络共 22 个焊盘全部 100% 连通 (`pad_connected = 22/22`)
- **DRC 验证**：
  - 嘉立创原生 DRC：`passed: true, violations: []` (**0 错误、0 警告**)
  - DFM 制造检查 (`easyeda pcb check`)：`ERROR=0`，0 尖角、0 非正交走线、0 悬空线、0 丝印压焊盘
  - 过孔规范：采用嘉立创 FPC 工艺合规的 20 mil 外径 / 12 mil 内径微过孔，所有过孔均置于器件焊盘外侧，避免锡膏流失。

---

## 四、 交付文件清单与结构

本目录 `/Users/zhangshuxuan/本地文稿/Rice_SapFlow_V01/` 下已归档所有生产与交接所需材料：
```text
/Users/zhangshuxuan/本地文稿/Rice_SapFlow_V01/
├── HANDOVER_TO_CODEX.md                     # 本交接总览文件
├── Rice_SapFlow_Complete_BOM.csv           # 完整 BOM 清单 (含立创商城 LCSC 编号与封装)
├── Rice_SapFlow_Complete_Netlist.enet      # 嘉立创标准工程完整网络表
├── Main_Controller_V01_Schematic_Final.svg  # 主控板原理图高清矢量图
├── Main_Controller_V01_Schematic_Final.png  # 主控板原理图光栅预览图
├── Main_Controller_V01_PCB_Final.png        # 主控板 PCB 渲染视图
├── Sensor_FPC_V01_Schematic_Final.svg       # 传感器板原理图高清矢量图
├── Sensor_FPC_V01_Schematic_Final.png       # 传感器板原理图光栅预览图
├── Sensor_FPC_V01_PCB_Final.png             # 传感器板 PCB 渲染视图
├── Main_Controller_V01/                     # 主控板工程备份与离线数据
└── Sensor_FPC_V01/                          # 传感器 FPC 工程备份与离线数据
```

---

## 五、 后续打样与测试注意事项
1. **FPC 打样工艺参数建议**：
   - 基材：聚酰亚胺 (PI) 双面板，铜厚 0.5 oz (18 µm)
   - 阻焊：黄色或黑色覆盖膜 (Coverlay)
   - 表面处理：沉金 (ENIG)，金手指区域需做电金或加厚沉金，并贴合 0.2 mm PI 或不锈钢补强片 (Stiffener)
2. **SMT 贴片建议**：
   - TMP117 (WSON-6) 芯片需严格控制底部散热焊盘锡膏厚度，建议开孔率降为 0%（即第一版不加锡），依靠引脚焊接固定以减少横向导热
   - PRF18BC471 PTC 焊接时避免长时间高温烙铁烫触
3. **固件调试说明**：
   - I²C 频率推荐配置为 400 kHz (Fast Mode)
   - TMP117 单次转换模式功耗极低（3.5 µA），建议采样完成后进入休眠，加热脉冲触发时间由高精度硬件定时器控制 (推荐脉冲持续时间 1.0 ~ 3.0 s)。
