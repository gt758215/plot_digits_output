# plot_digits_output

Digits log output Parser

cmd: python plot.py [filename]



This program find either strings of below in every line:
[INFO] Training
[INFO] Validation

If found, it will catch four parameters in the line, and store them into train or val dictionary.
lr = [%d.%d]
accuracy = [%d.%d]
loss = [%d.%d]
epoch [%d.%d]

Finally, polling those two dictionary, and plot PNG figure like:

![alt text](https://github.com/gt758215/plot_digits_output/blob/master/resnet50_momentun_epoch90.png)