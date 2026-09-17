# 経営科学・オペレーションズリサーチ 学術論文作成スキル

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

OpenCode / Claude Code / Codex 向けの経営科学（MS&E）学術論文作成スキル。トピック選定からモデリング、導出、数値実験、完全な初稿までをカバーします。

UTD-24 トップジャーナル **MS, OR, MSOM, POM** と、フィールドジャーナル **TS, TRB, DS, OMEGA, TRE, EJOR, IJPE, IJPR, C&IE** の計13誌に対応。

## 機能

AIエージェントを **0→初稿 5ステージパイプライン** でガイドします：

| ステージ | 成果物 | 主な出力 |
|---------|--------|---------|
| **S1**: トピック選定 | ギャップ表、ジャーナル推薦、貢献ステートメント | どのジャーナルか + 何が新しいか |
| **S2**: モデル構築 | 記法体系、仮定フレームワーク、数式化 | §3 モデル章 草案 |
| **S3**: 導出・分析 | Lemma→Theorem→Corollary 証明連鎖 | §4 分析章 草案 |
| **S4**: 数値実験 | パラメータ校正、感度分析、反実仮想 | §5-6 実験章 草案 |
| **S5**: 執筆・組立 | Introduction、文献レビュー、経営的示唆、Abstract | 完全初稿 |

**ドメイン特化型**：MS&Eジャーナル固有の慣習（モデル記述構造、証明階層、SAR形式の経営的示唆、査読者期待など）を組み込んでいます。

---

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/liyuanbo1024/management-science-writing.git
```

### 2. AIエージェントへのインストール

| エージェント | インストールコマンド |
|-------------|-------------------|
| **OpenCode** | `cp -r management-science-writing ~/.config/opencode/skills/` |
| **Claude Code** | `cp -r management-science-writing ~/.claude/skills/` |
| **Codex** | `cp -r management-science-writing ~/.agents/skills/` |
| **Cursor** | `cp -r management-science-writing ~/.cursor/skills/` |
| **Windsurf** | `cp -r management-science-writing ~/.windsurf/skills/` |

インストール後、自然言語でスキルを起動できます：
- `MSOMに動的価格設定の論文を書きたい。ポジショニングを手伝って`
- `モデルができた。構造的性質を導出して`
- `経営科学の論文執筆パイプラインを全部通して`

---

## 使い方

### パイプラインモード

```
「MS&E論文執筆パイプラインを通して実行して。私のトピックは…」
```

エージェントが現在の段階を評価し、S1→S5まで順次実行。各段階で確認を取ります。

### ステージジャンプ

| トリガーフレーズ | ジャンプ先 |
|----------------|----------|
| 「研究アイデアがある…」 | S1: トピック選定 |
| 「数理モデルを設計して」 | S2: モデル構築 |
| 「導出・証明して…」 | S3: 導出・分析 |
| 「数値実験を設計して」 | S4: 数値実験 |
| 「完全な論文を書いて」 | S5: 執筆・組立 |

### リファレンスモード

```
「MSの証明完全性に対する査読基準は？」
「EJORの経営的示唆はどう構成すべき？」
```

---

## 対応ジャーナル

### Tier 1 (UTD-24)
**Management Science (MS)**, **Operations Research (OR)**, **M&SOM (MSOM)**, **Production & Oper. Mgmt (POM)**

### Tier 2（フィールドジャーナル）
**TS, TRB, DS, OMEGA, TRE, EJOR, IJPE, IJPR, C&IE**

---

## ファイル構成

```
management-science-writing/
├── SKILL.md                              メインスキルファイル
├── references/                           8個の参照ファイル
├── assets/                               定理構造リファレンス
├── examples/                             LaTeXテンプレート + Python実験
├── README.md / README.zh-CN.md / .ja.md / .ko.md
└── LICENSE
```

---

## ライセンス

MIT License — [LICENSE](LICENSE) 参照。

---

## 謝辞

[agentskills.io](https://agentskills.io) 仕様と [OpenCode](https://github.com/anomalyco/opencode) のスキル作成方法論に基づく。MS&Eドメイン知識は INFORMS ジャーナルの編集声明とORコミュニティの出版スタイルガイドに依拠。
