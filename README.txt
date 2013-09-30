Generates story cards from tickets in Trac.

Usage:

  ./cards <ticket> [<ticket>...]

E.g.

  ./cards 904 907 1011

A maximum of four ticket numbers can be given.

Invalid ticket numbers are ignored.

The result is written to cards.svg, which is then converted to cards.pdf.

Installation
------------

Needs the "genshi" package (to generate the svg file) and Inkscape (to
generate the pdf).

  pip install -r requirements.txt
  sudo apt-get install inkscape
