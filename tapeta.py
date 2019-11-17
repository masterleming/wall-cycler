#!/usr/bin/python

import configparser   # for loading config file
import shelve         # for storing state
import pathlib
import os.path

class WallCollection:
	def __init__(self):
		self.collection = []
		self.lastWall = 0

	def next(self):
		if len(self.collection) == 0:
		   raise Exception('Cannot get next wallpaper! The collection is empty')

		self.lastWall = (self.lastWall + 1) % len(self.collection)
		return self.collection[self.lastWall]

	def update(self, files=[]):
		newFiles = [ f for f in files if f not in self.collection ]
		for i, f in enumerate(newFiles):
			self.collection.insert(self.lastWall + i + 1, f)
