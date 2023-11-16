# _*_ coding: utf-8 _*_
import streamlit as st
import streamlit_echarts as st_echarts
import pandas as pd
from pyecharts.charts import Bar
from pyecharts.charts import Pie
from pyecharts.charts import Line
from pyecharts.globals import ThemeType
from pyecharts import options as opts
import pages.utils as utils
# from utils import get_sorted_data
import os


def run():
    st.header('Basic information')
    f = None
    if st.session_state['base_file'] is None:
        f = st.file_uploader('upload a csv file here', type='csv')
        if f is None:
            st.warning("**Please upload a csv file**")
        else:
            st.session_state['base_file'] = pd.read_csv(f)
            st.write('**data process successfully!**')
            st.experimental_rerun()
    else:
        content = st.session_state['base_file'].copy(deep=True)
        theme = st.selectbox('Which theme do you want to show',
                             ('gender', 'Nationality', 'PlaceofBirth', 'StageID',
                              'SectionID', 'Topic', 'Semester', 'Relation', 'raisedhands',
                              'VisitedResources', 'AnnouncementsView', 'Discussion',
                              'ParentAnsweringSurvey', 'ParentschoolSatisfaction', 'StudentAbsenceDays'))
        type_of_chart = st.selectbox('Which type of chart do you want',
                                     ('Pie', 'Bar', 'Line'))

        grade_id = 'All'
        class_id = 'True_all'
        if st.button('Show the chart'):
            x_data, y_data = utils.get_sorted_data(theme, class_id, grade_id, {}, content)
            data_pair = [list(z) for z in zip(x_data, y_data)]
            data_pair.sort()
            x_data = []
            y_data = []
            for i in range(len(data_pair)):
                x_data.append(data_pair[i][0])
                y_data.append(data_pair[i][1])

            if type_of_chart == 'Pie':
                chart = (
                    Pie()
                    .add(
                        series_name=theme,
                        data_pair=data_pair,
                    )
                    .set_colors(["blue", "green", "yellow", "red", "pink", "orange", "purple", "black"])
                    .set_global_opts(title_opts=opts.TitleOpts(title="Pie-" + theme))
                )
            elif type_of_chart == 'Bar':
                chart = (
                    Bar()
                    .add_xaxis(x_data)
                    .add_yaxis('number', y_data)
                    .set_global_opts(title_opts=opts.TitleOpts(title="Bar-" + theme),
                                         xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 20}))
                )
            else:
                chart = (
                    Line()
                    .add_xaxis(x_data)
                    .add_yaxis('number', y_data)
                    .set_global_opts(title_opts=opts.TitleOpts(title="Line-" + theme),
                                        xaxis_opts=opts.AxisOpts(axislabel_opts={"rotate": 20}))
                )
            st_echarts.st_pyecharts(
                chart,
                theme=ThemeType.DARK
            )
            st.download_button('download', chart.render())
