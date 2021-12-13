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
    def __init__(self, x_val, y_val, cluster_id, color='red'):
        self.x = x_val
        self.y = y_val
        self.cid = cluster_id
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
                points[key] = Point(x, y, -1, 'red')
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
            points[key] = Point(base_p[0] + x_off, base_p[1] + y_off, -1, 'red')
            k -= 1
        else:
            continue


def visualize_data(points, centers, title, precision, time):
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

    plt.title(title)
    plt.xlabel(f'Time: {time:.2f}s, Precision: {precision:.2f}%')

    plt.scatter(x=x_arr, y=y_arr, c=colors)
    plt.show()


def get_dist(c_1, c_2):
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
    length = len(cluster)

    for point in cluster:
        sum = 0
        for other in cluster:
            if point == other:
                continue

            sum += get_dist(point, other)

        if (sum/length < shortest_dist) or shortest_dist == 0:
            shortest_dist = sum
            shortest_cords = point

    return shortest_cords


def init_clusters(centers, points): # change
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

        points[point].cid = centers[closest_cord].cid

        if centers[closest_cord].cid not in clusters:
            clusters[centers[closest_cord].cid] = {}
        clusters[points[point].cid][point] = points[point]


def average_dist(center, points):
    cnt = 0
    sum = 0
    for point in points:
        sum += get_dist(center, point)
        cnt += 1

    return sum/cnt


def get_rand_point(points):
    keys = list(points.keys())
    i = rd.randint(0, len(keys)-1)
    return keys[i]


def merge_dict(dict1, dict2):
    return {**dict1, **dict2}


def assign_colors(clusts):
    i = 0
    clust = clusts.copy()
    for cluster in clust:
        for point in clust[cluster]:
            clust[cluster][point].c = colors[i]
        i += 1
    return clust


def calculate_precision(centers, clusters):
    correct = 0
    all_clusts = 0
    for center in centers:
        if centers[center].cid in clusters:
            if average_dist(center, clusters[centers[center].cid]) < 500:
                correct += 1

            all_clusts += 1

    return (correct/all_clusts)*100


def find_min(matrix):
    min_val = 10000
    x, y = -1, -1

    for i in range(len(matrix)):
        if not matrix[i]:
            continue

        _min = min(matrix[i])
        if _min < min_val:
            min_val = _min
            y = i
            x = matrix[i].index(_min)

    return y, x

##################### ALGORITHMS #####################
def k_means(k, points, iter=15, centers = {}, precision = False):
    global clusters
    if len(centers) == 0:
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
                        centers[key] = Point(x, y, i)
                        break

    init_clusters(centers, points)
    for i in range(iter):
        new_centers = {}
        for center in centers:
            if centers[center].cid in clusters:
                new_center = get_mean_cords(clusters[centers[center].cid])
                if new_center is not None:
                    centers[center].x = new_center[0]
                    centers[center].y = new_center[1]
            else:
                new_center = center

            new_centers[new_center] = centers[center]

        centers = new_centers.copy()
        init_clusters(centers, points)

    clusters = assign_colors(clusters)
    for clust in clusters:
        points = merge_dict(points, clusters[clust])

    if precision:
        precision_value = calculate_precision(centers, clusters)
        return points, centers, precision_value

    return points.copy(), centers.copy()


def k_medoids(k, points, iter=10):
    global clusters
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
                    centers[key].cid = i
                    break

    init_clusters(centers, points)
    for i in range(iter):
        new_centers = {}
        for center in centers:
            new_center = get_medoid(clusters[centers[center].cid])
            new_centers[new_center] = clusters[centers[center].cid][new_center]

        centers = new_centers.copy()
        init_clusters(centers, points)

    clusters = assign_colors(clusters)
    for clust in clusters:
        points = merge_dict(points, clusters[clust])

    precision_value = calculate_precision(centers, clusters)

    return points, centers, precision_value


