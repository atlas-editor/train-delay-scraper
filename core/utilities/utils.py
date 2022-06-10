import re
from datetime import datetime, date


def add_current_year_to_datetime_string(datetime_string: str):
    """
    convert string in format 'dd.mm. hh:mm' to 'dd.mm.(current_year) hh:mm'

    DISCLAIMER: as parsing during the night is expected if the date in datetime_string matches '31.12. xx:yy'
    the previous year is used

    :param datetime_string: a given datetime in format='dd.mm. hh:mm'
    :return: string in format='dd.mm.(current_year) hh:mm'
    """
    current_year = date.today().year

    # regex for checking the format of the given string, this is just a general check
    # strings such as '33.44. 55:66' get a pass
    datetime_format_regex = re.compile("\d{2}\.\d{2}\. \d{2}:\d{2}")

    if not (len(datetime_string) == 12 and datetime_format_regex.match(datetime_string)):
        # raise a ValueError if the format does not match
        raise ValueError("The given string: '{}' does not match the format: 'dd.mm. hh:mm'".format(datetime_string))

    # if the date of the given string is 31.12. and we are checking it on 1.1. the previous year has to be used
    if datetime_string[:6] == "31.12." and date.today().day == 1 and date.today().month == 1:
        current_year = current_year - 1

    result = datetime_string[:6] + str(current_year) + datetime_string[6:]

    # this is a thorough check for the format, might raise ValueError
    datetime.strptime(result, '%d.%m.%Y %H:%M')

    return result


def get_difference_in_minutes_from_datetime(dt0, dt1):
    return int((dt0 - dt1).total_seconds()) // 60
