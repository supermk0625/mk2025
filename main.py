import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px

# Streamlit App Title
st.title("연도별 최고기온 분석")

# 파일 경로 지정 및 데이터 로드
file_path = 'daily_temp.csv'

# 데이터 로드
@st.cache_data
def load_data(file_path):
    try:
        data = pd.read_csv(file_path)
        return data
    except Exception as e:
        st.error(f"파일을 로드하는 동안 오류가 발생했습니다: {e}")
        return None

data = load_data(file_path)

# 데이터 유효성 검사
if data is not None:
    # 날짜 및 기온 컬럼 이름 설정 (예상되는 데이터 컬럼: 날짜, 최고기온(℃))
    if '날짜' not in data.columns or '최고기온(℃)' not in data.columns:
        st.error("데이터에 '날짜' 또는 '최고기온(℃)' 컬럼이 없습니다.")
    else:
        # 날짜 컬럼을 datetime 형식으로 변환
        data['날짜'] = pd.to_datetime(data['날짜'], errors='coerce')
        
        # 변환 실패한 날짜 제거
        data = data.dropna(subset=['날짜'])
        
        # 연도별 최고기온 계산
        data['Year'] = data['날짜'].dt.year
        yearly_max_temp = data.groupby('Year')['최고기온(℃)'].max()
        
        # 그래프 생성
        st.subheader("연도별 최고기온 그래프")
        fig, ax = plt.subplots()
        yearly_max_temp.plot(kind='line', marker='o', ax=ax)
        ax.set_title("연도별 최고기온")
        ax.set_xlabel("연도")
        ax.set_ylabel("기온 (°C)")
        plt.grid()
        
        # 그래프 출력
        st.pyplot(fig)
else:
    st.warning("데이터를 로드할 수 없습니다. 파일 경로를 확인해 주세요.")
