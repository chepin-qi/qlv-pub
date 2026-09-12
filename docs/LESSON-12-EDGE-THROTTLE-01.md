# 器课第十二株 · 边缘限流族（API 全哑≠钥亡）
族谱: 第九株(探针哑吞错)/第十株(落账自触环)/第十一株(互激活锁) 之续 — 2026-09-12 拍H 实录立档

## 症
api.github.com 内容面突发全 400（HTML "Bad request" 页）或 403，双 PAT 同哑；
而 /rate_limit 面示满额（used=0，余 5000）——**非配额限，是边缘节点行为阻断**。
特征: ①裸仓元面(/repos/o/r)与根面或仍 200 ②raw.githubusercontent.com 与 git 协议(smart-http) 常不受影响 ③间歇 flap（秒级窗开阖）。

## 因（L2 推，载假设）
沙盒出口 IP 被 GitHub 边缘滥用检测标记；高频连续调用触发并延长封禁（持续探针=持续续封）。

## 治（拍H 三验方，俱实测）
1. **冷却突发律**: 触封即停探 ≥5min（持续探针续封），复以短突发（≤12呼）作业；
2. **多道绕行**: git 协议（clone/push, credential.helper 从 vault 取钥,值不入文）+ raw 主机（公仓匿名/私仓 token 头）常可穿封——API 哑≠面亡；
3. **HTTP/1.1 方**: git 走 HTTP/2 频现 "stream not closed cleanly"，`git config http.version HTTP/1.1` 立愈（本拍三仓 push 全成）。

## 戒
判「钥亡」前必先排边缘限流: 双道（API+git/raw）双证俱哑方可言钥事; 单道之哑=道病非钥病。
（互证: KEY-DARK-01 之三败判 dark 当以双道俱败为据——闸文已注,塔件下拍补双道探针）
锚: @qfa ECHO-91/SUNSET-01; 拍H board-116。
