from flask import json
import os

""" Loads API keys from environment variables
"""
class keysObject:

  def __init__(self):
    self.clientID = self._getclientid()
    self.secretID = self._getsecretid()

  def _getclientid(self):
    return os.getenv("SPOTIFY_CLIENT_ID")

  def _getsecretid(self):
    return os.getenv("SPOTIFY_CLIENT_SECRET")

