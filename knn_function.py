import math
import csv
import operator


def load_data(filename1, filename2, training_set=[], minmax_set=[]):
    with open(filename1, 'rb') as csvfile:
        lines = csv.reader(csvfile)
        data_set = list(lines)

        for x in range(len(data_set)):

            for y in range(13):
                data_set[x][y] = float(data_set[x][y])

            # Preparing training data for KNN
            training_set.append(data_set[x])

    with open(filename2, 'rb') as csvfile2:
        lines1 = csv.reader(csvfile2)
        minmax_data = list(lines1)

        minmax_set.append(minmax_data[0])
        minmax_set.append(minmax_data[1])


# Distance calculation Function
def calculate_distance(instance1, instance2, length, freq_disconnect_min, freq_disconnect_max,
                       neighbouring_session_min, neighbouring_session_max):

    distance = 0
    distance_euclidean = 0

    for x in range(length):

        #  Calculate hamming distance
        if x == 2:
            if instance1[x] == instance2[x]:
                distance += 0
            else:
                distance += 2

        # calculating Euclidean distance for frequent disconnection and neighbouring session attributes
        elif x == 3:
            max_freq_disconnect = freq_disconnect_max
            min_freq_disconnect = freq_disconnect_min
            temp1 = (instance1[x] - min_freq_disconnect) / (max_freq_disconnect - min_freq_disconnect)
            temp2 = (instance2[x] - min_freq_disconnect) / (max_freq_disconnect - min_freq_disconnect)
            distance_euclidean += pow((temp1 - temp2), 2)

        elif x == 4:
            max_neighbouring_session = neighbouring_session_max
            min_neighbouring_session = neighbouring_session_min
            temp1 = (instance1[x] - min_neighbouring_session) / (max_neighbouring_session - min_neighbouring_session)
            temp2 = (instance2[x] - min_neighbouring_session) / (max_neighbouring_session - min_neighbouring_session)
            distance_euclidean += pow((temp1 - temp2), 2)

        else:
            if instance1[x] == instance2[x]:
                distance += 0
            else:
                distance += 1

    distance += math.sqrt(distance_euclidean)
    return distance


# Calculating neighbors based on distance
def get_neighbors(distances, k):

    neighbors = []
    for x in range(k):
        neighbors.append(distances[x][0])

    return neighbors


# Selecting or making decision
def get_response(neighbors):
    class_votes = {}

    for x in range(len(neighbors)):
        response = neighbors[x][-1]

        if response in class_votes:
            class_votes[response] += 1
        else:
            class_votes[response] = 1
    sorted_votes = sorted(class_votes.iteritems(), key=operator.itemgetter(1), reverse=True)

    return sorted_votes[0][0]


def knn(testset, filename1, filename2):

    # Necessary variables declaration
    trainingSet = []
    min_max_set = []
    k_value = 3

    load_data(filename1, filename2, trainingSet, min_max_set)
    frequent_disconnect_min = float(min_max_set[0][0])
    frequent_disconnect_max = float(min_max_set[1][0])
    neighbouring_session_min = float(min_max_set[0][1])
    neighbouring_session_max = float(min_max_set[1][1])

    calculated_distance = []

    length = len(testset)

    for x in range(len(trainingSet)):
        dist = calculate_distance(testset, trainingSet[x], length, frequent_disconnect_min,
                                  frequent_disconnect_max, neighbouring_session_min, neighbouring_session_max)
        calculated_distance.append((trainingSet[x], dist))

    calculated_distance.sort(key=operator.itemgetter(1))

    calculated_neighbors = get_neighbors(calculated_distance, k_value)

    res_neighbours = calculated_neighbors[0][0:-1]

    result = get_response(calculated_neighbors)

    return {"result": result, "neighbours": res_neighbours}
