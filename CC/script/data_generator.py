
# coding: utf-8

# In[1]:

import sys,os,random,networkx
import numpy as np


# In[2]:

def save_file(path, content):
    try:
        os.remove(path)
    except OSError:
        pass
    with open(path, 'a') as out:
        out.write(content+'\n')


# In[3]:

def read_lines(file_path):
    array = []
    with open(file_path, "r") as ins:
        for line in ins:
            line = line.replace("\n","")
            if len(line)>0:
                array.append(line)
    return array


# In[4]:

def make_user_label_file(node_size, label_cat, train_size, user_all_file, user_truth_file, user_train_file, user_target_file, user_network, homophily_probability, no_prob):
    colored_users = {}
    colored_keys = []
    max_counter = {}
    i=0
    while i<node_size:
        net = user_network[i]
        max_counter[i] = homophily_probability * len(net)
        i+=1
    if homophily_probability==0.5:
        make_user_files(node_size, label_cat, train_size, user_all_file, user_truth_file, user_train_file, user_target_file)
    else:
        for label in label_cat:  
            label_size = len(label)
            index = 1
            while index < label_size:
                user_index = 0
                while user_index in colored_users.keys():
                    user_index = random.randint(1, node_size)-1  
                #print(user_index)
                colored_users[user_index] = (label[0], label[index])
                colored_keys.append(user_index)
                index+=1
            # use user network based on the probability to label the nodes
        notEmpty = True
        while notEmpty:
            empty = 0
            if len(colored_users.keys())==node_size:
                notEmpty = False
            else:
                temp = []
                for user in colored_users.keys():
                    if user in colored_keys:
                        pass
                    else:
                        temp.append(user)
                colored_keys = []
                colored_keys = temp
                for user in colored_keys:
                    network = user_network[user]
                    uncolored_users = []
                    for friend in network:
                        if friend in colored_keys:
                            pass
                        else:
                            uncolored_users.append(friend)
                    if len(uncolored_users) ==0:
                        empty+=1
                    else:
                        color_label = colored_users[user][1]
                        #print(user)
                        #print(color_label)
                        for uncolor_u in uncolored_users:
                            if no_prob:
                                predict = random.random() 
                                if predict>homophily_probability:
                                    index = 1
                                    while label[index]==color_label:
                                        index+=1
                                    color_label = label[index]
                                colored_users[uncolor_u] = (label[0], color_label)
                            else:
                                if max_counter[user]>0:
                                    colored_users[uncolor_u] = (label[0], color_label)
                                    max_counter[user]=-1
                                else:
                                    index = 1
                                    while label[index]==color_label:
                                        index+=1
                                    color_label = label[index]
                                    colored_users[uncolor_u] = (label[0], color_label)
            if empty==node_size:
                notEmpty = False
        save_user_color(colored_users, label_cat, train_size, user_train_file, user_truth_file, user_target_file,user_all_file)


# In[5]:

def make_user_files(node_size, label_cat, train_size, user_all_file, user_truth_file, user_train_file, user_target_file):
    user_train = ''
    user_truth = ''
    user_target = ''
    user_all = ''
    for i in range (node_size):
        for label in label_cat:
            label_size = len(label)
            index = random.randint(1, label_size-1)
            user_all+= 'u'+str(i)+'\t'+label[0] +'\t'+label[index]+'\n'
            if i>train_size:
                j=1
                while j<label_size:
                    if j==index:
                        user_truth+= 'u'+str(i)+'\t'+label[0] +'\t'+label[index]+'\t'+'1.0'+'\n'
                    else:
                        user_truth+= 'u'+str(i)+'\t'+label[0] +'\t'+label[j]+'\t'+'0.0'+'\n'
                    user_target+= 'u'+str(i)+'\t'+label[0] +'\t'+label[j]+'\n'
                    j+=1
            else:
                j=1
                while j<label_size:
                    if j==index:
                        user_train+= 'u'+str(i)+'\t'+label[0] +'\t'+label[index]+'\t'+'1.0'+'\n' 
                    else:
                        user_train+= 'u'+str(i)+'\t'+label[0] +'\t'+label[j]+'\t'+'0.0'+'\n' 
                    j+=1
    save_file(user_train_file, user_train)
    save_file(user_truth_file, user_truth)
    save_file(user_target_file, user_target)
    save_file(user_all_file, user_all)


# In[6]:

