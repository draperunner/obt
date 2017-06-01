# The Oslo-Bergen Tagger for Python

This is a Python library for [The Oslo-Bergen Tagger](http://www.tekstlab.uio.no/obt-ny/), which parses the output of 
the tagger to a friendly format. Only Python 3 is supported at this time.

The library is in beta. See [Roadmap](#roadmap) for things that need to get implemented before a v1.0.0 can be released.

## Installation

You need to have The Oslo-Bergen Tagger installed, and the environment variable `OBT_PATH` set to the path of its
installation directory. You can use the provided code snippet below, or install it using the instructions in 
[The-Oslo-Bergen-Tagger GitHub repository](https://github.com/noklesta/The-Oslo-Bergen-Tagger). The following code snippet installs it in your home directory. If you want to install it 
somewhere else, you can change the `INSTALL_DIR` variable on the first line to your preferred installation directory.

```bash
INSTALL_DIR=$HOME
THIS_DIR=$PWD
cd $INSTALL_DIR
git clone git@github.com:noklesta/The-Oslo-Bergen-Tagger.git
cd The-Oslo-Bergen-Tagger
./bootstrap.sh
export OBT_PATH=$INSTALL_DIR/The-Oslo-Bergen-Tagger
echo 'export OBT_PATH=$OBT_PATH' >> $HOME/.bashrc
cd $THIS_DIR
```

You can then install this Python library with pip. To install for all users, do:
```bash
sudo pip3 install obt
```
To just install for your user, do:
```bash
pip3 install --user obt
```

And you are good to go!

## Usage
First, import the library
```python
import obt
```

Then, you can tag a string by passing it to the `tag_bm` function:
```python
my_string = "Jeg er streng."
tags = obt.tag_bm(my_string)
```
Or you can pass a file name using the `file` keyword argument:
```python
tags = obt.tag_bm(file="my_document.txt")
```

The resulting `tags` will be an array of tag objects, like so:
```python
[
  {
    "tall": "ent",
    "type": "pers hum",
    "base": "jeg",
    "person": "1",
    "word_tag": "<jeg>",
    "kasus": "nom",
    "raw_tags": "pron ent pers hum nom 1",
    "word": "Jeg",
    "ordklasse": "pron"
  },
  {
    "word_tag": "<er>",
    "base": "v\u00e6re",
    "tilleggstagger": [
      "a5",
      "pr1",
      "pr2",
      "<aux1/perf_part>"
    ],
    "tid": "pres",
    "raw_tags": "verb pres a5 pr1 pr2 <aux1/perf_part>",
    "word": "er",
    "ordklasse": "verb"
  },
  {
    "type": "appell",
    "best": "ub",
    "base": "streng",
    "word_tag": "<streng>",
    "tall": "ent",
    "ordklasse": "subst",
    "raw_tags": "subst appell mask ub ent",
    "word": "streng",
    "kj\u00f8nn": "mask"
  },
  {
    "word_tag": "<.>",
    "base": "$.",
    "tilleggstagger": [
      "<<<",
      "<punkt>",
      "<<<"
    ],
    "raw_tags": "clb <<< <punkt> <<<",
    "word": ".",
    "ordklasse": "clb"
  }
]
```

You can easily save this to a JSON file with the `obt.save_json` function:
```python
obt.save_json(tags, 'my_tags.json')
```

## Format
A documentation of the tag format will come here.

## Roadmap
Before a v1.0.0 release, the following boxes should be checked:
- [ ] Put "tilleggstagger" in proper items in tags object.
- [ ] Implement function for `./tag-nostat-bm.sh` from https://github.com/noklesta/The-Oslo-Bergen-Tagger
- [ ] Implement function for `./tag-nostat-nn.sh` from https://github.com/noklesta/The-Oslo-Bergen-Tagger
- [ ] Python 2 support
