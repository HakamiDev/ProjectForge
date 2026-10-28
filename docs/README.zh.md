<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · **中文** · [日本語](README.ja.md) · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**AI 智能体团队的操作系统。** 一条命令即可把一个普通文件夹变成井然有序的办公室：所有智能体在任何平台上都依据同一块看板工作；独立的质量关卡；决策治理；完整的审计追踪；可导出到 Power BI 的绩效指标；以及只需一个 HTML 文件即可运行的管理站点。

Python 3.9 或更高版本，无依赖，无需服务器。开源，采用 MIT 许可。

网站：https://hakamidev.github.io/ProjectForge/

## 安装

只需一行命令，粘贴到终端即可。它会下载工具并运行，提出四个问题，然后打开您的管理站点。

macOS 和 Linux（Terminal）：

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows（PowerShell）：

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

您也可以先在网站上选择平台和首选语言；两项选择都会带入安装命令，并在向导中预先选定。

## 解决的问题

- **对话会遗忘。** 规则和角色说明存放在文件夹中，而不是聊天记忆里，因此任何对话都可以接续工作。
- **智能体相互冲突。** 一块编号看板；“进行中”会锁定一行；校验和保护机制可防止冲突写入。
- **产出无人把关。** 质量保证负责人在成果交到所有者手中之前裁定通过或不通过。
- **决策停滞。** 未决事项最多五项，并设有 48 小时规则：超时后即采纳建议方案。
- **没有任何度量。** `report` 提供交付率、周期时间、QA 通过率以及各角色的工作负载；`export` 为 Power BI 写出 CSV 文件。
- **缺乏问责。** 每一次看板写入都有记录：谁、何时、改了什么。
- **敏感数据流入外部工具。** 具有约束力的数据策略，包含分级分类和获批工具清单。

## 您将获得

- **80 个专业领域**（战略、餐饮、房地产、软件、人力资源、教育等），以及 330 多个现成角色，一键即可添加。
- **18 个分组中的 130 项现成技能。** 技能是一个简短的文件，描述其适用时机、步骤、产出和验收标准，让员工按此执行，而不是临场发挥。
- **四个平台：**Claude、ChatGPT、Grok 和 Gemini。每位员工可以使用不同的平台。
- 网站和向导提供 **27 种界面语言**。首选语言即管理整个系统所用的语言，也是与员工沟通所用的语言。
- 由单个 HTML 文件构成的**管理站点**：看板、团队、决策、指标、现成命令库，以及一个注意力引擎，用于标示哪些事项已逾期或正在等待您处理。

## 命令

`new`、`build`、`watch`、`rows`、`add-row`、`set-status`、`add-role`、`add-skill`、`skills`、`decide`、`status`、`report`、`export`、`check`、`register`、`selftest`。

## 平台

| 平台 | 团队的设置方式 |
| --- | --- |
| Claude | 创建一个以您的项目命名的项目，并添加生成的文件夹。 |
| ChatGPT | 创建一个项目并上传文件夹中的文件。 |
| Grok | 创建一个项目，将 Compass 命令粘贴到其指令中，并添加文件。 |
| Gemini | 为每位员工创建一个 Gem，将其命令粘贴到指令中，并在 Knowledge 下添加文件。 |

请从项目文件夹的原始位置上传文件，并在文件变更后重新上传。据我们所知，Grok 和 Gemini 不会直接写入文件夹，因此需要您自行把它们的产出移入文件夹。这些步骤依据撰写时的公开文档；界面和限制由各平台决定，可能会有变化。

## 当前限制

- 向导和网站提供 27 种语言，但生成的项目文件（规则、角色说明、看板）和管理站点目前以阿拉伯语书写。员工会被告知应使用哪种语言工作，并用该语言回复您。
- 文件名、命令和看板的状态词保持为阿拉伯语，因为工具是按字面读取它们的。
- Windows 安装尚未在真实机器上测试。

## 面向开发者

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

源代码位于 `forge/`；`tools/build-single.py` 会在 `dist/` 中生成单文件工具。模板位于 `forge/templates/`，公开站点位于 `site/`。

## 许可证

MIT。
