# 已核实的关键帧与文生结构

以下来自开发者指南已读取的第2—3节。`N` 是最后一个实际镜头编号；`S.SS` 是目标时长，保留两位小数。不要把占位符原样交付。

## instruction

T2VA：没有关键帧 instruction，直接从三个主体字段开始。

I2VA：第一行固定为：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.
```

FL2VA：第一行按最终镜头和时长填写：

```text
How the reference pictures align with the target video — Picture 1 (from Shot 1) aligns with the 0.00-second mark of the target video; Picture 2 (from Shot N) aligns with the S.SS-second mark of the target video.
```

L2VA：只有尾帧，不虚构首帧引用：

```text
How the reference pictures align with the target video — <Picture 1> (from [Shot N]) aligns with the S.SS-second mark of the target video.
```

instruction 后空一行，再写主体字段。时长、文件名、标题与审核说明不得放在 instruction 前面。源文件保留排版；H3 Studio 批量版须按 [studio.md](studio.md) 另加行首时长前缀并压平，前缀属于上传封装，不属于本节模型 instruction。

## 三个主体字段

按以下顺序各出现一次：

- `integrated_multimodal_description:` 按时间线组织画面、主体、动作、镜头、说话人、实际台词和同步场景内声音；使用实际的 `[Shot 1]`、`[Shot 2]` 等镜头编号。
- `overall_soundscape:` 概括环境声、物理动作声和需要的非语言人声，与主体中的同步细节一致。
- `non_diegetic_music:` 观众听到、场景角色听不到的背景配乐；不需要时填 `N/A`。

I2VA 路径：首帧锚点 → 动作起点 → 连续变化 → 结果。
FL2VA 路径：首帧状态 → 可观察的中间变化 → 尾帧落点；通常优先连续单镜，但尊重明确的多镜需求。
L2VA 路径：合理前态 → 动作路径 → 最后镜头到达尾帧，不把尾帧误当开头。

下面是一个无旁白的8秒单图示例；时长只是示例，主体与参考图必须实际一致：

```text
For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced.

integrated_multimodal_description: [Shot 1] 8秒连续中景，严格从首帧中的桌面、蓝色瓷杯和窗边构图开始。0—1秒保持现有状态；1—6秒镜头沿桌面轻缓推进，窗帘向右轻摆一次，杯子始终静止，蒸汽自然上升；6—8秒镜头减速停止，保留蒸汽余动。只有窗帘轻擦声，没有人声。

overall_soundscape: 安静室内底噪和一次轻微窗帘摩擦。

non_diegetic_music: N/A
```

历史单图 `How the reference picture(s)...` 句式在部分旧工具中存在；本 Skill 的标准校验器不将它认作标准 I2VA。修订历史文件时说明格式变更，不把旧兼容例当官方当前要求。
