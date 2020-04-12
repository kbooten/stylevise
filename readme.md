# STYLE🗜VISE 

STYLE🗜VISE is a training program designed to goad writers toward more interesting syntax.  

The syntax of the sentence 'I am a dog.' can be thought of as its part-of-speech sequence: a *pronoun*, a *present tense verb*, an *article*, a *singular noun*, and then *punctuation*.  Style🗜Vise has read hundreds of thousands of sentences (extracted from the [Project Gutenberg corpus](https://www.gutenberg.org/) as well as [Amazon review data](https://snap.stanford.edu/data/web-Amazon.html), and it knows what part-of-speech sequences are common and which are rare. To get praise (👍) from Style🗜Vise, you have to write a sentence that avoids these frequent patterns. As you write, however, Style🗜Vise's restrictions will tighten so that you must avoid not just the most common (boring) syntax patterns but also rarer and rarer ones. If you bore Style🗜Vise, you'll lose one of your 10 lives (💖). If you run out of lives you'll have to start over. 

Style🗜Vise is one of a series of "progymnasmata" that aim to repurpose the techniques of Natural Language Processing to push the human writer into productively uncomfortable and unfamiliar positions.  It is a more gamified and sadistic elaboration of a program I [described here](http://computationalcreativity.net/iccc2019/assets/iccc_proceedings_2019.pdf#page=15).

***

A web-based version can be tested [here](https://stylevise.herokuapp.com/). However, I prefer the command line interface version, also in this repository. To interact with STYLE🗜VISE via the command line:

    python Stylevise.py

The CLI version has certain advantages over a full-fledged GUI.  Interactions with the program are easily recorded (output by default to `sv_output.txt`).  Because the interface uses the `cmd` module, it is possible to cycle through previous commands (on my Mac, by pressing `↑`). Since developing an interface with `cmd` is less fuss than making a GUI, it is also easier to change. I plan on adding features to the CLI that allow the user to keep track of their progress across sessions. Also, there is a certain aesthetic charm in the way that a CLI's minimalism focuses attention on the dyadic interaction between human and computer. 

For convenience, the output file and initial difficulty level can be set via the command line, e.g.:

    python Stylevise.py -o anotheroutput.txt -l 2 


The online demo version uses SpaCy's [`en_core_web_sm` model](https://spacy.io/usage/models).  Running locally, both the CLI and GUI versions will first look for the `en` model before defaulting to `en_core_web_sm`.  The `en` model probably works better, so I recommend using it. 

***

To see how syntax patterns were extracted from the corpora, see `getting_syntax_ngrams.ipynb`.

The citation for the Amazon review data:


    @misc{snapnets,
      author       = {Jure Leskovec and Andrej Krevl},
      title        = {{SNAP Datasets}: {Stanford} Large Network Dataset Collection},
      howpublished = {\url{http://snap.stanford.edu/data}},
      month        = jun,
      year         = 2014
    }



