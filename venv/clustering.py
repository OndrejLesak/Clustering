import matplotlib.pyplot as plt
import random as rd
import numpy as np
import time
import math


points = {}
colors = [
    '#f44336', '#e81e63', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4',
    '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107',
    '#ff9800', '#ff5722', '#795548', '#9e9e9e', '#607d8b', '#000000'
]


class Point():
    def __init__(self, x_val, y_val, color):
        self.x = x_val
        self.y = y_val
        self.c = color


def generateCoords(lb=-5000, ub=5000):
    x = rd.randint(lb, ub)
    y = rd.randint(lb, ub)
    return x, y


def generate_points(n, k):
    global points

    for _ in range(n):
        while True:
            x, y = generateCoords()
            key = (x, y)

            if key not in points:
                points[key] = Point(x, y, 'red')
                break

    while k > 0:
        keys = list(points.keys())
        i = rd.randint(0, len(points)-1)
        base_p = keys[i]
        x_off, y_off = generateCoords(-100, 100)

        while base_p[0] + x_off >= 5000 or base_p[0] + x_off <= -5000 \
            or base_p[1] + y_off >= 5000 or base_p[1] + y_off <= -5000:
            x_off, y_off = generateCoords(-100, 100)

        key = (base_p[0] + x_off, base_p[1] + y_off)
        if key not in points:
            points[key] = Point(base_p[0] + x_off, base_p[1] + y_off, 'red')
            k -= 1
        else:
            continue


def visualize_data(points, centers):
    data = list(points.values())
    x_arr = []
    y_arr = []
    colors = []
    for val in data:
        x_arr.append(val.x)
        y_arr.append(val.y)
        colors.append(val.c)

    plt.scatter(x=x_arr, y=y_arr, c=colors)
    plt.show()


def get_dist(c_1, c_2):
    distance = math.sqrt(pow(c_1[0] - c_2[0], 2) + pow(c_1[1] - c_2[1], 2))
    return distance


def get_mean(center, points):
    x_sum = 0
    y_sum = 0
    cnt = 0

    for point in points:
        if points[point].c == center.c:
            x_sum += point[0]
            y_sum += point[1]
            cnt += 1

    if cnt != 0:
        new_center = (x_sum/cnt, y_sum/cnt)
        return new_center
    else:
        return None


def get_distance():
    pass


def init_clusters(centers):
    global points

    center_cords = list(centers.keys())
    closest_r = 0
    closest_cord = None
    for point in points:
        closest_r = 0
        closest_cord = None
        for center in center_cords:
            distance = get_dist(point, center)
            if closest_r == 0:
                closest_r = distance
                closest_cord = center
                continue

            if distance < closest_r:
                closest_r = distance
                closest_cord = center

        points[point].c = centers[closest_cord].c


def k_means(k, type, iter=15):
    centers = {}

    if type == 'centroid':
        for i in range(k):
            while True:
                green_light = True
                x, y = generateCoords()
                key = (x, y)

                cent_cor = list(centers.keys()) if centers is not None else []
                if key not in centers:
                    for cor in cent_cor:
                        if get_dist(key, cor) < 1000:
                            green_light = False
                            break

                    if green_light:
                        centers[key] = Point(x, y, colors[i])
                        break

    for i in range(iter):
        init_clusters(centers)
        visualize_data(points, centers)

        new_centers = {}
        for center in centers:
            new_center = get_mean(centers[center], points)
            if new_center is not None:
                centers[center].x = new_center[0]
                centers[center].y = new_center[1]
                new_centers[new_center] = centers[center]
            else:
                new_centers[center] = centers[center]

        centers = new_centers.copy()


def main():
    t1 = time.time()
    generate_points(20, 20000)
    k_means(20, 'centroid', 10)
    t2 = time.time()

    print(f'{t2-t1:.2f}s')


if __name__ == '__main__':
    main()