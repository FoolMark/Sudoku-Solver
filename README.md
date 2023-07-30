# 数独解题器
## 环境要求
- python (推荐安装[Anaconda](https://www.anaconda.com/))
- numpy (Anaconda中一般自带)
- openpyxl (用于excel文件读写,Anaconda中一般自带)

## 使用指南
### 手动填入
- 在"data.xlxs"中的指定区域填入对应的数独初始状态
- python solve.py 运行程序
### 图像识别方案
- 截图保存为"input.jpg"
- python solve_image.py 运行程序
### 求解
- 结果将存在表格"data.xlxs"第二页中
- 若程序报错 "NotValidError", 请检查输入的数独初始状态是否正确
- 提供了两种算法，分别是使用标记数组的DFS，和转化为精确覆盖问题的Dancing Links搜索(默认算法)[Reference](https://oi-wiki.org/search/dlx/)，可在solve.py中通过注释代码进行选择
