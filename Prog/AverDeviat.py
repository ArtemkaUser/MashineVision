from math import sqrt


class AverDev:
    def __init__(self, array_1, array_2):
        self.first_array = array_1
        self.second_array = array_2
        self.max_deviation, self.first_column_for_table, self.second_column_for_table = self.max_deviation()
        self.average, self.average_dev = self.deviation()

    def max_deviation(self):
        deviation = []
        max_id = 0
        for i in range(len(self.first_array)-1):
            deviation.append(abs(self.first_array[i]-self.second_array[i]))
        maximum = deviation[0]
        for i in range(len(deviation)):
            if maximum < deviation[i]:
                maximum = deviation[i]
                max_id = i
        first_array, second_array = self.create_table(max_id)
        return max(deviation), first_array, second_array

    def deviation(self):
        temp = 0
        average = 0
        deviation = []
        for i in range(len(self.first_array)):
            deviation.append(self.first_array[i] - self.second_array[i])
            average += deviation[i]
        average = average/len(deviation)
        for i in range(len(self.first_array)):
            temp += pow(deviation[i]-average, 2)
        average_deviation = sqrt(temp / len(deviation))
        return average_deviation, average

    def create_table(self, max_id):
        first_array, second_array = [], []
        if max_id - 12 < 0:
            for i in range(24):
                first_array.append(self.first_array[i])
                second_array.append(self.second_array[i])
        elif max_id + 12 > len(self.first_array) - 1:
            for i in range(len(self.first_array) - 24, len(self.first_array)):
                first_array.append(self.first_array[i])
                second_array.append(self.second_array[i])
        else:
            begin_id = max_id - 12
            end_id = max_id + 12
            for i in range(begin_id, end_id):
                first_array.append(self.first_array[i])
                second_array.append(self.second_array[i])
        return first_array, second_array
