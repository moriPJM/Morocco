"""
ai_vector_search.py

Lightweight in-memory vector store using sentence-transformers + scikit-learn.
This module performs lazy model loading so the app only loads the embedding model when
vector features are required.

API:
- VectorStore(model_name='all-MiniLM-L6-v2')
    - build(docs: List[dict])  # docs: [{'id': str/int, 'text': str, 'meta': {...}}, ...]
    - query(query_text: str, top_k: int=5) -> List[dict]  # returns items with score and meta

Note: sentence-transformers (and its torch dependency) must be installed.
"""
from typing import List, Dict, Optional
import os
import logging
import json

logger = logging.getLogger(__name__)

try:
    # Imports are optional until vector features are used
    from sentence_transformers import SentenceTransformer
    import numpy as np
    from sklearn.neighbors import NearestNeighbors
    _HAS_SBT = True
except Exception:
    SentenceTransformer = None
    np = None
    NearestNeighbors = None
    _HAS_SBT = False


class VectorStore:
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        self.model_name = model_name
        # Avoid referencing SentenceTransformer in type hints when package may be missing
        self.model: Optional[object] = None
        self._embeddings = None  # numpy array (n, d)
        self._ids = []
        self._metas = []
        self._texts = []
        self._nn = None

    def _ensure_model(self):
        if not _HAS_SBT:
            raise ImportError("sentence-transformers or sklearn not installed. Please install requirements.txt")
        if self.model is None:
            logger.info(f"Loading embedding model: {self.model_name}")
            self.model = SentenceTransformer(self.model_name)

    def build(self, docs: List[Dict]):
        """Build the vector index from docs.

        docs: list of {'id': ..., 'text': ..., 'meta': {...}}
        """
        if not docs:
            raise ValueError("No documents provided to build the vector store")
        self._ensure_model()
        texts = [str(d.get('text', '')) for d in docs]
        self._ids = [d.get('id') for d in docs]
        self._metas = [d.get('meta', {}) for d in docs]
        self._texts = texts
        # compute embeddings
        emb = self.model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
        # normalize for cosine similarity
        norms = np.linalg.norm(emb, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        emb = emb / norms
        self._embeddings = emb
        # build nearest neighbors (cosine distance)
        self._nn = NearestNeighbors(n_neighbors=min(10, len(texts)), metric='cosine', algorithm='brute')
        self._nn.fit(self._embeddings)
        logger.info(f"Built vector store with {len(texts)} documents (dim={self._embeddings.shape[1]})")

    def save(self, path: str):
        """Persist embeddings, ids, metas and texts to a .npz/.json sidecar.

        path: base path without extension; will write {path}.npz and {path}.meta.json
        """
        if self._embeddings is None:
            raise RuntimeError("No embeddings to save")
        base = os.path.splitext(path)[0]
        np_path = base + '.npz'
        meta_path = base + '.meta.json'
        # numpy save (float32)
        try:
            import numpy as _np
            _np.savez_compressed(np_path, embeddings=self._embeddings.astype('float32'))
            meta = {
                'ids': list(self._ids),
                'metas': list(self._metas),
                'texts': list(self._texts),
                'model_name': self.model_name
            }
            with open(meta_path, 'w', encoding='utf-8') as f:
                json.dump(meta, f, ensure_ascii=False, indent=2)
            logger.info(f"Saved vector store to {np_path} (+{meta_path})")
            return np_path, meta_path
        except Exception as e:
            logger.warning(f"Failed to save vector store: {e}")
            raise

    @classmethod
    def load(cls, path: str):
        """Load a persisted vector store from disk. path is base without extension or with .npz"""
        base = os.path.splitext(path)[0]
        np_path = base + '.npz'
        meta_path = base + '.meta.json'
        if not os.path.exists(np_path) or not os.path.exists(meta_path):
            raise FileNotFoundError("Persisted vector store not found")
        try:
            import numpy as _np
            arr = _np.load(np_path)
            emb = arr['embeddings']
            with open(meta_path, 'r', encoding='utf-8') as f:
                meta = json.load(f)
            inst = cls(model_name=meta.get('model_name', 'all-MiniLM-L6-v2'))
            inst._ensure_model()
            # normalize if needed
            norms = np.linalg.norm(emb, axis=1, keepdims=True)
            norms[norms == 0] = 1.0
            emb = emb / norms
            inst._embeddings = emb
            inst._ids = meta.get('ids', [])
            inst._metas = meta.get('metas', [])
            inst._texts = meta.get('texts', [])
            inst._nn = NearestNeighbors(n_neighbors=min(10, len(inst._ids)), metric='cosine', algorithm='brute')
            inst._nn.fit(inst._embeddings)
            logger.info(f"Loaded vector store from {np_path} (docs={len(inst._ids)})")
            return inst
        except Exception as e:
            logger.warning(f"Failed to load vector store: {e}")
            raise

    def query(self, query_text: str, top_k: int = 5) -> List[Dict]:
        """Query the store and return top_k nearest documents with similarity scores (0..1).

        Returns list of dict: { 'id', 'score', 'text' (optional in meta), 'meta' }
        """
        if self._nn is None or self._embeddings is None:
            raise RuntimeError("Vector store not built. Call build(docs) first.")
        self._ensure_model()
        q_emb = self.model.encode([query_text], convert_to_numpy=True)
        q_emb = q_emb / (np.linalg.norm(q_emb, axis=1, keepdims=True) + 1e-12)
        distances, indices = self._nn.kneighbors(q_emb, n_neighbors=min(top_k, len(self._ids)))
        results = []
        for dist, idx in zip(distances[0], indices[0]):
            score = 1.0 - float(dist)  # cosine similarity approximate
            results.append({
                'id': self._ids[int(idx)],
                'score': score,
                'meta': self._metas[int(idx)],
                'text': self._texts[int(idx)]
            })
        return results


def build_docs_from_kb(kb: Dict) -> List[Dict]:
    """Flatten knowledge base dict into list of text documents suitable for embedding.

    - Extract city summaries, travel tips, cultural context and create small text blobs.
    - Each document has an 'id' and 'text' and optional 'meta'.
    """
    docs = []
    # country_info
    if 'country_info' in kb:
        ci = kb['country_info']
        text = f"Country: {ci.get('name')} Capital: {ci.get('capital')} Largest: {ci.get('largest_city')} Languages: {', '.join(ci.get('languages', []))}"
        docs.append({'id': 'country_info', 'text': text, 'meta': {'type': 'country_info'}})
    # travel_tips - best seasons
    tt = kb.get('travel_tips', {})
    if 'best_seasons' in tt:
        bs = tt['best_seasons']
        text = ' '.join([f"{k}: {v}" for k, v in bs.items()])
        docs.append({'id': 'best_seasons', 'text': text, 'meta': {'type': 'travel_tips'}})
    # cultural_context
    if 'cultural_context' in kb:
        cc = kb['cultural_context']
        text = ' '.join([f"{k}: {v}" for k, v in cc.items()])
        docs.append({'id': 'cultural_context', 'text': text, 'meta': {'type': 'cultural_context'}})
    # cities
    if 'cities' in kb and isinstance(kb['cities'], dict):
        for city, info in kb['cities'].items():
            parts = []
            if isinstance(info, dict):
                if 'summary' in info:
                    parts.append(info['summary'])
                if 'highlights' in info and isinstance(info['highlights'], list):
                    parts.append('Highlights: ' + '; '.join(info['highlights']))
                if 'tips' in info and isinstance(info['tips'], list):
                    parts.append('Tips: ' + '; '.join(info['tips']))
            text = '\n'.join(parts)
            # Split into paragraph-sized chunks for better retrieval granularity
            paragraphs = []
            # first split on double newlines
            for p in text.split('\n\n'):
                p = p.strip()
                if not p:
                    continue
                # further split long paragraphs into ~400-char chunks
                if len(p) > 800:
                    # naive sentence/char window split
                    start = 0
                    while start < len(p):
                        chunk = p[start:start+400].strip()
                        paragraphs.append(chunk)
                        start += 400
                else:
                    paragraphs.append(p)

            if not paragraphs:
                paragraphs = [text]

            for idx, para in enumerate(paragraphs, start=1):
                doc_id = f'city::{city}::p{idx}' if len(paragraphs)>1 else f'city::{city}'
                # add a short meta to help tagging
                docs.append({'id': doc_id, 'text': para, 'meta': {'type': 'city', 'city': city, 'part': idx}})
    
    # itineraries (旅程データ) - 概要と詳細を分離して検索精度向上
    if 'itineraries' in kb and isinstance(kb['itineraries'], list):
        for itin in kb['itineraries']:
            if not isinstance(itin, dict):
                continue
            itin_id = itin.get('id', 'unknown')
            city = itin.get('city', '')
            duration = itin.get('duration', '')
            
            # ドキュメント1: タイトル・サマリー・主要情報（短く重要な情報を凝縮）
            # 期間を強調するため最初に配置
            summary_parts = []
            if 'duration' in itin:
                summary_parts.append(f"期間: {duration}")
            if 'title' in itin:
                summary_parts.append(f"{itin['title']}")
            if 'summary' in itin:
                summary_parts.append(itin['summary'])
            if 'best_season' in itin:
                summary_parts.append(f"ベストシーズン: {itin['best_season']}")
            if 'budget_range' in itin:
                summary_parts.append(f"予算: {itin['budget_range']}")
            
            # ハイライトも概要に含める
            if 'highlights' in itin and isinstance(itin['highlights'], list):
                summary_parts.append("主な内容: " + ", ".join(itin['highlights']))
            
            summary_text = '\n'.join(summary_parts)
            docs.append({
                'id': f'itinerary::{itin_id}::summary',
                'text': summary_text,
                'meta': {'type': 'itinerary_summary', 'city': city, 'duration': duration, 'full_id': itin_id}
            })
            
            # ドキュメント2-N: 日程詳細（日ごとに分割）
            for day_key in ['day1', 'day2', 'day3', 'day4']:
                if day_key in itin and isinstance(itin[day_key], dict):
                    day_info = itin[day_key]
                    day_parts = [f"{itin.get('title', '')} - {day_info.get('title', day_key)}"]
                    
                    # 各時間帯の活動
                    for time_key in ['morning', 'afternoon', 'evening']:
                        if time_key in day_info and isinstance(day_info[time_key], dict):
                            time_info = day_info[time_key]
                            if 'activities' in time_info and isinstance(time_info['activities'], list):
                                for act in time_info['activities']:
                                    if isinstance(act, dict) and 'spot' in act:
                                        desc = act.get('description', '')
                                        day_parts.append(f"{act['spot']}: {desc}")
                    
                    if len(day_parts) > 1:  # タイトル以外のコンテンツがある場合のみ
                        day_text = '\n'.join(day_parts)
                        docs.append({
                            'id': f'itinerary::{itin_id}::{day_key}',
                            'text': day_text,
                            'meta': {'type': 'itinerary_day', 'city': city, 'duration': duration, 'day': day_key, 'full_id': itin_id}
                        })
    
    return docs
