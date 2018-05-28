#####################################################################################################
###
### Fichero de configuracion de Morbot
### Importante: tener todos los ficheros de patrones en el mismo directorio que
###             el fichero de configuracion
###
#####################################################################################################
##################################### Morbot Necromancer config #####################################
#####################################################################################################

# Log files:
LOG = "morbot.log"
input_LOGFILE = "/var/log/apache2/access.log"
output_LOGFILE_01 = "/var/log/apache2/morbot01.log"
output_LOGFILE_02 = "morbot02.log"
output_LOGFILE_03 = "morbot03.log"
output_LOGFILE_04 = "morbot04.log"
output_LOGFILE_05 = "morbot05.log"
output_LOGFILE_06 = "morbot06.log"
output_LOGFILE_07 = "morbot07.log"
output_LOGFILE_08 = "morbot08.log"

#####################################################################################################
#####################################################################################################
#####################################################################################################

# XML Pattern with all regexp and regex to exclude

# Attack rules:
attack_PATTERNS = "XML_attack_filter.xml"
useragent_PATTERNS = "XML_useragent_filter.xml"

# Exclude attacks by ID:
exclude_ids = [7,8]

#####################################################################################################
#####################################################################################################
#####################################################################################################

# Parser rules:
format_rules = "XML_uri_format.xml"

# Tecnology - Apache, F5, ... 
tecnology = "process-all"

#####################################################################################################
#####################################################################################################
#####################################################################################################

# Set General configs

# 5 by default, number of cores that process go to use
# Don't support more of 8 cores
number_of_cores = 1

# Number of second to wait after check the file again
loop_interval = 1

# load first priority signatures like SQLi and others 0 - NO, 1 - YES
priority_signatures = 1

# Activate userAgent Engine detection 0 - disable, 1 - enable
useragent_engine_detection = 1

#####################################################################################################
