"""
Given a spreadsheet of SFX data, this module computes a "threshold" equation and writes
it to the "Threshold" column.

"""

import sys, os, re

from tabdelimited import CsvFile, CsvRecord

class SfxRecord (CsvRecord):

    def __init__ (self, data, parent):
        CsvRecord.__init__(self, data, parent)

        self.start, self.to = self.get_range()

        self.threshold = self.get_threshold()
        self['Threshold'] = self.threshold

    def get_range(self):
        """
        custom from or to dates (e.g., "2000") override defaults which are expressed as a range ("1991-2001")

        NOTE: if either custom to or from is present, the default is ignored

        """

        c_from = self['Custom Date From']
        c_to = self['Custom Date To']

        if c_from or c_to:
            return c_from, c_to

        default = self['Default Dates']
        d_from = None
        d_to   = None

        splits = default.split('-')
        if len(splits) == 2:
            d_from = splits[0]
            d_to = splits[1]
        elif len(splits) == 1:
            d_from = splits[0]

        return d_from, d_to

        # print 'c_from: %s, c_to: %s, d_from: %s, d_to: %s' % (c_from, c_to, d_from, d_to)
        # return c_from or d_from, c_to or d_to

    def get_threshold(self):
        s = ""
        if self.start:
            s = "$obj->parsedDate('>=','%s',undef,undef)" % self.start
            if self.to:
                s += " && "
        if self.to:
            s += "$obj->parsedDate('<=','%s',undef,undef)" % self.to
        return s


class SfxFile (CsvFile):

    record_constructor = SfxRecord

    def __init__ (self, path):
        CsvFile.__init__ (self)
        self.read(path)
        print '%d records read' % len(self)


if __name__ == "__main__":
    path = '/Users/ostwald/Downloads/SLS Without Threshold.csv'

    sheet = SfxFile(path)

    for rec in sheet:
        # print 'from: %s, to: %s' % (rec.start, rec.to)
        print rec.threshold

    sheet.write ("/Users/ostwald/tmp/SLS With Threshold.txt")