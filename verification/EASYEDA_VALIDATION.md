# 嘉立创 EDA 重建与验证记录

日期：2026-10-03

本次现场工作只以 EasyEDA Pro V4 工程为验证对象。工程 UUID 为 `cf823b99abc3472f86efd2c874825dfb`，导出包为 [Rice_SapFlow_V01_EasyEDA.epro2](Rice_SapFlow_V01_EasyEDA.epro2)，导出结果报告 ZIP 完整性通过，但 `restoreVerified=false`，因此导出包尚未被重新导入验证。

现场建立了两个组合：`Main_Controller_V01`（页 `Main_Controller`）和 `Sensor_FPC_V01`（页 `Sensor_FPC`）。保存后分别执行了 typed reload，并用新的 `sch list --include-device-identity --include-pins --include-bbox --include-wires` 回读。

主控页有 19 个器件、41 条实际桩线/导线，原生 `sch drc` 返回 1 条提示级结果；`sch check` 没有浮空引脚、跨线、零长线或网标重复，但提示 19 个器件尚未有功能分区框。传感器页有 6 个器件、22 条实际桩线/导线，原生 `sch drc` 返回 0 条结果；`sch check` 没有浮空引脚、跨线、零长线或网标重复，但保留 1 条 GND 网标方向提示和缺少功能分区框提示。该方向提示的自动重连被几何守卫拒绝，原因是现有导线树有两个线段；没有强行删除或重画它。

现场库身份已回读：TMP117 `C2803242`、AO3400A `C20917`、FH12-6S-0.5SH(55) `C202118`、PRF18BC471QB5RB `C152572`、100 nF 0402 `C1525`、10 µF 0805 `C440198`、100 nF 0603 `C14663`、4.7 kΩ `C23162`、100 Ω `C22775`、100 kΩ `C25803`。原项目把 C1523（实际 1 nF）写成 100 nF，已修正为 C1525；原项目把 C6364657 当作 FH12，已修正为 C202118。

明确不用的 TMP117 ALERT/EP、接口保留脚和排针未用脚均用原生 NC 标记。电气连接使用真实非零桩线和电源/地/网络标记，未把同名文字单独当作连通证据。

仍未完成的内容：两个 EasyEDA PCB 页当前均为空（`pcb list` 返回 0 个器件），因此没有运行空板 DRC，也没有把空板结果当成项目通过；尚未完成布局、布线和铺铜。主控页与传感器页的功能分区框尚未绘制；SuperMini 的具体型号、排针顺序和天线净空尚未由实物确认；FH12 的下接触方向、FPC 插入宽度、接触长度和总厚度尚未实测；PRF18 作为植物热源的温升、校准和组织安全性尚未验证。因此本工程当前是可编辑的原理图候选，不能作为量产或下单依据。

相关原始回读包括：`easyeda_main_fresh_final.json`、`easyeda_sensor_fresh_final.json`、`easyeda_board_list_final.json`、`easyeda_project_export.json`、`easyeda_health_final.json`。
