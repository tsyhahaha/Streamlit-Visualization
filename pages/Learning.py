# _*_ coding: utf-8 _*_
"""
@File       : Learning.py
@Author     : Tao Siyuan
@Date       : 2022/8/6
@Desc       :...
"""
import streamlit as st
import streamlit_echarts as st_echarts
import pandas as pd
from pyecharts.globals import ThemeType
from pages.data_method import get_chart
import os
from sklearn.ensemble import RandomForestClassifier
import numpy as np
from pyecharts.charts import Bar
from pyecharts import options as opts


def run():
    st.header('Learning infomation')
    f = None
    if os.path.exists('data.csv'):
        f = pd.read_csv('data.csv')
    if f is None:
        st.warning("**Please upload a csv file**")
    else:
        content = f

        grade_id = st.selectbox(
            'GradeId',
            ['All', 2, 4, 5, 6, 7, 8, 9, 10, 11, 12]
        )
        if grade_id != 'All':
            class_id = st.selectbox(
                'ClassId',
                ['All', 1, 2, 3]
            )
        else:
            class_id = 'All'

        # 展示主题
        theme = st.selectbox('Which theme do you want to show',
                             ('Relation', 'raisedhands', 'VisitedResources', 'AnnouncementsView',
                              'Discussion', 'ParentAnsweringSurvey', 'ParentschoolSatisfaction',
                              'StudentAbsenceDays'))

        # 过滤元素
        filter_elements = st.multiselect('Choose some filter elements',
                                         ['gender', 'Nationality', 'PlaceofBirth', 'StageID',
                                          'SectionID', 'Topic', 'Semester', 'Relation'], [])
        filter_dict = {}
        for element in filter_elements:
            option = st.selectbox(element,
                                  list(set(content[element])))
            filter_dict[element] = option

        st.write('You selected:')
        show_dict = {'theme': theme, 'gradeId': grade_id, 'classId': class_id}
        show_dict.update(filter_dict)
        st.json(show_dict)

        if st.button('Show the chart', key='1'):
            chart = get_chart(grade_id, class_id, theme, filter_dict, content)
            st_echarts.st_pyecharts(
                chart,
                theme=ThemeType.DARK
            )
            st.download_button('download', chart.render())

        headers = list(content.columns)

        # 过滤元素
        compare_elements = st.multiselect('Among which factors would you like to compare their effect size on student achievement',
                                         ['All', 'gender', 'Nationality', 'PlaceofBirth', 'StageID', 'GradeID',
                                          'SectionID', 'Topic', 'Semester', 'Relation', 'raisedhands',
                                          'VisitedResources', 'AnnouncementsView', 'Discussion', 'ParentAnsweringSurvey',
                                          'ParentschoolSatisfaction', 'StudentAbsenceDays'],default=['All'])
        if len(compare_elements) == 0:
            st.warning("**Please choose factors you want to compare**")
        else:
            if 'All' in compare_elements:
                compare_elements = ['gender', 'Nationality', 'PlaceofBirth', 'StageID', 'GradeID',
                                              'SectionID', 'Topic', 'Semester', 'Relation', 'raisedhands',
                                              'VisitedResources', 'AnnouncementsView', 'Discussion', 'ParentAnsweringSurvey',
                                              'ParentschoolSatisfaction', 'StudentAbsenceDays']

            indexlist = []
            for element in compare_elements:
                indexOfEle = headers.index(element)
                indexlist.append(indexOfEle)

            content["gender"] = pd.factorize(content["gender"])[0].astype(int)
            content["Nationality"] = pd.factorize(content["Nationality"])[0].astype(int)
            content["PlaceofBirth"] = pd.factorize(content["PlaceofBirth"])[0].astype(int)
            content["StageID"] = pd.factorize(content["StageID"])[0].astype(int)
            content["GradeID"] = pd.factorize(content["GradeID"])[0].astype(int)
            content["SectionID"] = pd.factorize(content["SectionID"])[0].astype(int)
            content["Topic"] = pd.factorize(content["Topic"])[0].astype(int)
            content["Semester"] = pd.factorize(content["Semester"])[0].astype(int)
            content["Relation"] = pd.factorize(content["Relation"])[0].astype(int)
            content["ParentAnsweringSurvey"] = pd.factorize(content["ParentAnsweringSurvey"])[0].astype(int)
            content["ParentschoolSatisfaction"] = pd.factorize(content["ParentschoolSatisfaction"])[0].astype(int)
            content["StudentAbsenceDays"] = pd.factorize(content["StudentAbsenceDays"])[0].astype(int)

            init_x = content.iloc[:, :-1].to_numpy()
            init_y = content.iloc[:, -1].to_numpy()
            permutation = list(np.random.permutation(init_x.shape[0]))
            init_x = init_x[permutation, :]  # 将每一列的数据按permutation的顺序来重新排列。
            init_y = init_y[permutation]

            # 获取训练集、测试集
            x_test = init_x[400:, indexlist]
            y_test = init_y[400:]
            x = init_x[:400, indexlist]
            y = init_y[:400]


            reg_ran1 = RandomForestClassifier()
            reg_ran1.fit(x, y)
            importances = reg_ran1.feature_importances_

            x_data = compare_elements
            y_data = []
            for weight in importances:
                y_data.append(round(weight,2))

            if st.button('Show the chart', key='2'):
                chart = (
                    Bar(init_opts=opts.InitOpts(theme=ThemeType.MACARONS,
                                                width='1000px',
                                                height='1000px'))
                        .add_xaxis(x_data)
                        .add_yaxis('weights', y_data)
                        .set_global_opts(title_opts=opts.TitleOpts(title="Bar-Importance of Elements"),
                                         xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 20}))
                )
                st_echarts.st_pyecharts(
                    chart,
                    theme=ThemeType.DARK
                )
                st.download_button('download picture', chart.render())
