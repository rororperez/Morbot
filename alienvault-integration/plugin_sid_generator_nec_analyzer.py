#!/usr/bin/python

import re
import sys
import xml.etree.ElementTree as ET
import time
import os

'''
RCP - 22.05.2018 - 11:42 Initial version 

  INPUT: XML file with signature set
  OUTPUT: SQL file with all alienvault plugin & plugin_sids

'''

# Function to load all regexp
def load_xml_patterns(pattern_file, list_of_patterns):

  tree = ET.parse(pattern_file)
  filters = tree.getroot()

  for pattern in filters:
    rule_id     =       pattern[0].text
    description =       pattern[2].text

    list_of_patterns[rule_id] = description


def print_help():
  print "Use...."
  print " $1 - pattern XML file"
  print " $2 - output SQL file"
  print " $3 - [NEW/ADD] - Add new plugin_sids to the output SQL file"
   

def generate_SQL_file(list_of_patterns, output):

  outFile = open(output, 'w')

  outFile.write("-- Apache NEC-IDS\n")
  outFile.write("-- plugin_id: 8068\n")
  outFile.write('DELETE FROM plugin WHERE id = "8068";\n')
  outFile.write('DELETE FROM plugin_sid where plugin_id = "8068";\n')
  outFile.write("INSERT IGNORE INTO plugin (id, type, name, description) VALUES (8068, 1, 'NEC-IDS', 'NEC-IDS');\n")
  outFile.write("\n-- plugin sids...\n")

  for ID in list_of_patterns.keys():
    line = "INSERT INTO plugin_sid (plugin_id, sid, category_id, class_id, name) VALUES (8068, " + str(ID) + ", NULL, NULL, 'NEC-IDS : " + list_of_patterns[ID] +"');\n"
    outFile.write(line)    

  outFile.close()

def add_to_SQL_file(list_of_patterns, output):
  outFile = open(output, 'a')

  for ID in list_of_patterns.keys():
    line = "INSERT INTO plugin_sid (plugin_id, sid, category_id, class_id, name) VALUES (8068, " + str(ID) + ", NULL, NULL, 'NEC-IDS : " + list_of_patterns[ID] +"');\n"
    outFile.write(line)

  outFile.close()


# MAIN 
if __name__ == "__main__":

  if (sys.argv[1] == "--help") or (sys.argv[1] == "-h"):
    print_help()
    sys.exit()

  list_of_patterns = { }
  list_of_compile_patterns = { }

  XML_PATTERNS = sys.argv[1]
  output_SQLFILE = sys.argv[2]
  aDD = sys.argv[3]

  print '''\n\n***********************************************
    \nGenerating SQL file... :
    \n***********************************************\n
    '''
  load_xml_patterns(XML_PATTERNS, list_of_patterns)

  if aDD != 'ADD':
    generate_SQL_file(list_of_patterns, output_SQLFILE)
  else:
    add_to_SQL_file(list_of_patterns, output_SQLFILE)

  sys.exit()
