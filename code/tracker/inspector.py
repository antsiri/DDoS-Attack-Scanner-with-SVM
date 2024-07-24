import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import confusion_matrix, classification_report
import joblib
import warning

filename = './ml/model.sav'
classifier = joblib.load(filename)
dt_realtime = pd.read_csv('rt_data.csv')
dt_realtime.fillna(0, inplace=True)
result = classifier.predict(dt_realtime)

with open('.result', 'w') as f:
    f.write(str(result[0]))
