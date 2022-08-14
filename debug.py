#!/usr/bin/env python
import sys
import constant as cn

"""
MIT License

Copyright (c) 2022 Lawrence Byng

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""


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
    
