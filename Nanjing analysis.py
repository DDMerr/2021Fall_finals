import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import warnings


data = pd.read_excel("nanjing.xlsx")
df = data.iloc[:,0:9]
df.columns = ['name','type','state','address','addresses','room','area','price','second']
print(df)
print(df.shape)

print(df.isnull().sum())
df.dropna(subset=['addresses','price','room','area','second'],inplace=True)
print(df.isnull().sum())
print(df.duplicated().sum())

print(df.shape)



data1 = df.iloc[:,0:9]
print(data1)




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



df.head(20)
from sklearn.preprocessing import StandardScaler
scaler = StandardScaler()#标准化
data = pd.DataFrame(scaler.fit_transform(df[['name','type','state','address','addresses','room','area',"price",'second']]),columns=['name','type','state','address','addresses','room','area',"price",'second'])
print(data.head())


print(df.describe())


import seaborn as sns

plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
score = data1['type']
price=data1['price']

plt.scatter(x=score,y=price, s=10, c='b')
plt.show()


sns.distplot(data1['price'], bins=20)
plt.show()


import matplotlib.pyplot as plt
import seaborn as sns
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
quyu_price=data1.groupby('address')['price'].mean()
quyu_price.sort_values(ascending=True,inplace=True)
quyu_price.plot.bar(figsize=(12,7),color=['orange','moccasin','wheat','papayawhip','tan'],alpha=0.6)#画布大小和颜色
plt.ylabel('price')
plt.show()



quyu_price=data1.groupby('type')['price'].mean()
quyu_price.sort_values(ascending=True,inplace=True)
quyu_price.plot.bar(figsize=(12,8),color=['moccasin','orange','wheat','tan','papayawhip'],alpha=0.6)
plt.ylabel('price')
plt.show()



hdate = data1['room']
price=data1['price']
f,ax = plt.subplots(figsize=(10,7))
fig = sns.boxplot(x=hdate,y=price)
fig.axis(ymin=10000,ymax=100500)
plt.show()


fangyuan=data1.address.value_counts().sort_values()
plt.rcParams['font.sans-serif']=['SimHei']
plt.rcParams['axes.unicode_minus']=False
plt.figure(figsize=(15,13),dpi=80)
explode={}
for i in fangyuan.index:
    if i in ['江宁','浦口','玄武']:
        explode[i]=0
    else:
        explode[i]=0

plt.pie(fangyuan,labels=fangyuan.index,explode=explode.values(),autopct='%0.2f%%',colors=sns.color_palette('hls', n_colors=16))
plt.title('Nanjing Housing Distribution',fontsize=20)
plt.axis('equal')
plt.legend(loc='upper left')
plt.show()


import seaborn as sns
import matplotlib.pyplot as plt
sns.set(font='SimHei')  # 解决Seaborn中文显示问题
transformed_data = pd.get_dummies(data)
colormap = plt.cm.RdBu
plt.figure(figsize=(14,12))

plt.title('Pearson Correlation of Features', y=1.05, size=15)
sns.heatmap(transformed_data.astype(float).corr(),linewidths=0.1,vmax=1.0,
            square=True, cmap=colormap, linecolor='white', annot=True)
plt.show()







from collections import Counter
lista = data1['address']
c = Counter(lista)
print(c)



from pyecharts import options as opts
from pyecharts.charts import Map
from pyecharts.faker import Faker

quxian = ['江宁区', '浦口区',
          '玄武区', '鼓楼区', '雨花台区',
          '六合区', '栖霞区', '溧水区', '高淳区',
          '建邺区','句容区','秦淮区']

values3 = [106, 97, 10, 18, 24, 30, 42, 38, 29, 24, 16, 15]

english_names = {"江宁区":"JIANGNING",
                '浦口区':"PUKOU",
                '玄武区':"XUANWU",
                '鼓楼区':"GULOU",
                '雨花台区':"YUHUATAI",
                '六合区':"LIUHE",
                '栖霞区':"QIXIA",
                '溧水区':"LISHUI",
                '高淳区':"GAOCHUN",
                '建邺区':"JIANYE",
                '句容区':"JURONG",
                '秦淮区':"QINHUAI"}


c = (
    Map()
        .add("南京", [list(z) for z in zip(quxian, values3)], "南京", name_map=english_names)
        .set_global_opts(
        title_opts=opts.TitleOpts(title="Nanjing map"), visualmap_opts=opts.VisualMapOpts()
    )
        .render()
)

import os
os.system("open render.html")

