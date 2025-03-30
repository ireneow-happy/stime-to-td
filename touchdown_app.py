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

    output = io.BytesIO()
    df_with_coords.to_excel(output, index=False, header=False)
    output.seek(0)
    return output

# Streamlit UI
st.title("📊 Touch Down Map 轉換工具")
st.write("請上傳晶片 Excel 檔案，我會幫你轉換為 Touch Down map")

uploaded_file = st.file_uploader("📂 上傳 Excel 檔案", type=["xlsx"])

if uploaded_file:
    with st.spinner("⏳ 正在處理中..."):
        try:
            result_file = convert_to_touchdown_map(uploaded_file)
            st.success("✅ 轉換完成！請下載結果：")
            st.download_button(
                label="📥 下載 Touch Down map",
                data=result_file,
                file_name="touchdown_output.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )
        except Exception as e:
            st.error(f"❌ 發生錯誤：{e}")
