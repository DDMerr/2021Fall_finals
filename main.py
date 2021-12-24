import pandas
import matplotlib.pyplot as plt
from pypinyin import lazy_pinyin
from pylab import *  # Support language

# Solve display problems
plt.rcParams['font.sans-serif'] = ['SimHei']
plt.rcParams['axes.unicode_minus'] = False
markers = ['.', ',', 'o', 'v', '^', '<', '>', '1', '2', '3', '4', 's', '8', '*', 'X', 'd']
plt.figure(figsize=(12, 6))
data_of_three_year = []
template = pandas.read_excel('datadata.xlsx')
year2021 = []
year_groupby_2021 = {}
aera_groupby_2021 = {}
year2020 = []
year_groupby_2020 = {}
aera_groupby_2020 = {}
year2019 = []
year_groupby_2019 = {}
aera_groupby_2019 = {}


def cal_house_price_by_year(year_groupby, aera_groupby, title: str):
    plt.figure(figsize=(12, 6))
    avg_price_groupby_year = {}
    index = 0
    for key, values in year_groupby.items():
        sum_list = []
        for value in values:
            sum_list.append(value['单价'])
        arr_mean = np.mean(sum_list)
        avg_price_groupby_year[key] = arr_mean
    seq = sorted(avg_price_groupby_year)
    x = []
    y = []
    y1 = []
    for key in seq:
        print(key, avg_price_groupby_year[key])
        x.append(int(key))
        y.append(avg_price_groupby_year[key])
        data_of_three_year.append(avg_price_groupby_year[key])
    plt.plot(x, y, marker=markers[index], mec='r', mfc='w', label=''.join(lazy_pinyin('广州')))
    #
    index += 1
    for key, values in aera_groupby.items():
        avg_price_groupby_aera_month = {}
        for value in values:
            month = value['成交时间'].split('.')[1]
            if avg_price_groupby_aera_month.get(month) == None:
                avg_price_groupby_aera_month[month] = []
            avg_price_groupby_aera_month[month].append(value['单价'])
        y = []
        for i, j in avg_price_groupby_aera_month.items():
            y.append(np.mean(j))
        if (len(y) != 12 and title != '2021') or (len(y) != 7 and title == '2021'):
            continue
        plt.plot(x, y, marker=markers[index], mec='r', mfc='w', label=''.join(lazy_pinyin(key)))
        index += 1

    plt.legend(bbox_to_anchor=(1.0, 0.7))  # Let each line have a corresponding name
    plt.xticks(x)
    font2 = {'family': 'Times New Roman',
             'weight': 'normal',
             'size': 10
             }
    plt.xlabel("month", font2)  # X axis label
    plt.ylabel("price", font2)  # Y axis label
    plt.title(title)  # title
    plt.savefig(title + '.png')


for row_index, row in template.iterrows():
    # print(row['区'], row['单价'], row['成交价格'], row['成交时间'], row['成交年份'])
    month = row['成交时间'].split('.')[1]
    year = row['成交时间'].split('.')[0]
    # if month not in months:
    #     continue
    if year == '2020':
        if year_groupby_2020.get(month) == None:
            year_groupby_2020[month] = []
        if aera_groupby_2020.get(row['区']) == None:
            aera_groupby_2020[row['区']] = []
        aera_groupby_2020[row['区']].append(row)
        year_groupby_2020[month].append(row)
        # year2020.append(row)
    elif year == '2019':
        if year_groupby_2019.get(month) == None:
            year_groupby_2019[month] = []
        if aera_groupby_2019.get(row['区']) == None:
            aera_groupby_2019[row['区']] = []
        aera_groupby_2019[row['区']].append(row)
        year_groupby_2019[month].append(row)
        # year2019.append(row)
    else:
        if year_groupby_2021.get(month) == None:
            year_groupby_2021[month] = []
        if aera_groupby_2021.get(row['区']) == None:
            aera_groupby_2021[row['区']] = []
        aera_groupby_2021[row['区']].append(row)
        year_groupby_2021[month].append(row)
        # year2019.append(row)


cal_house_price_by_year(year_groupby_2019, aera_groupby_2019, '2019')
cal_house_price_by_year(year_groupby_2020, aera_groupby_2020, '2020')
cal_house_price_by_year(year_groupby_2021, aera_groupby_2021, '2021')

x = [i + 1 for i in range(12)]
plt.figure(figsize=(12, 6))
plt.plot(x, data_of_three_year[0:12], marker=markers[0], mec='r', mfc='w', label=2019)
plt.plot(x, data_of_three_year[12:24], marker=markers[1], mec='r', mfc='w', label=2020)
# plt.plot(x, data_of_three_year[24:]+[0,0,0,0,0,], marker=markers[2], mec='r', mfc='w', label=2021)
plt.plot(x[0:7], data_of_three_year[24:], marker=markers[2], mec='r', mfc='w', label=2021)
plt.legend(bbox_to_anchor=(1.0, 0.7))  # Let each line have a corresponding name
plt.xticks(x)
plt.title('Price change of GuangZhou during three years')  # title
plt.savefig('all.png')


def cal_area_percent(aera_groupby: dict, aera_size: int, price=None):
    cal_res = {}
    if price is None:
        price = float('-inf')
    for aera, data in aera_groupby.items():
        count = 0
        sum = 0
        for row in data:
            sum += 1
            if row['成交价格'] / row['单价'] > aera_size / 10000 and row['单价'] > price:
                count += 1
        cal_res[''.join(lazy_pinyin(aera))] = count / sum
    return cal_res


def draw_area_percent(title: str, data: dict, suffix=''):
    plt.figure(figsize=(12, 6))
    # print(data)
    plt.title(title)
    plt.bar(data.keys(), data.values())

    plt.savefig(title + ('' if suffix == '' else '-' + suffix) + '-percent.png')


draw_area_percent('2019', cal_area_percent(aera_groupby_2019, 140))
draw_area_percent('2020', cal_area_percent(aera_groupby_2020, 140))
draw_area_percent('2021', cal_area_percent(aera_groupby_2021, 140))

draw_area_percent('2019', cal_area_percent(aera_groupby_2019, 140, 35000), '35000')
draw_area_percent('2020', cal_area_percent(aera_groupby_2020, 140, 35000), '35000')
draw_area_percent('2021', cal_area_percent(aera_groupby_2021, 140, 35000), '35000')

