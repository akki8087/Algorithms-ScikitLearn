# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 19:21:05 2018

@author: NP
"""

# -*- coding: utf-8 -*-
"""
Created on Fri Jun  8 19:19:02 2018

@author: NP
"""

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 22 23:41:52 2018

@author: NP
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# reading data in pandas dataframe.
df_train = pd.read_csv("loantrain.csv")
df_test = pd.read_csv("loantest.csv")

#fill missing values.

df_train['Loan_Status'] = df_train['Loan_Status'].map(lambda x: 1 if x=='Y' else 0)
df_train['Credit_History'].fillna(df_train['Loan_Status'], inplace = True)
df_test = df_test.fillna({'Credit_History':1})

df = pd.concat([df_train,df_test])

df = df.fillna({'Dependents':0})
df = df.fillna({"Gender":'Male'})
df["LoanAmount"] = df["LoanAmount"].fillna(df.median()["LoanAmount"])
df = df.fillna({"Loan_Amount_Term":360})
df = df.fillna({"Married":"Yes"})
df = df.fillna({"Self_Employed":"No"})

# convert Dependentd '3+' to 3
df["Dependents"] = df.Dependents.apply(lambda x: int(str(x).replace("+", "")))

#Feature engineering

df["Total_income"] = df["ApplicantIncome"] + df["CoapplicantIncome"]
df['Loan_tot_income_ratio'] = (df['LoanAmount'] * 1000) / df['Total_income']
df['Per_month'] = df["Total_income"] - ( (df['LoanAmount'] * 1000) /df['Loan_Amount_Term'] )

df['coapplicant'] = 0
df['coapplicant'] = df['CoapplicantIncome'] > 0

#getting dummies of catagorical data.

cat_columns = ['Education', 'Gender', 'Married', 'Property_Area', 'Self_Employed','coapplicant']

df_d = pd.get_dummies(df,columns = cat_columns,drop_first = True)

dfr_train = df_d.dropna()
dfr_test = df_d[df_d.isnull().any(axis = 1)]
dfr_test = dfr_test.drop("Loan_Status",1)

col = ['Credit_History', 'Per_month','Dependents','LoanAmount', 'Loan_Amount_Term', 'Total_income', 'Education_Not Graduate', 'Gender_Male', 'Married_Yes',
       'Property_Area_Semiurban', 'Property_Area_Urban', 'Loan_tot_income_ratio','coapplicant_True']
X = dfr_train[col]
y = dfr_train['Loan_Status']

# SVM
from sklearn.linear_model import LogisticRegression
classifier = LogisticRegression(random_state = 0)
classifier.fit(X, y)

#validation
from sklearn.model_selection import cross_val_score
accuracies = cross_val_score(estimator = classifier, X = X,y = y,cv = 10)
print(accuracies.mean())
print(accuracies.std())
