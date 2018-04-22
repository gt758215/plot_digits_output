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


lr_reg = re.compile('lr\s\=\s(\d+(\.\d+)?)')
acc_reg = re.compile('accuracy\s\=\s(\d+(\.\d+)?)')
loss_reg = re.compile('loss\s\=\s(\d+(\.\d+)?)')
epoch_reg = re.compile('epoch\s(\d+(\.\d+)?)')

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

while True:
    line = file_in.readline()
    if not line:
        break
    is_train = my_find(train_reg, line)
    is_val = my_find(val_reg, line)
    if not is_train and not is_val:
        continue

    stage = is_train if is_train else is_val

    loss = my_find(loss_reg, line)
    if not loss:
        continue
    lr = my_find(lr_reg, line)
    acc = my_find(acc_reg, line)
    epoch = my_find(epoch_reg, line)
    #print("%s %s %s %s %s" % (stage, epoch, lr, loss, acc))
    if(stage == 'Training'):
        dict_train[float(epoch)] = (lr, loss, acc)
    else:
        dict_val[float(epoch)] = (lr, loss, acc)


'''

import pandas as pd
from pandas.plotting import table

train_table = []
val_table = []

for key in sorted(dict_train.iterkeys()):
    tmp = []
    tmp.append(key)
    a, b, c = dict_train.get(key)
    tmp.append(a)
    tmp.append(b)
    tmp.append(c)
    train_table.append(tmp)


train_df = pd.DataFrame( train_table, columns=['epoch', 'LR', 'loss', 'acc'])

#print(train_df)

for key in sorted(dict_val.iterkeys()):
    tmp = []
    tmp.append(key)
    a, b, c = dict_val.get(key)
    tmp.append(b)
    tmp.append(c)
    val_table.append(tmp)


val_df = pd.DataFrame( val_table, columns=['epoch', 'loss', 'acc'])

#print(val_df)
ax = plt.subplot(111, frame_on=False) # no visible frame
ax.xaxis.set_visible(False)  # hide the x axis
ax.yaxis.set_visible(False)  # hide the y axis
table(ax, val_df, rowLabels=['']*val_df.shape[0], loc='center')

plt.savefig('mytable.pdf', bbox_inches='tight')
'''

train_x = []
train_y1 = []
train_y2 = []
train_y3 = []

for key in sorted(dict_train.iterkeys()):
    #print(key)
    train_x.append(key)
    a, b, c = dict_train.get(key)
    train_y1.append(a)
    train_y2.append(b)
    train_y3.append(c)

val_x = []
val_y1 = []
val_y2 = []
val_y3 = []

for key in sorted(dict_val.iterkeys()):
    val_x.append(key)
    a, b, c = dict_val.get(key)
    val_y2.append(b)
    val_y3.append(c)


plt.figure(num=3, figsize=(10, 10),)

plt.subplot(312)
plt.grid()
plt.plot(train_x, train_y2)
plt.plot(val_x, val_y2, color='red', linestyle='--')
plt.xlim(0,train_x[-1]+1)
plt.ylim(0,)
#plt.xlabel("epoch")
plt.ylabel("Loss")

plt.subplot(311)
plt.grid()
plt.plot(train_x, train_y3)
plt.plot(val_x, val_y3, color='red', linestyle='--')
plt.xlim(0,train_x[-1]+1)
plt.ylim(0,1)
#plt.xlabel("epoch")
plt.ylabel("Acc")

plt.text(train_x[-1]/4, 1.2, r'Val',
         fontdict={'size': 16, 'color':'r'})
plt.text(train_x[-1]/4*3, 1.2, r'Train',
         fontdict={'size': 16, 'color':'b'})

#print(len(val_y2))
#print(len(val_x))

plt.subplot(313)
plt.grid()
plt.plot(train_x, train_y1)
plt.xlim(0,train_x[-1]+1)
plt.ylim(-0.1,)
plt.xlabel("epoch")
plt.ylabel("LR")

#plt.show()

#plt.subplot(414)
#val_x_idx = [i for i in range(0, len(val_x), len(val_x)//8)]
#val_y2_idx = [i for i in range(0, len(val_y2), len(val_y2)//8)]
#val_y3_idx = [i for i in range(0, len(val_y3), len(val_y3)//8)]

#val_x_tmp = [val_x[i] for i in val_x_idx]
#val_y2_tmp = [val_y2[i] for i in val_y2_idx]
#val_y3_tmp = [val_y3[i] for i in val_y3_idx]
#print(val_x_tmp)
#the_table = plt.table(cellText=[val_y2_tmp, val_y3_tmp],
#                      colWidths=[0.15]*9,
#                      colLabels=val_x_tmp,
#                      rowLabels=['val_loss', 'val_acc'],
#                      loc='bottom')
#plt.subplots_adjust(left=0.1, bottom=-0.5)


plt.savefig(file_out+'.png')
