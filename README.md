# Travel Planner Skill

给 Codex 使用的旅行规划与地图排程技能。它把“查资料 + 排路线 + 做预算”固化成一套可执行流程：事实先核验，地图按道路耗时排，价格标查询时间，无法确认的内容明确标成未核实。

## 它能做什么

- 规划 2–3 个旅行方向，再收敛成逐日时间轴
- 用地图工具排景点顺序、交通方式、距离与耗时
- 核验门票、预约、营业时间、限行和天气
- 生成吃、玩、住、行、拍、避六个维度
- 输出费用区间、隐藏成本、预约倒排和坏天气备选
- 对自驾方案做里程、停车、充电、夜驾和应急检查
- 行程中按“现在在哪、还来不来得及”即时调整

## 安装

把整个目录放进 Codex 的个人 skills 目录。

macOS / Linux：

```bash
git clone https://github.com/VowToMe/travel-planner-skill.git ~/.codex/skills/travel-planner
```

Windows PowerShell：

```powershell
git clone https://github.com/VowToMe/travel-planner-skill.git "$env:USERPROFILE\.codex\skills\travel-planner"
```

重新打开会话后，技能描述会被自动发现。

## 使用示例

```text
帮我规划国庆从杭州出发去福建的 5 天自驾，2 个人，预算 6000。
```

```text
把这三个景点排进西安两天路线，给出行方式和耗时。
```

```text
我们已经在泉州，下午下雨，今天剩下半天怎么改？
```

## 可选工具

技能不绑定特定服务。环境里有地图、火车、航班或酒店连接器时，优先使用结构化结果；没有时使用官方网站并明确标注未核实项。所有价格和库存都必须带查询时间与来源。

## 机械检查

用脚本检查路书是否缺天数、三餐、停车条、预约、应急和费用板块：

```bash
python scripts/check_plan.py 路书.md --drive --days 3
```

退出码 `0` 表示没有 FAIL；`WARN` 不影响退出码，但需要人工复核。

## 隐私

仓库不包含任何个人旅行偏好或行程。技能只使用用户在当前对话中主动给出的条件；持久偏好必须经过用户确认，并保存在用户自己的环境中。

## 许可证与来源

以 MIT License 发布。方法来源与边界见 [SOURCE.txt](SOURCE.txt)。
