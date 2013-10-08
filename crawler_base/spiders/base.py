# coding=utf-8
import urlparse
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor

from bs4 import BeautifulSoup
import datetime
import re

import crawler_base.items as items


class BaseSpider(CrawlSpider):
    name = 'base'
    #REQUIRED: allowed domains
    allowed_domains = ['contractaciopublica.gencat.cat', ]

    #REQUIRED: start url
    start_urls = [
            'https://contractaciopublica.gencat.cat/ecofin_pscp/AppJava/search.pscp?reqCode=searchPcan&pagingPage=1&advancedSearch=false&lawType=2', ]

    #REQUIRED: rules to follow pagination and parser pages
    rules = [
        Rule(SgmlLinkExtractor(
            allow=['/ecofin_pscp/AppJava/search\.pscp\?reqCode=searchPcan&lawType=2&advancedSearch=false&pagingPage=\d+&'], unique=True), follow=True),
        Rule(SgmlLinkExtractor(
            allow=['/ecofin_pscp/AppJava/awardnotice\.pscp\?reqCode=viewPcan&lawType=2&advancedSearch=false&idDoc=\d+&'], unique=True), 'parse_item'),]

    def sibling_exist(self, dom, element_text):
        element = dom.find('dt', text=element_text)
        if element:
            return element.nextSibling.nextSibling.text.replace('\t','')\
                          .replace('\r','').replace('\n','').encode('utf-8')
        else:
            return ""


    def parse_item(self, response):
        html = BeautifulSoup(response.body)

        #REQUIRED: select item to save objects
        item = items.CrawlerBaseItem()
        query = urlparse.urlparse(response.url).query
        item['id'] = urlparse.parse_qs(query)['idDoc'].pop()
        item['url'] = response.url
        item['title'] = html.find('h2').text.strip('\r\n\t')

        denominacio_contracte = html.find('dl', id="denominacio-contracte")

        item['organ'] = self.sibling_exist(denominacio_contracte,
                                           "Òrgan de contractació:")
        item['record'] = self.sibling_exist(denominacio_contracte,
                                            "Codi d'expedient:")
        item['record_type'] = self.sibling_exist(denominacio_contracte,
                                                 "Tipus d'expedient:")
        item['contract_type'] = self.sibling_exist(denominacio_contracte,
                                                   "Tipus de contracte:")
        item['procedure'] = self.sibling_exist(denominacio_contracte,
                                               "Procediment de licitació:")

        contract_data = html.find('div', "dades-contracte")

        item['description'] = self.sibling_exist(contract_data,
                                                 "Descripció de la prestació:")
        item['estimate'] = self.sibling_exist(contract_data,
                                              "Pressupost bàsic de licitació:")
        item['geo'] = self.sibling_exist(contract_data, "Àmbit geogràfic:")
        item['budget'] = self.sibling_exist(contract_data,
                                            "Pressupost indicatiu:")
        item['electronic_bid'] = self.sibling_exist(contract_data,
                                                    "Subhasta electrònica")
        item['date_allocation'] = self.sibling_exist(contract_data,
                                                     "Data d'adjudicació del contracte:")
        item['contract_term'] = self.sibling_exist(contract_data,
                                                   "Termini per a la formalització del contracte:")
        item['received_offers'] = self.sibling_exist(contract_data,
                                                     "Número d'ofertes rebudes:")
        item['amount'] = self.sibling_exist(contract_data, "Import:")
        item['company'] = self.sibling_exist(contract_data,
                                             "Dades de l'empresa adjudicatària:")

        return item
