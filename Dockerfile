FROM python

RUN apt update && apt install -y pandoc

RUN pip3 install --user beautifulsoup4 genanki pypandoc

COPY md2anki.py /code/md2anki/md2anki.py
COPY configs.json /code/md2anki/configs.json
COPY default.css /code/md2anki/default.css

WORKDIR /data

ENTRYPOINT ["python3", "/code/md2anki/md2anki.py"]