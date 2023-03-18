import streamlit as st
import pickle
import numpy as np
import datetime

st.title('Room Price Prediction')

st.header('INPUT')

attribute_values = []

col1, col2, col3, col4 = st.columns(4)
with col1:
    # "Phòng cho thuê": 0, "Căn hộ": 1, "Ký túc xá": 2, "Phòng ở ghép": 3, "Nhà nguyên căn": 4
    option = st.selectbox('Loại phòng', ('Phòng cho thuê', 'Căn hộ', 'Ký túc xá', 'Phòng ở ghép', 'Nhà nguyên căn'))
    if option == 'Phòng cho thuê':
        option = 0
    elif option == 'Căn hộ':
        option = 1
    elif option == 'Ký túc xá':
        option = 2
    elif option == 'Phòng ở ghép':
        option = 3
    else:
        option = 4
    attribute_values.append(option)
with col2:
    date = st.date_input('Ngày đăng', datetime.date(2023, 2, 2))
    # attribute_values.append(date)
with col3:
    number = st.number_input('Diện tích (m^2)', step=10)
    attribute_values.append(number)
with col4:
    number = st.number_input('Sức chứa (người)', step=1)
    attribute_values.append(number)

col5, col6, col7, col8 = st.columns(4)
with col5:
    number = st.number_input('Điện (đồng/số)', step=1000)
    attribute_values.append(number)
with col6:
    number = st.number_input('Nước (đồng/người)', step=20000)
    attribute_values.append(number)
with col7:
    choice = st.select_slider('Máy lạnh', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col8:
    choice = st.select_slider('WC riêng', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
    
col9, col10, col11, col12 = st.columns(4)
with col9:
    choice = st.select_slider('Chỗ để xe', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col10:
    choice = st.select_slider('Wifi', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col11:
    choice = st.select_slider('Tự do', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col12:
    choice = st.select_slider('Không chung chủ', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)

col13, col14, col15, col16 = st.columns(4)
with col13:
    choice = st.select_slider('Tủ lạnh', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col14:
    choice = st.select_slider('Máy giặt', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col15:
    choice = st.select_slider('Bảo vệ', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col16:
    choice = st.select_slider('Giường ngủ', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)

col17, col18, col19, col20 = st.columns(4)
with col17:
    choice = st.select_slider('Nấu ăn', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col18:
    choice = st.select_slider('Tivi', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col19:
    choice = st.select_slider('Thú cưng', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col20:
    choice = st.select_slider('Tủ quần áo', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)

col21, col22, col23, col24 = st.columns(4)
with col21:
    choice = st.select_slider('Của sổ', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col22:
    choice = st.select_slider('Máy nước nóng', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col23:
    choice = st.select_slider('Gác lửng', options=['Không', 'Có'], value='Có')
    if choice == 'Có':
        attribute_values.append(1)
    else:
        attribute_values.append(0)
with col24:
    city = st.selectbox('Thành phố', ('Hà Nội', 'Hồ Chí Minh'))
    
col25, col26, col27, col28 = st.columns(4)
with col25:
    if city == 'Hà Nội':
        district = st.selectbox('Quận', ('Quận Cầu Giấy', 'Quận Đống Đa', 'Quận Bắc Từ Liêm',
        'Quận Hai Bà Trưng', 'Quận Hoàng Mai', 'Quận Nam Từ Liêm',
        'Quận Thanh Xuân', 'Quận Hoàn Kiếm', 'Huyện Hoài Đức',
        'Quận Ba Đình', 'Quận Hà Đông', 'Quận Tây Hồ', 'Huyện Gia Lâm',
        'Huyện Thanh Trì', 'Huyện Đan Phượng', 'Quận Long Biên',
        'Huyện Đông Anh', 'Huyện Sóc Sơn'))
    else:
        district = st.selectbox('Quận', ('Quận 1', 'Quận Tân Bình',
        'Quận 7', 'Quận 3', 'Quận Bình Thạnh', 'Quận Thủ Đức', 'Quận 10',
        'Quận 8', 'Quận 4', 'Quận Tân Phú', 'Quận Phú Nhuận',
        'Quận Gò Vấp', 'Quận 5', 'Quận Bình Tân', 'Huyện Bình Chánh',
        'Quận 9', 'Quận 2', 'Quận 11', 'Quận 12', 'Huyện Nhà Bè', 'Quận 6',
        'Huyện Hóc Môn', 'Huyện Củ Chi'))

    district_mapping = {'Quận Cầu Giấy': 0, 'Quận Đống Đa': 1, 'Quận Bắc Từ Liêm': 2,
       'Quận Hai Bà Trưng': 3, 'Quận Hoàng Mai': 4, 'Quận Nam Từ Liêm': 5,
       'Quận Thanh Xuân': 6, 'Quận Hoàn Kiếm': 7, 'Huyện Hoài Đức': 8,
       'Quận Ba Đình': 9, 'Quận Hà Đông': 10, 'Quận Tây Hồ': 11, 'Huyện Gia Lâm': 12,
       'Huyện Thanh Trì': 13, 'Huyện Đan Phượng': 14, 'Quận Long Biên': 15,
       'Huyện Đông Anh': 16, 'Huyện Sóc Sơn': 17, 'Quận 1': 18, 'Quận Tân Bình': 19,
       'Quận 7': 20, 'Quận 3': 21, 'Quận Bình Thạnh': 22, 'Quận Thủ Đức': 23, 'Quận 10': 24,
       'Quận 8': 25, 'Quận 4': 26, 'Quận Tân Phú': 27, 'Quận Phú Nhuận': 28,
       'Quận Gò Vấp': 29, 'Quận 5': 30, 'Quận Bình Tân': 31, 'Huyện Bình Chánh': 32,
       'Quận 9': 33, 'Quận 2': 34, 'Quận 11': 35, 'Quận 12': 36, 'Huyện Nhà Bè': 37, 'Quận 6': 38,
       'Huyện Hóc Môn': 39, 'Huyện Củ Chi': 40}
    attribute_values.append(district_mapping[district])

with col26:
    option = st.selectbox('Giới tính', ('Cả nam và nữ', 'Nam', 'Nữ'),)
    if option == 'Nam':
        attribute_values.append(1)
        attribute_values.append(0)
    elif option == 'Nữ':
        attribute_values.append(0)
        attribute_values.append(1)
    else:
        attribute_values.append(1)
        attribute_values.append(1)

attribute_values.append(date.month)
attribute_values.append(date.year)

district_HN = ['Quận Cầu Giấy', 'Quận Đống Đa', 'Quận Bắc Từ Liêm',
       'Quận Hai Bà Trưng', 'Quận Hoàng Mai', 'Quận Nam Từ Liêm',
       'Quận Thanh Xuân', 'Quận Hoàn Kiếm', 'Huyện Hoài Đức',
       'Quận Ba Đình', 'Quận Hà Đông', 'Quận Tây Hồ', 'Huyện Gia Lâm',
       'Huyện Thanh Trì', 'Huyện Đan Phượng', 'Quận Long Biên',
       'Huyện Đông Anh', 'Huyện Sóc Sơn']

if district in district_HN:
    attribute_values.append(0)
else:
    attribute_values.append(1)

# st.write(attribute_values)

st.header('OUTPUT')

CatBoost_model = pickle.load(open('CatBoost_trained_model', 'rb'))
catboost_result = CatBoost_model.predict(np.array(attribute_values).reshape(1,-1))

st.success(catboost_result)
