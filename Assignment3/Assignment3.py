import csv
from collections import OrderedDict
import numpy
from dateutil.parser import parse
import datetime, time
from collections import defaultdict
class DataFrame(object):

    @classmethod
    def from_csv(cls, file_path, delimiting_character=',', quote_character='"'):
        with open(file_path, 'rU') as infile:
            reader = csv.reader(infile, delimiter=delimiting_character, quotechar=quote_character)
            data = []

            for row in reader:
                data.append(row)

            return cls(list_of_lists=data)

    def __init__(self,list_of_lists, header=True):

        if header:
            self.header = list_of_lists[0]
            self.data = list_of_lists[1:]
        else:
            self.header = ['column' + str(index + 1) for index, column in enumerate(self.data[0])]
            self.data = list_of_lists
        self.data = [OrderedDict(zip(self.header, row)) for row in self.data]

                                   #  ======== Assignment2 =========
        # ======== Task1 ==========

        if len(set(self.header)) == len(self.header):
            print('True')
        else:
            raise Exception('duplicates found')

        # =========Task2============

        self.strip_whitespace = [[x.strip(' ') for x in l] for l in list_of_lists]



    def __getitem__(self, item):

        if isinstance(item,(int,slice)):

            return self.data[item]

        elif isinstance(item,str):
            return [row[item] for row in self.data]

        elif isinstance(item,tuple):
            if isinstance(item[0],list) or isinstance(item[1],list):
                if isinstance(item[0],list):

                    rowz = [row for index,row in enumerate(self.data) if index in item[0]]
                else:
                     rowz = self.data[item[0]]

                if isinstance(item[1],list):
                    if all([isinstance(i,int) for i in item[1]]):
                        return [[column_value for index,column_value in enumerate(row.values()) if index in item[1]] for row in rowz]
                    elif all([isinstance(i,str) for i in item[1]]):
                        return [[row[col] for col in item[1]] for row in rowz]
                    else:
                        raise TypeError('type error')

                else:
                    return rowz[item[1]]

            else:
                if isinstance(item[0],(int,slice)) and isinstance(item[1],(int,slice)):
                    return [list(row.values())[item[1]] for row in self.data[item[0]]]
                elif isinstance(item[1],str):
                    return [row[item[1]] for row in self.data[item[0]]]
                else:
                    raise TypeError('type error')

        elif isinstance(item,list):
            if isinstance(item[0],str):

                return [OrderedDict(zip(item,[ value for key ,value in row.items() if key in item])) for row in self.data]

            elif isinstance(item[0],bool):
                return [row for is_needed,row in zip(item,self.data) if is_needed== True]

            else:
                raise TypeError('type error')

    def get_rows_where_column_has_value(self, column_name, value, index_only=False):
        if index_only:
            return [index for index, row_value in enumerate(self[column_name]) if row_value==value]
        else:
            return [row for row in self.data if row[column_name]==value]

   #=========Task3:=============

    def column(self, col_name):
        try:
            trans_num = [float(row[col_name]) for row in self.data] #This command works when values of column are Numbers
            return trans_num

        except:
            try:
                trans_time = [parse(row[col_name]) for row in self.data] #This command works when values of column are TimeStampes
                return trans_time
            except:
                trans_words = [str(row[col_name]) for row in self.data]   #This command works when values of column are Words
                return trans_words

    def max(self, col_name):
        num = self.column(col_name)   #Extracted Column
        maximum = max(num)
        return maximum
    def min(self, col_name):
        num = self.column(col_name)
        minimum = min(num)
        return minimum

    def median(self, col_name):
        num = self.column(col_name)
        mediann = numpy.median(num)
        return mediann

    def mean(self, col_name):
        num = self.column(col_name)
        average = sum(num)/len(num)
        return average

    def std(self, col_name):
        num = self.column(col_name)
        standard_deviation = numpy.std(num)
        return standard_deviation

      #===========Task4=============

    def add_row(self, list):
        if len(df.header) == len(list):
            self.data = self.data + [OrderedDict(zip(self.header, list))]
            return self.data
        else:
            raise Exception ('Coloums Not Match')

    #============Task5==============

    #def add_column(self,list_of_values,column_name):
        #if len(self.data) == len(list_of_values):

            #self.header=self.header+column_name

        #else:
            #raise Exception('Rows Not Match')

                                         # ======== Assignment 3 =================


