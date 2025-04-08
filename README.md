# 📊 Touch Down Map Converter

This Streamlit app converts wafer test **st_time maps** into **Touch Down order maps** to help with Touch Down pattern analysis. It supports multilingual interface (中文 / English / 한국어).

---

## 🌟 Features

- Upload an Excel file with `st_time` values.
- Automatically detect valid Touch Down timestamps.
- Convert the map into numerical Touch Down order (1, 2, 3, ...).
- Download the processed map as an Excel file.
- Interface language options: Traditional Chinese, English, Korean.

---

## 🚀 How to Use

1. Run the app with:
   ```bash
   streamlit run touchdown_app.py
   ```

2. Upload an Excel file (`.xlsx`) with your `st_time` map (default sheet name: `st_time`).

3. Wait for conversion and download the new file showing Touch Down order.

---

## 📁 Input Format

- Excel file must have test timestamps starting from row 2 and column 2 (excluding headers).
- Timestamps should be convertible to datetime.

---

## 🧩 Example

Before:
```
Row\Col | A | B | C
--------|---|---|---
1       |   |   |
2       | 13:05:01 | 13:05:01 | 13:06:15
```

After:
```
Row\Col | A | B | C
--------|---|---|---
1       |   |   |
2       |   1   |   1   |   2
```

---

## 📦 Requirements

```txt
streamlit
pandas
numpy
xlsxwriter
openpyxl
```

---

## 👩‍💻 Developed by

Made by **Irene** for QB00 internal use.  
© 2025

