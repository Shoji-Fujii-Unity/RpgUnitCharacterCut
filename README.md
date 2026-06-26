# PNG切り分けツール

このスクリプトは幅512、高さ1024のPNG画像を縦方向に4分割（高さ256ずつ）して、各パーツを出力します。
emon112様のAnima用LoraのRPG Character Sprite [Anima] [Illustrious]用にRPG MAKER UNIT用にPNGを切り分けます。
https://civitai.com/models/1397312/rpg-character-sprite-anima-illustrious

- 出力ファイル名は元のファイル名に次のサフィックスを付けます: `_front`, `_left`, `Right`, `_back`。
 - 透明色は画像の最初の1ドット（左上、座標(0,0)）のRGB色を透明色として扱います。さらに、同系色の範囲を指定するための許容値（`--tolerance`）を指定できます。

依存:

```
pip install pillow
```

使い方:

```
python split_png.py 入力画像.png [--tolerance TOLERANCE]

オプション:
	--tolerance, -t   透明色の許容範囲（RGB距離の最大値）。0=完全一致、例: 30
```

例: `character.png` を処理すると、`character_front.png`, `character_left.png`, `characterRight.png`, `character_back.png` が生成されます。
