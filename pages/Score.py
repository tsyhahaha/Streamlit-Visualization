# _*_ coding: utf-8 _*_
"""
@File       : Score.py
@Author     : Tao Siyuan
@Date       : 2022/8/6
@Desc       :...
"""
import json
import os

import streamlit as st
import streamlit_echarts as st_echarts
from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.globals import ThemeType
import pandas as pd

import numpy as np


def run():
    st.header('Score infomation')
    f = None
    if os.path.exists('data.csv'):
        f = pd.read_csv('data.csv')
    if f is None:
        st.warning("**Please upload a csv file**")
    else:
        str_mappers = f

        grade_id = st.selectbox(
            'GradeId',
            ['All', 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        )
        class_id = 'All'

        # 展示主题
        theme = 'Class'

        # 过滤元素
        filter_elements = st.multiselect('Choose some filter elements',
                                         ['gender', 'Nationality', 'PlaceofBirth', 'StageID',
                                          'SectionID', 'Topic', 'Semester', 'Relation'], [])
        filter_dict = {}
        for element in filter_elements:
            option = st.selectbox(element,
                                  list(set(str_mappers[element])))
            filter_dict[element] = option

        st.write('You selected:')
        show_dict = {'theme': 'score', 'gradeId': grade_id}
        show_dict.update(filter_dict)
        st.json(show_dict)

        if st.button('Show the chart'):
            x_data = [60, 80, 100]
            y_data = []
            for i in range(len(x_data)):
                sum = 0
                for j in range(len(str_mappers[theme])):
                    if int(str_mappers[theme][j]) == (x_data[i] - 40) // 20 \
                            and (int(str_mappers['GradeID'][j][2:4]) == grade_id or grade_id == 'All'):
                        need_to_filter = False
                        for key in filter_dict.keys():
                            if str_mappers[key][j] != filter_dict[key]:
                                need_to_filter = True
                                break

                        if not need_to_filter:
                            sum += 1
                y_data.append(sum)

            chart = (
                Bar()
                .add_xaxis(x_data)
                .add_yaxis('', y_data)
                .set_global_opts(
                    title_opts=opts.TitleOpts(title='Score', pos_left="10%"),
                    legend_opts=opts.LegendOpts(pos_top="5%")
                )
            )

            st_echarts.st_pyecharts(
                chart,
                theme=ThemeType.DARK
            )
            st.download_button('download', chart.render())

        st.header("Score prediction")
        with st.container():
            try:
                f = open('data.json', 'r')
                right_ratio = json.load(f)['right']
            except EOFError:
                print('error: data.json doesn\'t exist')
            st.markdown(
                "##### <center><font face=\"New Times Roman\" size=2>Currently, the prediction "
                "accuracy in the "
                "validation set is: " + str(right_ratio * 100) + "%</font></center>", unsafe_allow_html=True)
        # with st.container():
        st.markdown('##### single prediction')
        with st.form(key='my_form'):
            info = []
            f = open('mappers.json', 'r').read()
            str_mappers = json.loads(f)
            dirt = str_mappers.keys()
            for key in dirt:
                s = str_mappers[key]
                if key in ['raisedhands', 'VisitedResources', 'AnnouncementsView', 'Discussion']:
                    info.append(st.number_input(label=key, min_value=0, max_value=100))
                    continue
                if key == 'Class':
                    continue
                selection = list(s.keys())
                selection.sort()
                temp_input = str_mappers[key][st.selectbox(key, selection)]
                info.append(temp_input)
            flag = st.form_submit_button(label='Submit')
        st.markdown('---')
        info = np.array(info).reshape(1, -1)
        if flag:
            st.markdown("#### the prediction for class is: " + str(result))
            final = result * 20 + 40
            st.progress(final)
            if result == 1:
                st.markdown("your score is about 60, maybe you need try to ask for help with study.")
            elif result == 2:
                st.markdown("your score is about 80, and it's average. Keep up the good work.")
            elif result == 3:
                st.markdown("your score is nearly 100, excellent!")

        st.markdown('##### group prediction')
        f = st.file_uploader('upload a csv file here', type='csv')
        if f is None:
            st.warning("**Please upload a csv file and be aware of the format---the same of the "
                       "input but without the 'class' colunm!**")
        else:
            st.write('**data read successfully!**')
            content = pd.read_csv(f)
            content_save = content.copy(deep=True)
            if len(content.columns) == 16:
                headers = content.columns
                for header in headers:
                    if header not in ['raisedhands', 'VisitedResources', 'AnnouncementsView', 'Discussion', 'Class']:
                        content[header] = content[header].map(str_mappers[header])
                pred = model.predict(content.to_numpy().astype(int))
                pred_re = []
                for line in pred:
                    line = list(line)
                    pred_re.append(line.index(max(line)))
                content_save['Class'] = pred_re
                content.to_csv('result.csv')
                st.markdown('**Please click the download button to get the result**')
                st.download_button(
                    label='download group prediction result',
                    data=content_save.to_csv(),
                    file_name='result.csv',
                    mime='text/csv'
                )
