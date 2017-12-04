#***********************************************************************
# Copyright (C) Luca Baldini (luca.baldini@unipi.it)
#
# For the license terms see the file LICENSE, distributed along with this
# software.
#
# This program is free software; you can redistribute it and/or modify it
# under the terms of the GNU General Public License as published by the
# Free Software Foundation; either version 2 of the License, or (at your
# option) any later version.
#
# This program is distributed in the hope that it will be useful, but
# WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU
# General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#***********************************************************************


import urllib
import os
import sys
import logging
logging.basicConfig(level=logging.INFO, format='>>> %(message)s')


PAGE_TUPLE = (('applied_physics.txt', 'https://sites.google.com/a/unipi.it/prova_ap/people'), ('condensed_matter.txt', 'https://sites.google.com/a/unipi.it/physics-of-matter/people'), ('fundamental_interactions.txt', 'https://sites.google.com/a/unipi.it/fundamental-interactions/home/people'), ('theory_group.txt', 'https://sites.google.com/a/unipi.it/pisa-theory-group/staff'))



def download_page(url, file_path, overwrite=False):
    """Download a web page to disk.

    Note that by default we do not overwrite existing files.
    """
    if os.path.exists(file_path) and not overwrite:
        logging.info('File %s found!' % file_path)
        return
    logging.info('Downloading %s to %s...' % (url, file_path))
    urllib.URLopener().retrieve(url, file_path)
    logging.info('Done.')



class Person:

    """Small class encapsulating a person.
    """

    def __init__(self, full_name, affiliation, room, phone, email):
        """Constructor.
        """
        self.surname, self.name = [s.strip().title() for s in \
                                   full_name.split(' ', 1)]
        self.affiliation = affiliation
        self.room = room
        self.phone = phone
        self.email = email
        
    def __str__(self):
        """String formatting.
        """
        text = '%s %s' % (self.name, self.surname)
        if self.affiliation != '':
            text += ' (%s)' % self.affiliation
        if self.room != '':
            text += ', room %s' % self.room
        if self.phone != '':
            text += ', ext. %s' % self.phone
        if self.email != '':
            text += ', %s' % self.email
        return text



def parse_line(line):
    """Parse a single line (or portion of it) from the html file.
    """
    line = line.replace('<div>', '')
    for i, piece in enumerate(line.split('>')):
        logging.debug('%d -> %s' % (i, piece))
    if '<a' in line:
        index = 4
    else:
        index = 3
    try:
        val = line.split('>')[index].split('<')[0].strip(' ')
    except Exception as e:
        logging.debug('Cannot parse line "%s" (%s)' % (line, e))
        return ''
    if val.startswith('\xc2'):
        val = val[2:]
    return val
    

def parse_file(file_path, interactive=False):
    """Parse an entire file.
    """
    logging.info('Parsing file %s...'% file_path)
    n = 0
    # Read the entire file in memory as a long string with no endlines.
    text = open(file_path).read().replace('\n', '')
    # Split in chunks in correspondence of the email table headers
    blocks = text.split('E-mail')[1:]
    # Loop over the blocks.
    for block in blocks:
        lines = block.split('<td')[1:]
        iterator = lines.__iter__()
        for line in iterator:
            try:
                name = parse_line(line)
                line = iterator.next()
                affiliation = parse_line(line)
                line = iterator.next()
                room = parse_line(line)
                line = iterator.next()
                phone = parse_line(line)
                line = iterator.next()
                email = parse_line(line)
                person = Person(name, affiliation, room, phone, email)
                n += 1 
                logging.info(person)
            except:
                pass
            if interactive:
                raw_input()
    logging.info('Done, %d person(s) found.' % n)
    




if __name__ == '__main__':
    for file_name, url in PAGE_TUPLE:
        download_page(url, file_name)
        parse_file(file_name)
