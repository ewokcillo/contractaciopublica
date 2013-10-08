# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy.item import Item, Field

class CrawlerBaseItem(Item):
    # define the fields for your item here like:
    id = Field()
    organ = Field()
    record = Field()
    record_type = Field()
    contract_type = Field()
    procedure = Field()
    description = Field()
    estimate = Field()
    geo = Field()
    budget = Field()
    electronic_bid = Field()
    date_allocation = Field()
    contract_term = Field()
    received_offers = Field()
    amount = Field()
    company = Field()
    url = Field()
    title = Field()
