__author__ = 'SOROOSH'
import  common
import tabnak
import isna
import irna

def get_crawler(agency_name):
    return common.crawler_registry[agency_name]
