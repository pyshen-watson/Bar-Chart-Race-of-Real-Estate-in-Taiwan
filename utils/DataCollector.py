from dataclasses import dataclass, field
from wget import download as wget_download
from zipfile import ZipFile
from os import listdir, remove as rmfile
from shutil import rmtree
from os.path import join

import numpy as np
import pandas as pd
import pickle


# 類似於身分證字號，資料來源使用英文字母自首作為縣市區分標籤
code2name = { 'A':'台北市','B':'台中市','C':'基隆市','D':'台南市','E':'高雄市','F':'新北市','G':'宜蘭縣','H':'桃園縣','I':'嘉義市','J':'新竹縣','K':'苗栗縣','L':'台中縣','M':'南投縣','N':'彰化縣','O':'新竹市','P':'雲林縣','Q':'嘉義縣','R':'台南縣','S':'高雄縣','T':'屏東縣','U':'花蓮縣','V':'台東縣','W':'金門縣','X':'澎湖縣','Y':'陽明山','Z':'連江縣'}

@dataclass
class DataCollector:

    year: int
    season: int
    zipName: str = field(init=False)
    outName: str = field(init=False)

    def __post_init__(self):
        self.zipName = f'{self.year}-{self.season}.zip'
        self.outName = f'data/{self.year}-{self.season}.pickle'

    def download(self):
        # 資料來源: 內政部不動產成交案件實際資訊 Open Data: https://plvr.land.moi.gov.tw/DownloadOpenData
        pattern = f'https://plvr.land.moi.gov.tw//DownloadSeason?season={self.year}S{self.season}&type=zip&fileName=lvr_landcsv.zip'
        wget_download(pattern, self.zipName)

    def extract(self):
        # 將下載的zip檔解壓縮至temp資料夾
        with ZipFile(self.zipName, 'r') as zf:
            zf.extractall(path='./temp')

    def fetch(self):
        # a.csv 和 b.csv 為不動產交易紀錄， 而c.csv為租賃紀錄
        filenames = listdir('./temp/')
        targetnames = [filename for filename in filenames if 'a.csv' in filename or 'b.csv' in filename]

        self.data = dict()

        for name in targetnames:
            path = join('./temp/', name)
            countyName = code2name[name[0].upper()] + " "

            try:
                df = pd.read_csv(path)
                df = df[['鄉鎮市區', '單價元平方公尺']].iloc[1:]
            except:
                continue # 有一些奇怪的檔案無法正常開啟

            df = df.groupby('鄉鎮市區')['單價元平方公尺'].apply(list)
            df.index = countyName + df.index

            for key, value in df.to_dict().items():


                value = [ int(v) for v in value if isinstance(v, str) and v.isdigit()] # 這邊是為了過濾掉NaN

                if key in self.data.keys():
                    self.data[key] += value
                else:
                    self.data[key] = value

    def save(self, func=np.median):

        output = dict()

        for key, value in self.data.items():
            output[key] = np.int_(func(np.array(value)))

        # 以pickle的方式記錄，格式為 {"OO市 XX區": 資料}
        with open(self.outName, "wb") as f:
            pickle.dump(output, f)

    def remove(self):
        # 移除用不到的.csv檔和.zip檔
        rmfile(self.zipName)
        rmtree('./temp',)