def save_user_color(colored_users, label_cat, train_size, user_train_file, user_truth_file, user_target_file,user_all_file):
    user_train = ''
    user_truth = ''
    user_target = ''
    user_all = ''
    for i in range (node_size):
        label = colored_users[i]
        cat = find_cat(label[0], label_cat)
        label_size = len(cat)
        user_all+= 'u'+str(i)+'\t'+label[0] +'\t'+label[1]+'\n'
        if i>train_size:
            j=1
            while j<label_size:
                if label[1]==cat[j]:
                    user_truth+= 'u'+str(i)+'\t'+label[0] +'\t'+label[1]+'\t'+'1.0'+'\n' 
                else:
                    user_truth+= 'u'+str(i)+'\t'+label[0] +'\t'+cat[j]+'\t'+'0.0'+'\n'
                user_target+= 'u'+str(i)+'\t'+label[0] +'\t'+cat[j]+'\n'
                j+=1
        else:
            j=1
            while j<label_size:
                if label[1]==cat[j]:
                    user_train+= 'u'+str(i)+'\t'+label[0] +'\t'+label[1]+'\t'+'1.0'+'\n' 
                else:
                    user_train+= 'u'+str(i)+'\t'+label[0] +'\t'+cat[j]+'\t'+'0.0'+'\n' 
                j+=1
    save_file(user_train_file, user_train)
    save_file(user_truth_file, user_truth)
    save_file(user_target_file, user_target)
    save_file(user_all_file, user_all)


# In[7]:

def find_cat(user_cat, label_cat):
    i = 0
    result = []
    while i< len(label_cat):
        cat = label_cat[i]
        if user_cat == cat[0]:
            result = cat
            i=len(label_cat)
        else:
            i+=1
    return result


# In[8]:

def local_predictor(source, accuracy_label_cat, user_label_file, label_cat_info, predictor_file, no_prob):
    lines1 = read_lines(user_label_file)
    user_txt = ''
    max_counter = {}
    lines = np.random.permutation(lines1)
    for cat in accuracy_label_cat:
        max_counter[cat[1]] = float(cat[0])*len(lines)
    for line in lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        label_cat, accuracy = find_label_cat(accuracy_label_cat, cat, label, label_cat_info)
        max_counter[cat] -=1
        if no_prob:
            predict = random.random() 
            if predict>accuracy:
                index = 1
                while label_cat[index]==label:
                    index+=1
                label = label_cat[index]
            user_txt+= source+'\t'+user+'\t'+label_cat[0]+ '\t'+label+'\t'+'1.0'+'\n'
        else:
            if max_counter[cat]>0:
                user_txt+= source+'\t'+user+'\t'+label_cat[0]+ '\t'+label+'\t'+'1.0'+'\n'
            else:
                index = 1
                while label_cat[index]==label:
                    index+=1
                label = label_cat[index]
                user_txt+= source+'\t'+user+'\t'+label_cat[0]+ '\t'+label+'\t'+'1.0'+'\n'
    save_file(predictor_file, user_txt)
    return user_txt


# In[9]:

def find_label_cat(accuracy_label_cat, cat, label, label_cat_info):
    notFind = True
    index = 0
    while notFind:
        info = accuracy_label_cat[index]
        if info[1]==cat:
            notFind = False
            accuracy = info[0]
            label_cat = label_cat_info[index]
        else:
            index+=1
    return label_cat, accuracy


# In[10]:

def create_links(node_size, user_link_file):
    link_txt = ''
    edges = create_synthetic_graph(node_size)
    for edge in edges:
        link_txt+= 'u'+str(edge[0])+'\t'+'u'+str(edge[1])+'\t'+'1.0'+'\n'
    save_file(user_link_file, link_txt)
    return edges


# In[11]:

def create_synthetic_graph(node_size):
    m = 6
    p = 0.3 
    graph = networkx.powerlaw_cluster_graph(node_size, m, p, seed=None)
    return graph.edges()


# In[12]:

def create_likes(user_label_file, likes_label_cat, label_cat, likes_file, no_prob):
    lines1 = read_lines(user_label_file)
    likes_txt = ''
    max_counter = {}
    lines = np.random.permutation(lines1)
    for cat in likes_label_cat:
        max_counter[cat[1]] = float(cat[0])*len(lines)
    for line in lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        item = get_item(likes_label_cat,label_cat, cat, label, max_counter, no_prob)
        likes_txt += user+'\t'+item+'\t'+'1.0'+'\n'
    save_file(likes_file, likes_txt)


# In[13]:

def make_network(edges):
    user_network = {}
    for edge in edges:
        if edge[0] in user_network.keys():
            friends_0 = user_network[edge[0]]
            friends_0.append(edge[1])
        else:
            user_network[edge[0]] = [edge[1]]
        if edge[1] in user_network.keys():
            friends_0 = user_network[edge[1]]
            friends_0.append(edge[0])
        else:
            user_network[edge[1]] = [edge[0]]
    return user_network   


# In[14]:

