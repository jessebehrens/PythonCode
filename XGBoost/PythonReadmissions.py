#Uses the data located here: https://github.com/jessebehrens/SASExamples/tree/master/Viya/Programming/IntegratedPlatform/Data
#Import Packages
import numpy as np
import pandas as pd
import xgboost as xgb
from sklearn import preprocessing
from sklearn.metrics import accuracy_score
from sklearn.model_selection import train_test_split

#Read in the training dataset and drop variables that we will not model with
ABT=pd.read_csv('/sasdata/data/readmissions_raw.csv')

#Create a dataset with only our predictors 
ABT=ABT.drop(
    ['address','CITY','STATE','Postcode','Email','City_Lat', 'City_Long','Hospital_LONG',
     'Hospital_LAT','Hospital_Address','Hospital_ID','Hospital_Name','Phone', 'Patient_LON',
     'Patient_LAT', 'Admit_Date','Hospital_City', 'Hospital_State', 'Hospital_Zip_Code',
     'Hospital_Region','Hospital_County_Name','NPI','Discharge_Notes','Patient_Number',
     'PatientID'], axis=1)

#Create 0/1 values for our binary inputs
Binary=['Patient_Gender','Urban_Class','Marital_Status','Repeat_Care_Gap_Offenders',
             'High_NA_ast_Discharge']
Encoding = preprocessing.LabelEncoder()
for variable in Binary:
    ABT[variable]=Encoding.fit_transform(ABT[variable])

#Create onehot encoded variables
one_hot_diagnosis = pd.get_dummies(ABT['diagnosis'])
one_hot_contact=pd.get_dummies(ABT['Contact_Preference'])

#Merge the onehot encoded variables back in
ABT=ABT.join(one_hot_diagnosis)
ABT=ABT.join(one_hot_contact)

#Create a input dataset and a label dataset
y = pd.DataFrame(ABT['DV_Readmit_Flag'])
X =ABT.drop(['diagnosis','Contact_Preference','DV_Readmit_Flag'],axis=1)

#Split the input dataset into train and test
X_train, X_test, y_train, y_test=train_test_split(X, y, test_size=0.15, random_state=1985)

#Prep the data for input into XGBClassifier
X_train=X_train.values
y_train=y_train.values.ravel()

#Build the XGBoost Model
gbm = xgb.XGBClassifier(max_depth=3, n_estimators=300, learning_rate=0.01).fit(X_train, y_train)

#Run prediction on our test dataset
y_pred=gbm.predict(X_test.values)

#Look at misclassification
accuracy_score(y_test, y_pred)
