# MiniMax H3 Prompt Skill

为 MiniMax H3 编写、改写和检查视频提示词的独立 Codex Skill。可用于广告、产品视频、叙事、对白和旁白等场景，不依赖 H3 Studio 或诗词视频工作流。

## 能做什么

- 按输入选择 T2VA（文生）、I2VA（首帧）、FL2VA（首尾帧）、L2VA（尾帧）。
- 区分素材用途、动作路径、说话人、实际台词、同步音效和背景配乐。
- 检查已核实的结构化格式、关键帧对齐和镜头编号。
- 排查说明文字被念出的问题，明确文本检查与实际声音验收的区别。

不包含视频生成 API，不收集密钥，不自动提交付费任务。全能参考模式仅支持素材用途规划，完整结构化语法尚未核实。不会把英文、单镜头、闭唇或禁止字幕设为所有任务的默认要求。

## 安装

在未安装同名 Skill 的情况下：

```bash
git clone https://github.com/wzhoudargon/minimax-h3-prompt.git ~/.codex/skills/minimax-h3-prompt
```

或者从 Releases 下载 ZIP，解压其中的 `minimax-h3-prompt` 文件夹到 `~/.codex/skills/`。已有安装请先检查本地修改，再更新；不要直接覆盖自己的改动。

安装后在新会话中使用：

> 使用 $minimax-h3-prompt，根据我的参考图写一段 8 秒产品视频提示词，只有环境声，不加配乐。

## 本地格式检查

只需要 Python 3 标准库，在 Skill 目录运行：

```bash
python3 scripts/validate_prompt.py prompt.txt --mode I2VA --duration 8 --image-count 1
python3 scripts/test_validate_prompt.py
python3 scripts/test_studio_batch.py
```

如已确认当前部署的字符上限，可添加 `--max-chars`。检查通过仅代表结构合格，不证明动作合理、台词准确、媒体有效或生成声音通过验收。

## H3 Studio 批量输入

工作台只识别行首的 `数字秒` 来设置每条时长，正文时间不生效。参见 [工作台适配](references/studio.md)，使用 `scripts/export_studio_batch.py` 从标准原稿与逐条时长表导出。通用模型提示词保持原格式；单条生成仍需设置滑块。

## 内容与依据

- [SKILL.md](SKILL.md)：入口与工作流程。
- [模式格式](references/formats.md)：四种已核实格式。
- [对白与声音](references/sound.md)：声音路线及串读排查。
- [来源与验证范围](references/sources.md)：出处和未核实部分。

本版本通过 Skill 结构检查、6组通用格式测试、7组工作台导出测试及16条既有单图提示词格式检查；未完成四种模式的真实生成测试。模型规格和部署能力请以当前官方资料及实际入口为准。

这是独立整理的社区 Skill，不是 MiniMax 官方产品；不分发完整手册或第三方 Skill。
