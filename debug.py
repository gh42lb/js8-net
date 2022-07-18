#!/usr/bin/env python
import sys
import constant as cn

"""
This class handles the events from the varius control defined in js8_net_gui
"""
class Debug(object):

  """
  debug level 0=off, 1=info, 2=warning, 3=error
  """
  def __init__(self, debug_level):  
    self.debug_level = debug_level
   
  def get_debug_level(self):
    return self.debug_level

  def info_message(self, msg):
    if(self.get_debug_level() <= cn.DEBUG_INFO):
      sys.stdout.write("Info: " + msg + "\n")

  def warning_message(self, msg):
    if(self.get_debug_level() <= cn.DEBUG_WARNING):
      sys.stdout.write("Warning: " + msg + "\n")

  def error_message(self, msg):
    if(self.get_debug_level() <= cn.DEBUG_ERROR):
      sys.stdout.write("Error: " + msg + "\n")
    
