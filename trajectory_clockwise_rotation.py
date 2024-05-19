import sys
import matplotlib.pyplot as plt
from fitparse import FitFile
import numpy as np

# 用于将 fit 文件中的位置信息（经纬度）转换为度
def convert_semicircles_to_degrees(semicircle):
    return semicircle * (180.0 / 2**31)

# 解析 .fit 文件获取经纬度
def parse_fit_file(file_path):
    fitfile = FitFile(file_path)
    latitudes = []
    longitudes = []

    # 遍历所有的记录，找到包含位置信息的记录
    for record in fitfile.get_messages('record'):
        # 获取纬度
        latitude = record.get_value('position_lat')
        # 获取经度
        longitude = record.get_value('position_long')

        if latitude is not None and longitude is not None:
            latitudes.append(convert_semicircles_to_degrees(latitude))
            longitudes.append(convert_semicircles_to_degrees(longitude))

    return latitudes, longitudes

# 绘制轨迹图
def plot_trajectory(latitudes, longitudes, destination):
    plt.figure(figsize=(14, 6))

    # 绘制轨迹，顺时针旋转90度，即交换 x 和 y，y 取反
    plt.plot(np.array(latitudes), -np.array(longitudes), color='white', linewidth=2)

    # 找出顺时针旋转90度后图上的最左边（西端）和最右边（东端）的点
    max_lat_index = np.argmax(latitudes)  # 最右边的点，顺时针旋转后的最西端
    min_lat_index = np.argmin(latitudes)  # 最左边的点，顺时针旋转后的最东端

    # 标记最左边（东端）的点
    plt.plot(latitudes[min_lat_index], -longitudes[min_lat_index]+0.001, marker='o', markersize=8, color='green')
    plt.text(latitudes[min_lat_index], -longitudes[min_lat_index], ' Bielefeld  ', fontsize=15, fontname='Gentium Basic', ha='right', va='bottom', color='white', rotation=0)

    # 标记最右边（西端）的点
    plt.plot(latitudes[max_lat_index], -longitudes[max_lat_index], marker='*', markersize=8, color='red')
    plt.text(latitudes[max_lat_index], -longitudes[max_lat_index], '  %s' % destination, fontsize=15, fontname='Gentium Basic', ha='left', va='center', color='white', rotation=0)

    # 设置坐标轴比例相同
    plt.gca().set_aspect('equal', adjustable='datalim')

    # 隐藏坐标轴
    plt.axis('off')

    # 设置背景为透明
    plt.gca().set_facecolor('black')

    # 保存图像，保证背景透明度
    plt.savefig('trajectory.png', bbox_inches='tight', pad_inches=0, facecolor='black')

# 主函数
def main(file, destination):
    file_path = file
    latitudes, longitudes = parse_fit_file(file_path)
    plot_trajectory(latitudes, longitudes, destination)

# 调用主函数
main(sys.argv[1], sys.argv[2])

