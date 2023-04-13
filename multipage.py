# _*_ coding: utf-8 _*_
"""
@File       : multipage.py
@Author     : Tao Siyuan
@Date       : 2022/8/5
@Desc       :...
"""
import streamlit as st


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

