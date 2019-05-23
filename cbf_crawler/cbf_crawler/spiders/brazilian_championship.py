# -*- coding: utf-8 -*-
import scrapy
from scrapy.spiders import CrawlSpider
from cbf_crawler.items import MatchSummaryItem
import dateparser


class BrazilianChampionshipSpider(CrawlSpider):
    name = 'brazilian_championship'
    allowed_domains = ['cbf.com.br']
    start_urls = ['http://www.cbf.com.br/futebol-brasileiro/competicoes/'
                  'campeonato-brasileiro-serie-a/2018']

    def parse(self, response):

        # Get the links to all championship matches
        matches_details_urls = response.css(
            '.aside-rodadas ul li .partida-desc a::attr(href)'
        ).extract()

        for url in matches_details_urls:
            yield scrapy.Request(url, callback=self.parse_match_summary)

    def parse_match_summary(self, response):

        match_number = self._get_match_number(response)
        match_datetime = self._get_match_datetime(response)
        match_location = self._get_match_location(response)
        team_names = self._get_team_names(response)
        scoreboard = self._get_scoreboard(response)

        item = {
            'match_number': match_number,
            'match_datetime': match_datetime,
            'stadium_name': match_location['stadium_name'],
            'city': match_location['city'],
            'state': match_location['state'],
            'team_home_name': team_names['team_home_name'],
            'team_visitor_name': team_names['team_visitor_name'],
            'team_home_goals': scoreboard['team_home_goals'],
            'team_visitor_goals': scoreboard['team_visitor_goals'],
        }

        yield MatchSummaryItem(item)

    def _get_match_number(self, response):
        """
        The match number is the unique identifier of a championship match
        """

        raw_match_number = response.css(
            '.section-placar-header div.col-sm-3.text-right span::text'
        ).extract_first()
        return int(raw_match_number.strip().replace('Jogo: ', ''))

    def _get_team_names(self, response):
        """
        Team names comes together with state, like this: Criciuma - SC
        So, we need to remove the last 5 characters of these strings
        """

        css_query = '.time-nome::text'
        team_names_raw = response.css(css_query).extract()

        team_names = list(
            map(
                lambda name: name[:-5].strip(),
                team_names_raw
            )
        )

        props = ['team_home_name', 'team_visitor_name']
        return dict(zip(props, team_names))

    def _get_scoreboard(self, response):
        """
        Scoreboard is the match results (goals)
        """

        css_query = '.time-gols:not([class*="hidden"])::text'
        scoreboard_raw = response.css(css_query).extract()

        scoreboard = list(
            map(
                lambda goals: int(goals),
                scoreboard_raw
            )
        )

        props = ['team_home_goals', 'team_visitor_goals']
        return dict(zip(props, scoreboard))

    def _get_match_datetime(self, response):

        css_query = '.section-content-header .text-2::text'
        texts = response.css(css_query).extract()

        date_raw = texts[2]
        time_raw = texts[3]
        datetime_raw = ' '.join([date_raw, time_raw])

        datetime = dateparser.parse(datetime_raw,
                                    languages=['pt'],
                                    settings={'TIMEZONE': '-0300'})

        return datetime

    def _get_match_location(self, response):

        css_query = '.section-content-header .text-2::text'
        texts = response.css(css_query).extract()

        full_location_raw = texts[1].strip().split('-')
        stadium_name = full_location_raw[0]
        city = full_location_raw[1]
        state = full_location_raw[2]

        return {
            'stadium_name': stadium_name.strip(),
            'city': city.strip(),
            'state': state.strip()
        }
