# md2anki

This tools converts a Markdown file into anki flashcards.  
The input file must be of the following structure:

```md
# Question 1

Answer 1

# Question 2

Answer 2 with `code blocks`, **bold font etc.**
You can even import ![images](res/example_image.png)

```

# Usage

1. Install the required dependecies, listed below. 
2. Add a new entry to the `configs.json` for the desired Markdown file you want to convert. Some important notes:
    - `model_id` and `deck_id` **need to be unique** for every deck you create! Please [read the docs of `genanki`](https://github.com/kerrickstaley/genanki). **TL;DR** create **two new, distinct ids** in the python console by running `import random; random.randrange(1 << 30, 1 << 31)`.
3. Run `python3 md2anki.py configEntryName`. It will handle everything on its own.
    
# Configuration

Configuration options for each Anki decks are stored in `configs.json`.
An example entry looks like:

```json
{
    "readme": {
        "input_file": "Readme.md",
        "deckname": "Readme",
        "outputname": "readme.apkg", 
        "model_id" : 1477896232,
        "deck_id" : 2044944474
    }
}
```

- `readme`: The name for the configuration entry, which is passed to `md2anki`
- `input_file`: Path to the Markdown file, relative to `md2anki.py` or absolute.
- `deckname`: Name of the deck, how it should be named within Anki.
- `outputname`: Filename of the resulting anki package (in `cwd`).
- `model_id`: Unique id of the created model.
- `deck_id`: Unique id of the created model.

## Optional configuration parameters

- `css`: An array of `.css` files, that should be included into the cards. Path must be relative to `./md2anki.py` or absolute. Defaults to `["default.css"]`
- `pandoc_args`: An array of custom paramters for pandoc. Defaults to `["-s", "--highlight-style", "tango"]`


The respective call is `python3 md2anki.py readme` and results in creating the `readme.apkg` file in the current working directory.

# Dependencies & Installation

```bash
# Tested on Ubuntu 20.04 with `Python 3.8.5`

sudo apt update && sudo apt install -y pandoc python3-pip

git clone https://github.com/maik-s/md2anki.git

pip3 install --user -r requirements.txt
```

# Docker

This repository includes a `Dockerfile`. You can build the image from the directory with `docker build . -t md2anki`.
Then run `docker run -v "$(pwd):/data" md2anki configentry "/data/configs.json"` from the `cwd`, where your Markdown file **and** the `configs.json` is stored.
