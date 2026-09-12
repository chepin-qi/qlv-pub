# binmap_v3.py · BINMAP-v3 九类+misc六子类规则分类器(EXP-016/SI-MAX-TASK-QLV-01)
# 口径: head600字窗,首中即归; 零编数——n实载
import re, collections, math, json
RULES_V3=[("wake",r"WAKE|wake|唤醒|自醒|醒拍|dispatch|唤塔"),
 ("ack",r"收执|收讫|ack|ACK|谢|销号|CLEARED"),
 ("urge",r"催|urge|DEMAND|即拍|不候|deadline|限期|DRIVE-"),
 ("vote",r" vote|投票|表决|会签|附议|【签】|签署"),
 ("verdict",r"判词|裁定|终裁|verdict|【采】|【改】|【立】|RULING|裁决"),
 ("law",r"律|法|规制|LAW|章|铁律|戒|standard|STANDARD|制度"),
 ("data",r"\.json|数据|复算|实测|L1|sha256|median|谱|数据件"),
 ("report",r"报告|总成|盘账|盘|board-|报告书|综述|收评")]
MISC_SUB=[("system_meta",r"系统|版本|v\d+\.\d+|config|配置|环境|kernel|重启"),
 ("architecture",r"架构|机制|四象|环|塔|鼎炉|轮|周天|STACK|ARCH-"),
 ("debug_log",r"404|401|403|error|err|错|bug|失败|冲突|cancelled"),
 ("coordination",r"协调|协作|协同|讨论|接力|relay|配对|互唤|配合"),
 ("resource_plan",r"额度|quota|机时|rate limit|资源|预算|PAT|钥|secrets")]
def classify(t):
    h=t[:600]
    for n,p in RULES_V3:
        if re.search(p,h): return n
    return "misc"
def misc_sub(t):
    h=t[:600]
    for n,p in MISC_SUB:
        if re.search(p,h): return n
    return "unclassified"
def run(texts):
    d=collections.Counter(); s=collections.Counter()
    for t in texts:
        k=classify(t); d[k]+=1
        if k=="misc": s[misc_sub(t)]+=1
    return dict(d), dict(s)
if __name__=="__main__":
    import sys
    texts=[l for l in sys.stdin.read().split("\n\n") if l.strip()]
    d,s=run(texts)
    print(json.dumps({"n":len(texts),"九类":d,"misc子类":s},ensure_ascii=False,indent=1))
