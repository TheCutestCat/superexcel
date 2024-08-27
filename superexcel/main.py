import streamlit as st
import pandas as pd
from PromptsAndClasses.DynamicDataFormat import create_pydantic_class,DataExtractPrompt
from utils import openai_wrapper
from SearchResponse import extract_info_from_webpage,process_dataframe_parallel

@st.cache_data
def get_initial_data():
    # 示例数据
    data = {
        "Player": ["Pelé", "Diego Maradona", "Lionel Messi", "Cristiano Ronaldo"],
        "birth-date": [None,None,None,None],
        "height": [None,None,None,None],
        "nationality": [None,None,None,None],
        "club": [None,None,None,None],
        "position": [None,None,None,None],
    }
    df = pd.DataFrame(data)
    return df

# 示例的处理函数
def process_dataframe(df):
    df = process_dataframe_parallel(df,max_workers= 10)
    return df

# Streamlit应用
def main():
    st.title('Super Excel')

    # 初始化 session state
    if 'df' not in st.session_state:
        st.session_state.df = get_initial_data()
    
    if 'uploaded_file' not in st.session_state:
        st.session_state.uploaded_file = None
    
    if 'run_clicked' not in st.session_state:
        st.session_state.run_clicked = False

    uploaded_file = st.file_uploader("上传你的数据文件(WPS格式的xls文件解析可能会出错，这里有一个示例文件：https://r2.bedtimewhisper.com/football_legends.csv)")

    if uploaded_file is not None:
        st.session_state.uploaded_file = uploaded_file
        # 尝试不同编码格式，utf-8-sig, ISO-8859-1 或者 latin1
        try:
            df = pd.read_csv(st.session_state.uploaded_file, encoding='utf-8')
        except UnicodeDecodeError:
            df = pd.read_csv(st.session_state.uploaded_file, encoding='ISO-8859-1')
        except pd.errors.EmptyDataError:
            st.error("文件为空或者不是有效的CSV文件。请检查并重新上传。")
            return

        if df.empty:
            st.error("文件没有可以解析的列。请上传正确格式的CSV文件。")
        else:
            st.session_state.df = df

    # 输入新列名
    new_col_name = st.text_input("输入新列名并点击'添加新列'按钮:")

    # 按钮以添加新列
    if st.button("添加新列"):
        if new_col_name:
            if new_col_name not in st.session_state.df.columns:
                st.session_state.df[new_col_name] = ""  # 添加新列，并设置初始值为空字符串
                st.success(f"列 '{new_col_name}' 已添加!")
            else:
                st.warning(f"列 '{new_col_name}' 已经存在。")
        else:
            st.warning("请输入有效的列名。")

    # 直接显示 DataFrame，不再使用 expander
    edited_df = st.data_editor(
        st.session_state.df,
        num_rows="dynamic",
        use_container_width=True,
        key="editor_1"
    )
    # 每次编辑后立即更新 session state
    st.session_state.df = edited_df

    # 添加"运行"按钮进行处理
    if st.button("AI自动搜索"):
        with st.spinner('正在处理数据...'):
            st.session_state.df = process_dataframe(st.session_state.df)
        st.session_state.run_clicked = True
        st.rerun()

    if st.session_state.run_clicked:
        st.success("解析结束")
        st.session_state.run_clicked = False

if __name__ == '__main__':
    main()