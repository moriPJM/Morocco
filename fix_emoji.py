#!/usr/bin/env python
# -*- coding: utf-8 -*-

with open('streamlit_app.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 複数の方法で文字化けを修正
replacements = [
    ('🎪 楽しみ方・周り方', '🎪 楽しみ方・周り方'),
    ('� 楽しみ方・周り方', '🎪 楽しみ方・周り方'),
]

for old, new in replacements:
    content = content.replace(old, new)

with open('streamlit_app.py', 'w', encoding='utf-8') as f:
    f.write(content)

print('修正完了')