import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# CSV 파일 경로
FILE_PATH = 'daily_temp.csv'

# Streamlit 앱 제목
st.title('Daily Temperature Analysis')

# CSV 파일 읽기
@st.cache_data
def load_data():
    try:
        # CSV 파일을 읽어들임
        data = pd.read_csv(FILE_PATH)
        # 날짜 형식이 있다면 파싱하여 datetime 형식으로 변경
        data['Date'] = pd.to_datetime(data['Date'])
        return data
    except Exception as e:
        st.error(f"파일을 읽는 데 오류가 발생했습니다: {e}")
        return None

# 데이터 로드
data = load_data()

# 데이터가 잘 로드되었으면
if data is not None:
    # 데이터 보기
    st.subheader('데이터 미리보기')
    st.write(data.head())

    # 기온 통계 정보
    st.subheader('기온 통계')
    st.write(data['Temperature'].describe())

    # 기온 변화 시각화
    st.subheader('기온 변화 그래프')
    fig, ax = plt.subplots()
    ax.plot(data['Date'], data['Temperature'], label='Temperature')
    ax.set_xlabel('Date')
    ax.set_ylabel('Temperature')
    ax.set_title('Daily Temperature Over Time')
    plt.xticks(rotation=45)
    st.pyplot(fig)

    # 월별 평균 기온
    st.subheader('월별 평균 기온')
    data['Month'] = data['Date'].dt.month
    monthly_avg_temp = data.groupby('Month')['Temperature'].mean()
    st.write(monthly_avg_temp)

    # 월별 평균 기온 시각화
    fig2, ax2 = plt.subplots()
    monthly_avg_temp.plot(kind='bar', ax=ax2)
    ax2.set_xlabel('Month')
    ax2.set_ylabel('Average Temperature')
    ax2.set_title('Average Temperature by Month')
    st.pyplot(fig2)

# 예외 처리: 데이터가 없을 경우
else:
    st.warning('데이터를 로드할 수 없습니다.')
