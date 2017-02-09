from collections import OrderedDict
import csv
from dateutil.parser import parse
import datetime, time


class DataFrame(object):
    @classmethod
    def from_csv(cls, path):
        with open(path, 'rU') as f:
            reader = csv.reader(f, delimiter=',', quotechar='"')
            data = []
            for row in reader:
                data.append(row)
        return cls(data)

    def __init__(self, list_of_lists, header=True):
        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(self.data[0])]
            self.data = list_of_lists
            self.data = [OrderedDict(zip(self.header, row)) for row in self.data]
    # TASK1:
        if len(set(self.header)) == len(self.header):
            print('True')
        else:
            raise Exception('duplicates found')
    # TASK2:
        self.data = [map(lambda x: x.strip(), row) for row in self.data]
        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

    def __getitem__(self, item):
        if isinstance(item, (int, slice)):
            return self.data[item]

        elif isinstance(item, str):
            return [row[item] for row in self.data]

        elif isinstance(item, tuple):
            if isinstance(item[0], list) or isinstance(item[1], list):
                if isinstance(item[0], list):
                    rowz = [row for index, row in enumerate(self.data) if index in item[0]]
                else:
                    rowz = self.data[item[0]]

                if isinstance(item[1], list):
                    if all([isinstance(i, int) for i in item[1]]):
                        # python3 use values(),keys(),items() instead of itervalues()...
                        return [[column_value for index, column_value in enumerate(row.values()) if index in item[1]]
                                for row in rowz]
                    elif all([isinstance(i, str) for i in item[1]]):
                        return [[row[col] for col in item[1]] for row in rowz]
                    else:
                        raise TypeError('What the hell is this?')

                else:
                    return rowz[item[1]]

            else:
                if isinstance(item[0], (int, slice)) and isinstance(item[1], (int, slice)):
                    # python3 use values(),keys(),items() instead of itervalues()...
                    return [list(row.values())[item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1], str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('I don\'t know how to handle this...')

        elif isinstance(item, list):
            return [[value for key, value in row.items() if key in item] for row in self.data]

    # TASK3:
    def transform_type(self, col_name):
        time_check = 0
        try:
            # try if col is numeric
            nums = [float(row[col_name].replace(',', '')) for row in self.data]
            return nums, 1 if time_check else 0
        except:
            try:
                nums = [parse(row[col_name].replace(',', '')) for row in self.data]
                nums = [time.mktime(num.timetuple()) for num in nums]
                is_time = 1
                return nums, 1 if is_time else 0
            except:
                raise TypeError('Calculate Invalid')

    def min(self, col_name):
        nums, time_check = self.transform_type(col_name)
        result = min(nums)
        if time_check:
            return datetime.datetime.fromordinal(result)
        else:
            return result


    def max(self, col_name):
        nums, time_check = self.transform_type(col_name)
        result = max(nums)
        if time_check:
            return datetime.datetime.fromordinal(result)
        else:
            return result

    def median(self, col_name):
        nums, time_check = self.transform_type(col_name)
        nums = sorted(nums)
        center = int(len(nums) / 2)
        if len(nums) % 2 == 0:
            result = sum(nums[center - 1:center + 1]) / 2.0
            return datetime.datetime.fromtimestamp(result) if time_check else result
        else:
            result = nums[center]
            return datetime.datetime.fromtimestamp(result) if time_check else result

    def mean(self, col_name):
        nums, time_check = self.transform_type(col_name)
        result = sum(nums) / len(nums)
        return datetime.datetime.fromtimestamp(result) if time_check else result

    # sum/std of time make more sense when in the format of seconds so I won't transform to Y-M-D H-M format
    def sum(self, col_name):
        nums, time_check = self.transform_type(col_name)
        return sum(nums)

    def std(self, col_name):
        nums, time_check = self.transform_type(col_name)
        mean = sum(nums) / len(nums)
        return (sum([(num - mean) ** 2 for num in nums]) / len(nums)) ** 0.5

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value == value]
        else:
            return [row for row in self.data if row[column_name] == value]

    # TASK4:
    def add_rows(self, list_of_lists):
        columns_count = len(self.header)
        if sum([len(row) == columns_count for row in list_of_lists]) == len(list_of_lists):
            self.data = self.data + [OrderedDict(zip(self.header, row)) for row in list_of_lists]
            return self.data
        else:
            raise Exception('incorrect number of columns')

    # TASK5:
    def add_columns(self, list_of_values, column_name):
        if len(list_of_values) == len(self.data):
            self.header = self.header + column_name
            self.data = [OrderedDict(zip(list(old_row.keys()) + column_name, list(old_row.values()) + added_values))
                         for old_row, added_values in zip(self.data, list_of_values)]
            return self.data
        else:
            raise Exception('incorrect number of rows')

#Execute:

df = DataFrame.from_csv('SalesJan2009.csv')

#Task3:

test1 = df.min('Last_Login')
print(test1)
test2 = df.max('Price')
print(test2)

# Task4:

new_row = [['1/3/09 6:17','Product1','1200','Mastercard','carolina',
    'Basildon','England','United Kingdom','1/2/09 6:00','1/2/09 6:08','51.5','-1.1166667'],
['1/3/09 6:17','Product1','1200','Mastercard','carolina',
    'Basildon','England','United Kingdom','1/2/09 6:00','1/2/09 6:08','51.5','-1.1166667']]
df = df.add_rows(new_row)
print(df)

