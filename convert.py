#!/usr/bin/python3

from os.path import basename, dirname, join as pathjoin
from os import remove
import genanki
from bs4 import BeautifulSoup
import sys
import json
import pypandoc
import tempfile

assert len(sys.argv) > 0, "Missing input parameter"

config_entry = sys.argv[1]

input_file, deckname, outputname, model_id, deck_id = None, None, None, None, None

with open(pathjoin(dirname(sys.argv[0]), 'configs.json')) as config_file:
    configs = json.load(config_file)[config_entry]
    input_file = pathjoin(dirname(sys.argv[0]),configs["input_file"])
    deckname = configs["deckname"]
    outputname = configs["outputname"]
    model_id = configs["model_id"]
    deck_id = configs["deck_id"]

tempfile = tempfile.NamedTemporaryFile()
pypandoc.convert_file(input_file, to="html5", extra_args=["-s", "--highlight-style", "tango"], outputfile=tempfile.name)

class MyNote(genanki.Note):
  @property
  def guid(self):
    return genanki.guid_for(self.fields[0]) # only hash title field, so that we can update cards

filedirname = dirname(input_file)

with open(tempfile.name, 'r') as fh:
    soup = BeautifulSoup(fh, 'html.parser')
    css = """.card {
                font-family: arial;
                font-size: 20px;
                color: black;
                text-align: left;
            }
            .figure > .caption {display:none;} /* do not display figure captions*/
            figcaption { display: none; }
            """
    styles = soup.find_all("style")
    for style in styles:
        css += style.string
    my_model = genanki.Model(model_id, 'Simple Model with Media',
            fields=[
                {'name': 'Question'},
                {'name': 'Answer'}
            ],
            templates=[
                {
                'name': 'Card 1',
                'qfmt': '{{Question}}',
                'afmt': '{{FrontSide}}<hr id="answer">{{Answer}}',
                },
            ],css=css)

    my_deck = genanki.Deck(deck_id, deckname)
    my_package = genanki.Package(my_deck)
    my_package.media_files = []
    body = soup.find("body")
    fields = [None, None]
    for tag in body:
        if tag.name == "h1":
            if None not in fields:
                my_note = MyNote(model=my_model,fields=[str(fields[0]), str(fields[1])])
                my_deck.add_note(my_note)
            fields[0] = tag.string
            fields[1] = None
        else:
            if not fields[1]:
                fields[1] = ""
            if tag.name != None:
                imgs = tag.find_all("img")
                for img in imgs:
                    img_file = img.attrs["src"]
                    fullpath = pathjoin(filedirname, img_file)
                    my_package.media_files.append(fullpath)
                    img.attrs["src"] = basename(img.attrs["src"]) # remove subdir as anki cannot
                    img.attrs["alt"] = ""
            fields[1] += str(tag)

    if None not in fields:
        # Add remaining note
        my_note = MyNote(model=my_model,fields=[str(fields[0]), str(fields[1])])
        my_deck.add_note(my_note)

my_package.write_to_file(outputname)
tempfile.close()