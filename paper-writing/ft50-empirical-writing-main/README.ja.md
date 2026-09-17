# FT50 実証論文学術執筆スキル

[English](README.md) | [简体中文](README.zh-CN.md) | [日本語](README.ja.md) | [한국어](README.ko.md)

OpenCode / Claude Code / Codex 向けのFT50実証論文執筆スキル。リサーチクエスチョンの設定から理論構築、識別戦略、実証結果、頑健性検証、メカニズム分析、完全な初稿までをカバーします。

会計学、ファイナンス、経営学、マーケティング、オペレーションズ・情報システム、経済学の6分野にわたるFT50全50誌に対応。

## 機能

AIエージェントをFT50実証論文の **0→初稿 5ステージパイプライン** でガイドします：

| ステージ | 成果物 | 主な出力 |
|---------|--------|---------|
| **S1**: 研究課題とポジショニング | ギャップ表、ジャーナル推薦、貢献ステートメント | どのジャーナルか + 何が新しいか |
| **S2**: 理論と仮説 | 理論枠組み、概念モデル、検証可能仮説 | §2 理論・仮説 草案 |
| **S3**: 識別戦略と研究設計 | DID/RDD/IV/RCT/Synthetic Control、データ記述 | §3-4 研究設計 草案 |
| **S4**: 結果と頑健性 | 主要結果、頑健性ピラミッド、Oster bounds、メカニズム分析 | §5-6 結果・頑健性 草案 |
| **S5**: 執筆と組立 | Introduction、文献レビュー、議論、示唆、Abstract | 完全初稿 |

**ドメイン特化型**：FT50実証研究固有の方法論規範（識別戦略設計、頑健性ピラミッド、Oster boundsによる観測不能選択バイアス処理、メカニズム分析フレームワーク、6分野の査読者期待など）を内蔵しており、一般的な執筆スキルではカバーされません。

### 主な機能

- **識別戦略**：DID（スタガード、連続）、RDD（シャープ、ファジー）、IV（2SLS、Bartik、シフトシェア）、RCT、Synthetic Control、イベントスタディ
- **頑健性ピラミッド**：係数安定性プロット、Oster bounds、代替特定化、反証テスト、サンプル制限
- **メカニズム分析**：媒介効果 vs. 調整効果、横断面不均一性、構造推定
- **分野別ガイダンス**：会計学（TAR, JAE, JAR, CAR, RAST）、ファイナンス（JF, JFE, RFS, JFQA, RF）、経営学（AMJ, AMR, ASQ, OS, SMJ, JOM, JMS, JIBS）、マーケティング（MktSci, JMR, JM, JCR）、オペレーションズ・情報システム（MS, OR, MSOM, ISR）、経済学（AER, ECMA, JPE, QJE, REStud）

---

## インストール

### 1. リポジトリのクローン

```bash
git clone https://github.com/liyuanbo1024/ft50-empirical-writing.git
```

### 2. AIエージェントへのインストール

| エージェント | インストールコマンド |
|-------------|-------------------|
| **OpenCode** | `cp -r ft50-empirical-writing ~/.config/opencode/skills/` |
| **Claude Code** | `cp -r ft50-empirical-writing ~/.claude/skills/` |
| **Codex** | `cp -r ft50-empirical-writing ~/.agents/skills/` |
| **Cursor** | `cp -r ft50-empirical-writing ~/.cursor/skills/` |
| **Windsurf** | `cp -r ft50-empirical-writing ~/.windsurf/skills/` |

インストール後、自然言語でスキルを起動できます：

- `DIDで最低賃金の雇用効果を分析する論文を書きたい。ポジショニングを手伝って`
- `理論枠組みができた。スタガードDIDの識別戦略を設計してBacon分解を処理して`
- `FT50実証論文執筆パイプラインを全部通して`

---

## 使い方

### パイプラインモード

```
「FT50実証論文執筆パイプラインを通して実行して。私のトピックは…」
```

エージェントが現在の段階を評価し、S1→S5まで順次実行。各段階で確認を取ります。

### ステージジャンプ

| トリガーフレーズ | ジャンプ先 |
|----------------|-----------|
| 「研究アイデアがある…」 | S1: ポジショニング |
| 「理論枠組みを構築して」 | S2: 理論と仮説 |
| 「識別戦略を設計して」 | S3: 識別戦略 |
| 「結果を分析して/頑健性チェックを構築して」 | S4: 結果と頑健性 |
| 「完全な論文を書いて」 | S5: 執筆と組立 |

### リファレンスモード

```
「JFの因果識別に対する査読基準は？」
「Oster boundsをどう実装して観測不能選択バイアスを処理する？」
「経営学トップジャーナルの標準的メカニズム分析枠組みは？」
```

---

## ファイル構成

```
ft50-empirical-writing/
├── SKILL.md                              メインスキルファイル
├── references/
│   ├── journal-characteristics.md        50誌のFT50ジャーナル詳細（分野別）
│   ├── identification-strategies.md      DID/RDD/IV/RCT/Synthetic Control/イベントスタディ
│   ├── theory-hypothesis-guide.md        理論枠組み、仮説構築、概念モデル
│   ├── robustness-oster-guide.md         頑健性ピラミッド、Oster bounds、反証テスト
│   ├── mechanism-analysis.md            媒介、調整、不均一性、構造分析
│   ├── data-results-presentation.md      記述統計、結果テーブル、可視化
│   ├── reviewer-expectations.md          分野別FT50査読者期待
│   └── writing-patterns.md               既発表FT50論文の再利用可能な執筆パターン
├── assets/
│   └── regression-table-template.md      標準回帰テーブル規約
├── examples/
│   ├── manuscript_template.tex           ジャーナル形式LaTeXテンプレート
│   └── empirical_analysis.py             DID + Oster bounds 分析テンプレート
├── README.md / README.zh-CN.md / .ja.md / .ko.md
└── LICENSE
```

---

## 対応ジャーナル

### 会計学

**TAR**, **JAE**, **JAR**, **CAR**, **RAST**

### ファイナンス

**JF**, **JFE**, **RFS**, **JFQA**, **RF**

### 経営学

**AMJ**, **AMR**, **ASQ**, **OS**, **SMJ**, **JOM**, **JMS**, **JIBS**

### マーケティング

**MktSci**, **JMR**, **JM**, **JCR**

### オペレーションズ・情報システム

**MS**, **OR**, **MSOM**, **ISR**

### 経済学

**AER**, **ECMA**, **JPE**, **QJE**, **REStud**

---

## カスタマイズ

### ジャーナルの追加

`references/journal-characteristics.md` を編集し、テンプレートに従って新しいジャーナルエントリを追加します。

### 実証分析のデフォルト調整

`examples/empirical_analysis.py` の設定パラメータを変更します：

```python
@dataclass
class EmpiricalConfig:
    cluster_se: str = "state"   # クラスター標準誤差のレベル
    fe_absorb: str = "firm"     # 固定効果吸収変数
    oster_delta: float = 1.0    # Oster delta パラメータ
    # ...
```

---

## ライセンス

MIT License — [LICENSE](LICENSE) 参照。

---

## 謝辞

[agentskills.io](https://agentskills.io) 仕様と [OpenCode](https://github.com/anomalyco/opencode) のスキル作成方法論に基づく。FT50ドメイン知識は Financial Times Top 50 ジャーナルの編集声明と実証経営研究コミュニティの方法論ガイドに依拠。
