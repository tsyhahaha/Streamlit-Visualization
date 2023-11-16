# _*_ coding: utf-8 _*_
"""
@File       : main.py
@Author     : Tao Siyuan
@Date       : 2022/8/5
@Desc       :...
"""
import streamlit as st
from pages import Background, Home, Learning, Score

class Multipage:
    def __init__(self):
        self.pages = []

    def add_page(self, title, func):
        self.pages.append(
            {
                'title': title,
                'function': func
            }
        )

    def run(self):
        page = st.sidebar.selectbox(
            'Navigation',
            self.pages,
            format_func=lambda page: page['title']  # 显示名称作为option
        )
        page['function']()


st.set_page_config(page_title="Scorce Statistical", page_icon=":star2:", layout='wide')
st.title("Student Score Statistics")

app = Multipage()

if 'base_file' not in st.session_state:
    st.session_state['base_file'] = None
if 'group_pred_file' not in st.session_state:
    st.session_state['group_pred_file'] = None
    
# add pages
app.add_page('Home', Home.run)
app.add_page('Background', Background.run)
app.add_page('Learning', Learning.run)
app.add_page('Score', Score.run)

if __name__ == '__main__':
    app.run()
