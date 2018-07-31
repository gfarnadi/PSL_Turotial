
# coding: utf-8

# In[1]:

import os
from data_generator import read_lines,save_file


# In[2]:

def reformat_output(output_path, new_output_path):
    output_lines = read_lines(output_path)
    txt = ''
    output = {}
    for line in output_lines:
        info = line.split(',')
        user = info[0].replace("'",'')
        cat = info[1].replace("'",'')
        label = info[2].replace("'",'')
        truth = float(info[3].replace("'",''))
        if (user,cat) in output.keys():
            if user in ['u7','u8','u9']:
                (label_r,truth_r) = output[(user,cat)] 
                if truth>truth_r:
                    output[(user,cat)]  = (label,truth)
        else:
            if user in ['u7','u8','u9']:
                output[(user,cat)]  = (label,truth)
    for key in output.keys():
        txt+= key[0]+'\t'+key[1]+'\t'+output[key][0]+'\n'
    save_file(new_output_path, txt) 


# In[3]:

output_path = '../output/IS.csv'
new_output_path = '../output/IS_new.csv'
reformat_output(output_path, new_output_path)


# In[4]:

def accuracy(target_file, output_file):
    lines = read_lines(target_file)
    result = {}
    number = 0.0
    for line in lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        if float(info[3])>0.0:
            if user in ['u7','u8','u9']:
                result[(user,cat)] = label
                number+=1.0
    output_lines = read_lines(output_file)
    correct = 0.0
    for line in output_lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        if (user,cat) in result.keys():
            label_t = result[(user,cat)]
            if label_t==label:
                correct +=1.0
    accuracy = float(correct)/6.0
    return accuracy


# In[5]:

target_file = '../data/user_truth.txt'
output_file = '../output/IS_new.csv'
acc = accuracy(target_file, output_file)
acc


# In[ ]:




# In[ ]:



