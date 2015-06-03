WEBGESTALT
=========
Let the robot do your GO enrichments!

Small python script based on `selenium` to query the `webgestalt` web interface.
Returns a GO enrichment given a set of entrez ids and a background list.

Contributions and feature requests are welcome.

Installation
------------

1. Register with `webgestalt`
2. `mv config.py.example config.py`
3. Set your email adress in `config.py`

Usage
------------
An example is included in `test/`

`test/rejected.txt` contains the query genes.
  
    27
    91
    141
    154
    324
    332
    387
    390
    408
    551

`test/background.txt` has the same form as above and contains the background genes.

    >>> from webgestalt.runner import run
    >>> rejected = 'test/rejected.txt'
    >>> background = 'test/background.txt'
    >>> run(rejected, background, folder='test', name='results')

Licence
------------
This project is licensed under the MIT licence.
