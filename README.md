# ApartmentsPricePredictorScrapper
This is a simple scrapper for web scrapping apartments data from: \
https://gratka.pl/  
\
Data scrapped in this project is used to create ML model in this repo:\
\
\
And created model is used in website in this repo:\
https://github.com/patrinhoo/ApartmentsPricePredictorAPI
\
You can check working website here:\
https://apartmentspricepredictor.herokuapp.com/  


## Testing
To test this scrapper you need to navigate to parent directory and type

```
scrapy crawl apartments_scraper
```


## Technologies
Project is created with:
* Scrapy
* Scrapy Selenium


## Setup
To run this project you need to install Scrapy and Scrapy Selenium (all dependencies in requirements.txt):
```
$ pip install scrapy
$ pip install scrapy-selenium
```
