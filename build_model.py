import os
from pathlib import Path
from synonym_expander import SynonymExpander


if __name__ == "__main__":

    p = Path(os.environ["WORKDIRPATH"])
    p_wikidata = Path(os.environ["WIKIDATAPATH"])  # p / 'wikidata'
    print("build wikidata")
    SynonymExpander.build_wikidata(p / "wikipedia_entry_aliases.jsonl", p_wikidata)
    print("test wikidata")
    se_wikidata = SynonymExpander(p_wikidata)
    assert se_wikidata.resolve("孫悟空")[0]["qid"] == "Q2142"

    p_sudachi = Path(os.environ["SUDACHIPATH"])  # p / 'sudachi'
    print("build sudachi")
    SynonymExpander.build_wikidata(p / "sudachi_entry_aliases.jsonl", p_sudachi)
    print("test sudachi")
    se_sudachi = SynonymExpander(p_sudachi)
    assert se_sudachi.resolve("営業")[0]["qid"] == "000425"
