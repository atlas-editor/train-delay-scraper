import csv
from os.path import exists

from core.analyzer.delay import Delay


def write_delay_to_csv(working_path, delay: Delay):
    """
    writes the given delay into the appropriate csv file according to the train_id

    :param working_path: where the delays are stored
    :param delay: the delay to be recorded
    :return: True if the delay hasn't yet been recorder,
    False if the csv file already contains the given delay (only checks the last entry for duplicity)
    """
    working_csv_path = working_path + str(delay.train.id) + '.csv'

    # if the file exists check for duplicates
    if exists(working_csv_path):
        with open(working_csv_path, 'r') as read_file:
            rows = read_file.read().splitlines()
            for row in rows:
                date = row[:10] # row format='yyyy-mm-dd, ...'

                # if the date matches any other, the delay has already been recorded
                if date == str(delay.date):
                    return False

    # if the file does not exist or the last entry does not match the current delay, record it
    with open(working_csv_path, 'a') as output_file:
        writer = csv.writer(output_file)
        writer.writerow(delay.get_list())
        return True
