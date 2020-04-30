FROM python:3.7.3-stretch

WORKDIR /app

ENV WORKDIRPATH /app
ENV WIKIDATAPATH /app/wikidata
ENV SUDACHIPATH /app/sudachi

# hadolint ignore=DL3013
RUN pip3 install --upgrade pip && \
    pip3 install flask

COPY app.py .
COPY synonym_expander.py .
COPY build_model.py .
COPY model_files/ .
RUN mkdir $WIKIDATAPATH
RUN mkdir $SUDACHIPATH
RUN python build_model.py
RUN rm wikipedia_entry_aliases.jsonl
RUN rm sudachi_entry_aliases.jsonl
RUN rm build_model.py

EXPOSE 9000

CMD ["python3", "app.py"]