# Verdant Agent Lab

植物に包まれた研究所を舞台にした、オリジナルのHTMLピクセルオフィス実験です。人物やキャラクターを前提にせず、部屋・家具・机上小物を独立アセットとして分解し、配置データから再構成できる仕組みを目指します。

## Current build

- 4:3の人物なしベースマップ
- EXPLOREモードによるエリア選択とパーツプレビュー
- デスクトップ視差、モバイル拡大・ドラッグ移動
- 10個のエリア別パーツ
- 30個の原画由来オブジェクト切り出し
- キーボード操作、フォーカス表示、動き低減設定

## Preview

```bash
python3 -m http.server 4173 --directory .
```

Then open <http://127.0.0.1:4173>.

## Project structure

- `assets/scene-clean.png` — 人物・マスコット・人型ロボットを除去した主背景
- `assets/parts/*.png` — エリア単位の再利用パーツ
- `assets/object-crops/*.png` — 家具・設備・小物単位の切り出し
- `index.html` — シーンと探索UI
- `styles.css` — レスポンシブ配置、照明、ガラス反射、環境演出
- `script.js` — 視差、探索、選択、拡大、パン

## Inspiration and originality

設計上の参考は [Pixel Agents](https://github.com/pixel-agents-hq/pixel-agents) の公開ドキュメントです。特に、manifest駆動の家具カタログ、配置JSONと描画資産の分離、Canvasベースのシーン状態という抽象的な構造を参考にしています。

Pixel Agentsの名称、ロゴ、キャラクター、家具画像、既定レイアウト、UI文言、ソースコードは利用しません。本プロジェクトの画像、部屋構成、名称、マニフェスト、UIは独自に制作します。

## License

MIT. Generated and source-derived visual assets in this repository are published for this project; do not assume they inherit the licenses of unrelated reference projects.
