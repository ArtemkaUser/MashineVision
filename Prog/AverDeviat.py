from math import sqrt


class AverDev:
    def __init__(self, array_1, array_2, width=1, real_size=1):
        self.first = array_1
        self.second = array_2
        self.scale = width/real_size
        self.max_id = 0

    def max_deviation(self):
        deviation = list(map(lambda x, y: abs(x-y), self.first, self.second))
        self.max_id = deviation.index(max(deviation))
        return max(deviation)/self.scale

    def deviation(self):
        deviation = list(map(lambda x, y: x-y, self.first, self.second))
        average = sum(deviation)/len(deviation)
        return average/self.scale

    def average_dev(self):
        temp = 0
        deviation = list(map(lambda x, y: x - y, self.first, self.second))
        average = sum(deviation) / len(deviation)
        for i in range(len(self.first)):
            temp += pow(deviation[i] - average, 2)
        average_dev = sqrt(temp / len(deviation))
        return average_dev / self.scale

    def create_table(self, len_table=24):
        first_array, second_array = [], []
        if self.max_id - int(len_table/2) < 0:
            for i in range(24):
                first_array.append(self.first[i])
                second_array.append(self.second[i])
        elif self.max_id + int(len_table/2) > len(self.first) - 1:
            for i in range(len(self.first) - len_table, len(self.first)):
                first_array.append(self.first[i])
                second_array.append(self.second[i])
        else:
            begin_id = self.max_id - int(len_table/2)
            end_id = self.max_id + int(len_table/2)
            for i in range(begin_id, end_id):
                first_array.append(self.first[i])
                second_array.append(self.second[i])
        return first_array, second_array
