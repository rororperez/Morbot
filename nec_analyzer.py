#!/usr/bin/python

###################################################################################################
###
### Autor: Roberto Carlos Perez Gonzalez
### 
### Version: 1.1
### 
### Descripcion:
###   Se trata de un motor de reglas que a traves de expresiones regulares es capaz de 
###   detectar diferentes patrones de ataque webs.
###
###   Este motor se podria usar en cualquier tipo de logs aplicando los patrones adecuados.
###
###   Utiliza la libreria "zombie_analyzer_class.py" para poder realizar un multihilo y soportar
###   una gran cantidad de entrada de logs.
### 
###   El concepto es como el de un juego de ROL, donde un "Nigromante" se encarga de alzar
###   procesos "Zombies" en este caso, que son los que se encargan de procesar los difernetes logs
###   que entran y generar una salida con el RAW log + el patron detectado.
###
###
###################################################################################################

import re
import sys
import xml.etree.ElementTree as ET
import time
import os
import threading
import multiprocessing
import necromancer_config
from zombie_analyzer_class import Zombie

""" Function to load all regexp 
	Need:	pattern_file
			list_of_patterns
			exclude_ids
"""
def load_xml_patterns(pattern_file, list_of_patterns, exclude_ids, list_of_exceptions):

  tree = ET.parse(pattern_file)
  filters = tree.getroot()
  log = open(LOG, 'a')

  for pattern in filters:
    rule_id     =       pattern[0].text
    description =       pattern[2].text
    rule        =       pattern[1].text
    exception	=		pattern[4].text
    

    if int(rule_id) in exclude_ids:
      log.write("\nEscluding Rule ID: " + rule_id)
    else:
      log.write("\n Testing: Rule ID: " + rule_id)
      log.write("\n Description: " + str(description))
      log.write("\n Pattern: " + rule)
      log.write("\n Exceptions: " + str(exception))
 
      complete_rule		=	".*" + rule + ".*"
      
      list_of_patterns[rule_id]		=	complete_rule    
      list_of_exceptions[rule_id]	=	exception

  log.close()

""" 
	Control de number of cores
	4  by default
"""

def control_number_of_zombies(number_of_zombies):

  max_nzombies = 0

  if number_of_zombies > 8:
    max_nzombies = 8
  elif number_of_zombies < 0:
    max_nzombies = 2
  else:
    max_nzombies = number_of_zombies
  return max_nzombies


""" 
	Select tecnology and load rule_00 and rule_11
"""
def load_parser_rules(format_rules, select_tecnology, rule_id):

  tree = ET.parse(format_rules)
  tecnologies = tree.getroot()

  for tecnology in tecnologies:
    name	=       tecnology[0].text
    rule_00	=       tecnology[1].text
    rule_11	=       tecnology[2].text

    if name == select_tecnology:
      if rule_id == 0:
        return rule_00
        break
      elif rule_id == 1:
        return rule_11
        break
       
"""
	This function do:
	 - compile all patterns
	 - organize all patterns
	 - make a list with all patterns compiled

"""

def compile_all_patterns(list_of_patterns, organized_list_of_patterns, organized_list, list_of_compile_patterns):

  # organize by hits
  organized_list.sort()

  for number_of_hits in organized_list:

    rule_id	=	organized_list_of_patterns[number_of_hits]
    rule	=	list_of_patterns[rule_id]

    try:
      pmatch = re.compile(rule, re.IGNORECASE)

      list_of_compile_patterns[rule_id]	=	pmatch

    except:
      pass

"""
	Function for compile rule_00 and rule_11
"""
def compile_rule(rule):

  log = open(LOG, 'a')
  try:
    rule_pmatch = re.compile(rule, re.IGNORECASE)
    log.write(" Compile: " + str(rule) + "\n")
  except:
    pass

  log.close()
  return rule_pmatch

"""
	Learning module: see how many hits have each rule
"""
def learning_module(list_of_patterns, organized_list_of_patterns, organized_list):

  log = open(LOG, 'a')
  log.write(''' \n ***************************************
     \n   Begining de Learning module...
     \n   Testing all patterns...
     \n ***************************************\n)
  ''')
  compile_patterns = { }
  
  # compile all patterns
  for ID in list_of_patterns.keys():

    rule = list_of_patterns[ID]
    try:
      pmatch = re.compile(rule, re.IGNORECASE)

      compile_patterns[ID]	=	pmatch

    except:
      pass

  # test 100.000 lines and create the dictionary with hits
 
  for ID in compile_patterns.keys():

    log.write("\nCalculating time in regexp ID: " + ID + "\n")

    count = 0    
    count_lines = 0    
    
    try:
      inFile = open(input_LOGFILE, 'r')
      pmatch = compile_patterns[ID]

      initial_time = time.time()

      for logLine in inFile: 
        match_line = pmatch.match(logLine)
      
        if match_line:
          count = count + 1
     
        if count_lines > 9999:
          count_lines = 0
          break
        else:
          count_lines = count_lines + 1

      end_time = time.time()
      inFile.close()

      elapsed_time = end_time - initial_time
      log.write("     Elapsed time: " + str(elapsed_time) + " , Hits: " + str(count) +"\n")

      # Eliminate duplicate dictionaries entries
      organized_list_of_patterns[elapsed_time]	=	ID
      organized_list.append(elapsed_time)

      log.write("   - Rule ID: " + str(ID) + ", number of hits: " + str(count) + ", Elapsed time: " + str(elapsed_time) + "\n")

    except:
      log.write("Unexpected error at open the input log file: " + str(sys.exc_info()[0]) + "\n")
      pass

  log.close()

