#!/usr/bin/python

################################################################################################################
###
### Autor: Roberto Carlos Perez Gonzalez
###
### Version: 1.0
###
### Libreria utilizada para procesar los diferentes logs que tiene una maquina y aplicarle una serie de 
### filtros de expresiones regulares con el fin de detectar intrusiones en una maquina final.
###
###
################################################################################################################


import re
import sys
import os

class Zombie:
	
	""" Clase principal de motor de deteccion de patrones en logs """
	
	def __init__ (self, list_of_compile_patterns, list_of_compile_useragent_patterns, output, rule_00_compiled, 
					rule_11_compiled, fileInMemory, ua_engine_detection,
					list_of_exceptions, list_of_useragent_exceptions):
			
		self.list_of_compile_patterns			=	list_of_compile_patterns
		self.list_of_compile_useragent_patterns	=	list_of_compile_useragent_patterns
		self.output 							=	output
		self.rule_00_compiled					=	rule_00_compiled
		self.rule_11_compiled					=	rule_11_compiled
		self.fileInMemory						=	fileInMemory
		self.ua_engine_detection				=	ua_engine_detection
		
		self.list_of_exceptions					=	list_of_exceptions
		self.list_of_useragent_exceptions			=	list_of_useragent_exceptions
		
		# Pendiente:
		# Compilar los patrones de excepciones
		# Hacer match con las excepciones
		
		""" Select and execute the different engines """
		
		if self.ua_engine_detection == 1:
			
			self.analyzeAttacksWithUa()
			
		else:
			self.analyzeAttacks()
					
	
	def analyzeAttacks(self):
	
		outFile = open(self.output, 'a')

		for logLine in self.fileInMemory.split('\n',):

			if not self.rule_00_compiled.match(logLine):

				if self.rule_11_compiled.match(logLine):

					for ID in self.list_of_compile_patterns.keys():

						pmatch      =       self.list_of_compile_patterns[ID]
						match_line  =       pmatch.match(logLine)

						if match_line:
							line = "Pattern found ID: " + str(ID) + "; RAW line: " + logLine + "\n"
							outFile.write(line)
							break

		outFile.close()


		
	def analyzeAttacksWithUa (self):
		
		outFile = open(self.output, 'a')
	
		for logLine in self.fileInMemory.split('\n',):

			reported = 0

			if not self.rule_00_compiled.match(logLine):

				if self.rule_11_compiled.match(logLine):

					for ID in self.list_of_compile_patterns.keys():

						pmatch    	=	self.list_of_compile_patterns[ID]
						match_line	=	pmatch.match(logLine)

						if match_line:
							line = "Pattern found ID: " + str(ID) + "; RAW line: " + logLine + "\n"
							outFile.write(line)
							reported = 1
							break

					if reported == 0:
						
						for uaID in self.list_of_compile_useragent_patterns.keys():

							ua_pmatch		=	self.list_of_compile_useragent_patterns[uaID]
							ua_match_line	=	ua_pmatch.match(logLine)
              
							if ua_match_line:
								line = "Pattern found ID: " + str(uaID) + "; RAW line: " + logLine + "\n"
								outFile.write(line)
								break

		outFile.close()

			
