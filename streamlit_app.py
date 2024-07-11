import streamlit as st
import pandas as pd
import plotly.express as px
import io

# Function to combine multiple Excel files
def combine_excels(files):
    combined_df = pd.DataFrame()
    for file in files:
        try:
            df = pd.read_excel(file)
            combined_df = pd.concat([combined_df, df], ignore_index=True)
        except Exception as e:
            st.error(f"파일을 읽는 중 오류 발생: {file.name}. 오류: {e}")
    return combined_df

# Function to create a dashboard
def create_dashboard(df):
    required_columns = ['시작일정', '종료일정', '담당자', '금주 진행률(%)', '내용']
    
    if not all(col in df.columns for col in required_columns):
        missing_cols = [col for col in required_columns if col not in df.columns]
        st.error(f"필요한 컬럼이 누락되었습니다: {', '.join(missing_cols)}")
        return None
    
    df['시작일정'] = pd.to_datetime(df['시작일정'], errors='coerce')
    df['종료일정'] = pd.to_datetime(df['종료일정'], errors='coerce')
    
    try:
        df['금주 진행률(%)'] = df['금주 진행률(%)'].astype(float)
    except ValueError as e:
        st.error(f"'금주 진행률(%)' 컬럼의 데이터를 숫자로 변환하는 중 오류가 발생했습니다: {e}")
        return None
    
    # Convert '내용' column to strings explicitly
    df['내용'] = df['내용'].astype(str)
    
    # Adjust color scale to reflect progress up to 100%
    color_scale = px.colors.sequential.Viridis  # Example color scale; adjust as needed
    
    fig = px.timeline(df, x_start='시작일정', x_end='종료일정', y='내용', color='금주 진행률(%)',
                      color_continuous_scale=color_scale, title='진행률 대시보드', text='담당자',
                      range_color=(0, 100))  # Set color range from 0% to 100%
    fig.update_yaxes(categoryorder='total ascending')
    return fig

# Upload multiple files
uploaded_files = st.file_uploader("여러 Excel 파일을 업로드하세요", accept_multiple_files=True, type=['xlsx', 'xls'])

if uploaded_files:
    st.write("업로드된 파일:")
    for file in uploaded_files:
        st.write(file.name)
    
    # Combine the uploaded Excel files
    combined_df = combine_excels(uploaded_files)

    st.write("합쳐진 데이터:")
    st.dataframe(combined_df)
    
    # Create and display the dashboard
    st.write("진행률 대시보드:")
    dashboard = create_dashboard(combined_df)
    if dashboard:
        st.plotly_chart(dashboard)
    
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
