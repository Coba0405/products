import csv
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import platform
from matplotlib import rcParams

csv_file_path = '人口動態調査1920~2015.csv'

# csvファイルを読み込む
df = pd.read_csv(csv_file_path, encoding='utf-8')

if platform.system() == 'Darwin':
    plt.rcParams['font.family'] = 'Hiragino Sans'
elif platform.system() == 'Windows':
    plt.rcParams['font.family'] = 'Meiryo'
else:
    plt.rcParams['font.family'] = 'IPAexGothic'

# 数値であれば列名を文字列に変更する
df.columns =df.columns.astype(str)

# データの確認
# print(df.head())

plt.figure(figsize=(12,8))

# 1945年の人口ピラミッド
plt.barh(df['年齢'], -df['1945_人口（男）'], label='1945_人口（男）',alpha=0.7, color='#1f77b4')
plt.barh(df['年齢'], df['1945_人口（女）'], label='1945_人口（女）',alpha=0.7, color='#ff7f0e')

# ラベルとタイトル
plt.xlabel('人口')
plt.ylabel('年齢')
plt.title('1945年の人口ピラミッド')
plt.legend()
plt.grid(axis='x', linestyle='--')

# 最大人口を100万人単位に切り上げ
max_population = int(np.ceil(max(df['2015_人口（男）'].max(), df['2015_人口（女）'].max())/ 1000000) * 1000000)

# -max_populationからmax_populationまで100万人単位で目盛を設定
tick_values = np.arange(-max_population, max_population + 1, 1000000)

# x軸のラベルを「万」単位で表示
plt.xticks(tick_values, [f"{abs(x) // 10000}万" for x in tick_values])

# グラフを表示
plt.show()
