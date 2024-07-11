import streamlit as st
import pandas as pd
import io
import openpyxl


st.title("Excel 파일 합치기 챗봇")

# Function to combine multiple Excel files
def combine_excels(files):
    combined_df = pd.DataFrame()
    for file in files:
        df = pd.read_excel(file)
        combined_df = pd.concat([combined_df, df], ignore_index=True)
    return combined_df

# Upload multiple files
uploaded_files = st.file_uploader("여러 Excel 파일을 업로드하세요", accept_multiple_files=True, type=["xlsx", "xls"])

if uploaded_files:
    st.write("업로드된 파일:")
    for file in uploaded_files:
        st.write(file.name)
    
    # Combine the uploaded Excel files
    combined_df = combine_excels(uploaded_files)
    
    st.write("합쳐진 데이터:")
    st.dataframe(combined_df)
    
    # Provide a download button for the combined Excel file
    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='xlsxwriter') as writer:
        combined_df.to_excel(writer, index=False, sheet_name='Sheet1')
    processed_data = output.getvalue()
    
    st.download_button(
        label="합쳐진 Excel 파일 다운로드",
        data=processed_data,
        file_name="combined.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
