import logging
from datetime import datetime

from bs4 import BeautifulSoup

from core.parser.parser_exceptions import ElementNotFoundError, TrainNotInTerminalError, ArrivalDataLoadingError
from core.analyzer.trains import Train
from core.utilities import utils


class ZSRParser:

    def __init__(self, response, train: Train):
        """
        initialize parsing from the given response

        :param response: html file from which to parse data
        :param train: the train for which the delay data is being parsed
        """
        # save the current train
        self.train = train

        # use BeautifulSoup to parse the html file
        self.parser = BeautifulSoup(response, 'html.parser')

        # locate the (necessary) delay table
        self.delay_table = self.parser.find('table', class_='trainDelayTable')
        if self.delay_table is None:
            # if there is no delay table we can't load any data
            raise ElementNotFoundError('train_delay_table', "couldn't load the delay table")

        # locate the (necessary) last recorded station
        last_station_tag = self.delay_table.find('td', string='Informácia zo stanice')
        if last_station_tag:
            self.last_station = last_station_tag.findNextSibling().text.strip()
        else:
            # without this info we cannot decide if the train arrived in the terminal station
            raise ElementNotFoundError('last_station_info', "couldn't load the last station")

        self.arrived = (self.last_station == self.train.terminal)

        if self.arrived:
            try:
                self.actual_arrival = self.__get_arrival('actual')
                self.scheduled_arrival = self.__get_arrival('scheduled')
                self.delay = utils.get_difference_in_minutes_from_datetime(self.actual_arrival, self.scheduled_arrival)
            except ValueError:
                raise ArrivalDataLoadingError("couldn't load arrival time(s)")
        else:
            # as the data collecting will occur during the night this is an error
            raise TrainNotInTerminalError(self.last_station, "train hasn't reached the terminal")

    def __get_arrival(self, arrival_type):
        """
        return arrival based on type

        :param arrival_type: the type of arrival, either 'actual' or 'scheduled'
        :return:
        if 'actual' return actual time of arrival
        if 'scheduled' return scheduled time of arrival
        else return None
        """
        if arrival_type == "actual":
            search_string = "Čas príchodu"
        elif arrival_type == "scheduled":
            search_string = "Čas v stanici podľa CP"
        else:
            raise TypeError("the specified arrival_type must be either 'actual' or 'scheduled'")

        # find the appropriate tag
        arrival_tag = self.delay_table.find('td', string=search_string)

        if arrival_tag is None:
            # if either type of arrival is missing we cannot continue
            logging.error('[' + str(self.train.id) + '] the ' + arrival_type + ' arrival time is missing')
            raise ElementNotFoundError(arrival_type + '_arrival_time',
                                       "couldn't load " + arrival_type + " arrival time")

        arrival_string = arrival_tag.findNextSibling().text.strip()  # format='dd.mm. hh:mm'

        # arrival_string does not specify the year
        arrival_string_with_year = utils.add_current_year_to_datetime_string(
            arrival_string)  # format='dd.mm.yyyy hh:mm'

        # return the appropriate datetime, respecting the given format
        return datetime.strptime(arrival_string_with_year, '%d.%m.%Y %H:%M')