### BEGIN MAIN:

if __name__ == "__main__":

  LOG =	necromancer_config.LOG
  date = time.strftime("%d/%m/%Y - %H:%M:%S")
  log = open(LOG, 'a')

  log.write("Now: " + str(date) + ":\n")
  log.write('''\n Begining MorBot NecroMancer...\n 
               (()))                                                          
              /|x x|   
             /\( - )
     ___.-._/\/ 
    /=`_'-'-'/  !!
    |-{-_-_-}     !
    (-{-_-_-}    !
     \{_-_-_}   !
      }-_-_-}
      {-_|-_}
      {-_|_-}                                                                 
      {_-|-_}
      {_-|-_}  ZOT
  ____%%@ @%%_______\n                                
  ''')

  log.write("\n " + str(date) + " - Begining MORBOT real Time Apache Log analyzer... . . .. . .\n")
  log.write("\n " + str(date) + " - Loading basic configuration... . . .. . .\n")
  log.close()

  # Loading all config

  input_LOGFILE			=	necromancer_config.input_LOGFILE
  output_LOGFILE_01		=	necromancer_config.output_LOGFILE_01
  output_LOGFILE_02		=	necromancer_config.output_LOGFILE_02
  output_LOGFILE_03		=	necromancer_config.output_LOGFILE_03
  output_LOGFILE_04		=	necromancer_config.output_LOGFILE_04
  output_LOGFILE_05		=	necromancer_config.output_LOGFILE_05
  output_LOGFILE_06		=	necromancer_config.output_LOGFILE_06
  output_LOGFILE_07		=	necromancer_config.output_LOGFILE_07
  output_LOGFILE_08		=	necromancer_config.output_LOGFILE_08
  attack_PATTERNS		=	necromancer_config.attack_PATTERNS
  useragent_PATTERNS	=	necromancer_config.useragent_PATTERNS
  exclude_ids			=	necromancer_config.exclude_ids
  tecnology             =   necromancer_config.tecnology
  rule_00				=	load_parser_rules(necromancer_config.format_rules, tecnology, 0)
  rule_11 				=	load_parser_rules(necromancer_config.format_rules, tecnology, 1)
  MAX_ZOMBIES			=	control_number_of_zombies(necromancer_config.number_of_cores)
  loop_interval			=	necromancer_config.loop_interval
  ua_engine_detection	=	necromancer_config.useragent_engine_detection

  # Init all variables

  list_of_patterns = { }
  list_of_exceptions = { }
  
  list_of_useragent_patterns = { }
  list_of_useragent_exceptions = { }

  organized_list_of_patterns = { }
  organized_list_of_useragent_patterns = { }

  list_of_compile_patterns = { }
  list_of_compile_useragent_patterns = { }

  organized_list = []
  organized_list_of_useragent = []

  log = open(LOG, 'a')
  log.write('''\n\n***********************************************
    \nBegining to load all regexp:
    \n***********************************************\n
    ''')
  log.close()

  # Load and compile attack patterns & user-agent patterns
  load_xml_patterns(attack_PATTERNS, list_of_patterns, exclude_ids, list_of_exceptions)
  load_xml_patterns(useragent_PATTERNS, list_of_useragent_patterns, exclude_ids, list_of_useragent_exceptions)

  # Learning regexp order
  learning_module(list_of_patterns, organized_list_of_patterns, organized_list)
  learning_module(list_of_useragent_patterns, organized_list_of_useragent_patterns, organized_list_of_useragent)

  # Divide all the patterns if four sub-task 
  compile_all_patterns(list_of_patterns, organized_list_of_patterns, organized_list, list_of_compile_patterns)
  compile_all_patterns(list_of_useragent_patterns, organized_list_of_useragent_patterns, organized_list_of_useragent, 
    list_of_compile_useragent_patterns)

  log = open(LOG, 'a')
  log.write('''\n\n***********************************************
    \nAll patterns loaded:
    \n***********************************************\n
    ''')
  log.close()

  # Compile rule_00
  rule_00_compiled = compile_rule(rule_00)
  rule_11_compiled = compile_rule(rule_11)

  # Read the input file and send mem data to all process childs

  log = open(LOG, 'a')
  date = time.strftime("%d/%m/%Y - %H:%M:%S")
  log.write('''\n\n***********************************************
    \n ''' + str(date) +  ''' Procesing logs:
    \n***********************************************\n
    ''')

  # En este punto debemos lanzar todas los procesos hijos y esperar a que finalicen
  date = time.strftime("%d/%m/%Y - %H:%M:%S")
  log.write("Iniciando ejecucion de hilos " + str(date) + "\n")

  inFile = open(input_LOGFILE, 'r')
  inFile.seek(0, os.SEEK_END)

  fileBytePos = inFile.tell()
  inFile.close()

  allZombies = [] 
  active_zombies = 0
  state_of_zombies = {
    'zombie01'	:	'0',
    'zombie02'	:	'0',
    'zombie03'	:	'0',
    'zombie04'	:	'0',
    'zombie05'	:	'0',
    'zombie06'	:	'0',
    'zombie07'	:	'0',
    'zombie08'	:	'0'
    }

  while True:
    try:
      inFile = open(input_LOGFILE, 'r')

      inFile.seek(0, os.SEEK_END)
      sizeInputFile = inFile.tell()

      # Test if the file has been rotated
      if fileBytePos > sizeInputFile:
        fileBytePos = 0

      # Test if the file don't increase
      if not fileBytePos == sizeInputFile:
        # Seek in the last position
        inFile.seek(fileBytePos)

        date = time.strftime("%d/%m/%Y - %H:%M:%S")
        log.write("\nReading new data...." + str(date) + "\n")
        fileInMemory = inFile.read()

        # After read, the new fileBytePos
        fileBytePos = inFile.tell()
        inFile.close()

        # Begin to launch all zombies
        if active_zombies < MAX_ZOMBIES:
       
          if int(state_of_zombies['zombie01']) == 0:
			          
            zombie	=	multiprocessing.Process(name='zombie01', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_01, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie01']	=	'1' 
            log.write("Starting zombie type: zombie01\n")


          elif int(state_of_zombies['zombie02']) == 0:

            zombie	=	multiprocessing.Process(name='zombie02', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_02, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie02']	=	'1' 
            log.write("Starting zombie type: zombie02\n")


          elif int(state_of_zombies['zombie03']) == 0:
            print "Zombie 03"
            zombie	=	multiprocessing.Process(name='zombie03', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_03, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie03']	=	'1' 
            log.write("Starting zombie type: zombie03\n")


          elif int(state_of_zombies['zombie04']) == 0:
            zombie	=	multiprocessing.Process(name='zombie04', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_04, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie04']	=	'1' 
            log.write("Starting zombie type: zombie04\n")


          elif int(state_of_zombies['zombie05']) == 0: 
            zombie	=	multiprocessing.Process(name='zombie05', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_05, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie05']	=	'1' 
            log.write("Starting zombie type: zombie05\n")


          elif int(state_of_zombies['zombie06']) == 0:
            zombie      =       multiprocessing.Process(name='zombie06', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_06, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie06']        =       '1'
            log.write("Starting zombie type: zombie06\n")


          elif int(state_of_zombies['zombie07']) == 0:
            zombie      =       multiprocessing.Process(name='zombie07', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_07, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie07']        =       '1'
            log.write("Starting zombie type: zombie07\n")


          elif int(state_of_zombies['zombie08']) == 0:
            zombie      =       multiprocessing.Process(name='zombie08', target=Zombie, args=(list_of_compile_patterns, list_of_compile_useragent_patterns, 
                                output_LOGFILE_08, rule_00_compiled, rule_11_compiled, fileInMemory, ua_engine_detection, list_of_exceptions, list_of_useragent_exceptions))

            state_of_zombies['zombie08']        =       '1'
            log.write("Starting zombie type: zombie08\n")


          active_zombies = active_zombies + 1
       
          zombie.start()
          allZombies.append(zombie)

          date = time.strftime("%d/%m/%Y - %H:%M:%S")
          log.write(" - " +  str(date) + " - New ZoMbIe start; Number of active zombies: " + str(active_zombies) + "\n")
 
      log.write("" + str(allZombies) + "\n")

      for old_zombie in allZombies:

        #status = old_zombie.is_alive()
        #log.write("Estatus: " + str(status) + "\n")
 
        if not old_zombie.is_alive():
          zombie_to_delete		=	allZombies.index(old_zombie)
          name_zombie_to_delete	=	old_zombie.name

          log.write("New Zombie end..." + name_zombie_to_delete + "\n")

          del allZombies[zombie_to_delete]
          active_zombies = active_zombies - 1
          state_of_zombies[name_zombie_to_delete] = '0'
          log.write("Numero de zombies: " + str(active_zombies) + "\n") 

      time.sleep(loop_interval)

    except:
      log.write("Unexpected error at open the input log file: " + str(sys.exc_info()[0]) + "\n")
      time.sleep(10)


  # Ending Necromancer
  date = time.strftime("%d/%m/%Y - %H:%M:%S")
  log.write("Finalizando Necromancer" + str(date) + "\n")

  log.close()

