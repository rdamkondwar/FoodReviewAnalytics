from sklearn import metrics
from sklearn.ensemble import RandomForestClassifier
from sklearn import svm
from sklearn import tree
from sklearn.linear_model import LinearRegression
from sklearn import linear_model
import numpy as np

##########TRAINING SET###########
infile = "trainset.csv"
z = np.loadtxt(infile, delimiter=",")
x = z[:,0:16]
y  = z[:,16]

##########TEST SET ###############
myfile = "testset.csv"
c = np.loadtxt(myfile, delimiter=",")
a = c[:,0:16]
b  = c[:,16]

#######TRAINING RESULTS######
m = -2000
n = 700
##################
print "RANDOM FOREST"
clssf1 = RandomForestClassifier(n_estimators=20)
clssf1.fit(x[m:], y[m:])
clssf1.predict(x[:n])
expected = y[:n]
predicted1 = clssf1.predict(x[:n])
predicted1
print(metrics.classification_report(expected, predicted1,digits=5))
clssf1.predict(a)
expected_test = b
predicted_test1 = clssf1.predict(a)
print(metrics.classification_report(expected_test, predicted_test1,digits=5))
################
print "SVM"
clssf2 = svm.SVC(kernel = 'linear')
clssf2.fit(x[m:], y[m:])
clssf2.predict(x[:n])
expected = y[:n]
predicted2 = clssf2.predict(x[:n])
predicted2
print(metrics.classification_report(expected, predicted2,digits=5))
clssf2.predict(a)
expected_test = b
predicted_test2 = clssf2.predict(a)
print(metrics.classification_report(expected_test, predicted_test2,digits=5))
#################
print "DECISION TREE"
clssf3 = tree.DecisionTreeClassifier() 
clssf3.fit(x[m:], y[m:])
clssf3.predict(x[:n])
expected = y[:n]
predicted3 = clssf3.predict(x[:n])
predicted3
print(metrics.classification_report(expected, predicted3,digits=5))
clssf3.predict(a)
expected_test = b
predicted_test3 = clssf3.predict(a)
print(metrics.classification_report(expected_test, predicted_test3,digits=5))
################
print "LINEAR REGRESSION"
clssf4 = LinearRegression()
clssf4.fit(x[m:], y[m:])
clssf4.predict(x[:n])
expected = y[:n]
predicted4 = clssf4.predict(x[:n])
predicted4
final_predicted = [ 1 if aa > 0.5 else 0 for aa in predicted4 ]
final_expected = [ 1 if aa > 0.5 else 0 for aa in expected ]
print(metrics.classification_report(final_expected, final_predicted,digits=5))
clssf4.predict(a)
expected_test = b
predicted_test4 = clssf4.predict(a)
final_predicted4 = [ 1 if aa > 0.5 else 0 for aa in predicted_test4 ]
final_expected = [ 1 if aa > 0.5 else 0 for aa in expected_test ]
print(metrics.classification_report(final_expected, final_predicted4,digits=5))
################
print "LOGISTIC REGRESSION"
clssf5 = linear_model.LogisticRegression(C=1e5)
clssf5.fit(x[m:], y[m:])
clssf5.predict(x[:n])
expected = y[:n]
predicted5 = clssf5.predict(x[:n])
predicted5
print(metrics.classification_report(expected, predicted5,digits=5))
clssf5.predict(a)
expected_test = b
predicted_test5 = clssf5.predict(a)
print(metrics.classification_report(expected_test, predicted_test5,digits=5))
################
