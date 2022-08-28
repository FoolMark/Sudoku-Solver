# 数独解题器
## 环境要求
- python (推荐安装[Anaconda](https://www.anaconda.com/))
- numpy (Anaconda中一般自带)
- openpyxl (用于excel文件读写,Anaconda中一般自带)

## 使用指南
- 在"data.xlxs"中的指定区域填入对应的数独初始状态
- python solve.py 运行程序, 结果将存在表格"data.xlxs"第二页中
- 若程序报错 "NotValidError", 请检查输入的数独初始状态是否正确