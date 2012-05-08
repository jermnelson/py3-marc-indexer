#! /usr/bin/python
# -*- coding: utf8 -*-

# Copyright 2009-2010 Gabriel Sean Farrell
# Copyright 2008-2010 Mark A. Matienzo
#
# This file is part of Kochief.
# 
# Kochief is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# Kochief is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with Kochief.  If not, see <http://www.gnu.org/licenses/>.

"""Indexes documents in a Solr instance."""

import argparse
import os
import sys
import time
import marc,pymarc
import csv,logging,datetime
from multiprocessing import Process,Lock,Pool
import urllib.request, urllib.parse, urllib.error
import urllib.request, urllib.error, urllib.parse
import marc as module

try:
    import xml.etree.ElementTree as et  # builtin as of Python 2.5
except ImportError:
    import elementtree.ElementTree as et

try:
    import django.conf as conf
except ImportError:
    class stub_settings(object):
        def __init__(self,**args):
            self.SOLR_DIR = args['SOLR_DIR']
            self.SOLR_URL = args['SOLR_URL']

    class stub_conf(object):
        def __init__(self,settings):
            self.settings = settings
    settings = stub_settings(SOLR_DIR='/usr/local/solr_server/multicore/marc_catalog',
                             SOLR_URL='http://0.0.0.0:8984/solr/marc_catalog/')
    conf = stub_conf(settings=settings)
   
## import django.core.management.base as mb
time_stamp = datetime.datetime.today().strftime("%Y%m%d-%H")    
logging.basicConfig(filename="%slog/%smarc-solr-indexer.log" % ('./',time_stamp),
                    level=logging.INFO)
arg_parser = argparse.ArgumentParser(description='Index MARC records into Solr')
arg_parser.add_argument('--new',
                        dest='new',
                        help='Create a new index.  If the index already exists, all docs in the index will be deleted before this indexing.')
#arg_parser.add_argument('--parser',
#                        dest='parser',
#                        action='handle',
#                        metavar='PARSER', 
#                        help='Use PARSER (in discovery/parsers) to parse files or urls for indexing')
arg_parser.add_argument('file_or_urls',
                        nargs="+",
                        #action='append',  
                        help = '[file_or_url ...] Indexes documents in a Solr instance.')

print_lock = Lock()

def index_shard(marc_recs):
    pid = os.getpid()
    tmp_csv_file = 'tmp%s.csv' % pid
    print_lock.acquire()
    print("Converting CSV in process pid=%s..." % (pid))
    print_lock.release()
    t1 = time.time()
    counter = 0
    try:
        csv_handle = open(tmp_csv_file, 'w')
        csv_writer = csv.DictWriter(csv_handle, module.FIELDNAMES)
        fieldnames_dict = dict()
        for row in module.FIELDNAMES:
            fieldnames_dict[row] = row
        csv_writer.writerow(fieldnames_dict)
        for record in marc_recs:
            print_lock.acquire()
            if counter%100:
                sys.stderr.write('.')
            print_lock.release()
            try:
                indexed_dict = module.get_record(record,ils=module.settings.ILS)
                if indexed_dict is not None:
                    for row in indexed_dict.items():
                        key,value = row
                        if type(value) == list or type(value) == set:
                            value = '|'.join([item for item in value])
                            indexed_dict[key] = value
                        elif type(value) == dict:
                            value = '|'.join([item for item in value.values()])
                    csv_writer.writerow(indexed_dict)
                    counter += 1
                else:
                    print_lock.acquire()
                    marc_error_file = open('tutt-errors.mrc','ab')
                    marc_error_file.write(record.as_marc().encode('utf8','ignore'))
                    marc_error_file.close()
                    error_msg = "Invalid indexing of row=%s in pid=%s title=%s" % (counter,
                                                                                   pid,
                                                                                   record.title())
                    print(error_msg)
                    logging.error(error_msg)
                    print_lock.release()
            except:
                print_lock.acquire()
                error_msg = "Error %s in %s row=%s" % (sys.exc_info()[0],pid,counter)
                if record is not None:
                    marc_error_file = open('tutt-errors.mrc','ab')
                    marc_error_file.write(record.as_marc().encode('utf8','ignore'))
                    marc_error_file.close()
                    error_msg = '%s title=%s' % (error_msg,record.title())
                print(error_msg)
                logging.error(error_msg)
                print_lock.release()
 
    finally:
        csv_handle.close()
    record_count = counter
    t2 = time.time()
    solr_response = load_solr(tmp_csv_file)
    t3 = time.time()
    print_lock.acquire()
    logging.error("Solr Response in process pid=%s %s" % (pid,solr_response))
    print_lock.release()
    os.remove(tmp_csv_file)
    p_time = (t2 - t1) / 60
    l_time = (t3 - t2) / 60
    t_time = p_time + l_time
    rate = record_count / (t3 - t1)
    print_lock.acquire()
    logging.error("""Processing w/pid %s took %0.3f minutes.
Loading took %0.3f minutes.  
That's %0.3f minutes total for %d records, 
at a rate of %0.3f records per second.
""" % (pid,p_time, l_time, t_time, record_count, rate))
    print_lock.release()


def pool_multiprocess_index(file_or_urls,shard_size=10000):
    pool = Pool(processes=3)
    for file_ref in file_or_urls:
        reader = pymarc.MARCReader(open(file_ref,'rb'))
        print("Start-up multiprocess pool")
        pool.map_async(index_shard,reader,shard_size)
    print("Finished multiprocess")

