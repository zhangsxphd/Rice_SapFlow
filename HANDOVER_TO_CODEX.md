# Rice_SapFlow 当前交接

当前项目在 `/Users/zhangshuxuan/本地文稿/Rice_SapFlow_V01`，嘉立创工程 UUID 为 `a422d704ace24952ae3d8c1eb5094d0b`。

以 `README.md`、`docs/OPTIMIZED_DESIGN.md` 和 `verification/optimization/RESULTS.md` 为当前交接依据。当前原生文件为 `Rice_SapFlow_Optimized.epro2`。优化前交接原文保存在 `verification/optimization/HANDOVER_before_optimization.md`，其中的 GPIO0/1/3、PTC 恒定加热、电压跳线、金手指和完成状态描述已经失效。

当前电路：ESP32-C3 插拔模块、HT7530-7 3.0V 受控电源、AO3400A 低侧开关、470Ω ±0.5% 精密加热电阻、双 TMP117、两端 FH12-6S-0.5SH(55) 插座、单孔测试焊盘。固件暂按 GPIO4/3/1 实现 SDA/SCL/HEATER_EN；实际 SuperMini 型号、排距及针脚方向需确认。

已经授权优化现有原理图及 PCB，并配套实现采样、WiFi 原始数据与故障关断。本次没有实物烧录，没有温升、流量标定或制造文件下单。后续继续工作时先读取最终验证记录和原生工程，按实物型号修订，不能从旧报告推断现状，也不要运行旧 KiCad 生成器。
