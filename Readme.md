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
3. Run `./python3 md2anki.py configEntryName`. It will handle everything on its own.
    
## Example

An example entry for `configs.json` looks like:

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

- `input_file`: Path to the Markdown file, relative to `md2anki.py` or absolute.
- `deckname`: Name of the deck, how it should be named within Anki.
- `outputname`: Filename of the resulting anki package.
- `model_id`: Unique id of the created model.
- `deck_id`: Unique id of the created model.

The respective call is `python3 md2anki.py readme` and results in creating the `readme.apkg` file.

# Dependencies

    # Tested with `Python 3.6.9` on `Ubuntu 18.04` and `Python 3.7.3` on `Debian Buster`.

    sudo apt update && sudo apt install -y pandoc

    pip3 install --user beautifulsoup4 genanki pypandoc