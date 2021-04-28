
import pandas as pd


#%%
'''大問1'''
# csvの読み込み
csv = pd.read_csv('/Users/rukaoide/Documents/\
04.pandasテスト/ex3_biblio.csv', encoding='shift-jis')
csv
df = pd.DataFrame(csv)
df

# 先頭の5行を表示
csv.head()
df.head()

# 欠損値を0に
csv.fillna(0)
df.fillna(0)

# 図書館数で降順に並び替える
csv.sort_values(by='図書館数', ascending=False)
df.sort_values(by='図書館数', ascending=False)


#%%
'''大問2'''
csv_2 = pd.read_csv('/Users/rukaoide/Documents/\
04.pandasテスト/ex3_physicalSize.csv', encoding='shift-jis')
csv_2
df_2 = pd.DataFrame(csv_2)
df_2

# データの次元数
csv_2.shape
df_2.shape

# 欠損値の確認
csv_2.isnull()
df_2.isnull()

# BMIを計算し「BMI_○」に格納
bmi_list_m, bmi_list_f = [], []

for h, w in zip(csv_2['身長_男'], csv_2['体重_男']):
    bmi_m = w / (h*0.01)**2
    bmi_list_m.append(bmi_m)

for h, w in zip(df_2['身長_女'], df_2['体重_女']):
    bmi_f = w / (h*0.01)**2
    bmi_list_f.append(bmi_f)

df_bmi = pd.DataFrame({
    'BMI_男': bmi_list_m,
    'BMI_女': bmi_list_f
})
pd.merge(df_2, df_bmi, how='left')

# 別解
df_2['BMI_男'] = df_2['体重_男'] / (df_2['身長_男']/100)**2
df_2['BMI_女'] = df_2['体重_女'] / (df_2['身長_女']/100)**2


#%%
csv_3 = pd.read_csv('/Users/rukaoide/Documents/\
04.pandasテスト/ex3_power.csv', encoding='shift-jis')
csv_2_new = pd.read_csv('/Users/rukaoide/Documents/\
04.pandasテスト/ex3_physicalSize.csv', encoding='shift-jis', dtype={'年齢':str})

df_3 = pd.DataFrame(csv_3)
df_2_new = pd.DataFrame(csv_2_new)
df_3_new = pd.merge(df_2_new, df_3, how='inner', on='年齢')
df_3_new

# 男性のデータのみ抽出
df_3_new.filter(like='男', axis=1)

# 男性の平均身長150cm以上、170cm未満の行を抽出
df_3_new[df_3_new['身長_男'] >= 150][df_3_new['身長_男'] < 170]
# 別解
df_3_new[(df_3_new['身長_男'] >= 150) & (df_3_new['身長_男'] < 170)]


#%%
'''大問3'''
csv_4 = pd.read_csv('/Users/rukaoide/Documents/04.pandasテスト/\
ex3_来店アンケート.csv', encoding='shift-jis', engine='python')
df_4 = pd.DataFrame(csv_4)
df_4

# 年齢データの基礎統計量の取得
df_4['年齢'].describe()

# 来店のきっかけ別の人数と平均年齢を取得
#df_4.groupby('来店のきっかけ', as_index=False)['年齢'].mean()
df_4_new = df_4.groupby('来店のきっかけ').agg(
    {'来店のきっかけ': ['count'], '年齢': ['mean']})
df_4_new.columns = ['人数', '平均年齢']
df_4_new

# 来店のきっかけと雰囲気の満足度で人数カウント
pd.crosstab(df_4['来店のきっかけ'], df_4['雰囲気の満足度'])


#%%
'''大問4'''
csv_5 = pd.read_csv('/Users/rukaoide/Documents/04.pandasテスト/\
ex3_仮想通貨価格_20180930.csv', encoding='shift-jis', engine='python')
df_5 = pd.DataFrame(csv_5)
df_5

# 日付列をdatetime型へ変換
df_5['date'] = pd.to_datetime(df_5['date'], format='%Y年%m月%d日')
df_5

# 2015年1月と2018年1月の高値平均値を算出して比較
df_5_201501 = df_5[(df_5['date'].dt.year == 2015) & (df_5['date'].dt.month == 1)]
df_5_201801 = df_5[(df_5['date'].dt.year == 2018) & (df_5['date'].dt.month == 1)]
df_5_201501 = df_5_201501.dropna()
df_5_201801 = df_5_201801.dropna()
df_5_201501['高値'].mean()
df_5_201801['高値'].mean()

# 終値を線形補間して、1日ごとのデータに変換
df_5.set_index('date', inplace=True)
df_5
end_price = df_5['終値'].resample('D').interpolate('linear')
end_price


#%%
'''追加問題'''
# dfをcsvファイルに変換
csv_6 = pd.read_csv('/Users/rukaoide/Documents/04.pandasテスト/\
panda_test.csv', encoding='shift-jis')
df_6 = pd.DataFrame(csv_6)
df_6.to_csv('/Users/rukaoide/Documents/04.pandasテスト/\
panda2.csv')

# Sex列, Embarked列をone-hotエンコーディングに変更
df_6 = pd.get_dummies(df_6, columns=['Sex', 'Embarked'])
df_6

# Age列の欠損値をAge列の中央値で埋める
df_6['Age'].median()
df_6['Age'].fillna(df_6['Age'].median(), inplace=True)
df_6

# 男女別のSatisfiedの0と1の数と割合をクロス集計で(行)正規化して表示
pd.crosstab(df_6['Sex'], df_6['Satisfied'], normalize='index')

# Git_practice