def multiprocess_index(file_or_urls,shard_size=10000):
    lock = Lock()
    t1 = time.time()
    total_recs = 0
    for file_ref in file_or_urls:
        reader = pymarc.MARCReader(open(file_ref,'rb'),utf8_handling="xmlcharrefreplace")
#        error_recs = open('%s-bad.mrc' % file_ref,'wb')
        print("Starting multiprocess index for %s, sharding by %s" % (file_ref,
                                                                      shard_size))
        count = 1
        marc_recs = []
        while 1:
            try:
                rec = next(reader)
            except ValueError as error:
                lock.acquire()
                error_msg = "%s for record %s in %s" % ("ValueError: {0}".format(error),
                                                        count,
                                                        file_ref)
                print(error_msg)
                logging.error(error_msg)
                lock.release()
                count += 1
                pass
                #rec = next(reader)
            except StopIteration:
                break
            if not count%shard_size:
                marc_recs.append(rec)
                shard_process = Process(target=index_shard,args=(marc_recs,))
                if shard_process is not None:
                    shard_process.start()
                    shard_process.join()
                else:
                    lock.acquire()
                    error_msg = "Unable to process %s total_recs=%s" % (file_ref,total_recs)
                    print(error_msg)
                    logging.error(error_msg)
                    lock.release()
                    marc_recs = []
            else:
                marc_recs.append(rec)
            if count%1000:
                sys.stderr.write(".")
            else:
                sys.stderr.write(str(count))
            count += 1
            total_recs += count
    t2 = time.time()
    total_time = (t2 - t1) / 60.0
    print("Finished multi-processing %s in %0.3f" % (total_recs,
                                                     total_time))
                                
#def handle(*file_or_urls, **options):
#    new = options.get('new')
#    if new:
#       data = '<delete><query>*:*</query></delete>'
#       r = urllib.request.Request(conf.settings.SOLR_URL + 'update?commit=true')
#       r.add_header('Content-Type', 'text/xml')
#       r.add_data(data)
#       f = urllib.request.urlopen(r)
#       print("Solr response to deletion request:")
#       print(f.read())
#    if file_or_urls:
#       parser = options.get('parser')
#       module = None
#       if parser:
#           if parser.endswith('.py'):
#               parser = parser[:-3]
#           module = __import__('.' + parser, globals(), 
#                        locals(), [parser])
#       for file_or_url in file_or_urls:
#           if not module:
#                # guess parser based on file extension
#               if file_or_url.endswith('.mrc'):
#                   import marc as module
#               if not module:
#                    raise ("Please specify a parser.")
#            print("Converting %s to CSV ..." % file_or_url)
#            t1 = time.time()
#            data_handle = urllib.request.urlopen(file_or_url)
#            try:
#                csv_handle = open(CSV_FILE, 'w')
#                record_count = module.write_csv(data_handle, csv_handle, 
#                        collections=options.get('collections'))
#            finally:
#                csv_handle.close()
#            t2 = time.time()
#            load_solr(CSV_FILE)
#            t3 = time.time()
#            os.remove(CSV_FILE)
#            p_time = (t2 - t1) / 60
#            l_time = (t3 - t2) / 60
#            t_time = p_time + l_time
#            rate = record_count / (t3 - t1)
#            print("""Processing took %0.3f minutes.
#Loading took %0.3f minutes.  
#That's %0.3f minutes total for %d records, 
#at a rate of %0.3f records per second.
#""" % (p_time, l_time, t_time, record_count, rate))


def get_multi():
    """Inspect solr schema.xml for multivalue fields."""
    multivalue_fieldnames = []
    schema = et.parse(conf.settings.SOLR_DIR + '/conf/schema.xml')
    fields_element = schema.find('fields')
    field_elements = fields_element.findall('field')
    for field in field_elements:
        if field.get('multiValued') == 'true':
            multivalue_fieldnames.append(field.get('name'))
    return multivalue_fieldnames

def load_solr(csv_file):
    """
    Load CSV file into Solr.  solr_params are a dictionary of parameters
    sent to solr on the index request.
    """
    file_path = os.path.abspath(csv_file)
    solr_params = {}
    for fieldname in get_multi():
        tag_split = "f.%s.split" % fieldname
        solr_params[tag_split] = 'true'
        tag_separator = "f.%s.separator" % fieldname
        solr_params[tag_separator] = '|'
    solr_params['stream.file'] = file_path
    solr_params['stream.contentType'] = 'text/plain;charset=utf-8'
    solr_params['commit'] = 'true'
    params = urllib.parse.urlencode(solr_params)
    update_url = conf.settings.SOLR_URL + 'update/csv?%s'
    #print("Loading records into Solr ...")
    try: 
        response = urllib.request.urlopen(update_url % params)
    except IOError:
        raise IOError('Unable to connect to the Solr instance.')
    #print("Solr response:")
    #print(response.read())
    return response.read()


def cleanup_csv():
   for row in os.listdir():
       if row[-3:] == 'csv':
           load_solr(row)
           os.remove(row)
           print("Loaded %s into solr and removed" % row)

if __name__ == '__main__':
    args = arg_parser.parse_args()
    #print("Passed in %s" % args.file_or_urls)
    multiprocess_index(args.file_or_urls)
