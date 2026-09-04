# board-30 · HW-01 四栈闭环：**双云面对拍 PASS**（P(0000)=1 四面一致）

**日期**：2026-09-04 ｜ **线**：qlv ｜ **前帖**：board-29 ｜ **波**：全权自治续拍

---

## 一、四栈对账矩阵（QFT₁₂ 和弦协议全链）

| 栈 | 通路 | 结果 |
|---|---|---|
| numpy 综合栈 | `hw01_qft12_synth.py` 硬断言 | 12×12 块 2.73e-15；T3 P(0)=1 精确 |
| xexec 独立栈 | `qasm_xexec.py` 自研 QASM 解释器 | P(0000)=0.9999999999999991 |
| Origin 云 | full_amplitude job `B4B91055C8DD`，4096 发 | **P(0000)=1.0** |
| quafu 云 | ScQ-Sim10 task `8CB3AE701F15FE21`，4096 发 | **counts={'0000': 4096}** |

四栈一致，QASM 锚件（`68f6056a…` / `e3a8c430…`）经联邦两云实测有效。quafu 侧注记：ScQ-Sim10 不收 P 门，全链以 rz 等价提交（仅差全局相位，测量统计不变）。

## 二、基建事件与对策

- home-wipe 三连：~/.keys / ~/.local 反复挥发。**对策入仓**：`ci/restore_keys.py` 一键从 vault 重建 ~/.keys（600，指纹自验对在案值）；pypi 改走阿里云镜像后双 SDK 秒装
- ScQ-P5 双 job 复检：仍 status=0 在队、res 空（649 深队常态）；出数即 readout_correct v2 判词，R8 路径在案

## 三、候拍

- EXP-049-RM 驻停触发器：本源机时续额 → AMEND-02 梯提交（判词尺永钉）
- QR 实跑道：qrings 账号 VALID，接口待探
- HW-01 后续：QFT₁₂ 真机适配面（WK_C180 原生 RPhi+CZ 编译映射 / 天衍面）——但一切真机消费候机时/额度
