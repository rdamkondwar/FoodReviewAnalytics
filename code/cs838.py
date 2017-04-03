
# coding: utf-8

# In[16]:

import py_entitymatching as em
import pandas as pd
import os, sys


# In[ ]:




# In[31]:

datasets_dir = "/users/rohitsd/Desktop/Datasets"


# In[ ]:




# In[ ]:




# In[33]:

path_A = datasets_dir + '/' + 'yelp_data.csv'
path_B = datasets_dir + '/' + 'zomato_data.csv'


# In[39]:

A = em.read_csv_metadata(path_A, key='ID')
B = em.read_csv_metadata(path_B, key='ID')


# In[ ]:




# In[41]:

ab = em.AttrEquivalenceBlocker()


# In[ ]:




# In[50]:

C1 = ab.block_tables(A, B, 
                    l_block_attr='zipcode', r_block_attr='zipcode', 
                    l_output_attrs=['name', 'city', 'zipcode', 'review_count', 'latitude', 'longitude', 'rating', 'address', 'zomato_id', 'yelp_id'],
                    r_output_attrs=['name', 'city', 'zipcode','review_count', 'latitude', 'longitude', 'rating', 'address', 'zomato_id', 'yelp_id'],
                    l_output_prefix='l_', r_output_prefix='r_')


# In[51]:

len(C1)


# In[52]:

C1.to_csv('c.csv')


# In[53]:

C1.head()


# In[ ]:




# In[54]:

block_f = em.get_features_for_blocking(A, B)


# In[ ]:




# In[55]:

block_f


# In[ ]:




# In[56]:

rb = em.RuleBasedBlocker()
rb.add_rule(['name_name_lev_sim(ltuple, rtuple) < 0.4'], block_f)


# In[ ]:




# In[ ]:




# In[ ]:




# In[57]:

D = rb.block_candset(C1, show_progress=False)


# In[58]:

D.to_csv('D.csv')


# In[ ]:




# In[59]:

len(D)


# In[60]:

S = em.sample_table(D, 600)


# In[61]:

S


# In[ ]:




# In[ ]:




# In[62]:

D


# In[63]:

S.to_csv('S.csv')


# In[64]:

#G = em.label_table(S, 'label')


# In[65]:


#G.head()


# In[66]:


len(S)


# In[67]:

path_labeled_data = datasets_dir + '/' + 'labeled.csv'


# In[ ]:




# In[68]:

G = em.read_csv_metadata(path_labeled_data, key='_id', 
                         fk_ltable='l_ID', fk_rtable='r_ID',
                         ltable=A, rtable=B)


# In[ ]:




# In[69]:

G.head()


# In[90]:

train_test = em.split_train_test(G, train_proportion=0.5)
I = train_test['train']
J = train_test['test']


# In[91]:

I.to_csv('I.csv')
J.to_csv('J.csv')


# In[ ]:




# In[92]:

match_f = em.get_features_for_matching(A, B)


# In[93]:

match_f.feature_name


# In[94]:

H = em.extract_feature_vecs(I, 
                            feature_table=match_f, 
                            attrs_after='label',
                            show_progress=False)  


# In[95]:

I.head()


# In[96]:

#matcher
dt = em.DTMatcher(name='DecisionTree', random_state=0)
svm = em.SVMMatcher(name='SVM', random_state=0)
rf = em.RFMatcher(name='RF', random_state=0)
lg = em.LogRegMatcher(name='LogReg', random_state=0)
ln = em.LinRegMatcher(name='LinReg')
nb = em.NBMatcher(name='Naive Bayes')

result_recall = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
        k=5,
        target_attr='label', metric='recall', random_state=0)

result_recall['cv_stats']




# In[ ]:




# In[97]:

result_precision = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
        k=5,
        target_attr='label', metric='precision', random_state=0)

result_precision['cv_stats']


# In[98]:

result_f1 = em.select_matcher([dt, rf, svm, ln, lg, nb], table=H, 
        exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
        k=5,
        target_attr='label', metric='f1', random_state=0)

result_f1['cv_stats']


# In[99]:

L = em.extract_feature_vecs(J, 
                            feature_table=match_f, 
                            attrs_after='label',
                            show_progress=False)  


# In[100]:

L.head()


# In[104]:

rf.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')


# In[105]:

#NOW apply the best ML model to test set L


predictions = rf.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)



# In[106]:

eval_result = em.eval_matches(predictions, 'label', 'predicted')
em.print_eval_summary(eval_result)


# In[ ]:




# In[107]:

lg.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')


# In[108]:

predictions_lg = lg.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)


# In[109]:

eval_result2 = em.eval_matches(predictions_lg, 'label', 'predicted')
em.print_eval_summary(eval_result2)


# In[ ]:




# In[110]:

dt.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')
predictions_dt = dt.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)

eval_result_dt = em.eval_matches(predictions_dt, 'label', 'predicted')
em.print_eval_summary(eval_result_dt)


# In[ ]:




# In[111]:

svm.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')
predictions_svm = svm.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)

eval_result_svm = em.eval_matches(predictions_dt, 'label', 'predicted')
em.print_eval_summary(eval_result_svm)


# In[ ]:




# In[112]:

ln.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')
predictions_ln = ln.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)

eval_result_ln = em.eval_matches(predictions_ln, 'label', 'predicted')
em.print_eval_summary(eval_result_ln)


# In[ ]:




# In[113]:

nb.fit(table=H, 
      exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'],
       target_attr='label')
predictions_nb = nb.predict(table=L, exclude_attrs=['_id', 'l_ID', 'r_ID', 'label'], 
              append=True, target_attr='predicted', inplace=False)

eval_result_nb = em.eval_matches(predictions_nb, 'label', 'predicted')
em.print_eval_summary(eval_result_nb)


# In[ ]:



