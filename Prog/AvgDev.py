from math import sqrt


class AverDev:
    def __init__(self, first, second):
        self.first = first
        self.second = second
        self.max_id = False

    def max_deviation(self):
        deviation = list(map(lambda x, y: abs(x - y), self.first, self.second))
        self.max_id = deviation.index(max(deviation))
        return max(deviation)

    def deviation(self):
        temp = 0
        deviation = list(map(lambda x, y: abs(x - y), self.first, self.second))
        average = sum(deviation)/len(deviation)
        for i in range(len(self.first)):
            temp += pow(deviation[i]-average, 2)
        average_deviation = sqrt(temp / len(deviation))
        return average_deviation, average

    def create_table(self):
        first, second = [], []
        if self.max_id - 12 < 0:
            for i in range(24):
                first.append(self.first[i])
                second.append(self.second[i])
        elif self.max_id + 12 > len(self.first) - 1:
            for i in range(len(self.first) - 24, len(self.first)):
                first.append(self.first[i])
                second.append(self.second[i])
        else:
            begin_id = self.max_id - 12
            end_id = self.max_id + 12
            for i in range(begin_id, end_id):
                first.append(self.first[i])
                second.append(self.second[i])
        return first, second
