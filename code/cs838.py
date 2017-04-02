
# coding: utf-8

# In[1]:

import py_entitymatching as em
import pandas as pd
import os, sys


# In[ ]:




# In[2]:

datasets_dir = "/users/rohitsd/Desktop/Datasets"


# In[ ]:




# In[ ]:




# In[3]:

path_A = datasets_dir + '/' + 'yelp_data.csv'
path_B = datasets_dir + '/' + 'zomato_data.csv'


# In[4]:

A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')


# In[ ]:




# In[5]:

ab = em.AttrEquivalenceBlocker()


# In[ ]:




# In[6]:

C1 = ab.block_tables(A, B, 
                    l_block_attr='zipcode', r_block_attr='zipcode', 
                    l_output_attrs=['name', 'city', 'zipcode', 'review_count', 'latitude', 'longitude', 'rating', 'address', 'zomato_id', 'yelp_id'],
                    r_output_attrs=['name', 'city', 'zipcode','review_count', 'latitude', 'longitude', 'rating', 'address', 'zomato_id', 'yelp_id'],
                    l_output_prefix='l_', r_output_prefix='r_')


# In[13]:

len(C1)


# In[7]:

C1.to_csv('c.csv')


# In[14]:

C1.head()


# In[ ]:




# In[9]:

block_f = em.get_features_for_blocking(A, B)


# In[ ]:




# In[10]:

block_f


# In[ ]:




# In[11]:

rb = em.RuleBasedBlocker()
rb.add_rule(['name_name_lev_sim(ltuple, rtuple) < 0.4'], block_f)


# In[ ]:




# In[ ]:




# In[ ]:




# In[12]:

D = rb.block_candset(C1, show_progress=False)


# In[13]:

D.to_csv('D.csv')


# In[ ]:




# In[14]:

len(D)


# In[15]:

S = em.sample_table(D, 600)


# In[16]:

S


# In[ ]:




# In[ ]:




# In[17]:

D


# In[18]:

S.to_csv('S.csv')


# In[25]:

#G = em.label_table(S, 'label')


# In[ ]:


#G.head()


# In[19]:


len(S)


# In[20]:

path_labeled_data = datasets_dir + '/' + 'labeled.csv'


# In[ ]:




# In[21]:

G = em.read_csv_metadata(path_labeled_data, key='_id', 
                         fk_ltable='l_ID', fk_rtable='r_ID',
                         ltable=A, rtable=B)


# In[ ]:




# In[22]:

G.head()


# In[42]:

train_test = em.split_train_test(G, train_proportion=0.5)
I = train_test['train']
J = train_test['test']


# In[43]:

I.to_csv('I.csv')
J.to_csv('J.csv')


# In[ ]:




# In[24]:

match_f = em.get_features_for_matching(A, B)


# In[25]:

match_f.feature_name


# In[26]:

H = em.extract_feature_vecs(I, 
                            feature_table=match_f, 
                            attrs_after='label',
                            show_progress=False)  


# In[27]:

I.head()


# In[29]:

#matcher
dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')

result = em.select_matcher([dt, rf, svm, ln, lg], table=H, 
        exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
        k=5,
        target_attr='label', metric='recall', random_state=0)

result['cv_stats']




# In[ ]:




# In[33]:

result2 = em.select_matcher([dt, rf, svm, ln, lg], table=H, 
        exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
        k=5,
        target_attr='label', metric='precision', random_state=0)

result2['cv_stats']


# In[34]:

L = em.extract_feature_vecs(J, 
                            feature_table=match_f, 
                            attrs_after='label',
                            show_progress=False)  


# In[35]:

L.head()


# In[36]:

rf.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')


# In[37]:

#NOW apply the best ML model to test set L


predictions = rf.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)



# In[38]:

eval_result = em.eval_matches(predictions, 'label', 'predicted')
em.print_eval_summary(eval_result)


# In[ ]:




# In[39]:

lg.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')


# In[40]:

predictions_lg = lg.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)


# In[41]:

eval_result2 = em.eval_matches(predictions_lg, 'label', 'predicted')
em.print_eval_summary(eval_result2)


# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:




# In[ ]:



