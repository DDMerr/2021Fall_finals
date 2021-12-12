#Yunjia Zhang's part
import os
import pandas as pd
import numpy as np
import warnings
from sklearn.preprocessing import StandardScaler
import seaborn as sns
import matplotlib.pyplot as plt
from collections import Counter
from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker


#Read data
data = pd.read_excel("nanjing.xlsx")
df = data.iloc[:,0:9]
df.columns = ['name','type','state','address','addresses','room','area','price','second']
#print(df)
#print(df.shape)#View data dimensions
#print(df.isnull().sum())#Detect null value
df.dropna(subset=['addresses','price','room','area','second'],inplace=True)
#print(df.isnull().sum())
#print(df.duplicated().sum())#Detection of duplicate values
#print(df.shape)
data1 = df.iloc[:,0:9]
#print(data1)



#Convert text-based features to numeric

warnings.filterwarnings("ignore")
df["name"] = pd.factorize(df["name"])[0].astype(np.uint16)
df["type"] = pd.factorize(df["type"])[0].astype(np.uint16)
df["state"] = pd.factorize(df["state"])[0].astype(np.uint16)
df["address"] = pd.factorize(df["address"])[0].astype(np.uint16)
df["addresses"] = pd.factorize(df["addresses"])[0].astype(np.uint16)
df["room"] = pd.factorize(df["room"])[0].astype(np.uint16)
df["area"] = pd.factorize(df["area"])[0].astype(np.uint16)
df["second"] = pd.factorize(df["second"])[0].astype(np.uint16)

print(df.head())


#Standardization processing and normalization processing

df.head(20)
scaler = StandardScaler()  #standardization
data = pd.DataFrame(scaler.fit_transform(df[['name', 'type', 'state', 'address', 'addresses', 'room', 'area', "price", 'second']]),
        columns=['name', 'type', 'state', 'address', 'addresses', 'room', 'area', "price", 'second'])
print(data.head())
print(df.describe()) #Data description
#Normalization()


#Scatter graph

score = data1['type']
price = data1['price']
plt.scatter(x=score, y=price, color='red',marker='o',alpha=0.5, s=10)
plt.title("The relationship between property type and price")  # set title
plt.show()

#Price Histogram
sns.set()
sns.distplot(data1['price'], bins=20, kde=True, rug=True, vertical=True)
plt.title("Price density range")
plt.show()
#Histogram()

#Address and price relationship histogram

Regional_price = data1.groupby('address')['price'].mean()  # Find the mean
Regional_price.sort_values(ascending=True, inplace=True)  # Find the sort
Regional_price.plot.bar(figsize=(12, 7), color=['orange', 'moccasin', 'wheat', 'papayawhip', 'tan'],
                        alpha=0.6)  # Canvas size and color
plt.ylabel('price')
plt.title("Address and price relationship")
plt.show()

#Histogram_1()

#Type and price relationship histogram

Regional_price = data1.groupby('type')['price'].mean()
Regional_price.sort_values(ascending=True, inplace=True)
Regional_price.plot.bar(figsize=(12, 8), color=['mistyrose','lightpink','pink', 'palevioletred', 'hotpink', 'violet', 'mediumorchid'], ec='k', lw=1, alpha=0.6)
plt.ylabel('price')
plt.title("Type and price relationship")
plt.show()

#Histogram_2()

#Area and price relationship box plot

hdate = data1['room']
price = data1['price']
f,ax = plt.subplots(figsize=(10, 7))
fig = sns.boxplot(x=hdate, y=price)
fig.axis(ymin=10000, ymax=100500)
plt.title("Area and price relationship")
plt.show()

#box_plot()

#Pie chart of distribution of new houses in Nanjing

Housing_resources = data1.address.value_counts().sort_values()

plt.figure(figsize=(15, 13), dpi=80)
explode = {}
for i in Housing_resources.index:
    if i in ['JiangNing', 'PuKou']:
        explode[i] = 0
    else:
        explode[i] = 1

plt.pie(Housing_resources, labels=Housing_resources.index, explode=explode.values(), autopct='%0.2f%%',
            colors=sns.color_palette('hls', n_colors=16))
plt.title('Nanjing Housing Distribution', fontsize=20)
plt.axis('equal')
plt.legend(loc='upper left')
plt.show()

#pie_chart()

#Correlation thermodynamic diagram

transformed_data = pd.get_dummies(data)
colormap = plt.cm.RdBu
plt.figure(figsize=(14, 12))
#Solve the problem that the negative sign '-' is displayed as a square in the saved image

plt.title('Pearson Correlation of Features', y=1.05, size=15)
sns.heatmap(transformed_data.astype(float).corr(), linewidths=0.1, vmax=1.0, square=True, cmap=colormap, linecolor='white', annot=True)
plt.show()

#Thermodynamic_diagram()

#Statistics address information

lista = data1['address']
c = Counter(lista)
#print(c)

#nanjing map

# Basic data

quxian = ['江宁区', '浦口区',
          '玄武区', '鼓楼区', '雨花台区',
          '六合区', '栖霞区', '溧水区', '高淳区',
          '建邺区', '句容区', '秦淮区']

values3 = [106, 97, 10, 18, 24, 30, 42, 38, 29, 24, 16, 15]

c = (
    Map()
        .add("南京", [list(z) for z in zip(quxian, values3)], "南京")
        .set_global_opts(
        title_opts=opts.TitleOpts(title="Nanjing map"), visualmap_opts=opts.VisualMapOpts()
    )
        .render()
)

os.system("open render.html")



