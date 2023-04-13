# _*_ coding: utf-8 _*_
"""
@File       : data_method.py
@Author     : Tao Siyuan
@Date       : 2022/8/6
@Desc       :...
"""
import numpy as np
from pyecharts.charts import Bar
from pyecharts import options as opts


def get_sorted_data(theme, class_id, grade_id, filter_dict, content):
    length = len(content['gender'])
    if type(content[theme][0]) != np.int64:
        x_data = list(set(content[theme]))
        y_data = []
        for i in range(len(x_data)):
            sum = 0
            for j in range(length):
                if content[theme][j] == x_data[i] \
                        and (int(content['Class'][j]) == class_id or class_id == 'True_all') \
                        and (int(content['GradeID'][j][2:4]) == grade_id or grade_id == 'All'):

                    need_to_filter = False
                    for key in filter_dict.keys():
                        if content[key][j] != filter_dict[key]:
                            need_to_filter = True
                            break

                    if not need_to_filter:
                        sum += 1
            y_data.append(sum)

        data_pair = [list(z) for z in zip(x_data, y_data)]
        data_pair.sort()
        x_data = []
        y_data = []
        for i in range(len(data_pair)):
            x_data.append(data_pair[i][0])
            y_data.append(data_pair[i][1])

        return x_data, y_data
    else:
        x_data = ['0-20', '20-40', '40-60', '60-80', '80-100']
        y_data = []
        for i in range(len(x_data)):
            sum = 0
            for j in range(length):
                if i * 0 <= int(content[theme][j]) <= (i + 1) * 20 \
                        and (int(content['Class'][j]) == class_id or class_id == 'True_all') \
                        and (int(content['GradeID'][j][2:4]) == grade_id or grade_id == 'All'):

                    need_to_filter = False
                    for key in filter_dict.keys():
                        if content[key][j] != filter_dict[key]:
                            need_to_filter = True
                            break

                    if not need_to_filter:
                        sum += 1
            y_data.append(sum)

        return x_data, y_data


def get_chart(grade_id, class_id, theme, filter_dict, content):
    if class_id == 'All':
        x_data_class1, y_data_class1 = get_sorted_data(theme, 1, grade_id, filter_dict, content)
        x_data_class2, y_data_class2 = get_sorted_data(theme, 2, grade_id, filter_dict, content)
        x_data_class3, y_data_class3 = get_sorted_data(theme, 3, grade_id, filter_dict, content)

        class_list = (
            Bar()
            .add_xaxis(x_data_class1)
            .add_yaxis('class1', y_data_class1)
            .add_yaxis('class2', y_data_class2)
            .add_yaxis('class3', y_data_class3)
            .set_global_opts(
                title_opts=opts.TitleOpts(title=theme.capitalize(), pos_left="10%"),
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )
        return class_list

    else:
        x_data_class, y_data_class = get_sorted_data(theme, class_id, grade_id, filter_dict, content)

        class_list = (
            Bar()
            .add_xaxis(x_data_class)
            .add_yaxis('class%d' % class_id, y_data_class)
            .set_global_opts(
                title_opts=opts.TitleOpts(title=theme.capitalize(), pos_left="10%"),
                legend_opts=opts.LegendOpts(pos_top="5%")
            )
        )
        return class_list
