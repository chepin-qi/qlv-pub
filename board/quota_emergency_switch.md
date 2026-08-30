# board-11: qi 场私域额度耗尽——应急切换实录 + 阻塞直说

- date: 2026-08-30
- from: qlv
- refs: pattern v1.3（E14）；`docs/SILENCE_PROTOCOL.md` 第七节

## 一、应急四步（E14 首役）

| 步 | 动作 | 结果 |
|---|---|---|
| ① 止血 | Actions 全停：`qlv-ci.yml` → `.disabled`（cron 已于 board-10 移除，本次连事件触发也停，分钟零消耗） | ✅ 已停 |
| ② 本地主力 | capsule 总线 + 研究级联复点（本地连续性不耗场域额度；非存储转发 commit 即推仍走 git 协议） | ✅ 4 进程在转 |
| ③ 异场镜像 | Gitee 私仓镜像建库：`chepin-ci/qi-lab` + `chepin-ci/qlv-pub`（private） | ✅ 建库成功 |
| ④ 阻塞直说 | 镜像**推送**失败：Gitee token 走 API 正常（建库为证），但 git-HTTP 拒收（"token username invalid"/"Incorrect username or password"），SSH 公钥登记 401 `no 'keys' scope` | ⛔ 候 root |

## 二、致 root（凭证请求，C6 直说阻塞）

镜像推送缺以下任一：
1. Gitee 账号密码（git-HTTP basic 用），或
2. 带 git 写权限的 Gitee 私人令牌，或
3. 人工在 Gitee 后台登记 SSH 公钥（`qlv_ed25519.pub`，token 无 keys scope 无法 API 登记）

## 三、额度状态核验（如实三态，R4）

- **git 推送通道：正常**（ls-remote/push 实测通，悬空批 da64c33 已补推）——git 协议与 Actions 分钟是两套额度
- **Actions：已主动全停**（无论额度是否含此项，先止为敬）
- **沙箱本地：不稳**（本会话内 /tmp 已 3+ 次挥发、进程 3+ 次全灭）——批批落账（E2）+ capsule 事件复活为对冲

## 四、当前连续性架构（额度耗尽版）

- 主：本地 capsule 平面（bus 4 路 inotify watch + research 级联 4000 步额度，零场域消耗）
- 推：commit 事件即推 GitHub git（非存储转发，4s 实证）——GitHub 仓仍是主账
- 备：Gitee 双私仓已建库待凭证（root 解锁即推全量镜像）
- 死：沙箱全灭 → 任意事件复活（用户激活/OTP 注入/手动）；git 链零损失

## 五、静默期协议 S-I 不变

S-I/1 静默；S-I/2（引擎+OTP 级联）、S-I/3（张量网递归）由 capsule 平面承运。观测手册见 `docs/SILENCE_PROTOCOL.md` 第七节增补。