#============ Task1 =============

    def sort_by(self,col_name,reverse=True):
        num = self.column(col_name)
        print(num)
        if reverse:
                col_sort = sorted(num)  # For Numeric Columns
                return col_sort
        elif reverse:
            col = [row[col_name] for row in self.data]
            sort_str = sorted(col,key=str.upper)  # For String Columns
            return sort_str
        else:
            col = [row[col_name] for row in self.data]
            try:
                sort_str=sorted(col, key=lambda x: datetime.datetime.strptime(x,"%m/%d/%y %H:%M"))  #For Time Columns
            except:
                sort_str=sorted(col, key=lambda x: datetime.datetime.strptime(x,"%m/%d/%y %I:%M"))

            return sort_str

#========= Task 3 ============

    def group_by(self,col1,col2):
        candidate1=self.column(col1)
        candidate2=self.column(col2)
        zip_cols = zip(candidate1,candidate2)
        d=defaultdict(list)
        for k,v in zip_cols:
            d[k].append(v)
        grouped = d.items()           # dict_items([('yellow', [1, 4]), ('mid', [3]), ('did', [4]), ('msid', [5])])
        select = dict(grouped)        # {'yellow': [1, 4], 'mid': [3], 'did': [4], 'msid': [5]}
        values = list(select.values())
        return grouped, values
        #for s in values:
            #print(*s)

        #blank_list = []
        #blank_list.append([values,agged])
        #return DataFrame(blank_list)

def avg(list_of_values):
    return sum(list_of_values)/float(len(list_of_values))

#============ Task2 =================

class Series(list):


    def __eq__(self, other):
        ret_list = []
        for item in self:
            ret_list.append(item == other)
        return ret_list

    def __gt__(self, other):
        ret_list = []
        for item in self:
            ret_list.append(item > other)
        return ret_list

    def __lt__(self, other):
        ret_list = []
        for item in self:
            ret_list.append(item < other)
        return ret_list

    def __ge__(self, other):
        ret_list = []
        for item in self:
            ret_list.append(item >= other)
        return ret_list

    def __le__(self, other):
        ret_list = []
        for item in self:
            ret_list.append(item <= other)
        return ret_list


raw_file = open('SalesJan2009.csv')
file_read = csv.reader(raw_file)
file_list = list(file_read)
file_list[559][2]='13000'


print(file_list)
for row in file_list:
    if len(row) == 12:
        continue
    print('False')     #All have length of 12.
print(file_list[0])
print(file_list[0][1])

# Execut test:
print('Execut test: ')

df = DataFrame(file_list)

# Execute test for Assignment2 Task2:
print('Execute test for Assignment2 Task2: ')

print(df.strip_whitespace)

# Execute test for Assignment2 Task3:
print('Execute test for Assignment2 Task3: ')

test1 = df.max('Transaction_date')
print(test1)
test2 = df.min('Transaction_date')
print(test2)
test3 = df.median('Price')
print(test3)
test4 = df.mean('Price')
print(test4)
test5 = df.std('Price')
print(test5)

# Execute test for Assignment2 Task4:
print('Execute test for Assignment2 Task4: ')

new_line = ['1/5/09 4:10', 'Product1', '1200', 'Mastercard', 'Nicola', 'Roodepoort', 'Gauteng', 'South Africa', '1/5/09 2:33', '1/7/09 5:13', '-26.1666667', '27.8666667']
show_new_line=df.add_row(new_line)
print(show_new_line)

# Execute test for Assignment2 Task5:

# Execute test for Assignment 3 Task1:
print('Execute test for Assignment3 Task1: ')

test6 = df.sort_by('Transaction_date',False)
test7 = df.sort_by('Account_Created',False)
print(test6)
print(test7)


#Execute test for Assignment3 Task2:
print('Execute test for Assignment3 Task2: ')

get_Price_col = df['Price']
change_to_float = list(map(float, get_Price_col))
change_Time = df.sort_by('Transaction_date')

TF_Price = Series.__gt__(change_to_float,1400)
TF_Str = Series.__eq__(df['Name'],'Nikki')
TF_Time = Series.__ge__(change_Time,datetime.datetime(2009, 1, 10, 6, 30))

print(df[TF_Price])
print(TF_Price)
print(TF_Str)
print(TF_Time)
#Execute test for Assignment3 Task3:
print('Execute test for Assignment3 Task3: ')

print(df.group_by('Product','Price'))
print(df.group_by('Name','Price'))
#print(df.group_by('Transaction_date','Price'))
#print(df.group_by('Latitude','Price',func()))

#df.group_by('Payment_Type', 'Price', avg)