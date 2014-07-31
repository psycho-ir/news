__author__ = 'SOROOSH'
import  common
import tabnak
import isna

def get_crawler(agency_name):
    return common.crawler_registry[agency_name]