def get_item(likes_label_cat, label_cat, cat, label, max_counter, no_prob):
    notFind = True
    cat_index = 0
    item = ''
    while notFind:
        items = likes_label_cat[cat_index]
        if items[1]==cat:
            prob = items[0]
            notFind = False
            label_index = 1
            label_not_find = True
            labels = label_cat[cat_index]
            while label_not_find:
                if labels[label_index]==label:
                    label_not_find = False
                    predict = random.random()
                    if no_prob:
                        if predict<prob:
                            item = items[label_index+1]
                        else:
                            if label_index==1:
                                item = items[3]
                            else:
                                item = items[2]
                    else:
                        if max_counter[cat]>0:
                            item = items[label_index+1]
                            max_counter[cat]-=1
                        else:
                            if label_index==1:
                                item = items[3]
                            else:
                                item = items[2]
                            
                else:
                    label_index+=1 
        else:
            cat_index+=1
    return item


# In[15]:

def make_data(node_size, train_size, folder_path):
    #label_cat = [['gender','female','male'], ['age', 'young', 'middle_age', 'old']]
    label_cat = [['gender','female','male']]
    #accuracy_label_cat_1 =  [[0.6, 'gender','female','male'], [0.6, 'age', 'young', 'middle_age', 'old']]
    #accuracy_label_cat_2 =  [[0.7, 'gender','female','male'], [0.7, 'age', 'young', 'middle_age', 'old']]
    accuracy_label_cat_1 =  [[0.7, 'gender','female','male']]
    accuracy_label_cat_2 =  [[0.7, 'gender','female','male']]
    # create user data
    user_truth_file = folder_path+ 'user_truth.txt'
    user_target_file = folder_path+ 'user_target.txt'
    user_train_file = folder_path+ 'user_train.txt'
    user_all_file = folder_path+ 'user_all.txt'
    # create (user-user) links
    user_link_file = folder_path+ 'friend_obs.txt'
    edges = create_links(node_size, user_link_file)
    user_network = make_network(edges)
    homophily_probability = 0.9
    make_user_label_file(node_size, label_cat, train_size, user_all_file, user_truth_file, user_train_file, user_target_file, user_network, homophily_probability, True)
    # create local redictors
    predictor_file_1 = folder_path+ 'local_predictor_1_obs.txt'
    predictor_file_2 = folder_path+ 'local_predictor_2_obs.txt'
    predict_1 = local_predictor('s1',accuracy_label_cat_1, user_all_file, label_cat, predictor_file_1, False)
    predict_2 = local_predictor('s2',accuracy_label_cat_2, user_all_file, label_cat, predictor_file_2, False)
    source_file = folder_path+ 'source_obs.txt'
    save_file(source_file,'s1\t1.0'+'\n'+'s2\t1.0')
    predictor_all_file = folder_path+ 'local_predictor_obs.txt'
    save_file(predictor_all_file, predict_1+predict_2)
    # create (user-item) likes
    #likes_label_cat = [[0.8,'gender', 'romance', 'action'], [0.8,'age', 'animation', 'drama', 'classic']]
    likes_label_cat = [[0.8,'gender', 'romance', 'action']]
    likes_file = folder_path+ 'likes_obs.txt'
    create_likes(user_all_file, likes_label_cat, label_cat, likes_file, False)


# In[16]:

node_size = 100
train_size = 6
folder_path = '../data/'
make_data(node_size, train_size, folder_path)


# In[17]:

model_txt = '''1: Source(S) & Predicts(S,U,A,L)-> Is(U,A,L)^2
1: Source(S) & ~Predicts(S,U,A,L)-> ~Is(U,A,L)^2
1: Friend(U,V) & Is(V,A,L)-> Is(U,A,L)^2
1: Friend(V,U) & Is(V,A,L)-> Is(U,A,L)^2
1: Friend(U,V) & ~Is(V,A,L)-> ~Is(U,A,L)^2
1: Friend(V,U) & ~Is(V,A,L)-> ~Is(U,A,L)^2
1: Likes(U,T) & Likes(V,T) & Is(V,A,L) -> Is(U,A,L)^2
1: Likes(U,T) & Likes(V,T) & ~Is(V,A,L) -> ~Is(U,A,L)^2
1: Is(U,A,+L) = 1
'''

data_txt = '''predicates:
  Predicts/4: closed
  Friend/2: closed
  Likes/2: closed
  Source/1: closed
  Is/3: open
observations:
  Predicts: ../data/local_predictor_obs.txt
  Source: ../data/source_obs.txt
  Friend: ../data/friend_obs.txt
  Likes : ../data/likes_obs.txt
  Is : ../data/user_train.txt
targets: 
  Is : ../data/user_target.txt
truth: 
  Is : ../data/user_truth.txt
'''
model_path = '../model/user_modeling.psl'
data_path =  '../model/user_modeling.data'
save_file(model_path,model_txt)
save_file(data_path,data_txt)


# In[ ]:



