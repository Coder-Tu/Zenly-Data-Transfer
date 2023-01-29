import pandas as pd
from datetime import datetime
import os
path='./locations'
 
## 声明一个空的DataFrame，用来做最终的数据合并
final_data = pd.DataFrame()
# 声明一个空的DataFrame，用来做最终的数据合并
final_data = pd.DataFrame()
 
def get_all_files(path):
    global final_data
    print("-"*20 + "函数被调用" + "-"*20)
    files = os.listdir(path)
    for file in files:
        if os.path.isfile(path + "/" +file):
            print(file+">>>>>是文件")
            filename,extension=os.path.splitext(file)
            # 判断是不是文本文件
            if extension=='.html':
                # 获取文件内容
                file_data = pd.read_html(str(path +'/'+file), header=1)[0]
                date_time = filename
                file_data['dateTime'] = date_time + ' ' + file_data['Unnamed: 0']
                final_data = final_data.append(file_data,ignore_index=True)
                #append描述：在列表ls最后(末尾)添加一个元素object
                print("《《《《合并"+filename+"文件数据》》》》")
                
        # 判断是不是文件夹
        elif os.path.isdir(path+'/'+file):
            print(file + "￥￥￥￥是文件夹￥￥￥￥￥￥")
            get_all_files(path + '/' + file)
get_all_files(path)
print("数据合并完成")

#转时间戳函数
def time2stamp(cmnttime):
    cmnttime=datetime.strptime(cmnttime,'%Y-%m-%d %H:%M:%S')
    stamp=int(datetime.timestamp(cmnttime))
    return stamp
final_data['dataTime'] = final_data['dateTime'].apply(time2stamp)

def deletecontent(locations):
    content = locations.split() 
    locations = content[0]
    return locations

# 新增Zenly中缺失的列
final_data['locType'] = 1
final_data['longitude'] = final_data['Longitude'].apply(deletecontent)
final_data['longitude'] = final_data['longitude'] + '00'
final_data['latitude'] = final_data['Latitude'].apply(deletecontent)
final_data['latitude'] = final_data['latitude'] + '00'
final_data['heading'] = 0
final_data['accuracy'] = 5
final_data['speed'] = final_data['Speed']
final_data['distance'] = 0
final_data['isBackForeground'] = 1
final_data['stepType'] = 0
final_data['altitude'] = final_data['Altitude']

final_data_zuji = pd.DataFrame(final_data, columns=['dataTime', 'locType', 'longitude', 'latitude', 'heading', 'accuracy', 'speed', 'distance', 'isBackForeground', 'stepType', 'altitude'])
final_data_zuji.head()
final_data_zuji.to_csv(r'ZenlyBackUpData.csv', index=None)
print("一生足迹App数据转化完成，现在可以导入了！")
