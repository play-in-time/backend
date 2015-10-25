from flask import json

""" Loads API keys from a JSON-formatted file called 'keys.json'
    Expects keys.json to reside in the current directory.
"""
class keysObject:

  def __init__(self):
    self.clientID = self._getclientid()
    self.secretID = self._getsecretid()

  def _getclientid(self):
    keyfile = open('keys.json', 'r')
    keys = json.load(keyfile)
    return keys["clientID"]

  def _getsecretid(self):
    keyfile = open('keys.json', 'r')
    keys = json.load(keyfile)
    return keys["clientSecret"]

