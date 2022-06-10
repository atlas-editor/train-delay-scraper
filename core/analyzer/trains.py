import csv


class Train:
    def __init__(self, train_id, train_type, train_name, start, terminal, start_time, arrival_time):
        """
        initialize an instance of a Train with all relevant info

        :param train_id:
        :param train_type:
        :param train_name:
        :param start:
        :param terminal:
        :param start_time:
        :param arrival_time:
        """
        self.id = train_id
        self.train_type = train_type
        self.train_name = train_name
        self.start = start
        self.terminal = terminal
        self.start_time = start_time
        self.arrival_time = arrival_time


class SetOfTrains:
    def __init__(self, trains=None):
        if trains is None:
            trains = set()
        self.trains = trains

    @classmethod
    def from_file(cls, filename):
        """
        create a SetOfTrains instance from a csv file(with header) in format=
        (train_type,train_id,train_name,start,start_time,arrival_time,arrival)

        :param filename: file from which to load data
        :return: an instance of SetOfTrains with loaded data from filename
        """
        all_trains = set()

        with open(filename, 'r') as input_file:
            reader = csv.reader(input_file)

            # skip the header
            iterator = iter(reader)
            next(iterator)

            for row in iterator:
                train = Train(int(row[1]), row[0], row[2], row[3], row[6], row[4], row[5])
                all_trains.add(train)

        return cls(all_trains)

    def add(self, train):
        self.trains.add(train)

    def find(self, train_id):
        for train in self.trains:
            if train.id == train_id:
                return train
