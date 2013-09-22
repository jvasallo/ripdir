#!/usr/bin/env python
import os
import yaml
import socket
import urllib

# getting settings from config
configfile = os.path.join(os.path.dirname(__file__), 'settings.yaml')
stream = open(configfile, 'r')
config = yaml.load(stream)

socket.setdefaulttimeout(config['loc_settings']['timeout'])
store_folder = config['loc_settings']['storage_dir']
folder_info_dict = config['folders']

for each_folder in folder_info_dict:
    store_dir = os.path.join(os.path.dirname(__file__), store_folder, each_folder)
    folder_dict = folder_info_dict[each_folder]
    print folder_dict
    file_type = folder_dict['file_type']
    url = folder_dict['url']
    try:
        os.mkdir(store_dir)
    except OSError:
        print "[WARN] Directory %s already exists" % each_folder

    for item_num in range(folder_dict['start_range'], folder_dict['end_range']):
        if item_num < 10 and folder_dict['patterns']['under_ten']:
            file_name = folder_dict['patterns']['under_ten'] % item_num
        else:
            file_name = folder_dict['patterns']['generic'] % item_num

        url_full_path = "%s/%s.%s" % (url, file_name, file_type)
        store_full_path = "%s/%s.%s" % (store_dir, file_name, file_type)

        urllib.urlretrieve(url_full_path, store_full_path)
        print "Successfully downloaded %s.%s" % (file_name, file_type)