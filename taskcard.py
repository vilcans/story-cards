#!/bin/env python

import sys
import os
import csv
import urllib
import genshi.template
import subprocess
import codecs

# Edit me!
TRAC_URL = 'http://localhost/trac/'

DATA_DIR = os.path.abspath(os.path.dirname(__file__))
template_loader = genshi.template.TemplateLoader([ DATA_DIR ], auto_reload=True)
template = template_loader.load('card-template.svg')


def get_data(ticket_no):
    print 'Getting data for ticket %s' % ticket_no
    f = urllib.urlopen('%s/ticket/%s?format=csv' % (TRAC_URL, ticket_no))
    if f.code / 100 != 2:
        raise RuntimeError('Http error %s' % f.code)
    reader = csv.DictReader(f)
    row = reader.next()
    f.close()
    return dict((k, unicode(v, 'utf-8')) for (k, v) in row.items())


pdf_filenames = []

def write(file_number, variables):
    for number in range(1, 5):
        variables.setdefault('summary%d' % number, '.' * 60)
        variables.setdefault('id%d' % number, '        ')
        variables.setdefault('description%d' % number, '')

    svg_filename = 'cards%s.svg' % file_number
    pdf_filename = 'cards%s.pdf' % file_number

    print 'Creating', svg_filename
    output = codecs.open(svg_filename, 'w', 'utf-8')
    svg = unicode(template.generate(**variables))
    output.write(svg)
    output.close()

    print 'Creating', pdf_filename
    subprocess.check_call(['inkscape', '--export-pdf', pdf_filename, svg_filename])
    pdf_filenames.append(pdf_filename)

variables = {}
file_number = 1
number = 1
ticket_numbers = sys.argv[1:]

for arg_no, ticket_no in enumerate(ticket_numbers):
    last = (arg_no == len(ticket_numbers) - 1)
    try:
        data = get_data(ticket_no)
    except Exception as e:
        print >>sys.stderr, 'Failed to get data for ticket %s: ignored' % ticket_no
    else:
        for key, value in data.iteritems():
            variables[key + str(number)] = value
        number += 1
    if last or number > 4:
        write(file_number, variables)
        variables = {}
        number = 1
        file_number += 1

print 'Merging PDFs'
subprocess.check_call(['pdftk'] + pdf_filenames + ['cat', 'output', 'cards.pdf'])
print 'Created cards.pdf'

