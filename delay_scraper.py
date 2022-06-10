import logging
import os

from core.analyzer.delay import Delay
from core.crawler import crawler
from core.parser.parser import ZSRParser
from core.parser.parser_exceptions import *
from core.s_logger.s_logger import ScraperLogger
from core.utilities.data_utils import write_delay_to_csv
from core.utilities.run_utils import *


def main():
    # initialize the logger config and intro message
    logging.basicConfig(filename='data/logs.log', filemode='a', format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S', level=logging.DEBUG)       
    scraper_logger = ScraperLogger(logging.getLogger(__name__))

    # load all settings
    settings = load_settings()

    # pick the crawler specific settings
    crawler_settings = settings['crawler_settings']

    # pick the data_saver specific settings
    data_saver_settings = settings['data_saver_settings']

    # load url, and train ids and shuffle them
    url, trains_ids = crawler_settings['url'], load_train_ids(crawler_settings)

    # load all trains
    all_trains = load_trains(crawler_settings)

    # get headers for connection
    headers = crawler.get_headers()

    # keep track of new delays
    number_of_new_data = 0

    for train_id in trains_ids:
        scraper_logger._train_id = train_id
        scraper_logger.processing_train()

        # save current url and train
        current_url = url.format(train_id)
        current_train = all_trains.find(train_id)

        # try to connect to the current_url
        try:
            response = crawler.get_html(current_url, headers)
        except Exception as e:
            scraper_logger.loading_error(e)
            continue
        else:
            scraper_logger.connection_established()

        # parse the downloaded html file
        try:
            parser = ZSRParser(response, current_train)
        except (ElementNotFoundError, ArrivalDataLoadingError, TrainNotInTerminalError) as e:
            scraper_logger.loading_error(e)
            continue
        except Exception as e:
            scraper_logger.unexpected_error(e)
            continue
        else:
            scraper_logger.parsing_successful()

        # save all the relevant delay data
        delay = Delay.from_parser(parser)
        scraper_logger.log_delay(delay)

        # record the delay if new
        if write_delay_to_csv(data_saver_settings['folder_path'], delay):
            number_of_new_data = number_of_new_data + 1
            scraper_logger.new_delay()
        else:
            scraper_logger.old_delay()

    # final info, log if some delay data is missing
    missing = (number_of_new_data != len(trains_ids))
    scraper_logger.finalise(number_of_new_data, missing)


if __name__ == '__main__':
    main()

