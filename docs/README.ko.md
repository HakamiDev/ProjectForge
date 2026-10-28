<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · [日本語](README.ja.md) · **한국어** · [Kiswahili](README.sw.md)

</p>

**AI 에이전트 팀을 위한 운영 체제.** 명령 하나로 평범한 폴더가 규율 있는 사무실로 바뀝니다. 모든 에이전트가 어떤 플랫폼에서든 하나의 보드를 기준으로 일하고, 독립적인 품질 관문, 의사결정 거버넌스, 완전한 감사 추적, Power BI로 내보낼 수 있는 성과 지표, 그리고 HTML 파일 하나로 실행되는 관리 사이트를 갖추고 있습니다.

Python 3.9 이상, 의존성 없음, 서버 불필요. 오픈 소스이며 MIT 라이선스입니다.

웹사이트: https://hakamidev.github.io/ProjectForge/

## 설치

터미널에 한 줄을 붙여 넣기만 하면 됩니다. 도구를 내려받아 실행하고, 네 가지 질문을 한 뒤, 관리 사이트를 엽니다.

macOS 및 Linux(Terminal):

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows(PowerShell):

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

사이트에서 먼저 플랫폼과 선호 언어를 선택할 수도 있습니다. 두 선택 사항은 설치 명령에 반영되며 마법사에서 미리 선택된 상태로 표시됩니다.

## 해결하는 문제

- **채팅은 잊어버립니다.** 규칙과 역할 지침서는 채팅 기억이 아니라 폴더에 보관되므로, 어떤 채팅에서든 작업을 이어갈 수 있습니다.
- **에이전트끼리 충돌합니다.** 번호가 매겨진 하나의 보드, '진행 중'이 되면 행이 잠기고, 체크섬 보호 장치가 충돌하는 쓰기를 막습니다.
- **검증되지 않은 결과물.** 품질 보증 책임자가 소유자에게 전달되기 전에 합격 또는 불합격을 판정합니다.
- **지연되는 의사결정.** 미결 안건은 최대 5건이며, 48시간 규칙에 따라 기한이 지나면 권고안이 그대로 채택됩니다.
- **측정되는 것이 없습니다.** `report`는 납품률, 사이클 타임, QA 합격률, 역할별 업무량을 보여 주고, `export`는 Power BI용 CSV 파일을 작성합니다.
- **책임 소재가 없습니다.** 보드에 대한 모든 쓰기는 누가, 언제, 무엇을 했는지 기록됩니다.
- **민감한 데이터가 외부 도구로 유출됩니다.** 분류 체계와 승인된 도구를 규정한 구속력 있는 데이터 정책.

## 제공 기능

- **80개 전문 분야**(전략, 외식업, 부동산, 소프트웨어, 인사, 교육 등)와 클릭 한 번으로 추가할 수 있는 330개 이상의 준비된 역할.
- **18개 그룹, 130개의 준비된 스킬.** 스킬은 사용 시점, 단계, 산출물, 합격 기준을 설명하는 짧은 파일로, 직원은 즉흥적으로 처리하지 않고 이를 따라 작업합니다.
- **네 가지 플랫폼:** Claude, ChatGPT, Grok, Gemini. 직원마다 서로 다른 플랫폼을 사용할 수 있습니다.
- 웹사이트와 마법사에서 **27개 인터페이스 언어**를 지원합니다. 선호 언어는 시스템 전체를 관리하는 언어이자 직원과 소통할 때 쓰는 언어입니다.
- HTML 파일 하나로 구성된 **관리 사이트**: 보드, 팀, 의사결정, 지표, 준비된 명령 라이브러리, 그리고 지연되었거나 사용자의 처리를 기다리는 항목을 알려 주는 주의 환기 엔진.

## 명령

`new`, `build`, `watch`, `rows`, `add-row`, `set-status`, `add-role`, `add-skill`, `skills`, `decide`, `status`, `report`, `export`, `check`, `register`, `selftest`.

## 플랫폼

| 플랫폼 | 팀 설정 방법 |
| --- | --- |
| Claude | 프로젝트 이름으로 프로젝트를 만들고 생성된 폴더를 추가합니다. |
| ChatGPT | 프로젝트를 만들고 폴더의 파일을 업로드합니다. |
| Grok | 프로젝트를 만들고 Compass 명령을 지침에 붙여 넣은 뒤 파일을 추가합니다. |
| Gemini | 직원마다 Gem을 만들고 해당 명령을 지침에 붙여 넣은 뒤 Knowledge 아래에 파일을 추가합니다. |

파일은 프로젝트 폴더의 원래 위치에서 업로드하고, 변경된 파일은 다시 업로드하십시오. 저희가 아는 바로는 Grok과 Gemini는 폴더에 직접 쓰지 않으므로, 그 결과물은 직접 폴더로 옮겨야 합니다. 이 절차는 작성 시점의 공개 문서를 따른 것이며, 인터페이스와 제한은 각 플랫폼이 정하므로 변경될 수 있습니다.

## 현재의 제한 사항

- 마법사와 웹사이트는 27개 언어로 표시되지만, 생성되는 프로젝트 파일(규칙, 역할 지침서, 보드)과 관리 사이트는 현재 아랍어로 작성됩니다. 직원에게는 어떤 언어로 일해야 하는지 안내되며, 그 언어로 사용자에게 답변합니다.
- 파일 이름, 명령, 보드의 상태 용어는 도구가 문자 그대로 읽기 때문에 아랍어로 유지됩니다.
- Windows 설치는 아직 실제 기기에서 테스트되지 않았습니다.

## 개발자용

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

소스는 `forge/`에 있으며, `tools/build-single.py`는 `dist/`에 단일 파일 도구를 생성합니다. 템플릿은 `forge/templates/`에, 공개 사이트는 `site/`에 있습니다.

## 라이선스

MIT.
