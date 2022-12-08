# 說明
臺灣的房價不斷攀升，你知道哪個行政區的房價最高嗎?

我們可以透過內政部不動產成交案件實際資訊的[Open Data](https://plvr.land.moi.gov.tw/DownloadOpenData) 來推估各個季度的市價。


# 環境
- 作業系統: WSL (Windows Subsystem of Linux)
- Python版本: `3.8.10`
- 套件管理工具: `Peotry`
- 相關套件:
    - numpy: `1.23.5`
    - pandas: `1.5.2`
    - matplotlib: `3.6.2`
    - wget: `3.2`
    - tqdm: `4.64.1`
    - bar-chart-race: `0.1.0`

# 執行

## 方法一: 使用 Peotry

1. 根據[此文章](https://blog.kyomind.tw/python-poetry/#%E5%AE%89%E8%A3%9D-Poetry)指引安裝Peotry
1. 執行 `peotry install` 安裝相關套件
1. 使用安裝好的Python版本執行`main.ipynb`

## 方法二: 使用 Pip
1. 執行 `pip install -r requiremen.txt` 安裝相關套件
1. 執行 `main.ipynb`

## 方法三: 使用Google Colab (不建議)
1. 將 `main.ipynb` 上傳至 Google Drive
1. 連線至執行階段後，上傳 `DataCollector.py` 
1. 使用pip安裝 `wget` 和 `bar-chart-race`
1. 執行 `main.ipynb` (無法輸出中文字型)

## 方法四: 使用GitHub Codespaces (不建議)
1. 執行 `main.ipynb` (無法輸出中文字型)

# 結果
## 中位數版本(較準確)
![median.gif](./output/median.gif "median.gif")
## 平均數版本
![mean.gif](./output/mean.gif "mean.gif")
