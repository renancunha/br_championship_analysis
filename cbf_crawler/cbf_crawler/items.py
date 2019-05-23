# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class MatchSummaryItem(scrapy.Item):
    match_number = scrapy.Field()
    match_datetime = scrapy.Field()
    stadium_name = scrapy.Field()
    city = scrapy.Field()
    state = scrapy.Field()
    team_home_name = scrapy.Field()
    team_visitor_name = scrapy.Field()
    team_home_goals = scrapy.Field()
    team_visitor_goals = scrapy.Field()
