from PIL import Image
import sys
import os
import argparse
import math

SUFFIXES = ["_front", "_left", "Right", "_back"]


def make_transparent_by_color(img: Image.Image, trans_rgb, tolerance: int = 0):
    # img is RGBA
    if tolerance <= 0:
        # exact match (fast path)
        data = list(img.getdata())
        new_data = []
        for px in data:
            if px[:3] == trans_rgb:
                new_data.append((px[0], px[1], px[2], 0))
            else:
                new_data.append((px[0], px[1], px[2], px[3]))
        img.putdata(new_data)
        return img

    tol_sq = tolerance * tolerance
    data = list(img.getdata())
    new_data = []
    r0, g0, b0 = trans_rgb
    for px in data:
        dr = px[0] - r0
        dg = px[1] - g0
        db = px[2] - b0
        dist_sq = dr * dr + dg * dg + db * db
        if dist_sq <= tol_sq:
            new_data.append((px[0], px[1], px[2], 0))
        else:
            new_data.append((px[0], px[1], px[2], px[3]))
    img.putdata(new_data)
    return img


def split_image(path: str, tolerance: int = 0):
    im = Image.open(path).convert("RGBA")
    w, h = im.size
    if (w, h) != (512, 1024):
        print(f"警告: 期待するサイズは512x1024ですが、実際は{w}x{h}です。続行しますが結果が異なる可能性があります。")

    trans_color = im.getpixel((0, 0))[:3]

    base, _ = os.path.splitext(os.path.basename(path))

    for i, suf in enumerate(SUFFIXES):
        top = i * 256
        box = (0, top, 512, top + 256)
        part = im.crop(box)
        part = part.convert("RGBA")
        part = make_transparent_by_color(part, trans_color, tolerance)
        out_name = f"{base}{suf}.png"
        part.save(out_name)
        print(f"Saved: {out_name}")


def parse_args(argv=None):
    p = argparse.ArgumentParser(description="PNGを4分割して透明色を適用します。透明色は(0,0)の色で、許容範囲を指定できます。")
    p.add_argument("input", help="入力PNGファイル")
    p.add_argument("-t", "--tolerance", type=int, default=0,
                   help="透明色の許容範囲（RGB距離の最大値）。0=完全一致、最大約441")
    return p.parse_args(argv)


def main():
    args = parse_args()
    path = args.input
    tol = args.tolerance
    if tol < 0:
        print("--tolerance は0以上の整数で指定してください。")
        return
    if not os.path.exists(path):
        print(f"ファイルが見つかりません: {path}")
        return
    split_image(path, tolerance=tol)


if __name__ == '__main__':
    main()
