# 器课第十三株 · 拍中树清族（工作面被拍中清抹）
族谱: 十二株(边缘限流)之续 — 2026-09-12 拍J 实录立档

## 症
沙盒 /tmp 于拍中被清两次: ①四仓克隆全灭 ②git 命令执行中 cwd 消失("Unable to read current working directory")。
次生灾: 克隆检出线途中被清→工作树缺件而 HEAD 有件→`git add -A` 将**缺件判为删除**混入提交——qr_e3_transpile_probe.py 险亡（拍尾核 stat 发现,即恢复）。

## 治（三律,即拍生效）
1. **工作面徙持久挂载**: 克隆仓置 /mnt/agents/output/.work/(vault 同面,实测跨清存活),/tmp 仅弃物。
2. **add 定向律**: 禁 `git add -A`;只 `git add <本拍件路径>` 定向——缺件永不混删。
3. **推前 stat 核**: commit 后 push 前 `git show --stat HEAD` 过目,delete mode 非所谋即恢复(本拍实证救回)。

## 戒
推后必验远端(raw 双道):链件/被伤件俱 200 方宣讫(本拍 chain_head+#206+qr_e3 三验过)。
锚: 器课十二株(边缘限流)同治——一封一清,皆环境之敌,塔件不推则已,推必带核。
