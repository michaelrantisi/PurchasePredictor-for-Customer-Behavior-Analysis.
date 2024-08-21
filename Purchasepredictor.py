# -*- coding: utf-8 -*-
"""project 3 and 4

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1guG_gEA-ubtTjAngCbrOjawkzv18H4ak
"""

import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC, LinearSVC
from sklearn.naive_bayes import GaussianNB
from sklearn.preprocessing import LabelEncoder
from sklearn.metrics import confusion_matrix
from sklearn.metrics import precision_score,recall_score,accuracy_score,f1_score
from sklearn.decomposition import PCA
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.feature_selection import RFE
from sklearn.model_selection import GridSearchCV
from sklearn.model_selection import KFold
from sklearn.metrics import classification_report

# Load the dataset
file_path = '/content/drive/MyDrive/Data.csv'
data = pd.read_csv(file_path)

# Display the first few rows of the dataset to understand its structure
data.head()

labelencoder=LabelEncoder()
data['Made_Purchase']=labelencoder.fit_transform(data['Made_Purchase'])
data['Month_SeasonalPurchase']=labelencoder.fit_transform(data['Month_SeasonalPurchase'])
data['CustomerType']=labelencoder.fit_transform(data['CustomerType'])
data['Cookies Setting']=labelencoder.fit_transform(data['Cookies Setting'])
data.head()

data=data.drop(['Education','Gender','Marital Status'],axis=1)
data.info()

data.groupby('Made_Purchase').agg(['mean','median'])

total=data.isna().sum().sort_values(ascending=False)
percent1=data.isna().sum()/data.isna().count()*100
percent2=(round(percent1,1)).sort_values(ascending=False)
missing_data=pd.concat([total,percent2],axis=1,keys=['Total missing values','%'])
missing_data

data = data.fillna(method='ffill')
data=data.dropna()
data.shape

data.groupby('Made_Purchase').agg(['mean','median'])

column = 'HomePage_Duration'

# Plot before outlier removal
plt.figure(figsize=(12, 6))
plt.subplot(1, 2, 1)
sns.boxplot(y=data[column])
plt.title('Before Outlier Removal')

q1=data.quantile(0.25)
q3=data.quantile(0.75)
IQR=q3-q1
print("The IQR of each column is \n",IQR)

data=data[~((data<(q1-1.5*IQR))|(data>(q3+1.5*IQR)))]
# Plot after outlier removal
plt.subplot(1, 2, 2)
sns.boxplot(y=data[column])
plt.title('After Outlier Removal')

plt.tight_layout()
plt.show()

data_Stand=data.drop(['Month_SeasonalPurchase','OS','SearchEngine','Zone','Type of Traffic','CustomerType','Cookies Setting','WeekendPurchase','Made_Purchase'],axis=1)
std_scaler=StandardScaler()
num_std=std_scaler.fit_transform(data_Stand)
num_std_df = pd.DataFrame(num_std, columns=data_Stand.columns)
num_std_df.head()

dataE=data[['Month_SeasonalPurchase','OS','SearchEngine','Zone','Type of Traffic','CustomerType','Cookies Setting','WeekendPurchase','Made_Purchase']]
data_fixed=pd.concat([num_std_df,dataE],axis=1)
data_fixed.head()

data_fixed.isna().sum()

data_fixed = data_fixed.fillna(method='ffill')
data_fixed=data_fixed.dropna()
data.shape

y=data_fixed['Made_Purchase']
x=data_fixed.drop('Made_Purchase',axis=1)
x_train,x_test,y_train,y_test=train_test_split(x,y,test_size=0.2,random_state=42)
fold=KFold(n_splits=5,shuffle=True,random_state=1)
rfe=RFE(estimator=RandomForestClassifier(),n_features_to_select=None)
params={'n_features_to_select':list(range(1,20))}
model_cv=GridSearchCV(estimator=rfe,param_grid=params,scoring='accuracy',verbose=1,cv=fold,return_train_score=True)
model_cv.fit(x_train,y_train)
best_params = model_cv.best_params_
print(best_params)

feature_ranking = model_cv.best_estimator_.ranking_
selected_feature_indices = feature_ranking == 1
print("Selected feature indices:",selected_feature_indices )

x.head

Y=data_fixed['Made_Purchase']
X = data_fixed.drop(['Made_Purchase', 'LandingPage', 'LandingPage_Duration', 'GoogleMetric:Page Values', 'SeasonalPurchase', 'SearchEngine', 'CustomerType'], axis=1)
X_train,X_test,Y_train,Y_test=train_test_split(X,Y,test_size=0.2,random_state=42)

random_forest=RandomForestClassifier(n_estimators=100,random_state=0)
random_forest.fit(X_train,Y_train)
y_predictions=random_forest.predict(X_train)
random_forest.score(X_train,Y_train)
acc_random_forest=round(random_forest.score(X_train,Y_train)*100,2)
print(acc_random_forest)
con=confusion_matrix(Y_train,y_predictions)
print(con)
print(classification_report(Y_train,y_predictions,digits=3))

y_predictions=random_forest.predict(X_test)
random_forest.score(X_test,Y_test)
acc_random_forest_test=round(random_forest.score(X_test,Y_test)*100,2)
print(acc_random_forest_test)
con=confusion_matrix(Y_test,y_predictions)
print(con)
print(classification_report(Y_test,y_predictions,digits=3))

