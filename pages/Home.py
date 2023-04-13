# _*_ coding: utf-8 _*_
"""
@File       : Home.py
@Author     : Tao Siyuan
@Date       : 2022/8/6
@Desc       :...
"""
import streamlit as st
import requests
from streamlit_lottie import st_lottie
import pandas as pd
import os


def load_lottie(url):
    r = requests.get(url)
    if r.status_code != 200:
        return None
    return r.json()


def run():
    if os.path.exists("data.csv"):
        os.remove("data.csv")
    if os.path.exists("group_result.csv"):
        os.remove("group_result.csv")
    st.write('# Home')
    lottie_back = load_lottie('https://assets3.lottiefiles.com/private_files/lf30_cldvedro.json')
    lottie_study = load_lottie('https://assets8.lottiefiles.com/packages/lf20_ttnc5lln.json')
    lottie_score = load_lottie('https://assets7.lottiefiles.com/packages/lf20_ayv3qmag.json')
    with st.container():
        st.subheader('Hello, here is students data analyse APP!')
    f = st.file_uploader('upload a csv file here', type='csv')
    if f is None:
        st.warning("**Please upload a csv file**")
    else:
        text = pd.read_csv(f)
        text.to_csv('data.csv', index=None)
        st.write('**data process successfully!**')

    st.header("Background Information")
    with st.container():
        l_column, r_column = st.columns((1, 1))
        with l_column:
            st.markdown(
                '<font face="New Times Roman" size="4">If you want to get basic information about your child\'s '
                'gender, country, etc., make sure you have uploaded the '
                'data and then go to the **Background page** where you will find the answers you want.</font>',
                unsafe_allow_html=True)
        with r_column:
            st_lottie(lottie_back, height=150)

    st.markdown('---')

    st.header("Learning Information")
    with st.container():
        l_column, r_column = st.columns((1, 1))
        with l_column:
            st.markdown('<font face="New Times Roman" size="4">If you want to refer to information such as how often '
                        'students raise their hands in class, parental guidance, '
                        'etc., please make sure to jump to the **Learning page** to '
                        'see the analysis results after the data is uploaded.</font>', unsafe_allow_html=True)
        with r_column:
            st_lottie(lottie_study, height=150)

    st.markdown('---')

    st.header("Score information")
    with st.container():
        l_column, r_column = st.columns((1, 1))
        with l_column:
            st.markdown(
                '<font face="New Times Roman" size="4">If you want to visualize a student\'s Score, '
                'or if you want to predict a student\'s Score based on existing data, make sure you go to '
                'the **Score page** once the data is uploaded .</font>',
                unsafe_allow_html=True)
        with r_column:
            st_lottie(lottie_score, height=150)
    st.markdown("---")
    with st.container():
        c1, c2 = st.columns(2)
        with c1:
            with st.form('123'):
                st.markdown("##### contact us")
                st.text_input(label='your email')
                st.text_input(label='your telephone')
                st.text_input(label='your suggest')
                st.form_submit_button('submit')
    # try:
        # thread.join()
    # except RuntimeError:
    #     print('Thread hadn\'t begin')
