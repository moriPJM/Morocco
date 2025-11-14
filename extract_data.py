#!/usr/bin/env python3
"""
観光地データをstreamlit_app.pyから抽出してJSONファイルに保存するスクリプト
"""

import json
import re
import os

def extract_spots_data():
    """streamlit_app.pyから観光地データを抽出"""
    
    # streamlit_app.pyを読み込み
    with open('streamlit_app.py', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # spotsデータ配列の開始と終了を見つける
    start_pattern = r'spots = \['
    end_pattern = r'    \]\s*\n\s*return spots'
    
    start_match = re.search(start_pattern, content)
    end_match = re.search(end_pattern, content)
    
    if not start_match or not end_match:
        print("データ配列が見つかりませんでした")
        return None
    
    # データ部分を抽出
    data_section = content[start_match.end()-1:end_match.start()+5]  # ]まで含める
    
    # Pythonコードとして評価
    try:
        # 安全にevalするための準備
        spots_data = eval(data_section)
        print(f"抽出成功: {len(spots_data)} 件の観光地データ")
        return spots_data
    except Exception as e:
        print(f"データ抽出エラー: {e}")
        return None

def main():
    """メイン処理"""
    print("観光地データを抽出中...")
    
    spots = extract_spots_data()
    if not spots:
        print("デ���タ抽出に失敗しました")
        return
    
    # dataディレクトリが存在することを確認
    os.makedirs('data', exist_ok=True)
    
    # JSONファイルに保存
    json_path = os.path.join('data', 'spots.json')
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(spots, f, ensure_ascii=False, indent=2)
    
    print(f"データを {json_path} に保存しました")
    print(f"観光地数: {len(spots)} 件")
    
    # データの検証
    cities = set(spot['city'] for spot in spots)
    categories = set(spot['category'] for spot in spots)
    
    print(f"都市数: {len(cities)}")
    print(f"カテゴリ数: {len(categories)}")
    print("都市一覧:", ', '.join(sorted(cities)))
    print("カテゴリ一覧:", ', '.join(sorted(categories)))

if __name__ == "__main__":
    main()