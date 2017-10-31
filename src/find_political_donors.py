import heapq as q
import datetime
import sys
from collections import defaultdict


class Recipient:

    def __init__(self):
        self.total_trans = 0
        self.total_contr = 0
        self.medians = []
        self.min_heap = []
        self.max_heap = []

    def insert(self, contribution):
        self.total_trans += 1
        self.total_contr += contribution
        if contribution > self.get_median():
            q.heappush(self.min_heap, contribution)
        else:
            q.heappush(self.max_heap, contribution*-1)

        if len(self.max_heap) > len(self.min_heap):
            q.heappush(self.min_heap, -1 * q.heappop(self.max_heap))
        if len(self.min_heap) > len(self.max_heap) + 1:
            q.heappush(self.max_heap, -1 * q.heappop(self.min_heap))

    def get_median(self):
        if len(self.min_heap) == 0 and len(self.max_heap) == 0:
            return 0
        if len(self.min_heap) > len(self.max_heap):
            return self.min_heap[0]
        elif len(self.max_heap) == len(self.min_heap):
            return ((-1 * self.max_heap[0]) + self.min_heap[0])/float(2)

    def for_date(self, contribution):
        self.total_trans += 1
        self.total_contr += contribution
        self.medians.append(contribution)

    def get_median_for_date(self):
        if len(self.medians) == 1:
            return self.medians[0]
        self.medians.sort()

        if len(self.medians) % 2 == 1:
            return float(self.medians[len(self.medians)/2])
        else:
            return 0.5 * (float(self.medians[len(self.medians)/2] + float(self.medians[len(self.medians)/2 - 1])))


class Main:

    def __init__(self):
        self.reference_for_zip = defaultdict(dict)
        self.reference_for_date = defaultdict(dict)
        self.output1 = open(sys.argv[2], 'w')
        self.output2 = open(sys.argv[3], 'w')

    def create_by_zip(self):
        f = open(sys.argv[1], 'r')
        l = f.readline()
        while l:
            line = l.split('|')
            if len(line[15]) != 0:
                l = f.readline()
                continue
            if len(line[0]) == 0 or len(line[14]) == 0:
                l = f.readline()
                continue
            if len(line[10]) < 5:
                self.by_date(line)
                l = f.readline()
                continue
            if len(line[13]) != 8:
                self.by_zip(line)
                l = f.readline()
                continue
            self.by_zip(line)
            self.by_date(line)
            l = f.readline()

    def by_zip(self, line):
        recip = line[0]
        zipcode = line[10][:5]
        amt = line[14]

        if zipcode in self.reference_for_zip[recip]:
            obj = self.reference_for_zip[recip][zipcode]
        else:
            obj = Recipient()
        obj.insert(int(amt))
        tt = obj.total_trans
        tc = obj.total_contr
        median = obj.get_median()
        if median - int(median) >= 0.5:
            median = int(median) + 1
        else:
            median = int(median)
        self.reference_for_zip[recip][zipcode] = obj
        self.output1.write(recip + "|" + zipcode + "|" + str(median) + "|" + str(tt) + "|" + str(tc) + "\n")
        # print recip, zipcode, median, tt, tc

    @staticmethod
    def is_valid(date_entry):
        try:
            datetime.datetime(year=int(date_entry[4:8]), month=int(date_entry[:2]), day=int(date_entry[2:4]))
        except ValueError:
            return False
        return True

    def by_date(self, line):
        recip = line[0]
        amt = int(line[14])
        date_entry = line[13]
        if self.is_valid(date_entry):
            date = datetime.datetime(year=int(date_entry[4:8]), month=int(date_entry[:2]), day=int(date_entry[2:4]))
            if date in self.reference_for_date[recip]:
                obj = self.reference_for_date[recip][date]
            else:
                obj = Recipient()
            obj.for_date(amt)
            self.reference_for_date[recip][date] = obj

    def generate_output_by_date(self):
        keys = self.reference_for_date.keys()
        keys.sort()
        for k in keys:
            inner_keys = self.reference_for_date[k].keys()
            inner_keys.sort()
            for inner_key in inner_keys:
                ob = self.reference_for_date[k][inner_key]
                median = ob.get_median_for_date()
                if median - int(median) >= 0.5:
                    median = int(median) + 1
                else:
                    median = int(median)
                inner_key = str(inner_key)
                year = inner_key[:4]
                month = inner_key[5:7]
                day = inner_key[8:10]
                date = month + day + year
                self.output2.write(k + "|" + date + "|" + str(median) + "|" + str(ob.total_trans) + "|" + str(ob.total_contr) + "\n")
                # print k, inner_key, median, ob.total_trans, ob.total_contr, ob.medians


m = Main()
m.create_by_zip()
m.generate_output_by_date()
