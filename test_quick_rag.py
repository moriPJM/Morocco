from test_vector_search import *

print("\n=== 重要テスト: マラケシュ2泊3日クエリ ===")
kb = get_knowledge_base()
docs = build_docs_from_kb(kb)
vs = VectorStore()
vs.build(docs)

query = "マラケシュ2泊3日のモデルコースを提案して"
results = vs.query(query, top_k=5)

print(f"\nクエリ: '{query}'")
print("=" * 60)
for i, r in enumerate(results, 1):
    print(f"{i}位: {r['id']} (類似度: {r['score']:.1%})")
    if '2n3d' in r['id']:
        print("  ✓ 正解！2泊3日コースが検出されました")
print("\n結果: ", end="")
if results[0]['id'].find('2n3d') >= 0:
    print("✓ 成功！2泊3日コースが1位です")
elif any('2n3d' in r['id'] for r in results[:3]):
    print("⚠ 2泊3日コースは上位3件に入っていますが1位ではありません")
else:
    print("✗ 失敗：2泊3日コースが上位3件に入っていません")
