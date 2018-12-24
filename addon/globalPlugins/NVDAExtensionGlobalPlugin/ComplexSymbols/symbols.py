#NVDAExtensionGlobalPlugin/ComplexSymbols/symbols.py
#A part of NVDAExtensionGlobalPlugin add-on
#Copyright (C) 2016 paulber19
#This file is covered by the GNU General Public License.
#See the file COPYING for more details.


import addonHandler
from logHandler import log
from languageHandler import curLang
import os
import globalVars
import codecs

symbolCategoriesFile = ("symbolCategories", "dic")
userConfigPath = os.path.abspath(os.path.join(globalVars.appArgs.configPath, ""))

class SymbolsManager(object):
	def __init__(self):
		self.ready = False
		self.basicSymbolCategoriesDic = {}
		self.basicOrderedSymbolCategoryNames = []
		self.basicOrderedSymbols = {}
		if not self.loadBasicSymbolCategories():
			log.error("Error: No complex symbol installed")
			return
		from ..settings import _addonConfigManager
		self.addonConfigManager = _addonConfigManager
		self.userSymbolCategoriesDic = self.addonConfigManager.getUserComplexSymbols()
		self.ready = True
		
	def isReady(self):
		return self.ready
	
	def loadBasicSymbolCategories(self):
		symbol_description_separator = "\t"
		curCategory = None
		fileName = self.getSymbolCategoriesDicPath()
		if fileName == None:
			return False
		symbolCategories= {}
		orderedSymbols = {}
		with codecs.open(fileName, "r", "utf_8_sig", errors="replace") as f:
			for line in f:
				if line.isspace() or line.startswith("#"):
					# Whitespace or comment.
					continue
				
				line = line.rstrip("\r\n")
				if self.isCategorieName(line):
					curCategory = line[1:-1]
					self.basicOrderedSymbolCategoryNames.append(curCategory)
					symbolCategories[curCategory] = {}
					orderedSymbols[curCategory] = []
					continue
				l= line.split(symbol_description_separator)
				if (len(l) == 2)  and l[0] and l[1] :
					symbol = l[0]
					description = l[1]
					if curCategory == None:
						log.error("Symbol without category: %s"%line)
						continue
					symbolCategories[curCategory][symbol] = description
					orderedSymbols[curCategory].append(symbol)
				else:
					log.error("Symbol and description incorrect: %s" % line)
	
	
		if len(symbolCategories.keys())== 0:
			return False

		self.basicSymbolCategoriesDic = symbolCategories.copy()
		self.orderedSymbols = orderedSymbols.copy()
		return True
	
	

		
	def getUserSymbolCategories(self):
		return self.userSymbolCategoriesDic 
	def saveUserSymbolCategories(self, symbolCategories):
		self.userSymbolCategoriesDic= symbolCategories.copy()
		self.addonConfigManager.saveUserComplexSymbols(symbolCategories)
		
	def getUserSymbolCategoriesFile(self, locale):
		file  = symbolCategoriesFile[0]+"-"+locale+"."+symbolCategoriesFile[1]
		file = os.path.join(userConfigPath, file)
		if os.path.isfile(file):
			return file
		if "_" in locale:
			file  = symbolCategoriesFile[0]+"-"+locale.split("_")[0]+"."+symbolCategoriesFile[1]
			file = os.path.join(userConfigPath, file)
			if os.path.isfile(file):
				return file
	
		return None
	
	def getSymbolCategoriesDicPath1(self):
		userFile = self.getUserSymbolCategoriesFile(curLang)
		if userFile !=None:
			return userFile
	
		localeList = [curLang]
		if '_' in curLang:
			localeList.append(curLang.split('_')[0])
		localeList.append("eng")
		addonFolderPath = addonHandler.getCodeAddon().path
		for locale in localeList:
	
			file = ".".join(symbolCategoriesFile)
			fileName=os.path.join(addonFolderPath,"locale",locale.encode("utf-8"),file)
			if os.path.isfile(fileName):
				return fileName
		return None
	def getSymbolCategoriesDicPath(self):
		userFile = self.getUserSymbolCategoriesFile(curLang)
		if userFile !=None:
			return userFile
		localeList = [curLang]
		if '_' in curLang:
			localeList.append(curLang.split('_')[0])
		localeList.append("eng")
		addonFolderPath = addonHandler.getCodeAddon().path
		fileName = ".".join(symbolCategoriesFile)
		for locale in localeList:
			file=os.path.join(addonFolderPath,"locale",locale.encode("utf-8"),fileName)
			if os.path.isfile(file):
				return file
		return None

	
	def isCategorieName(self, line):
		if line[0] == "[" and line[-1] == "]":
			name  = line[1:-1]
			if len(name):
				return True
	
		return False
	

	def getUserSymbolAndDescriptionList( self, categoryName, userComplexSymbols  = None):
		if not userComplexSymbols :
			userComplexSymbols = self.addonConfigManager.getUserComplexSymbols()
			
		if categoryName not in userComplexSymbols.keys():
			return ([], [])
		
		userSymbols = userComplexSymbols[categoryName]
		symbolList= []
		descriptionList = []
		for symbol in userSymbols.keys():
			symbolList.append(symbol)                                                                                                                                                                                                                                                                                                            
			descriptionList.append(userSymbols[symbol])
		
		return (symbolList, descriptionList)
	
	

	def getSymbolAndDescriptionList(self, categoryName):
		userSymbolCategoriesDic = self.addonConfigManager.getUserComplexSymbols()
		userSymbolsDic  = {}
		if categoryName in userSymbolCategoriesDic .keys():
			userSymbolsDic = userSymbolCategoriesDic [categoryName].copy()
		basicSymbolsDic = {}
		orderedSymbols  = []
		if categoryName in self.basicSymbolCategoriesDic .keys():
			basicSymbolsDic = self.basicSymbolCategoriesDic [categoryName].copy()
			orderedSymbols = self.orderedSymbols[categoryName][:]
		#merge two dictionnaries
		symbolList= []
		descriptionList = []
		for symbol in orderedSymbols:
			symbolList.append(symbol)                                                                                                                                                                                                                                                                                                            
			descriptionList.append(basicSymbolsDic [symbol])
		for symbol in userSymbolsDic.keys():
			symbolList.append(symbol)                                                                                                                                                                                                                                                                                                            
			descriptionList.append(userSymbolsDic [symbol])
		return (symbolList, descriptionList)
			

			
	def getBasicCategoryNames(self):
		return self.basicOrderedSymbolCategoryNames
	def getCategoryNames(self):
		userSymbolCategoriesDic = self.addonConfigManager.getUserComplexSymbols()
		symbolCategoryNames = self.basicOrderedSymbolCategoryNames[:]
		for categoryName in userSymbolCategoriesDic .keys():
			if categoryName not in symbolCategoryNames :
				symbolCategoryNames .append(categoryName)
	
		return symbolCategoryNames
		