#!/usr/bin/env python3
"""
extract_images.py
vmdx / vmod ファイルから images/ フォルダの画像を一括抽出するスクリプト。

使い方:
    python extract_images.py

    vmdx/ フォルダに .vmdx / .vmod ファイルを置いて実行。
    images/cards/ に全画像が展開される。
"""

import zipfile
import os
import sys
from pathlib import Path

# ===== 設定 =====
VMDX_DIR    = Path("vmdx")          # vmdx/vmodファイルを置くフォルダ
OUTPUT_DIR  = Path("images/cards")  # 画像の出力先
EXTENSIONS  = {".vmdx", ".vmod"}    # 対象拡張子
# ================


def extract_images(vmdx_path: Path, output_dir: Path) -> int:
    """1つのvmdxファイルから images/ 以下のPNGを抽出。抽出枚数を返す。"""
    count = 0
    try:
        with zipfile.ZipFile(vmdx_path, 'r') as z:
            for entry in z.namelist():
                # images/ 以下のPNGのみ対象
                if not entry.lower().startswith("images/"):
                    continue
                if not entry.lower().endswith(".png"):
                    continue
                # ファイル名だけ取り出す（サブディレクトリは作らない）
                filename = Path(entry).name
                if not filename:
                    continue

                dest = output_dir / filename
                # 既存ファイルはスキップ（上書きしない）
                if dest.exists():
                    continue

                data = z.read(entry)
                dest.write_bytes(data)
                count += 1
    except zipfile.BadZipFile:
        print(f"  [SKIP] ZIPとして読めない: {vmdx_path.name}")
    except Exception as e:
        print(f"  [ERROR] {vmdx_path.name}: {e}")
    return count


def main():
    # 出力フォルダ作成
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    # vmdxフォルダ確認
    if not VMDX_DIR.exists():
        VMDX_DIR.mkdir(parents=True)
        print(f"'{VMDX_DIR}' フォルダを作成しました。")
        print(f".vmdx / .vmod ファイルをこのフォルダに置いて再実行してください。")
        sys.exit(0)

    # 対象ファイルを収集
    targets = [
        p for p in VMDX_DIR.iterdir()
        if p.suffix.lower() in EXTENSIONS
    ]

    if not targets:
        print(f"'{VMDX_DIR}' に .vmdx / .vmod ファイルが見つかりません。")
        sys.exit(0)

    print(f"対象ファイル: {len(targets)}件")
    print(f"出力先: {OUTPUT_DIR}\n")

    total = 0
    for path in sorted(targets):
        count = extract_images(path, OUTPUT_DIR)
        print(f"  {path.name}: {count}枚抽出")
        total += count

    existing = len(list(OUTPUT_DIR.glob("*.png")))
    print(f"\n完了。今回抽出: {total}枚 / 累計: {existing}枚")


if __name__ == "__main__":
    main()
