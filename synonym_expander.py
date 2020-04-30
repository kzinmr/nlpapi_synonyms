from collections import defaultdict

import json
import pickle
from pathlib import Path


class SynonymExpander:
    """
    与えられた単語のシノニムからエンティティIDリストを取得する。
     - 単語の同義語拡張を行うだけで、正規化は行わないことに注意。
    """

    def __init__(self, dir_path):

        if isinstance(dir_path, str):
            dir_path = Path(dir_path)

        # QID: wikipedia ページエントリのID
        if (dir_path / "qid2words.pkl").exists() and (
            dir_path / "word2qid.pkl"
        ).exists():
            # QID -> シノニム関係にある単語リスト
            with open(dir_path / "qid2words.pkl", "rb") as fp:
                self.qid2words: Dict[str, List[str]] = pickle.load(fp)
            # 単語 -> QIDリスト
            with open(dir_path / "word2qid.pkl", "rb") as fp:
                self.word2qid: Dict[str, List[str]] = pickle.load(fp)
        else:
            print("No pkl exists.")
            exit(1)

    @classmethod
    def build_wikidata(cls, wikipedia_aliases_path, dir_path="."):
        """ 次の形式の1行jsonから必要な前処理を施す: {'id', 'title', 'aliases'} """

        if isinstance(dir_path, str):
            dir_path = Path(dir_path)

        # QID: wikipedia ページエントリのID
        with open(wikipedia_aliases_path, "r", encoding="utf8") as fp:
            entries = [json.loads(l) for l in fp]

        # QID -> シノニム関係にある単語リスト
        qid2words = {d["id"]: [d["title"]] + d["aliases"] for d in entries}
        # QID: wikipedia ページエントリのID
        word2qid = defaultdict(list)
        for d in entries:
            word2qid[d["title"]].append(d["id"])
            for a in d["aliases"]:
                word2qid[a].append(d["id"])

        with open(dir_path / "qid2words.pkl", "wb") as fp:
            pickle.dump(qid2words, fp)

        with open(dir_path / "word2qid.pkl", "wb") as fp:
            pickle.dump(word2qid, fp)

    def resolve(self, word: str):
        """ 与えられた単語のエントリ候補を取得する """
        if word in self.word2qid:
            return [
                {"qid": qid, "surfaces": self.qid2words[qid]}
                for qid in self.word2qid[word]
            ]
        return []
