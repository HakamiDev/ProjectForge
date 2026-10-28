<p align="center"><img src="../site/logo/logo-192.png" width="96" alt="Project Forge"></p>

# Project Forge

<p align="center">

[English](../README.md) · [العربية](README.ar.md) · [Français](README.fr.md) · [Español](README.es.md) · [Deutsch](README.de.md) · [Italiano](README.it.md) · [Português](README.pt.md) · [Nederlands](README.nl.md) · [Türkçe](README.tr.md) · [Русский](README.ru.md) · [Українська](README.uk.md) · [Македонски](README.mk.md) · [Polski](README.pl.md) · [Română](README.ro.md) · [Ελληνικά](README.el.md) · [فارسی](README.fa.md) · [اردو](README.ur.md) · [हिन्दी](README.hi.md) · [বাংলা](README.bn.md) · [Bahasa Indonesia](README.id.md) · [Bahasa Melayu](README.ms.md) · [Tiếng Việt](README.vi.md) · [ไทย](README.th.md) · [中文](README.zh.md) · **日本語** · [한국어](README.ko.md) · [Kiswahili](README.sw.md)

</p>

**AI エージェントチームのためのオペレーティングシステム。** コマンド 1 つで、ただのフォルダーが規律ある職場に変わります。あらゆるプラットフォームで全エージェントが同じ 1 枚のボードを使って作業し、独立した品質ゲート、意思決定ガバナンス、完全な監査証跡、Power BI にエクスポートできるパフォーマンス指標、そして単一の HTML ファイルで動作する管理サイトを備えています。

Python 3.9 以降、依存関係なし、サーバー不要。オープンソース、MIT ライセンスです。

Web サイト: https://hakamidev.github.io/ProjectForge/

## インストール

ターミナルに 1 行を貼り付けるだけです。ツールをダウンロードして実行し、4 つの質問をしたあと、管理サイトを開きます。

macOS と Linux（Terminal）:

```
curl -fsSL https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.sh | bash
```

Windows（PowerShell）:

```
irm https://raw.githubusercontent.com/HakamiDev/ProjectForge/main/install.ps1 | iex
```

サイトでは、先にプラットフォームと使用言語を選択することもできます。どちらもインストールコマンドに反映され、ウィザードで事前に選択された状態になります。

## 解決する課題

- **チャットは忘れる。** ルールとロール説明書はチャットの記憶ではなくフォルダーに保存されるため、どのチャットからでも作業を再開できます。
- **エージェント同士が衝突する。** 番号付きの 1 枚のボード。「進行中」にすると行がロックされ、チェックサムによる保護で競合する書き込みを防ぎます。
- **未検証の成果物。** 品質保証責任者が、オーナーに届く前に合格か不合格かを判定します。
- **滞る意思決定。** 未決の案件は最大 5 件までで、48 時間ルールにより、期限後は推奨案が採用されます。
- **何も測定されない。** `report` は納品率、サイクルタイム、QA 合格率、ロールごとの負荷を出力し、`export` は Power BI 用の CSV ファイルを書き出します。
- **説明責任がない。** ボードへの書き込みはすべて、誰が、いつ、何を行ったかが記録されます。
- **機密データが外部ツールに流れる。** 分類と承認済みツールを定めた、拘束力のあるデータポリシー。

## 主な機能

- **80 の専門分野**（戦略、飲食、不動産、ソフトウェア、人事、教育など）と、ワンクリックで追加できる 330 以上の用意済みロール。
- **18 グループ、130 の用意済みスキル。** スキルとは、使うべき場面、手順、成果物、受け入れ基準を記した短いファイルで、従業員は場当たり的に対応せず、これに従って作業します。
- **4 つのプラットフォーム:** Claude、ChatGPT、Grok、Gemini。従業員ごとに異なるプラットフォームを使えます。
- Web サイトとウィザードは **27 の表示言語**に対応。優先言語は、システム全体の管理と従業員とのやり取りに使われる言語です。
- 単一の HTML ファイルで動く**管理サイト**: ボード、チーム、意思決定、指標、用意済みコマンドのライブラリ、そして遅延している項目やあなたの対応待ちの項目を知らせるアテンションエンジン。

## コマンド

`new`、`build`、`watch`、`rows`、`add-row`、`set-status`、`add-role`、`add-skill`、`skills`、`decide`、`status`、`report`、`export`、`check`、`register`、`selftest`。

## プラットフォーム

| プラットフォーム | チームのセットアップ方法 |
| --- | --- |
| Claude | プロジェクト名と同じ名前のプロジェクトを作成し、生成されたフォルダーを追加します。 |
| ChatGPT | プロジェクトを作成し、フォルダー内のファイルをアップロードします。 |
| Grok | プロジェクトを作成し、Compass コマンドを指示欄に貼り付けて、ファイルを追加します。 |
| Gemini | 従業員ごとに Gem を作成し、そのコマンドを指示欄に貼り付けて、Knowledge にファイルを追加します。 |

ファイルは元の場所にあるプロジェクトフォルダーからアップロードし、変更があったファイルは再度アップロードしてください。私たちの知る限り、Grok と Gemini はフォルダーに直接書き込まないため、その出力は手動でフォルダーに移してください。手順は執筆時点の公開ドキュメントに基づいています。インターフェースや制限は各プラットフォームが定めるもので、変更される可能性があります。

## 現在の制限

- ウィザードと Web サイトは 27 言語で表示されますが、生成されるプロジェクトファイル（ルール、ロール説明書、ボード）と管理サイトは、現時点ではアラビア語で書かれます。従業員には作業に使う言語が伝えられ、その言語で返答します。
- ファイル名、コマンド、ボードのステータス語は、ツールが文字どおりに読み取るため、アラビア語のままです。
- Windows でのインストールは、まだ実機でテストされていません。

## 開発者向け

```
git clone https://github.com/HakamiDev/ProjectForge.git
cd ProjectForge
python3 -m forge
python3 -I tests/testforge.py
python3 -I tools/build-single.py
python3 -I tools/build-site.py
```

ソースは `forge/` にあります。`tools/build-single.py` は `dist/` に単一ファイルのツールを生成します。テンプレートは `forge/templates/`、公開サイトは `site/` にあります。

## ライセンス

MIT。
