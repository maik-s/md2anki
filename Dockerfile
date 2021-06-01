FROM python

RUN apt update && apt install -y wget curl

# install latest pandoc release 
# s/o to https://gist.github.com/steinwaywhw/a4cd19cda655b8249d908261a62687f8
RUN curl -s https://api.github.com/repos/jgm/pandoc/releases/latest | grep "browser_download_url.*amd64.deb" | cut -d : -f 2,3 | tr -d '\"' | wget -q -O /tmp/pandoc.deb -i -
RUN dpkg -i /tmp/pandoc.deb

COPY requirements.txt /tmp/requirements.txt
RUN pip3 install --user -r /tmp/requirements.txt

COPY md2anki.py /code/md2anki/md2anki.py
COPY configs.json /code/md2anki/configs.json
COPY default.css /code/md2anki/default.css

WORKDIR /data

ENTRYPOINT ["python3", "/code/md2anki/md2anki.py"]