def divisive(k, points):
    index = 0
    centers = {}
    asserted_clusters = {}

    if k != 1:
        # RANDOM KEY
        key1 = get_rand_point(points)
        key2 = get_rand_point(points)

        while key1 == key2:
            key2 = get_rand_point(points)

        centers[key1] = Point(key1[0], key1[1], index)
        index += 1
        centers[key2] = Point(key2[0], key2[1], index)
        index += 1

        new_points, new_centers = k_means(2, points, centers=centers) # creates 2 clusters
        k -= 2

        asserted_clusters = clusters.copy()  # assert first clusters
        centers = new_centers.copy()

        while k > 0:
            max_dist, max_cord = 0, None

            # CALCULATE DISTANCES
            for center in centers:
                avg_dist = average_dist(center, asserted_clusters[centers[center].cid])
                if max_dist == 0:
                    max_dist = avg_dist
                    max_cord = center
                elif avg_dist > max_dist:
                    max_dist = avg_dist
                    max_cord = center

            cluster_to_develop = asserted_clusters[centers[max_cord].cid].copy() # cluster we are dividing

            new_centers = {}
            key1 = get_rand_point(cluster_to_develop) # 1st random point from cluster
            key2 = get_rand_point(cluster_to_develop) # 2nd random point from cluster

            while key1 == key2:
                key2 = get_rand_point(cluster_to_develop)

            new_centers[key1] = Point(key1[0], key1[1], index)
            index += 1
            new_centers[key2] = Point(key2[0], key2[1], index)
            index += 1

            new_points, new_centers = k_means(2, cluster_to_develop, centers=new_centers) # compute new clusters

            asserted_clusters.pop(centers[max_cord].cid)
            centers.pop(max_cord)

            asserted_clusters = merge_dict(asserted_clusters, clusters)
            centers = merge_dict(centers, new_centers)

            k -= 1

        asserted_clusters = assign_colors(asserted_clusters)

        for clust in asserted_clusters:
            points = merge_dict(points, asserted_clusters[clust])

        precision_value = calculate_precision(centers, asserted_clusters)

        return points, centers, precision_value
    else:
        return points, centers


def agglomerative(k, points):
    global clusters
    matrix = []
    centers = []


    for point in points:
        centers.append(point)

    for i in range(len(centers)):
        matrix.append([])
        for j in range(i):
            matrix[i].append(get_dist(centers[i], centers[j]))

    for i, point in enumerate(points):
        clusters[i] = {}
        points[point].cid = i
        clusters[i][point] = points[point]


    while len(clusters) > k:
        min_y, min_x = find_min(matrix)

        cluster_1 = clusters[points[centers[min_x]].cid]
        cluster_2 = clusters[points[centers[min_y]].cid]

        clust_2_cid = points[centers[min_y]].cid

        for point in cluster_2:
            cluster_2[point].cid = points[centers[min_x]].cid

        clusters[points[centers[min_x]].cid] = merge_dict(cluster_1, cluster_2)

        for i in range(len(matrix[min_x])):
            matrix[min_x][i] = get_dist(centers[min_x], centers[i])

        for j in range(min_y + 1, len(matrix)):
            matrix[j][min_x] = get_dist(centers[min_x], centers[j])
            del matrix[j][min_y]

        del matrix[min_y]
        del centers[min_y]
        clusters.pop(clust_2_cid)

    new_centers = {}
    for center in centers:
        new_centers[center] = points[center]

    clusters = assign_colors(clusters)

    precission_value = calculate_precision(new_centers, clusters)

    return points, new_centers, precission_value


def main():
    t1 = time.time()
    generate_points(20, 10000)

    title = 'AGGLOMERATIVE'

    # final_points, final_centers, precision = k_means(20, points, 10, precision=True)
    # final_points, final_centers, precision = k_medoids(20, points, 10)
    # final_points, final_centers, precision = divisive(20, points)


    final_points, final_centers, precision = agglomerative(20, points)
    t2 = time.time()


    visualize_data(final_points, final_centers, title, precision, t2-t1)

    print(f'{t2-t1:.2f}s')
    print(f'Precision of the algorithm: {precision:.2f}%')


if __name__ == '__main__':
    main()