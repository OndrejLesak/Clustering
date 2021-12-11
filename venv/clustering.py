import matplotlib.pyplot as plt
import matplotlib.markers as markers
import random as rd
import numpy as np
import time
import math


rd.seed(2)

clusters = {}
points = {}
colors = [
    '#ff0000', '#ffbe7d', '#9c27b0', '#673ab7', '#3f51b5', '#2196f3', '#03a9f4',
    '#00bcd4', '#009688', '#4caf50', '#8bc34a', '#cddc39', '#ffeb3b', '#ffc107',
    '#ff9800', '#ff5722', '#795548', '#9e9e9e', '#607d8b', '#ffc0cb'
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
    markers = []
    for val in data:
        x_arr.append(val.x)
        y_arr.append(val.y)
        colors.append(val.c)
        markers.append('.')

    center_data = list(centers.values())
    for val in center_data:
        x_arr.append(val.x)
        y_arr.append(val.y)
        colors.append('#000000')


    plt.scatter(x=x_arr, y=y_arr, c=colors)
    plt.show()


def get_dist(c_1, c_2):
    # distance = math.sqrt(pow(c_1[0] - c_2[0], 2) + pow(c_1[1] - c_2[1], 2))
    distance = abs(c_1[0] - c_2[0]) + abs(c_1[1] - c_2[1])
    return distance


def get_mean_cords(cluster):
    x_sum = 0
    y_sum = 0
    cnt = 0

    for point in cluster:
        x_sum += point[0]
        y_sum += point[1]
        cnt += 1

    if cnt != 0:
        new_center = (x_sum/cnt, y_sum/cnt)
        return new_center
    else:
        return None


def get_medoid(cluster):
    shortest_dist = 0
    shortest_cords = None

    for point in cluster:
        sum = 0
        for other in cluster:
            if point == other:
                continue

            sum += get_dist(point, other)

        if (sum/len(cluster) < shortest_dist) or shortest_dist == 0:
            shortest_dist = sum
            shortest_cords = point

    return shortest_cords


def init_clusters(centers, points):
    global clusters
    clusters = {}

    for point in points:
        closest_r = 0
        closest_cord = None
        if point in centers:
            continue

        for center in centers:
            distance = get_dist(point, center)
            if closest_r == 0:
                closest_r = distance
                closest_cord = center
                continue

            if distance < closest_r:
                closest_r = distance
                closest_cord = center

        points[point].c = centers[closest_cord].c

        if centers[closest_cord].c not in clusters:
            clusters[centers[closest_cord].c] = {}
        clusters[points[point].c][point] = points[point]


def average_dist(center, points):
    cnt = 0
    sum = 0
    for point in points:
        sum += get_dist(center, point)
        cnt += 1

    return sum/cnt


def k_means(k, points, iter=15, centers = {}):

    for i in range(k):
        while True:
            green_light = True
            x, y = generateCoords()
            key = (x, y)

            if key not in centers:
                for cor in centers:
                    if get_dist(key, cor) < 1000:
                        green_light = False
                        break

                if green_light:
                    centers[key] = Point(x, y, colors[i])
                    break

    for i in range(iter):
        init_clusters(centers, points)

        new_centers = {}
        for center in centers:
            if centers[center].c in clusters:
                new_center = get_mean_cords(clusters[centers[center].c])
                if new_center is not None:
                    centers[center].x = new_center[0]
                    centers[center].y = new_center[1]
            else:
                new_center = center

            new_centers[new_center] = centers[center]

        centers = new_centers.copy()

    return points, centers


def k_medoids(k, points, iter=10):
    centers = {}
    keys = list(points.keys())

    for i in range(k):
        while True:
            green_light = True
            j = rd.randint(0, len(points) - 1)
            key = keys[j]

            if key not in centers:
                for cor in centers:
                    if get_dist(key, cor) < 400:
                        green_light = False
                        break

                if green_light:
                    centers[key] = points[key]
                    centers[key].c = colors[i]
                    break

    for i in range(iter):
        init_clusters(centers, points)

        new_centers = {}
        for center in centers:
            new_center = get_medoid(clusters[centers[center].c])
            new_centers[new_center] = clusters[centers[center].c][new_center]

        centers = new_centers.copy()

    return points, centers


def divisive(k, points):
    color_index = 0
    centers = {}
    max_dist, max_cord = 0, None
    key1, key2 = None, None

    while True:
        key1 = generateCoords()
        key2 = generateCoords()
        if key1 == key2:
            continue
        break

    centers[key1] = Point(key1[0], key1[1], colors[color_index])
    color_index += 1
    centers[key2] = Point(key2[0], key2[1], colors[color_index])

    points, centers = k_means(2, points, centers=centers)

    # CALCULATE DISTANCES
    for center in centers:
        avg_dist = average_dist(center, clusters[centers[center].c])
        if max_dist == 0:
            max_dist = avg_dist
            max_cord = center

        elif avg_dist > max_dist:
            max_dist = avg_dist
            max_cord = center

    return points, centers



def main():
    t1 = time.time()
    generate_points(20, 10000)

    # final_points, final_centers = k_means(20, points, 10)
    # final_points, final_centers = k_medoids(20, points, 10)
    final_points, final_centers = divisive(20, points)
    visualize_data(final_points, final_centers)
    t2 = time.time()

    print(f'{t2-t1:.2f}s')


if __name__ == '__main__':
    main()