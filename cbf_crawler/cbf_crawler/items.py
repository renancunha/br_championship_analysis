# -*- coding: utf-8 -*-
import scrapy


class MatchItem(scrapy.Item):
    match_number = scrapy.Field()
    match_datetime = scrapy.Field()
    stadium_name = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    team_home_name = scrapy.Field()
    team_visitor_name = scrapy.Field()
    team_home_goals = scrapy.Field()
    team_visitor_goals = scrapy.Field()
    yellow_cards_home = scrapy.Field()
    yellow_cards_visitor = scrapy.Field()
    red_cards_home = scrapy.Field()
    red_cards_visitor = scrapy.Field()
