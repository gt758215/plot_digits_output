#!/usr/bin/python2.7
import re
import sys
import matplotlib.pyplot as plt

#file_name = 'record_1.txt'
if len(sys.argv) < 2:
    print('No input')
    quit()

file_name = sys.argv[1]
file_in = open(file_name, 'r')
file_out = file_name.split('.')
if len(file_out) == 1:
    file_out = file_out[0]
else:
    file_out = '.'.join(file_out[:-1])


epoch_reg = re.compile('epoch\s(\d+(\.\d+)?)')
parser_reg = re.compile('\s(\w+)\s\=\s([.0-9]*)')

train_reg = re.compile('\[INFO\] (Training)')
val_reg = re.compile('\[INFO\] (Validation)')

dict_val = {}
dict_train = {}

def my_find(reg, line):
    m = reg.search(line)
    if m:
        return m.group(1)
    else:
        return None

def my_find2(reg, line):
    m = reg.findall(line)
    if m:
        return m
    else:
        return None

while True:
    line = file_in.readline()
    if not line:
        break
    is_train = my_find(train_reg, line)
    is_val = my_find(val_reg, line)
    if not is_train and not is_val:
        continue

    stage = is_train if is_train else is_val
    found_text = my_find2(parser_reg, line)
    def find(list, str):
        if not list:
            return False
        for k, v in list:
            if k == str:
                return True
        return False

    if not find(found_text, 'loss'):
        continue

    epoch = my_find(epoch_reg, line)

    if(stage == 'Training'):
        dict_train[float(epoch)] = found_text
    else:
        dict_val[float(epoch)] = found_text

train_x = []
train_y = {}
for key in sorted(dict_train.iterkeys()):
    #print(key)
    train_x.append(key)
    names_and_numbers = dict_train.get(key)

    for k, v in names_and_numbers:
        if not train_y.get(k):
            train_y[k] = []
        train_y[k].append(v)

val_x = []
val_y = {}
for key in sorted(dict_val.iterkeys()):
    #print(key)
    val_x.append(key)
    names_and_numbers = dict_val.get(key)

    for k, v in names_and_numbers:
        if not val_y.get(k):
            val_y[k] = []
        val_y[k].append(v)


sub_number = 100*len(train_y)+10

#for key in train_y.iterkeys():
#    print(key)
#    for v in train_y.get(key):
#        print(v)

#for key in val_y.iterkeys():
#    print(key)
#    for v in val_y.get(key):
#        print(v)


plt.figure(figsize=(10, 5*len(train_y)),)
# set title of all
plt.suptitle(file_name, fontsize=24)

for key in train_y.iterkeys():
    # change section of subfigure
    sub_number += 1
    plt.subplot(sub_number)

    #print(key)
    # point grid line
    plt.grid()
    # add space between subfigures
    plt.subplots_adjust(hspace=0.5)

    # set train data points
    train_values = train_y.get(key)
    plt.plot(train_x, train_values)

    # set validation data points
    if val_y.get(key):
        val_values = val_y.get(key)
        plt.plot(val_x, val_values, color='red', linestyle='--')

    # set range of x axie and y axie
    plt.xlim(0,train_x[-1]+1)
    if(key.startswith('acc')):
        plt.ylim(0,1)
    else:
        plt.ylim(0,)

    # set label
    plt.xlabel("epoch")
    plt.ylabel(key)

    # get figure size range
    axes = plt.gca()
    bottom, top = axes.get_ylim()
    left, right = axes.get_xlim()
    height = top - bottom
    width = right - left

    # set string we need
    plt.text(right + 0.03*width, top - 0.1*height, r'Train',
             fontdict={'size': 16, 'color':'b'})
    if val_y.get(key):
        plt.text(right + 0.03*width, top - 0.2*height, r'Val',
                fontdict={'size': 16, 'color':'r'})

plt.savefig(file_out+'.png')
