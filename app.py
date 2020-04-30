from flask import Flask, request, jsonify
from flask.logging import create_logger
import logging
import os
from pathlib import Path

from synonym_expander import SynonymExpander


app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
LOG = create_logger(app)
LOG.setLevel(logging.INFO)

if (
    Path(os.environ["WIKIDATAPATH"]).is_dir()
    and Path(os.environ["SUDACHIPATH"]).is_dir()
):

    p_wikidata = Path(os.environ["WIKIDATAPATH"])
    se_wikidata = SynonymExpander(p_wikidata)
    p_sudachi = Path(os.environ["SUDACHIPATH"])
    se_sudachi = SynonymExpander(p_sudachi)

else:
    LOG.error(f"InitError: \n {os.environ['MODELPATH']} doesn't exist.")


def synonym_expand_wikidata(query):
    return se_wikidata.resolve(query)


def synonym_expand_sudachi(query):
    return se_sudachi.resolve(query)


@app.route("/")
def home():
    html = f"<h3>SynonymExpander Home</h3>"
    return html.format(format)


@app.route("/synonyms/wikidata", methods=["POST"])
def synonym_expander_wikidata():
    """Performs synonym_expand with wikidata dictionary
        
        input looks like:
        {
            "query": "営業",
        }
        
        result looks like:
        {
            "matched_entries":
            [
                {'qid': 'Q2142', 'surfaces': ['孫悟空', 'カカロット']},
                {'qid': 'Q449824', 'surfaces': ['孫悟空', '孫悟空 (曖昧さ回避)']},
                {'qid': 'Q11773777', 'surfaces': ['孫悟空', '斉天大聖']}
            ]
        }
    """

    # Logging the input payload
    json_payload = request.json
    LOG.info(f"JSON payload: \n{json_payload.keys()}")
    try:
        query = json_payload["query"]
    except Exception as e:
        LOG.error(f"Error:\n {e}")

    try:
        results = synonym_expand_wikidata(query)
        LOG.info(f"Process: \n Success!")
    except Exception as e:
        LOG.error(f"Error: \n {e}")

    LOG.info(f"Prediction value: \n#:{len(results)}\n{results[:5]}")
    return jsonify({"matched_entries": results})


@app.route("/synonyms/sudachi", methods=["POST"])
def synonym_expander_sudachi():
    """Performs synonym_expand with sudachi dictionary
        
        input looks like:
        {
            "query": "営業",
        }
        
        result looks like:
        {
            "matched_entries":
            [
                {'qid': '000425', 'surfaces': ['営業', '営業', 'セールス', 'sales']},
            ]
        }
    """

    # Logging the input payload
    json_payload = request.json
    LOG.info(f"JSON payload: \n{json_payload.keys()}")
    try:
        query = json_payload["query"]
    except Exception as e:
        LOG.error(f"Error:\n {e}")

    try:
        results = synonym_expand_sudachi(query)
        LOG.info(f"Process: \n Success!")
    except Exception as e:
        LOG.error(f"Error: \n {e}")

    LOG.info(f"Prediction value: \n#:{len(results)}\n{results[:5]}")
    return jsonify({"matched_entries": results})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80, debug=True)
