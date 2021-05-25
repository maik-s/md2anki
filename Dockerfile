FROM python

RUN apt update && apt install -y pandoc

RUN pip3 install --user beautifulsoup4 genanki pypandoc

WORKDIR /code

COPY md2anki.py /code/md2anki
COPY configs.json /code/md2anki
COPY default.css /code/md2anki

ENTRYPOINT ["python3", "md2anki/md2anki.py"]