# H3 Studio 批量时长适配

适用证据：用户2026-09-15提供的工作台截图，以及对应工作台版本的批量时长说明。2～15秒是该工作台的适配范围，不声明为所有 MiniMax H3 接口的通用能力。

## 两份内容各司其职

- **模型提示词原稿**：保留标准 instruction、空行和三个字段，不加中文秒数前缀。通用格式校验器检查这一份。
- **工作台批量粘贴版**：每任务一个物理行，以 `数字秒，` 开头，后接压平的模型提示词。前缀是工作台的任务时长配置，不能为了标准模型格式把它删掉。

```text
6秒，For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced. integrated_multimodal_description: [Shot 1] ... overall_soundscape: ... non_diegetic_music: N/A
13秒，For the target video, at 0.00 seconds into the target video, <Picture 1> (from [Shot 1]) is fully referenced. integrated_multimodal_description: [Shot 1] ... overall_soundscape: ... non_diegetic_music: N/A
```

以上省略号仅说明封装格式，实际交付使用完整正文。

工作台只从每行开头读取“数字＋秒”；正文里的 `13-second continuous shot`、`0—13秒` 或朗诵窗口都不设置请求总时长。无前缀会使用默认时长滑块，所以全部显示“10秒 默认”表示独立时长没有生效。

当前工作台支持2～15秒内的小数，例如 `6.5秒，`。不把超限值截成15秒，先调整分段方案。**单条模式不解析该前缀，必须设置滑块。**生成结果可能受帧数和帧率约束，配置时长不等于已经验收输出时长。

## 导出

先按已确认时长表排序原稿，显式为每个原稿给出一个时长：

```bash
python3 scripts/export_studio_batch.py \
  --prompts shot-01.txt shot-02.txt \
  --durations 6 13 \
  --output studio-batch.txt
```

导出器拒绝缺时长、数量不一致、越界、重复前缀、部分已识别的正文总时长冲突及越界窗口；不会根据动作时间点猜总时长。它检查和封装文本，不提交生成，也不替代语义校验。默认不覆盖文件，确认替换既有导出时使用 `--force`。

导入后必须核对工作台逐条时长标签与时长表一致，且没有意外显示“默认”；未读取实际界面时只能报告本地前缀检查通过。原稿、时长表、导出版保持对应，不能把带前缀单行直接送给通用模型格式校验器或当作所有API的统一输入。

当需要确认工作台是否从最终模型输入剥离前缀时，应检查实际请求链路；本适配未据截图推断它一定剥离。
