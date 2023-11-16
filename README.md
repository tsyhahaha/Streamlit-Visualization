# README
本仓库是利用 streamlit 构建的可视化网页 app。在本项目中，实现了：
* 基于 streamlit 的 multipage 前端显示
* 基于 echarts 的统计数据可视化
* 机器学习的模型部署（简单的 keras model 搭建的学生成绩预测模型）

run:
```
stremalit run main.py
```

如果遇到 tensorflow 的 ImportError: libstdc... 问题，可以尝试：
```
conda install -c conda-forge libstdcxx-ng
```
