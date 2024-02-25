from pathlib import Path
import requests

import scrapy
import json

class WeatherSpider(scrapy.Spider):
    name = "weather"

    def start_requests(self):
        urls = [
            "https://meteo.gov.tm",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        cities = response.css(".weather-wrapper .flip .province-item")

        weather = []

        for city in cities:
            cells = city.css('td::text').getall()
            img = city.css('img::attr(src)').get()
            degree = cells[0]
            c = {
                    'degree': degree,
                    'img': img,
                    'name': cells[1]
                    }
            weather.append(c) 
            
        data = {'cities': json.dumps(weather)}
        url = 'http://216.250.12.31:8777/api/weather'
        response = requests.post(url, data)
            