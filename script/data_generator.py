
# coding: utf-8

# In[1]:

import sys,os,random,networkx


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

def make_user_label_file(node_size, label_cat, train_size, user_all_file, user_truth_file, user_train_file, user_target_file):
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


# In[5]:

def local_predictor(source, accuracy_label_cat, user_label_file, label_cat_info, predictor_file):
    lines = read_lines(user_label_file)
    user_txt = ''
    for line in lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        label_cat, accuracy = find_label_cat(accuracy_label_cat, cat, label, label_cat_info)
        predict = random.random() 
        if predict>accuracy:
            index = 1
            while label_cat[index]==label:
                index+=1
            label = label_cat[index]
        user_txt+= source+'\t'+user+'\t'+label_cat[0]+ '\t'+label+'\t'+'1.0'+'\n'
    save_file(predictor_file, user_txt)
    return user_txt


# In[6]:

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


# In[7]:

def create_links(node_size, user_link_file):
    link_txt = ''
    edges = create_synthetic_graph(node_size)
    for edge in edges:
        link_txt+= 'u'+str(edge[0])+'\t'+'u'+str(edge[1])+'\t'+'1.0'+'\n'
    save_file(user_link_file, link_txt)


# In[8]:

def create_synthetic_graph(node_size):
    m = 6
    p = 0.3 
    graph = networkx.powerlaw_cluster_graph(node_size, m, p, seed=None)
    return graph.edges()


# In[9]:

def create_likes(user_label_file, likes_label_cat, label_cat, likes_file):
    lines = read_lines(user_label_file)
    likes_txt = ''
    for line in lines:
        info = line.split('\t')
        user = info[0]
        cat = info[1]
        label = info[2]
        item = get_item(likes_label_cat,label_cat, cat, label)
        likes_txt += user+'\t'+item+'\t'+'1.0'+'\n'
    save_file(likes_file, likes_txt)


# In[10]:

def get_item(likes_label_cat, label_cat, cat, label):
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
                    if predict<prob:
                        item = items[label_index+1]
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


# In[11]:

def make_data(node_size, train_size, folder_path):
    label_cat = [['gender','female','male'], ['age', 'young', 'middle_age', 'old']]
    accuracy_label_cat_1 =  [[0.8, 'gender','female','male'], [0.6, 'age', 'young', 'middle_age', 'old']]
    accuracy_label_cat_2 =  [[0.6, 'gender','female','male'], [0.9, 'age', 'young', 'middle_age', 'old']]
    # create user data
    user_truth_file = folder_path+ 'user_truth.txt'
    user_target_file = folder_path+ 'user_target.txt'
    user_train_file = folder_path+ 'user_train.txt'
    user_all_file = folder_path+ 'user_all.txt'
    make_user_label_file(node_size, label_cat, train_size, user_all_file, user_truth_file, user_train_file, user_target_file)
    # create local redictors
    predictor_file_1 = folder_path+ 'local_predictor_1_obs.txt'
    predictor_file_2 = folder_path+ 'local_predictor_2_obs.txt'
    predict_1 = local_predictor('s1',accuracy_label_cat_1, user_all_file, label_cat, predictor_file_1)
    predict_2 = local_predictor('s2',accuracy_label_cat_2, user_all_file, label_cat, predictor_file_2)
    predictor_all_file = folder_path+ 'local_predictor_obs.txt'
    save_file(predictor_all_file, predict_1+predict_2)
    # create (user-user) links
    user_link_file = folder_path+ 'friend_obs.txt'
    create_links(node_size, user_link_file)
    # create (user-item) likes
    likes_label_cat = [[0.8,'gender','romance', 'action'], [0.8,'age','animation', 'drama', 'classic']]
    likes_file = folder_path+ 'likes_obs.txt'
    create_likes(user_all_file, likes_label_cat, label_cat, likes_file)


# In[12]:

node_size = 10
train_size = 6
folder_path = '/Users/Gfarnadi/Movies/PSL_tutorial/data/'
make_data(node_size, train_size, folder_path)


# In[13]:

model_txt = '''10: Predicts(S,U,A,L)-> Is(U,A,L)^2
10: Friend(U,V) & Is(V,A,L)-> Is(U,A,L)^2
10: Friend(V,U) & Is(V,A,L)-> Is(U,A,L)^2
10: Likes(U,T) & Likes(V,T) & Is(V,A,L) -> Is(U,A,L)^2
10: Is(U,A,+L) = 1
'''

data_txt = '''predicates:
  Predicts/4: closed
  Friend/2: closed
  Likes/2: closed
  Is/3: open
observations:
  Predicts: data/local_predictor_obs.txt
  Friend: data/friend_obs.txt
  Likes : data/likes_obs.txt
  Is : data/user_train.txt
targets: 
  Is : data/user_target.txt
truth: 
  Is : data/user_truth.txt
'''
model_path = '../model/user_modeling.psl'
data_path =  '../model/user_modeling.data'
save_file(model_path,model_txt)
save_file(data_path,data_txt)

