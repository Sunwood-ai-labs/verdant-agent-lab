# Verdant Agent Lab

> Status: structural prototype. It is not yet a complete visual reproduction of
> the supplied reference. See `docs/reference-fidelity-gate.md` for the hard
> completion criteria and current object-level mismatches.

植物に包まれた研究所を舞台にした、オリジナルのHTMLピクセルオフィス実験です。人物やキャラクターを前提にせず、部屋・家具・机上小物を独立アセットとして分解し、配置データから再構成できる仕組みを目指します。

## Current build

- 4:3の人物なしベースマップ
- EXPLOREモードによるエリア選択とパーツプレビュー
- デスクトップ視差、モバイル拡大・ドラッグ移動
- 10個のエリア別パーツ
- 30個の原画由来オブジェクト切り出し
- 36個の透明な再利用スプライトと3つのversioned manifest
- オブジェクト選択・配置・ドラッグ・削除・永続化・JSON出力ビルダー
- キーボード操作、フォーカス表示、動き低減設定
- 写真を40×30へ正規化した41オブジェクトの構造プロトタイプレイアウト
- 14アンカー構造配置スコア（94.2/100、画像再現度や完成度ではない）
- Pixel Agents既定21×22間取りを保持した、16pxグリッド対応ソーラーパンクプリセット
- 家具64枚・床9枚・接続壁16マスクをまとめる再現可能な開発ランタイムZIP生成

## Preview

```bash
python3 -m http.server 4173 --directory .
```

Then open <http://127.0.0.1:4173>.

- Scene: <http://127.0.0.1:4173/index.html>
- Characterless canonical render: <http://127.0.0.1:4173/canonical.html>
- Builder: <http://127.0.0.1:4173/builder.html>

Pixel Agents向けプリセット:

```bash
npm run build:pixel-agents-solarpunk-default
npm run validate:pixel-agents-solarpunk-default
npm run assemble:pixel-agents-solarpunk-runtime
```

詳細は [`pixel-agents-solarpunk-default/README.md`](pixel-agents-solarpunk-default/README.md) を参照してください。

## Project structure

- `assets/scene-clean.png` — 人物・マスコット・人型ロボットを除去した主背景
- `assets/parts/*.png` — エリア単位の再利用パーツ
- `assets/object-crops/*.png` — 家具・設備・小物単位の切り出し
- `index.html` — シーンと探索UI
- `styles.css` — レスポンシブ配置、照明、ガラス反射、環境演出
- `script.js` — 視差、探索、選択、拡大、パン
- `builder.html` / `builder.js` — 36パーツを配置できるオリジナルビルダー
- `assets/layouts/starter.v1.json` — versionedスターターレイアウト
- `assets/layouts/reference-anchors.v1.json` — 写真から抽出した主要配置アンカー
- `scripts/score-layout.mjs` — 配置の構造類似度ゲート

## Inspiration and originality

設計上の参考は [Pixel Agents](https://github.com/pixel-agents-hq/pixel-agents) の公開ドキュメントです。特に、manifest駆動の家具カタログ、配置JSONと描画資産の分離、Canvasベースのシーン状態という抽象的な構造を参考にしています。

本プロジェクトの家具・床・壁画像、名称、マニフェスト、HTML UIは独自に制作しています。オプションの互換性プリセットだけは、Pixel Agentsの既定21×22配置JSONをMIT Licenseに従って保持し、画像資産を差し替えます。出典とライセンス境界は [`THIRD_PARTY_NOTICES.md`](THIRD_PARTY_NOTICES.md) に記録しています。

## License

MIT. Generated and source-derived visual assets in this repository are published for this project; do not assume they inherit the licenses of unrelated reference projects.
