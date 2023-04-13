# _*_ coding: utf-8 _*_
"""
@File       : main.py
@Author     : Tao Siyuan
@Date       : 2022/8/5
@Desc       :...
"""
import streamlit as st
from multipage import Multipage
from pages import Background, Home, Learning

st.set_page_config(page_title="Scorce Statistical", page_icon=":star2:", layout='wide')
st.title("Student Score Statistics")

app = Multipage()

# add pages
app.add_page('Home', Home.run)
app.add_page('Background', Background.run)
app.add_page('Learning', Learning.run)
# app.add_page('Score', Score.run)

if __name__ == '__main__':
    app.run()
