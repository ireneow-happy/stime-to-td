import pandas as pd
import numpy as np
import streamlit as st
import io

def convert_to_touchdown_map(file, sheet_name="st_time"):
    df = pd.read_excel(file, sheet_name=sheet_name, header=None)
    df_with_coords = df.copy()
    die_region = df_with_coords.iloc[1:, 1:]
    die_region_dt = die_region.applymap(pd.to_datetime, errors='coerce')
    die_region_dt_sec = die_region_dt.applymap(lambda x: x.replace(microsecond=0) if pd.notnull(x) else x)
    timestamp_counts = pd.Series(die_region_dt_sec.values.ravel()).dropna().value_counts().sort_index()
    valid_touchdown_times = timestamp_counts[timestamp_counts > 1].index
    time_to_valid_td = {time: idx + 1 for idx, time in enumerate(valid_touchdown_times)}
    df_with_coords.iloc[1:, 1:] = die_region_dt_sec.applymap(lambda x: time_to_valid_td.get(x) if x in time_to_valid_td else np.nan)
    return df_with_coords

# Streamlit App
st.set_page_config(page_title="Touch Down Map 轉換工具", layout="centered")

# Language Selection
language = st.sidebar.selectbox("Select Language / 選擇語言 / 언어 선택", ["中文", "English", "한국어"])

# Multilingual Text
text = {
    "中文": {
        "title": "📊 Touch Down Map 轉換工具",
        "description": "這是一個線上工具，可將晶片測試 st_time map，轉換為 Touch Down order map, 方便進行Touch Down分析。",
        "upload_label": "📁 上傳 Excel 檔案",
        "success": "✅ 轉換完成！請下載結果：",
        "download": "📥 下載 Touch Down map",
        "error": "❌ 發生錯誤："
    },
    "English": {
        "title": "📊 Touch Down Map Converter",
        "description": "This is an online tool that converts wafer test st_time maps into Touch Down order maps for easier Touch Down analysis.",
        "upload_label": "📁 Upload Excel File",
        "success": "✅ Conversion completed! Please download the result:",
        "download": "📥 Download Touch Down map",
        "error": "❌ Error occurred: "
    },
    "한국어": {
        "title": "📊 터치다운 맵 변환 도구",
        "description": "이 도구는 칩 테스트 st_time 맵을 터치다운 순서 맵으로 변환하여 터치다운 분석을 쉽게 합니다.",
        "upload_label": "📁 엑셀 파일 업로드",
        "success": "✅ 변환 완료! 결과를 다운로드하세요:",
        "download": "📥 터치다운 맵 다운로드",
        "error": "❌ 오류 발생: "
    }
}

st.title(text[language]["title"])
st.markdown(text[language]["description"])

uploaded_file = st.file_uploader(text[language]["upload_label"], type=["xlsx"])
if uploaded_file is not None:
    try:
        result_df = convert_to_touchdown_map(uploaded_file)
        buffer = io.BytesIO()
        with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:
            result_df.to_excel(writer, index=False, header=False)
        st.success(text[language]["success"])
        st.download_button(
            label=text[language]["download"],
            data=buffer.getvalue(),
            file_name="touchdown_converted.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
    except Exception as e:
        st.error(f"{text[language]['error']}{e}")

st.markdown("---")
st.markdown("Made by **Irene** for QB00 use. © 2025")