gaussian=GaussianNB()
gaussian.fit(X_train,Y_train)
y_predictions=gaussian.predict(X_train)
gaussian.score(X_train,Y_train)
acc_gaussian=round(gaussian.score(X_train,Y_train)*100,2)
print(acc_gaussian)
con=confusion_matrix(Y_train,y_predictions)
print(con)
print(classification_report(Y_train,y_predictions,digits=3))

gaussian=GaussianNB()
gaussian.fit(X_test,Y_test)
y_predictions=gaussian.predict(X_test)
gaussian.score(X_test,Y_test)
acc_gaussian_test=round(gaussian.score(X_test,Y_test)*100,2)
print(acc_gaussian_test)
con=confusion_matrix(Y_test,y_predictions)
print(con)
print(classification_report(Y_test,y_predictions,digits=3))

logreg=LogisticRegression()
logreg.fit(X_train,Y_train)
y_predictions=logreg.predict(X_train)
logreg.score(X_train,Y_train)
acc_logreg=round(logreg.score(X_train,Y_train)*100,2)
print(acc_logreg)
con=confusion_matrix(Y_train,y_predictions)
print(con)
print(classification_report(Y_train,y_predictions,digits=3))

logreg=LogisticRegression()
logreg.fit(X_test,Y_test)
y_predictions=logreg.predict(X_test)
logreg.score(X_test,Y_test)
acc_logreg_test=round(logreg.score(X_test,Y_test)*100,2)
print(acc_logreg_test)
con=confusion_matrix(Y_test,y_predictions)
print(con)
print(classification_report(Y_test,y_predictions,digits=3))

decisiontree=DecisionTreeClassifier()
decisiontree.fit(X_train,Y_train)
y_predictions=decisiontree.predict(X_train)
decisiontree.score(X_train,Y_train)
acc_decisiontree=round(decisiontree.score(X_train,Y_train)*100,2)
print(acc_decisiontree)
con=confusion_matrix(Y_train,y_predictions)
print(con)
print(classification_report(Y_train,y_predictions,digits=3))

decisiontree=DecisionTreeClassifier()
decisiontree.fit(X_test,Y_test)
y_predictions=decisiontree.predict(X_test)
decisiontree.score(X_test,Y_test)
acc_decisiontree_test=round(decisiontree.score(X_test,Y_test)*100,2)
print(acc_decisiontree_test)
con=confusion_matrix(Y_test,y_predictions)
print(con)
print(classification_report(Y_test,y_predictions,digits=3))

svc=LinearSVC()
svc.fit(X_train,Y_train)
y_predictions=svc.predict(X_train)
svc.score(X_train,Y_train)
acc_svc=round(svc.score(X_train,Y_train)*100,2)
print(acc_svc)
con=confusion_matrix(Y_train,y_predictions)
print(con)
print(classification_report(Y_train,y_predictions,digits=3))

svc=LinearSVC()
svc.fit(X_test,Y_test)
y_predictions=svc.predict(X_test)
svc.score(X_test,Y_test)
acc_svc_test=round(svc.score(X_test,Y_test)*100,2)
print(acc_svc_test)
con=confusion_matrix(Y_test,y_predictions)
print(con)
print(classification_report(Y_test,y_predictions,digits=3))

svm_model = SVC(kernel='linear')
svm_model.fit(X_train, Y_train)
svm_predictions = svm_model.predict(X_test)
acc_svm_test = round(accuracy_score(Y_test, svm_predictions) * 100, 2)
print(f"SVM Test Accuracy: {acc_svm_test}%")
print(confusion_matrix(Y_test, svm_predictions))
print(classification_report(Y_test, svm_predictions, digits=3))

xgb_model = XGBClassifier(use_label_encoder=False, eval_metric='mlogloss')
xgb_model.fit(X_train, Y_train)
xgb_predictions = xgb_model.predict(X_test)
acc_xgb_test = round(accuracy_score(Y_test, xgb_predictions) * 100, 2)
print(f"XGBoost Test Accuracy: {acc_xgb_test}%")
print(confusion_matrix(Y_test, xgb_predictions))
print(classification_report(Y_test, xgb_predictions, digits=3))

results = pd.DataFrame({
    'Model': [
        'Random Forest',
        'Gaussian',
        'Logistic Regression',
        'Decision Tree',
        'LinearSVC',
        'SVM',
        'XGBoost'
    ],
    'Training Score': [
        acc_random_forest,
        acc_gaussian,
        acc_logreg,
        acc_decisiontree,
        acc_svc,
        acc_svm_test,
        acc_xgb_test
    ]
})

result_df = results.sort_values(by='Training Score', ascending=False)
result_df = result_df.set_index('Model')
result_df

results = pd.DataFrame({
    'Model': [
        'Random Forest',
        'Gaussian',
        'Logistic Regression',
        'Decision Tree',
        'LinearSVC',
        'SVM',
        'XGBoost'
    ],
    'Testing Score': [
        acc_random_forest_test,
        acc_gaussian_test,
        acc_logreg_test,
        acc_decisiontree_test,
        acc_svc_test,
        acc_svm_test,
        acc_xgb_test
    ]
})

result_df = results.sort_values(by='Testing Score', ascending=False)
result_df = result_df.set_index('Model')
result_df