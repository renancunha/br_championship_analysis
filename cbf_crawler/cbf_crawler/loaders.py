# -*- coding: utf-8 -*-
from scrapy.loader import ItemLoader
from .items import MatchItem
from scrapy.loader.processors import TakeFirst, Compose, MapCompose, Identity
import dateparser
from w3lib.html import remove_tags


def clean_match_number(value):
    return int(
        value.strip().replace('Jogo: ', '')
    )


def clean_team_name(value):
    return value[:-5].strip()


def parse_local_datetime(values):
    complete_datetime_string = ''.join(values)
    return dateparser.parse(
        complete_datetime_string,
        languages=['pt'],
        settings={'TIMEZONE': '-0300'}
    )


def extract_stadium_name(location):
    return location.split('-')[0]


def extract_city(location):
    return location.split('-')[1]


def extract_state(location):
    return location.split('-')[2]


def count_values(values):
    return str(len(values))


def to_int(str):
    return int(str)


class TakeLast(object):
    """
    A processor to get the last object, similar to TakeFirst
    """

    def __call__(self, values):
        return values[-1]


class MatchItemLoader(ItemLoader):

    # defaults
    default_item_class = MatchItem
    default_output_processor = TakeFirst()

    # input processors
    match_number_in = MapCompose(clean_match_number)
    team_home_name_in = MapCompose(clean_team_name)
    team_visitor_name_in = MapCompose(clean_team_name)
    match_datetime_in = Compose(parse_local_datetime)
    stadium_name_in = MapCompose(remove_tags, extract_stadium_name, str.strip)
    city_in = MapCompose(remove_tags, extract_city, str.strip)
    state_in = MapCompose(remove_tags, extract_state, str.strip)
    yellow_cards_home_in = Compose(count_values)
    yellow_cards_visitor_in = Compose(count_values)
    red_cards_home_in = Compose(count_values)
    red_cards_visitor_in = Compose(count_values)

    # output processors
    yellow_cards_home_out = Compose(TakeFirst(), to_int)
    yellow_cards_visitor_out = Compose(TakeFirst(), to_int)
    red_cards_home_out = Compose(TakeFirst(), to_int)
    red_cards_visitor_out = Compose(TakeFirst(), to_int)
    team_home_goals_out = Compose(TakeFirst(), to_int)
    team_visitor_goals_out = Compose(TakeLast(), to_int)
