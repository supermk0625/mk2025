import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px

# Streamlit 앱 제목
st.title('기후 데이터 분석')

# 데이터 로드
@st.cache_data
def load_data():
    try:
        data = pd.read_csv('daily_temp.csv')
        return data
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None

data = load_data()

if data is not None:
    # 데이터 통계 정보
    st.write("### 데이터 통계정보")
    st.write(data.describe())

    # 날짜 데이터를 datetime 형식으로 변환
    if 'date' in data.columns:
        try:
            data['date'] = pd.to_datetime(data['date'])
            data = data.sort_values(by='date')
        except Exception as e:
            st.error(f"Error processing date column: {e}")

    # 사용자 선택: 시각화 및 분석
    st.subheader('Data Visualization and Analysis')

    # 날짜 범위 선택 슬라이더
    if 'date' in data.columns:
        min_date = data['date'].min()
        max_date = data['date'].max()

        selected_range = st.slider(
            "Select date range:",
            min_value=min_date, 
            max_value=max_date, 
            value=(min_date, max_date)
        )

        filtered_data = data[(data['date'] >= selected_range[0]) & (data['date'] <= selected_range[1])]
        st.write(f"### Filtered Data ({selected_range[0]} to {selected_range[1]}):")
        st.dataframe(filtered_data)

        # 시각화: 시간에 따른 온도 변화
        if 'temperature' in data.columns:
            st.write("### Temperature Over Time:")
            plt.figure(figsize=(10, 5))
            plt.plot(filtered_data['date'], filtered_data['temperature'], marker='o', linestyle='-', color='blue')
            plt.title('Temperature Over Time')
            plt.xlabel('Date')
            plt.ylabel('Temperature')
            plt.grid(True)
            st.pyplot(plt)

    # 특정 열의 히스토그램
    if 'temperature' in data.columns:
        st.write("### Temperature Distribution:")
        plt.figure(figsize=(8, 5))
        plt.hist(data['temperature'], bins=20, color='skyblue', edgecolor='black')
        plt.title('Temperature Distribution')
        plt.xlabel('Temperature')
        plt.ylabel('Frequency')
        st.pyplot(plt)

    # 사용자 입력에 따른 필터링
    st.subheader('Custom Filter Options')
    if 'temperature' in data.columns:
        temp_min = data['temperature'].min()
        temp_max = data['temperature'].max()

        temp_range = st.slider(
            "Select temperature range:", 
            min_value=float(temp_min), 
            max_value=float(temp_max), 
            value=(float(temp_min), float(temp_max))
        )

        temp_filtered_data = data[(data['temperature'] >= temp_range[0]) & (data['temperature'] <= temp_range[1])]
        st.write(f"### Data for Temperatures Between {temp_range[0]} and {temp_range[1]}:")
        st.dataframe(temp_filtered_data)

else:
    st.error("Data could not be loaded. Please check the file path or data format.")

    
