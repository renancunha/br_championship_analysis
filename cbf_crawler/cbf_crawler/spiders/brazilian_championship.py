# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from cbf_crawler.items import MatchItem
from cbf_crawler.loaders import MatchItemLoader
import dateparser


class BrazilianChampionshipSpider(CrawlSpider):
    name = 'brazilian_championship'
    allowed_domains = ['cbf.com.br']
    start_urls = ['http://www.cbf.com.br/futebol-brasileiro/competicoes/'
                  'campeonato-brasileiro-serie-a/2018']

    rules = [
        Rule(
            LinkExtractor(
                restrict_css='.aside-rodadas ul li .partida-desc a'
            ),
            callback='parse_match_summary'
        )
    ]

    def parse_match_summary(self, response):

        il = MatchItemLoader(response=response)

        il.add_css(
            'match_number',
            '.section-placar-header div.col-sm-3.text-right span::text'
        )

        il.add_css('team_home_name', '.time-left .time-nome::text')

        il.add_css('team_visitor_name', '.time-right .time-nome::text')

        il.add_css(
            'match_datetime',
            '.section-content-header .text-2:nth-child(n+2)::text'
        )

        # Query to the match location
        # We have the stadium name, city and state together in a string
        # This string is separated by dashes
        location_query = '.section-content-header ' \
                         '.col-sm-8 .text-2:nth-child(1)'

        il.add_css('stadium_name', location_query)
        il.add_css('city', location_query)
        il.add_css('state', location_query)

        # We use a base query to select the cards from the match
        # 2n + 1 = odd items (tags)
        # 2n = even items
        cards_query = '.jogo-escalacao .row:not(.hidden-sm) ' \
                      '.col-xs-6:nth-child(%s) .icon-%s-card'

        il.add_css('yellow_cards_home', cards_query % ('2n+1', 'yellow'))
        il.add_css('yellow_cards_visitor', cards_query % ('2n', 'yellow'))
        il.add_css('red_cards_home', cards_query % ('2n+1', 'red'))
        il.add_css('red_cards_visitor', cards_query % ('2n', 'red'))

        il.add_css(
            'team_home_goals',
            '.time-gols:not([class*="hidden"])::text'
        )
        il.add_css(
            'team_visitor_goals',
            '.time-gols:not([class*="hidden"])::text'
        )

        item = il.load_item()
        yield item
