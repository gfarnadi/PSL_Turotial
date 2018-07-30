
# coding: utf-8

# In[15]:

import os
from data_generator import read_lines,save_file


# In[16]:

def reformat_output(output_path, new_output_path):
    output_lines = read_lines(output_path)
    txt = ''
    output = {}
    for line in output_lines:
        info = line.split(',')
        user = info[0].replace("'",'')
        cat = info[1].replace("'",'')
        label = info[2].replace("'",'')
        truth = info[3].replace("'",'')
        if (user,cat) in output.keys():
            (label_r,truth_r) = output[(user,cat)] 
            if truth>truth_r:
                output[(user,cat)]  = (label,truth)
        else:
            output[(user,cat)]  = (label,truth)
    for key in output.keys():
        txt+= key[0]+'\t'+key[1]+'\t'+output[key][0]+'\n'
    save_file(new_output_path, txt) 


# In[17]:

output_path = '../output/IS.csv'
new_output_path = '../output/IS_new.csv'
reformat_output(output_path, new_output_path)


# In[18]:

def accuracy(target_file, output_file):
    lines = read_lines(target_file)
    result = {}
    number = 0
    for line in lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        result[(user,cat,label)] = float(info[3])
        number+=1
    output_lines = read_lines(output_file)
    correct = 0.0
    for line in output_lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        if (user,cat,label) in result.keys():
            truth = result[(user,cat,label)]
            if truth == 1.0:
                correct +=1
    accuracy = float(correct)*3/float(number)
    return accuracy


# In[19]:

target_file = '../data/user_truth.txt'
output_file = '../output/IS_new.csv'
accuracy(target_file, output_file)


# In[ ]:



