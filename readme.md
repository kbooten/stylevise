# STYLE🗜VISE 

STYLE🗜VISE is a training program designed to goad writers toward more interesting syntax.  

The syntax of the sentence 'I am a chair.' can be thought of as its part-of-speech sequence: a *pronoun*, a *present tense verb*, an *article*, a *singular noun*, and then *terminal punctuation*.  Style🗜Vise has read hundreds of thousands of sentences (extracted from the [Project Gutenberg corpus](https://www.gutenberg.org/) as well as [Amazon review data](https://snap.stanford.edu/data/web-Amazon.html)), and it knows what part-of-speech sequences are common and which are rare. To get praise (👍) from Style🗜Vise, you have to write a sentence that avoids the most common patterns. As you write, however, Style🗜Vise's restrictions will tighten so that you must avoid not just the most common syntax patterns but also rarer and rarer ones. If you bore Style🗜Vise by failing to do so, you'll lose one of your 10 lives (💖). If you run out of lives, you'll have to start over. 

Style🗜Vise is one of a series of "progymnasmata" that aim to repurpose the techniques of Natural Language Processing to push the human writer into productively uncomfortable and unfamiliar positions.  It is a more gamified and sadistic elaboration of a program I [described here](http://computationalcreativity.net/iccc2019/assets/iccc_proceedings_2019.pdf#page=15).

***

A web-based version can be tested [here](https://stylevise.herokuapp.com/).  (It is a bit slow to load, and there can be some disruptive lag---something I hope to fix.) However, I prefer the command line interface version, also in this repository. To interact with STYLE🗜VISE via the command line:

    python Stylevise.py

The CLI version has certain advantages over a full-fledged GUI.  Interactions with the program are easily recorded (output by default to `sv_output.txt`).   Since developing an interface with `cmd` is less fuss than making a GUI, it is also easier to change. The CLI version also remembers what the user has written in previous sessions and demands that they differ from those sentences as well. There is also a certain aesthetic charm in the way that a CLI's minimalism focuses attention on the dyadic interaction between human and computer. And, without all the fuss of sending queries to and fro, the CLI app should run a bit more quickly and reliably.

Because the CLI uses the `cmd` module, it is possible to cycle through previous commands (on my Mac, by pressing `↑`).

For convenience, the output file and initial difficulty level can be set via the command line, e.g.:

    python Stylevise.py -o anotheroutput.txt -l 2 

The online demo version uses SpaCy's [`en_core_web_sm` model](https://spacy.io/usage/models).  Running locally, both the CLI and GUI versions will first look for the `en` model before defaulting to `en_core_web_sm`.  The `en` model probably works better, so I recommend using it. 

***

Described in a conference talk, "Language Models and 'Models of Experience,'" *Vilém Flusser and his "Languages"*, Vilém Flusser Archive, June 2020. 



