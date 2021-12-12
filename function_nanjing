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
def type_conversion(name):
    """

    This function is aimed at data preprocessing.
    The purpose is to convert the features based on the data in the data set from text to numbers.
    :param name:
    :return:

    """
    warnings.filterwarnings("ignore")
    df[name] = pd.factorize(df[name])[0].astype(np.uint16)
    print(df.head())
#type_conversion("name")
#type_conversion("type")
#type_conversion("state")
#type_conversion("address")
#type_conversion("room")

#Standardization processing and normalization processing
def Normalization():
    """
    This function is also aimed at data preprocessing, and standardizes and normalizes them.

    :return:
    """
    df.head(20)
    scaler = StandardScaler()  #standardization
    data = pd.DataFrame(
        scaler.fit_transform(df[['name', 'type', 'state', 'address', 'addresses', 'room', 'area', "price", 'second']]),
        columns=['name', 'type', 'state', 'address', 'addresses', 'room', 'area', "price", 'second'])
    print(data.head())
    print(df.describe()) #Data description
#Normalization()


#Scatter graph
def Scatter_graph():
    """
    Generate a scatter chart to show the general trend of different house types in different price ranges.
    :return:
    """
    score = data1['type']
    price = data1['price']
    plt.scatter(x=score, y=price, color='red',marker='o',alpha=0.5, s=10)
    plt.title("The relationship between property type and price")  # set title
    plt.show()

#Price Histogram
def Histogram():
    """
    This function This function wants to analyze the unit price density per square meter of houses
    from the entire city to determine the price of most houses and the overall price distribution.
    :return:
    """

    sns.set()
    sns.distplot(data1['price'], bins=20, kde=True, rug=True, vertical=True)
    plt.title("Price density range")
    plt.show()
#Histogram()

#Address and price relationship histogram
def Histogram_1():
    """
    Analyze the housing prices in the area and found that
    the housing prices in the prosperous areas are the highest
    :return:
    """

    Regional_price = data1.groupby('address')['price'].mean()  # Find the mean
    Regional_price.sort_values(ascending=True, inplace=True)  # Find the sort
    Regional_price.plot.bar(figsize=(12, 7), color=['orange', 'moccasin', 'wheat', 'papayawhip', 'tan'],
                        alpha=0.6)  # Canvas size and color
    plt.ylabel('price')
    plt.title("Address and price relationship")
    plt.show()

#Histogram_1()

#Type and price relationship histogram
def Histogram_2():
    """
    Analyze the relationship between housing types and housing prices,
    and found that the housing prices of the sub-commercial type are the highest

    :return:
    """

    Regional_price = data1.groupby('type')['price'].mean()
    Regional_price.sort_values(ascending=True, inplace=True)
    Regional_price.plot.bar(figsize=(12, 8), color=['mistyrose','lightpink','pink', 'palevioletred', 'hotpink', 'violet', 'mediumorchid'], ec='k', lw=1, alpha=0.6)
    plt.ylabel('price')
    plt.title("Type and price relationship")
    plt.show()

#Histogram_2()

#Area and price relationship box plot
def box_plot():
    """
    This function aimed to analyze the box plot of the influence of the number of rooms in the house on the price.
    It can be seen that the average price of having four or five rooms is the highest, and having more or fewer rooms will affect the price.

    :return:
    """
    hdate = data1['room']
    price = data1['price']
    f,ax = plt.subplots(figsize=(10, 7))
    fig = sns.boxplot(x=hdate, y=price)
    fig.axis(ymin=10000, ymax=100500)
    plt.title("Area and price relationship")
    plt.show()

#box_plot()

#Pie chart of distribution of new houses in Nanjing
def pie_chart():
    """
    The purpose of this function is to generate a pie chart
    in order to see the activity of the real estate market in different regions more intuitively.
    :return:
    """

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
def Thermodynamic_diagram():
    """
    This function is to generate heat maps of different related elements to determine the degree of influence of different factors
    such as room type, area, area, etc., the darker the color and the larger the number, the greater the mutual influence.
    :return:
    """

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
def nanjing_map():
    """
    The reason for calling the pyechart package to generate a map is that the precise latitude and longitude of the real estate cannot be obtained, 
    and using this package to generate a map does not require precise latitude and longitude.

    This function analyzes the number of sold houses in each district in Nanjing, and combines the analysis results to judge the popularity of the real estate through the shade of the color. 
    The darker the area, the higher the house purchase rate.

    :return:
    """
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


