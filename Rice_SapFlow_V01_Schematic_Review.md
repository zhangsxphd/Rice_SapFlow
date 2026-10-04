# Rice_SapFlow_V01 电路复核

本项目最初只有 PCB 和手绘 SVG，没有原生电气原理图。原报告 ERC PASS 的结论没有原生检查证据，现已撤回。嘉立创 EDA 重建参数在 `design/easyeda/`，检查结果在 `verification/`。

主控设计意图：模块提供 +5V、GND、+3V3，GPIO 信号经 SDA/SCL 接传感器；4.7kΩ 上拉到 +3V3。HEATER_EN 经 100Ω 接 AO3400A Gate，100kΩ 从 Gate 到 GND；Source 接 GND，Drain 接 HEATER_RETURN。SJ1 的 1、2、3 分别接 +3V3、HEATER_VCC、+5V，默认开路；只可选一侧焊接，严禁同时桥接两侧。

门极阈值不是充分导通电压；不能用 VGS(th) 推出“3.3V 必然饱和”。AO3400A 库记录提供 2.5V 栅压下的导通电阻，应结合实际脉冲电流与温升验证。100kΩ 下拉保留默认关断意图，软件初始化与实物复位状态尚未测试。

TMP117 的正确引脚为 1 SCL / 2 GND / 3 ALERT / 4 ADD0 / 5 V+ / 6 SDA。原 SVG 混淆 GND 与 ADD0，现已修正。两颗芯片各配 100nF 0402 去耦；采购号改为 **C1525 / CL05B104KO5NNNC，100nF 16V X7R**。原 C1523 是 1nF，不能代替设计要求。

主板 10µF 0805 对应 C440198 / GRM21BR61H106KE43L，额定电压 50V；100nF 0603 对应 C14663。FH12-6S-0.5SH(55) 对应 **C202118**，下接触；原 C6364657 是不同厂家的器件，不能凭名称相近当作同一机械封装。PTC 对应 **PRF18BC471QB5RB / C152572**，原 RB 型号与采购号不符。

FPC 三个候选的单侧测点距热源为 2/3/4 mm，含尖端的总长分别为 36/40/45 mm。禁布区只禁止铺铜，不能同时禁止信号线、焊盘和传感器本身。铜导热旁路的影响需要热学试验，不是“无铺铜便完全消除”。

当前电路设计尚有机械与热源适用性待验证项，不能宣称 ERC、完整布线或量产验证已通过。依据：

- [TI TMP117 数据手册](https://www.ti.com/lit/ds/symlink/tmp117.pdf)
- [Murata PRF 系列手册](https://www.murata.com/-/media/webrenewal/products/thermistor/ptc/prf/bc-e0225x-e.ashx?cvid=20231016060000000000&la=en)
- [Samsung CL05B104KO5NNN 产品参数](https://product.samsungsem.com/mlcc/CL05B104KO5NNN.do)
- [Hirose FH12 产品页](https://www.hirose.com/en/product/p/CL0586-0582-5-55)
