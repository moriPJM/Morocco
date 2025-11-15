"""
ベクトル検索（RAG）の動作確認テストスクリプト
"""
import os
import sys
from dotenv import load_dotenv

load_dotenv()

# Streamlit依存を避けるため、直接ai_vector_searchをテスト
try:
    from ai_vector_search import VectorStore, build_docs_from_kb
    print("✓ ai_vector_search モジュールのインポート成功")
except ImportError as e:
    print(f"✗ ai_vector_search モジュールのインポート失敗: {e}")
    sys.exit(1)

# 知識ベースの読み込み
def get_knowledge_base():
    """知識ベースを取得（streamlit_app.pyから簡略化）"""
    import json
    
    base = {
        'country_info': {'name': 'モロッコ王国'},
        'travel_tips': {'best_seasons': {'spring': '3-5月: 温暖で観光に最適'}}
    }
    
    # 外部JSONファイルを読み込み
    kb_dir = os.path.join(os.path.dirname(__file__), 'data', 'ai_knowledge')
    if os.path.isdir(kb_dir):
        for fname in os.listdir(kb_dir):
            if fname.endswith('.json'):
                fpath = os.path.join(kb_dir, fname)
                try:
                    with open(fpath, 'r', encoding='utf-8') as f:
                        data = json.load(f)
                        base.update(data)
                        print(f"  ✓ {fname} を読み込みました")
                except Exception as e:
                    print(f"  ✗ {fname} の読み込み失敗: {e}")
    
    return base

print("\n=== ステップ1: 知識ベースの読み込み ===")
kb = get_knowledge_base()
print(f"知識ベースのキー: {list(kb.keys())}")

print("\n=== ステップ2: ドキュメントの構築 ===")
docs = build_docs_from_kb(kb)
print(f"構築されたドキュメント数: {len(docs)}")
for i, doc in enumerate(docs, 1):
    doc_preview = doc['text'][:100].replace('\n', ' ') + '...' if len(doc['text']) > 100 else doc['text']
    print(f"  Doc {i}: id={doc['id']}, text長={len(doc['text'])}, preview={doc_preview}")

print("\n=== ステップ3: ベクトルストアの構築 ===")
vs = VectorStore()
vs.build(docs)
print(f"✓ ベクトルストア構築完了: {len(docs)}件のドキュメント, 次元={vs._embeddings.shape[1] if vs._embeddings is not None else 'N/A'}")

print("\n=== ステップ4: テストクエリの実行 ===")
test_queries = [
    "マラケシュ2泊3日のモデルコースを提案して",
    "マラケシュ 旅行プラン",
    "マラケシュでおすすめの観光スポット",
    "ラバトの観光情報",
    "モロッコのベストシーズン"
]

for query in test_queries:
    print(f"\n--- クエリ: '{query}' ---")
    results = vs.query(query, top_k=3)
    for i, result in enumerate(results, 1):
        doc_id = result['id']
        score = result['score']
        text = result['text']
        text_preview = text[:150].replace('\n', ' ') + '...' if len(text) > 150 else text
        print(f"  結果 {i}: id={doc_id}, 類似度={score:.1%}")
        print(f"    テキスト: {text_preview}")

print("\n=== ステップ5: マラケシュ関連データの確認 ===")
if 'itineraries' in kb:
    print("✓ itineraries キーが知識ベースに存在します")
    itins = kb['itineraries']
    if isinstance(itins, list):
        marrakech_itins = [it for it in itins if it.get('city') == 'マラケシュ']
        print(f"  マラケシュ関連の旅程数: {len(marrakech_itins)}")
        for itin in marrakech_itins:
            print(f"    - {itin.get('id')}: {itin.get('title')} ({itin.get('duration')})")
else:
    print("✗ itineraries キーが知識ベースに見つかりません")

print("\n=== テスト完了 ===")
print("\n結論:")
print("  ✓ ベクトル検索システムが正常に動作しています" if len(docs) > 0 else "  ✗ ベクトル検索に問題があります")
