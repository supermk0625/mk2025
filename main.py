import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import koreanize_matplotlib
import plotly.express as px

# 제목 설정
st.title("연도별 최고 및 최저 기온 시각화")

# 데이터 읽기
data_path = 'daily_temp.csv'
try:
    data = pd.read_csv(data_path)
except FileNotFoundError:
    st.error(f"파일을 찾을 수 없습니다: {data_path}")
    st.stop()

# 데이터 확인
data['날짜'] = pd.to_datetime(data['날짜'], errors='coerce')
if data['날짜'].isnull().any():
    st.error("날짜 형식이 잘못되었습니다. '날짜' 열에 올바른 날짜 형식이 포함되어야 합니다.")
    st.stop()

# 연도 추출 및 그룹화
data['year'] = data['날짜'].dt.year
if '기온' not in data.columns:
    st.error("'기온' 열이 데이터에 포함되어 있어야 합니다.")
    st.stop()

# 연도별 최고기온 및 최저기온 계산
annual_stats = data.groupby('year')['기온'].agg(['max', 'min']).reset_index()
annual_stats.rename(columns={'max': 'max_temp', 'min': 'min_temp'}, inplace=True)

# 그래프 생성
fig, ax = plt.subplots(figsize=(10, 6))
ax.plot(annual_stats['year'], annual_stats['max_temp'], label='최고 기온', color='red', marker='o')
ax.plot(annual_stats['year'], annual_stats['min_temp'], label='최저 기온', color='blue', marker='o')

# 그래프 꾸미기
ax.set_title('연도별 최고 및 최저 기온', fontsize=16)
ax.set_xlabel('연도', fontsize=12)
ax.set_ylabel('기온 (°C)', fontsize=12)
ax.legend()
ax.grid(True, linestyle='--', alpha=0.7)

# 그래프 출력
st.pyplot(fig)

