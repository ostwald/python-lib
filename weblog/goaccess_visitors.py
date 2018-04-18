import os, json, sys, time, datetime
from UserList import UserList
from UserDict import UserDict

class OrderedDict (UserDict):
    
    def sorted_values(self):
        sorted_keys = sorted(self.data.keys())
        return map (lambda x:self.data[x], sorted_keys)

class Month(OrderedDict):
    """
    data is DataPoints
    """
    def __init__(self, month):
        self.month = month
        self.name = datetime.date(2018, month, 1).strftime('%B')
        self.data = {}
        self.total_hits = 0
        self.total_visitors = 0

    def add (self, point):
        self[point.day] = point
        self.total_hits += point.hits
        self.total_visitors += point.visitors

    def report(self):
        # print '\n- {} -'.format(self.name)
        # print '\n- {} - avg hits/day: {} avg visitors/day: {})'.format(self.name, self.get_avg_hits(), self.get_avg_visitors())
        print '\n- {} - {})'.format(self.name, self.total_visitors)
        # sorted_points = sorted(self.data, key=lambda x:x.date.day)

        return # skip daily reports

        for point in self.sorted_values():
            # print '- {} - {}'.format(point.date.day, point.visitors)
            point.report()

    def get_avg_hits(self):
        return self.total_hits / len(self.data.keys())

    def get_avg_visitors(self):
        return self.total_visitors / len(self.data.keys())

class Year(OrderedDict):
    """
    data is months
    """
    def __init__(self, year):
        self.year = year
        self.data = UserDict()
        self.sortKey = lambda x:x.year

    def add (self, point):
        month = point.date.month
        if not self.data.has_key(month):
            self.data[month] = Month(month)
        self.data[month].add (point)



    def report (self):
        print '\n** {} **'.format(self.year)
        # sorted_keys = sorted(self.data, key=lambda x:x.date.month)

        for month in self.sorted_values():
            month.report()

class Visitors (OrderedDict):
    """
    data is years
    """

    def __init__ (self, path):
        content = open(path, 'r').read()
        obj = json.loads(content)
        data = map (DataPoint, obj['visitors']['data'])
        print 'there are {} data points'.format(len(data))

        self.data = UserDict()
        self.sortKey = lambda x:x.year
        for point in data:
            year = point.date.year
            if not self.data.has_key(year):
                self.data[year] = Year(year)
            self.data[year].add (point)

    def report (self):
        # sorted_years = sorted(self.data, lambda x:x.year)
        for year in self.sorted_values():
            year.report()

class DataPoint:

    def __init__ (self, data):
        self.day = data['data']
        self.hits = data['hits']['count']
        self.visitors = data['visitors']['count']
        self.date_OLD = time.strptime(self.day, "%Y%m%d")
        self.date = datetime.date(int(self.day[0:4]), int(self.day[4:6]), int(self.day[6:8]))

    def report (self):
        print '{} - {} - {}'.format(self.date.day, self.hits, self.visitors)

if __name__ == '__main__':
    path = '/Users/ostwald/Documents/Dlese/dlese_visitors.json'
    visitors = Visitors(path)
    visitors.report()
    print 'DONE'
