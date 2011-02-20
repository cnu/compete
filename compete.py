#!/usr/bin/python
#
# Copyright (c) 2011 by Srinivasan R
#
# Licensed under the MIT License. Please read the LICENSE file carefully.
#

'''A library that provides a python interface to the Compete.com API.

Please visit http://developer.compete.com/ and get a API Key to use this library.
'''

__author__ = 'Srinivasan R'
__version__ = '0.1'

import csv
import urllib2
from xml.etree import ElementTree as ET

strip = lambda x: x.strip() if x else None # Strip text else return None

def fetch(domain, apikey):
    d = {'domain':domain, 'apikey':apikey}
    api_url = "http://api.compete.com/fast-cgi/MI?d=%(domain)s&ver=3&apikey=%(apikey)s&size=large" %(d)
    response = urllib2.urlopen(api_url)
    xmlstring = response.read()
    return process(xmlstring)
    
def process(xmlstring):
    result = {}
    tree = ET.fromstring(xmlstring)
    dmn_tag = tree.find('dmn')
    result['domain'] = {'name':strip(dmn_tag.find('nm').text)}

    # Parse the 'Trust' tag
    trust_tag = dmn_tag.find('trust')
    result['domain']['trust'] = {'caption':trust_tag.get('caption'), # Trust
                                 'value':strip(trust_tag.find('val').text),
                                 'link':strip(trust_tag.find('link').text),
                                 'icon':strip(trust_tag.find('icon').text)}

    # Parse the 'rank' tag
    rank_tag = dmn_tag.find('rank')
    result['domain']['rank'] = {'caption':rank_tag.get('caption'), # Profile
                                'value':strip(rank_tag.find('val').text),
                                'link':strip(rank_tag.find('link').text),
                                'icon':strip(rank_tag.find('icon').text)}

    # Parse the 'metrics' tag
    metrics_tag = dmn_tag.find('metrics')
    result['domain']['metrics'] = {'caption':metrics_tag.get('caption'), # Profile
                                   'link':strip(metrics_tag.find('link').text),
                                   'icon':strip(metrics_tag.find('icon').text)}
    # Parse the val tag of the metrics tag
    result['domain']['metrics']['value'] = {'month':strip(metrics_tag.find('val').find('mth').text),
                                            'year':strip(metrics_tag.find('val').find('yr').text),
                                            'unique_visitors':{'ranking':strip(metrics_tag.find('val').find('uv').find('ranking').text),
                                                               'count':strip(metrics_tag.find('val').find('uv').find('count').text)}
                                            }

    # Parse the 'deals' tag
    deals_tag = dmn_tag.find('deals')
    result['domain']['deals'] = {'caption':deals_tag.get('caption'), # Deals
                                 'value':strip(deals_tag.find('val').text),
                                 'link':strip(deals_tag.find('link').text),
                                 'icon':strip(deals_tag.find('icon').text)}

    return result
