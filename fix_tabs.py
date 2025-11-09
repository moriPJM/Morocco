#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ファイルを読み込み
with open('streamlit_app.py', 'r', encoding='utf-8', errors='replace') as f:
    content = f.read()

# 該当する行を置換
old_line = '"📝 概要", "✨ 特徴", "🌟 見どころ", "🎯 楽しみ方", "🚗 アクセス"'
new_line = '"🎯 一言でどんな場所か", "✨ 特徴", "👀 見どころ", "🎪 楽しみ方・周り方", "🚗 アクセス・注意点"'

# 文字化けした行も含めて広範囲に検索・置換
content = content.replace(old_line, new_line)

# 文字化けした文字列も検索して置換
if '� 概要' in content:
    content = content.replace('� 概要', '🎯 一言でどんな場所か')

# ファイルに書き戻し
with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('タブタイトル修正完了')