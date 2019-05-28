# CBF Crawler

This is a Scrapy project that contains a spider called ``brazilian_championship``. 
This spider was developed aiming to crawl data from the [CBF (Brazilian Football Confederation)](https://www.cbf.com.br/) website.

The idea of this project is to extract information about each football match of the Brazilian Football Championship. 
This information could be used to do an analytic study of the championship or even to create machine learning models based on that data.

## Item Schema

We collect a lot of information about each match. The schema below shows an example of a scrapped item:
````
{
   "match_number":342,
   "team_home_name":"Corinthians",
   "team_visitor_name":"Vasco da Gama",
   "match_datetime":"2018-11-17 19:00:00",
   "stadium_name":"Arena Corinthians",
   "city":"Sao Paulo",
   "state":"SP",
   "yellow_cards_home":2,
   "yellow_cards_visitor":2,
   "red_cards_home":0,
   "red_cards_visitor":0,
   "team_home_goals":1,
   "team_visitor_goals":0
}
````

You can see an example of a page crawled to get those informations [here](https://www.cbf.com.br/futebol-brasileiro/competicoes/campeonato-brasileiro-serie-a/2018/232).

## Running

To run this spider and crawl the data, you just have to run:
````
scrapy crawl brazilian_championship
````

If you want to store the output in a csv file called ``output.csv``:
````
scrapy crawl brazilian_championship -o output.csv -t csv
````

## Development

The first version of the spider (the "MVP") was made using the most easy way to crawl the data: looping the links and
extracting the values from the tags directly in the spider code.

A much better version was made refactoring almost the entire code.
Now I'm using rules and link extractors to follow the links, and item loaders to process the collected data.
Item loaders is a very efficient pattern because allows the code reuse, testing, and others.

The source-code was written applying the PEP8 style guide for Python code.
