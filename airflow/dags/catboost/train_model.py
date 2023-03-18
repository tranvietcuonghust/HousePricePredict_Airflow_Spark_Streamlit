import pandas as pd
import numpy as np
from datetime import datetime 
import psycopg2 as pg
import pandas.io.sql as psql

connection = pg.connect("host=postgres dbname=airflow user=airflow password=airflow")
df = psql.read_sql('SELECT * FROM housedata;', connection)

dict = {'loai_phong':'Loai phong','ngay_dang':'Ngay dang','gia_phong':'Gia phong',
       'dien_tich':'Dien tich','suc_chua':'Suc chua', 'dien':'Dien','nuoc':'Nuoc','may_lanh':'May lanh',
       'wc_rieng':'WC rieng', 'cho_de_xe':'Cho de xe', 'wifi':'Wifi', 'tu_do':'Tu do', 'khong_chung_chu':'Khong chung chu', 'tu_lanh':'Tu lanh',
       'may_giat':'May giat', 'bao_ve':'Bao ve','giuong_ngu':'Giuong ngu','nau_an':'Nau an', 'tivi':'Tivi','thu_cung':'Thu cung',
       'tu_quan_ao':'Tu quan ao', 'cua_so':'Cua so', 'may_nuoc_nong':'May nuoc nong','gac_lung':'Gac lung','quan':'Quan','nam':'Nam','nu':'Nu'}
 
df.rename(columns=dict,
          inplace=True)

#df = pd.read_csv('/opt/spark/resources/data/cleaned_house_price_data.csv')

print(len(df))
print(df.columns)
features = ['Loai phong', 'Ngay dang',
       'Dien tich', 'Suc chua', 'Dien', 'Nuoc', 'May lanh',
       'WC rieng', 'Cho de xe', 'Wifi', 'Tu do', 'Khong chung chu', 'Tu lanh',
       'May giat', 'Bao ve', 'Giuong ngu', 'Nau an', 'Tivi', 'Thu cung',
       'Tu quan ao', 'Cua so', 'May nuoc nong', 'Gac lung', 'Quan', 'Nam', 'Nu']
target = 'Gia phong'
X = df[features]
y = df[target]

print(X['Loai phong'].unique())
roomtype_mapping = {"Phòng cho thuê": 0, "Căn hộ": 1, "Ký túc xá": 2, "Phòng ở ghép": 3, "Nhà nguyên căn": 4}
X['Loai phong'] = X['Loai phong'].map(roomtype_mapping)
X.head()

def month_year(X):
    month = []
    year = []
    for i in range(len(X)):
        # obj = datetime.strptime(str(X['Ngay dang'][i]), '%Y-%m-%d')
        obj=X['Ngay dang'][i]
        month.append(obj.month)
        year.append(obj.year)
    return month, year 

month, year = month_year(X)
X['Tháng'] = month
X['Năm'] = year
X = X.drop('Ngay dang', axis=1)
X.head()

# District encoding
from sklearn import preprocessing
le = preprocessing.LabelEncoder()
le.fit(X['Quan'])
arr = le.transform(X['Quan'])
X = X.drop('Quan', axis=1)
X['Quan'] = arr
X.head()

X['Quan'].unique()

# Drop difficult features
# X = X.drop('ĐIẠ CHỈ', axis=1)
# X.head()

from sklearn.model_selection import train_test_split

# SEED = 42 
# TEST_SIZE = 0.2
# X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=TEST_SIZE, stratify=y, random_state=SEED) 
# VAL_SIZE = 0.2
# X_train, X_valid, y_train, y_valid =  train_test_split(X_train, y_train, test_size=VAL_SIZE, stratify=y_train, random_state=SEED)  
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)
X_train, X_valid, y_train, y_valid = train_test_split(X_train, y_train, test_size=0.2)

from catboost import CatBoostRegressor
from sklearn.metrics import accuracy_score, classification_report
import warnings
warnings.filterwarnings('ignore')

# get data
# path = 'data/Invistico_Airline.csv'
# X_train, y_train, X_valid, y_valid, X_test, y_test = dp.data_prepare(path)

# model
CatBoost_model = CatBoostRegressor(
    iterations=50,
)

# train
CatBoost_model.fit(
    X_train, y_train,
    eval_set=(X_valid, y_valid),
    logging_level='Silent',
    plot=False
)

y_pred = CatBoost_model.predict(X_test)

print(y_pred)

from sklearn.metrics import mean_absolute_error
print("MAE",mean_absolute_error(y_test,y_pred))

import pickle
pickle.dump(CatBoost_model, open('CatBoost_trained_model', 'wb'))
