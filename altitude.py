import sys
import matplotlib.pyplot as plt
from fitparse import FitFile
import numpy as np

# 用于将 fit 文件中的位置信息（经纬度）转换为度
def convert_semicircles_to_degrees(semicircle):
    return semicircle * (180.0 / 2**31)

# 计算两点之间的距离
def calculate_distance(lat1, lon1, lat2, lon2):
    # 将经纬度转换为弧度
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # 地球半径 (km)
    R = 6371.0
    
    # 计算经纬度差值
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    
    # 使用 Haversine 公式计算两点间距离
    a = np.sin(dlat/2.0)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon/2.0)**2
    c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
    
    distance = R * c * 1000  # 转换为米
    return distance

# 解析 .fit 文件获取经纬度和高度
def parse_fit_file(file_path):
    fitfile = FitFile(file_path)
    latitudes = []
    longitudes = []
    altitudes = []  # 存储高度数据

    # 遍历所有的记录，找到包含位置和高度信息的记录
    for record in fitfile.get_messages('record'):
        # 获取纬度、经度和高度
        latitude = record.get_value('position_lat')
        longitude = record.get_value('position_long')
        altitude = record.get_value('altitude')

        if latitude is not None and longitude is not None and altitude is not None:
            latitudes.append(convert_semicircles_to_degrees(latitude))
            longitudes.append(convert_semicircles_to_degrees(longitude))
            altitudes.append(altitude)

    return latitudes, longitudes, altitudes

# 绘制高度变化图
def plot_altitude_change(latitudes, longitudes, altitudes):
    plt.figure(figsize=(14, 6))

    # 计算每个点的距离
    distances = [0]
    for i in range(1, len(latitudes)):
        dist = calculate_distance(latitudes[i-1], longitudes[i-1], latitudes[i], longitudes[i])
        distances.append(distances[-1] + dist)

    # 绘制高度变化曲线
    plt.plot(distances, altitudes, color='white', linewidth=2)

    # 填充曲线下方的区域
    plt.fill_between(distances, 0, altitudes, color='white', alpha=0.3)

    # 设置背景为黑色
    plt.gca().set_facecolor('black')

    # 隐藏 x, y 轴标签
    plt.xticks([])
    plt.yticks([])
    plt.ylim(40, np.max(altitudes))
    # 保存图像，保证背景透明度和背景颜色
    plt.savefig('altitude.png', bbox_inches='tight', pad_inches=0, facecolor='black')

# 主函数
def main(file):
    file_path = file  # 根据您的说明更改为 'test.fit'
    latitudes, longitudes, altitudes = parse_fit_file(file_path)
    plot_altitude_change(latitudes, longitudes, altitudes)

# 调用主函数
main(sys.argv[1])

