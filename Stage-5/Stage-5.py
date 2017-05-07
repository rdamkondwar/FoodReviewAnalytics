
# coding: utf-8

# In[393]:

from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np
import pandas as pd


# In[394]:

infile = "/Users/rohitsd/Desktop/Stage-5/E2.csv"


# In[395]:

df = pd.read_csv(infile)


# In[396]:

df


# In[397]:

len(df)


# In[398]:

train_len = 600
tune_len = 110
test_len = 600


# In[399]:

#id_col = df.ix[:,0:1]
x = df.iloc[:,[8,11,12,13,14,15]]
y= df.ix[:,16]


# In[ ]:




# In[400]:

x


# In[ ]:




# In[ ]:




# In[421]:

print "RANDOM FOREST"
clssf1 = RandomForestClassifier(n_estimators=30)
clssf1.fit(x[:train_len], y[:train_len])
predicted1 = clssf1.predict(x[train_len+tune_len:])
expected1=y[train_len+tune_len:]
print(metrics.classification_report(expected1, predicted1,digits=5))


# In[402]:

#LinearRegression()
print "Linear Regression"
clssf2 = LinearRegression()
clssf2.fit(x[train_len:], y[train_len:])
predicted2 = clssf2.predict(x[train_len+tune_len:])
expected2=y[train_len+tune_len:]

#print predicted2
final_predicted2 = [ int(round(aa)) for aa in predicted2 ]
final_expected2 = [ int(round(aa)) for aa in expected2 ]
print(metrics.classification_report(final_expected2, final_predicted2,digits=5))


# In[412]:

#LinearRegression()
print "LOGISTIC REGRESSION"
clssf3 = linear_model.LogisticRegression(C=1e5)
clssf3.fit(x[:train_len], y[:train_len])
predicted3 = clssf3.predict(x[train_len:(train_len + tune_len)])
expected3=y[train_len:(train_len + tune_len)]
print(metrics.classification_report(expected3, predicted3,digits=5))


# In[404]:

print "DECISION TREE"
clssf4 = tree.DecisionTreeClassifier() 
clssf4.fit(x[:train_len], y[:train_len])
expected4 = y[train_len+tune_len:]
predicted4 = clssf4.predict(x[train_len+tune_len:])
print(metrics.classification_report(expected4, predicted4,digits=5))


# In[405]:

print "SVM"
clssf5 = svm.SVC(kernel = 'linear')
clssf5.fit(x[:train_len], y[:train_len])
expected5 = y[train_len+tune_len:]
predicted5 = clssf5.predict(x[train_len+tune_len:])
print(metrics.classification_report(expected5, predicted5,digits=5))


# In[422]:

print "Running Trained Models..."

print "Random Forest"
predicted1 = clssf1.predict(x[train_len+tune_len:])
expected1=y[train_len+tune_len:]
print(metrics.classification_report(expected1, predicted1,digits=5))

print "Linear Regression"
predicted2 = clssf2.predict(x[train_len+tune_len:])
expected2=y[train_len+tune_len:]
#print predicted2
final_predicted2 = [ int(round(aa)) for aa in predicted2 ]
final_expected2 = [ int(round(aa)) for aa in expected2 ]
print(metrics.classification_report(final_expected2, final_predicted2,digits=5))

print "LOGISTIC REGRESSION"
predicted3 = clssf3.predict(x[train_len:])
expected3=y[train_len:]
print(metrics.classification_report(expected3, predicted3,digits=5))

print "DECISION TREE"
expected4 = y[train_len:]
predicted4 = clssf4.predict(x[train_len:])
print(metrics.classification_report(expected4, predicted4,digits=5))

print "SVM"
expected5 = y[train_len:]
predicted5 = clssf5.predict(x[train_len:])
print(metrics.classification_report(expected5, predicted5,digits=5))

