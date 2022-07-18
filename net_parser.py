#!/usr/bin/env python
import PySimpleGUI27 as sg
import sys
import JS8_Client
import debug as db
import threading
import json
import constant as cn
import js8_net_gui
import js8_net_events
import js8_net_client
import random
import getopt
import net_parser

from datetime import datetime, timedelta
from datetime import time


"""
This class handles outgoing parsing / field replacement and incoming parsing of phrases
there are two main methods that are accessed by the other modules...
outgoing parsing is handled via the method replaceFields
incoming parsing is handled via the method decodeTriggers
"""
class NetParser(object):

  """
  debug level 0=off, 1=info, 2=warning, 3=error
  """
  def __init__(self, debug, view, window, js8client, js8net):
    self.debug = debug
    self.view = view
    self.window = window
    self.js8client=js8client
    self.js8net = js8net
   
  """
  process ROSTER: message
  general format: WH6NCS: @HINET ... ROSTER IS: <CALLSIGN> <NAME>, <CALLSIGN> <NAME> ...
  
  example 1: WH6NCS: @HINET OK THE ROSTER IS: WH6ABC FRED, WH6DEF PETER
  example 2: WH6NCS: @HINET OK THE ROSTER IS: WH6ABC, WH6DEF PETER
  please note <NAME> is optional.
  """
  def decodeRosterTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage(self.window['input_netgroup'].get() +" THE ROSTER IS: ", text) ):
      self.debug.info_message("decodeTriggers. 'THE ROSTER IS:'")

      """ setting the round is done here as well as in starting the round. Multiple calls to incRound at start is not a problem"""
      """ set the current round to the one we are now starting out on"""
      """ update the display combo to reflect the next round but do not update current round until starting out on the next round"""
      if( self.js8net.getCurrentRound() == self.window['option_currentround'].get() ):
        self.js8net.incRound()
    
      hostname = self.js8net.nameFromSavedCalls(last_call)
      if(hostname == "-"):
        hostname = self.js8net.getNcsHostName()

      calls = last_call + ' ' + hostname + ', ' + text.split(" THE ROSTER IS: ")[1]
      calls_list = calls.split(", ")
      numcalls = len(calls_list)

      if(self.window['input_ncs'].get().strip() == ""):
        self.window['input_ncs'].Update(value=last_call)

      """
      space out the stations based on max signal width and position in the roster
      net control is always at 1337
      """
      offset_split_string = self.js8net.offsets_list.split(',')
      max_offsets = len(offset_split_string)
      stn_offset = offset_split_string[0]
      offset_count=1
      
      for x in range(numcalls):
        if(x>-1):
           call = calls_list[x].split(' ')[0]
			
           if(x==0):
             self.view.updatePrevField(call)
           elif(x==1):
             self.view.updateNextField(call)
             
           """is the name included or just the call sign """ 
           split_string = calls_list[x].strip().split(' ')
           if(len(split_string) == 1):
             calls_list[x] = calls_list[x] + ' -'

           """ is this my station if so set the main offset field """
           if(self.js8net.getStationCallSign() == call):
             self.window['main_offset'].update(stn_offset)
             self.window['main_offset'].update(disabled = True)
             self.window['cb_presetoffset'].update(value=False)
             
           if(x==0):
             calls_list[x] += ' <NCS> ' + str(stn_offset) + ' 0 0 0'
           else:             
             calls_list[x] += ' <STANDBY> ' + str(stn_offset) + ' 0 0 0'

           self.debug.info_message("decodeRosterTrigger. calls list:" + calls_list[x])

           if(offset_count<max_offsets):
             stn_offset=offset_split_string[offset_count]
             offset_count = offset_count + 1
           else:
             """ need to skip the first one second time around as that is for net control only """			   
             stn_offset=offset_split_string[1]
             offset_count=2

      if(numcalls>0):
        self.view.updateCallNameStatus(None, calls_list[0].split(' ')[0], calls_list[0].split(' ')[1], calls_list[0].split(' ')[2])

      self.js8net.roster = calls_list
      self.view.refreshRoster(calls_list)

  """      
  process net announcement QST
  specific format: ... THE <NET NAME> STARTS AT <START TIME> ZULU ON <NET FREQUENCY> MHZ. PLS USE <NET GROUP> GRP ...
  
  example: WH6NCS: @HINET QST QST THE HAWAII JS8 NET STARTS AT 04:30 ZULU ON 7.095MHZ. PLS USE @HINET GRP
  """
  def decodeQstTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage("@ALLCALL QST QST ", text) ):
      self.debug.info_message("decodeTriggers. '@ALLCALL QST QST'")

      if( (" NET STARTS AT ") in text):
        self.window['cb_savedetails'].Update(value=True)
    
        split1 = text.split(' NET STARTS AT', 1)
        pre_text = split1[0].strip()
        netname = pre_text.split('THE ', 1)[1].strip()
        self.window['input_netname'].Update(value=netname)
        self.debug.info_message("decodeTriggers. QST netname: " + netname)

        split2 = split1[1].split('ZULU', 1)
        starttime = split2[0].strip()
        self.window['input_starttime'].Update(value=starttime)
        self.debug.info_message("decodeTriggers. QST starttime: " + starttime)

        split3 = split2[1].split('MHZ', 1)
        netfre = split3[0].split('ON', 1)[1].strip()
        self.window['input_netfre'].Update(value=netfre)
        self.debug.info_message("decodeTriggers. QST netfre: " + netfre)
 
        split4 = split3[1].split('GRP', 1)
        netgrp = split4[0].split('PLS USE', 1)[1].strip()       
        self.window['input_netgroup'].Update(value=netgrp)
        self.debug.info_message("decodeTriggers. QST netgrp: " + netgrp)

        self.window['input_ncs'].Update(value=last_call)
        self.view.checkDisableAllButtons()

  """
  process opening the net
  specific format 1: WELCOME TO THE <PROFILE> EDITION OF THE <NET NAME> NET. GE THIS IS <NCS NAME> UR HOST. THIS IS A <NUM ROUNDS> ROUND <NET TYPE>'
  example: WELCOME TO THE TUESDAY EDITION OF THE HAWAII JS8 NET. GE THIS IS LB UR HOST. THIS IS A ONE ROUND ROUND TABLE NET'

  specific format 2: WELCOME TO THE <PROFILE> EDITION OF THE <NET NAME> NET. GE THIS IS <NCS NAME> UR HOST. THIS IS A <NET TYPE> GOING <NUM ROUNDS> ROUND(S).'
  example: WELCOME TO THE TUESDAY EDITION OF THE HAWAII JS8 NET. GE THIS IS LB UR HOST. THIS IS A ROUND TABLE NET GOING 3 ROUNDS'
  """
  def decodeOpenNetTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage("WELCOME TO THE ", text) ):
      self.debug.info_message("decodeTriggers. OPEN THE NET")

      if( (" WELCOME TO THE ") in text):
        self.window['cb_savedetails'].Update(value=True)

        self.view.refreshRoster([])
        self.js8net.resetRoster()
        self.js8net.setRoster( self.js8net.getRoster() + [last_call + ' ' + '-' + ' <NCS> ' + '0' + ' ' + '0' + ' ' + '0' + ' ' + '0'] )

        if(self.window['input_ncs'].get().strip() == ""):
          self.window['input_ncs'].Update(value=last_call)

        split1 = text.split(' EDITION', 1)
        pre_text = split1[0].strip()
        edition = pre_text.split('WELCOME TO THE ', 1)[1].strip()
        self.window['option_profile'].Update(value=edition)
        self.debug.info_message("decodeTriggers. OPEN edition: " + edition)

        split1_b = split1[1].split(' NET', 1)
        pre_text = split1_b[0].strip()
        netname = pre_text.split('OF THE ', 1)[1].strip()
        self.window['input_netname'].Update(value=netname)
        self.debug.info_message("decodeTriggers. QST netname: " + netname)
        
        split2 = split1_b[1].split(' UR HOST', 1)
        hostname = split2[0].split("THIS IS ", 1)[1].strip()

        callindex = self.js8net.findRoster(last_call)
        self.js8net.updateRoster(callindex, last_call, hostname, '<NCS>')
        self.debug.info_message("decodeTriggers. OPEN hostname: " + hostname)
        self.js8net.ncs_hostname = hostname

        starttime = self.window['input_starttime'].get().strip()
        if(starttime == ""):
          utcnow = datetime.utcnow()
          starttime = "{hours:02d}:{minutes:02d}".format(hours=utcnow.hour, minutes=utcnow.minute)
          self.window['input_starttime'].Update(value=starttime)
          self.debug.info_message("decodeTriggers. OPEN nettype: start time: " + str(starttime))

        """ from here on there can be two formats
        THIS IS A <NUM ROUNDS> ROUND <NET TYPE>
        THIS IS A <NET TYPE> GOING <NUM ROUNDS> ROUND(S).
        """
        if( (" DIRECTED NET") in text):
          self.debug.info_message("decodeTriggers. OPEN nettype: DIRECTED")
          self.window['option_menu'].Update(value='Directed')

          if(" GOING " in text):
            """ OK THIS IS format 2 """
            split3 = split2[1].split(' GOING ', 1)
            num = split3[1].split(" ROUND", 1)[0].strip()
            self.window['input_rounds'].Update(value=num)
            self.debug.info_message("decodeTriggers. OPEN numrounds: " + num)
          else:  
            """ OK THIS IS format 1 """
            split3 = split2[1].split(' DIRECTED NET', 1)
            numrounds = split3[0].split("THIS IS A ", 1)[1].strip()
            num = numrounds.split(' ROUND ', 1)[0].strip()
            self.window['input_rounds'].Update(value=num)
            self.debug.info_message("decodeTriggers. OPEN numrounds: " + num)
          
          """ set the current round to ONE"""
          self.window['option_currentround'].Update(value="ONE")
          self.js8net.current_round = ""

        elif( (" ROUND TABLE NET") in text):
          self.debug.info_message("decodeTriggers. OPEN nettype: ROUND TABLE")
          self.window['option_menu'].Update(value='Round Table')

          if(" GOING " in text):
            """ OK THIS IS format 2 """
            split3 = split2[1].split(' GOING ', 1)
            num = split3[1].split(" ROUND", 1)[0].strip()
            self.window['input_rounds'].Update(value=num)
            self.debug.info_message("decodeTriggers. OPEN numrounds: " + num)
          else:  
            """ OK THIS IS format 1 """
            split3 = split2[1].split(' ROUND TABLE NET ', 1)
            numrounds = split3[0].split("THIS IS A ", 1)[1].strip()
            num = numrounds.split(' ROUND', 1)[0].strip()
            self.window['input_rounds'].Update(value=num)
            self.debug.info_message("decodeTriggers. OPEN numrounds: " + num)

        split4 = split3[1].split(' GRP', 1)
        netgrp = split4[0].split('PLS USE @', 1)[1].strip()       
        if(self.window['input_netgroup'].get().strip() ==""):
          self.window['input_netgroup'].Update(value= ("@" + netgrp) )
        self.debug.info_message("decodeTriggers. Open net netgrp: @" + netgrp)

        self.view.checkDisableAllButtons()

  """
  process net control sent check in request messages to extract minimal information of group name and net control call sign
  specific format: WH6NCS: @HINET ANY CHECK-INS?
  note it is not necessary to decode all check in requests. one is more than sufficient and not even necessary.
  """
  def decodeCheckInsRequestTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage("ANY CHECK-INS?", text) ):
      self.debug.info_message("decodeTriggers. CHECK-INS")

      split1 = text.split(' ANY CHECK-INS?', 1)
      pre_text = split1[0].strip()
      netgrp = pre_text.split('@', 1)[1].strip()
      self.debug.info_message("decodeTriggers. groupname: " + netgrp)
      if(self.window['input_netgroup'].get().strip() == ""):
        self.window['input_netgroup'].Update(value=netgrp)

      if(self.window['input_ncs'].get().strip() == ""):
        self.window['input_ncs'].Update(value=last_call)

  """
  process the actual checkin messages received by net control
  
  general format1: ... <SWL>...
  general format2: ... <CHECK>...
  general format3: ... <CK-IN>...
  general format4: ... <CK IN>...
  general format5: ... <CKIN>...
  general format6: @HINET...
  
  example: WH6ABC: @HINET CHECK ME IN PLS?
  example: WH6ABC: @HINET CHECK ME IN SWL ONLY PLS?
  
  The above formats should be sufficient for automatic checkin
  If necessary, net control can do a manually adjust the roster status of the station
  """
  def decodeCheckInsTrigger(self, dict_obj, text, last_call, mode):
    callindex = self.js8net.findRoster(last_call)
    if(callindex != -1):
      status = self.js8net.getRosterStatus(callindex)
      if(status == "<HEARD>"):
        """ OK good so far now try to upgrade the status to <CHECKIN> or <SWL> automatically """
        if(" SWL" in text):
          """ OK this is format1: ... <SWL>... """
          self.debug.info_message("decodeCheckInsTrigger. Setting " + last_call + " to <SWL>")
          self.js8net.updateRosterStatus(callindex, "<SWL> ")
        elif("CHECK" in text):
          """ OK this is format2: ... <CHECK>... """
          self.debug.info_message("decodeCheckInsTrigger. setting status for " + last_call + " to <CHECKIN>")
          self.js8net.updateRosterStatus(callindex, "<CHECKIN>")
        elif("CK-IN" in text):
          """ OK this is format3: ... <CK-IN>... """
          self.debug.info_message("decodeCheckInsTrigger. setting status for " + last_call + " to <CHECKIN>")
          self.js8net.updateRosterStatus(callindex, "<CHECKIN>")
        elif("CK IN" in text):
          """ OK this is format4: ... <CK IN>... """
          self.debug.info_message("decodeCheckInsTrigger. setting status for " + last_call + " to <CHECKIN>")
          self.js8net.updateRosterStatus(callindex, "<CHECKIN>")
        elif("CKIN" in text):
          """ OK this is format5: ... <CKIN>... """
          self.debug.info_message("decodeCheckInsTrigger. setting status for " + last_call + " to <CHECKIN>")
          self.js8net.updateRosterStatus(callindex, "<CHECKIN>")
        elif("@HINET" in text):
          """ OK this is format6: @HINET... """
          self.debug.info_message("decodeCheckInsTrigger. setting status for " + last_call + " to <CHECKIN>")
          self.js8net.updateRosterStatus(callindex, "<CHECKIN>")

  """
  process qsy message from net control
  specific format: WH6NCS: @HINET QSY TO <FREQ>
  example: WH6NCS: @HINET QSY TO 7.078
  please note that stations wishing to automatically adjust the freq based on this message must use the command line option '--update_freq_on_qsy'
  """
  def decodeQsyTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage(" QSY TO ", text) ):
      self.debug.info_message("decodeTriggers. QSY message")

      split1 = text.split(' QSY TO ', 1)
      frequency = split1[1].strip()
      self.debug.info_message("decodeTriggers. qsy frequency: " + frequency)
      
      if(self.js8net.getUpdateFreqOnQsy() == True ):
        offset = int(self.window['main_offset'].get() )
        if(frequency != ""):
          self.window['input_netfre'].Update(value=frequency)
          freq = float(frequency.split("MH")[0])
          int_freq = int(freq * 1000000)
          self.js8net.setDialAndOffset(int_freq, offset)

  """
  process a new offsets plan sent by net control
  specific format: WH6ABC: @HINET ... OFFSETS PLAN IS: <COMMA SEPARATED LIST>
  example: WH6ABC: @HINET OK THE NEW OFFSETS PLAN IS: 1337,500,600,700,800,900
  """
  def decodeOffsetsPlanTrigger(self, dict_obj, text, last_call, mode):

    if( self.js8client.isTextInMessage(" OFFSETS PLAN IS: ", text) ):
      self.debug.info_message("decodeTriggers. New Offsets Plan")

      split1 = text.split(' OFFSETS PLAN IS: ', 1)
      the_plan = split1[1].strip()
      self.js8net.updateRosterOffsetsFromPlan(the_plan)
      self.debug.info_message("decodeTriggers. Offsets Plan Is: " + the_plan)

  """
  process first on the roster
  specific format 1: WH6NCS  @HINET ... FIRST ON THE ROSTER IS <CALLSIGN>. ...
  example: WH6NCS: @HINET OK LETS GET STARTED. FIRST ON THE ROSTER IS WH6ABC. GE JIM START US OUT PLS.
  
  specific format 2: WH6NCS  @HINET ... FIRST ON THE LIST IS <CALLSIGN>. ...
  example: WH6NCS: @HINET OK LETS START AT THE TOP. FIRST ON THE LIST IS WH6ABC. GE FRED YOUR REPORT PLS.
  
  general format 3: ... START WITH <CALLSIGN> ...
  example: WH6NCS  @HINET OK LETS GET STARTED. WE START WITH WH6ABC.
  example: WH6NCS  @HINET OK LETS START WITH WH6ABC.

  general format 4: ... BEGIN WITH <CALLSIGN> ...
  example: WH6NCS  @HINET OK LETS GET STARTED. WE BEGIN WITH WH6ABC.
  example: WH6NCS  @HINET OK LETS BEGIN WITH WH6ABC.
  
  general format 5: ... <CALLSIGN> IS FIRST ...
  example: WH6NCS  @HINET OK LETS GET STARTED. WH6ABC IS FIRST ON THE LIST. GE TOM YOUR REPORT PLS.

  please note <CALLSIGN> is verified to make sure it is a valid participant of the net and that net control is making the message
  """
  def decodeStartRoundTrigger(self, dict_obj, text, last_call, mode):
    first = ""	  
    if( self.js8client.isTextInMessage("FIRST ON THE ROSTER IS ", text) ):
      """ OK this is format 1: WH6NCS  @HINET ... FIRST ON THE ROSTER IS <CALLSIGN>. ... """
      if( self.js8net.getCurrentRound() == self.window['option_currentround'].get() ):
        self.js8net.incRound()

      split1 = text.split('FIRST ON THE ROSTER IS', 1)
      narrowed_text = split1[1].strip()
      first = narrowed_text.split('.', 1)[0].strip()
      callindex = self.js8net.findRoster(first)
      """ verify this is a valid call sign """
      if(callindex != -1):
        self.js8net.incrementStatus(callindex, -1, -1)
        self.js8net.startTimer(first, True)
      self.debug.info_message("decodeTriggers. First: " + first)
        
    elif( self.js8client.isTextInMessage("FIRST ON THE LIST IS ", text) ):
      """ OK this is format 2: WH6NCS  @HINET ... FIRST ON THE LIST IS <CALLSIGN>. ... """
      if( self.js8net.getCurrentRound() == self.window['option_currentround'].get() ):
        self.js8net.incRound()

      split1 = text.split('FIRST ON THE LIST IS', 1)
      narrowed_text = split1[1].strip()
      first = narrowed_text.split('.', 1)[0].strip()
      callindex = self.js8net.findRoster(first)
      """ verify this is a valid call sign """
      if(callindex != -1):
        self.js8net.incrementStatus(callindex, -1, -1)
        self.js8net.startTimer(first, True)
      self.debug.info_message("decodeTriggers. First: " + first)
        
    elif( self.js8client.isTextInMessage(" START WITH ", text) ):
      """ OK this is format 3: ... START WITH <CALLSIGN> ... """
      split1 = text.split(' START WITH ', 1)
      narrowed_text = split1[1].strip()
      first = narrowed_text.split('.', 1)[0].strip()
      callindex = self.js8net.findRoster(first)
      """ verify this is a valid call sign """
      if(callindex != -1):
        self.js8net.incrementStatus(callindex, -1, -1)
        self.js8net.startTimer(first, True)
        if( self.js8net.getCurrentRound() == self.window['option_currentround'].get() ):
          self.js8net.incRound()
        self.debug.info_message("decodeTriggers. First: " + first)
          
    elif( self.js8client.isTextInMessage(" BEGIN WITH ", text) ):
      """ OK this is format 4: ... BEGIN WITH <CALLSIGN> ... """
      split1 = text.split(' BEGIN WITH ', 1)
      narrowed_text = split1[1].strip()
      first = narrowed_text.split('.', 1)[0].strip()
      callindex = self.js8net.findRoster(first)
      """ verify this is a valid call sign """
      if(callindex != -1):
        self.js8net.incrementStatus(callindex, -1, -1)
        self.js8net.startTimer(first, True)
        if( self.js8net.getCurrentRound() == self.window['option_currentround'].get() ):
          self.js8net.incRound()
        self.debug.info_message("decodeTriggers. First: " + first)
        
    elif( self.js8client.isTextInMessage(" IS FIRST", text) ):
      """ OK this is format 5: ... <CALLSIGN> IS FIRST ... """
      split1 = text.split(' IS FIRST', 1)
      narrowed_text = split1[0].strip()
      split2 = narrowed_text.split(' ')
      first = split2[(len(split2)-1)]
      
      callindex = self.js8net.findRoster(first)
      """ verify this is a valid call sign """
      if(callindex != -1):
        self.js8net.incrementStatus(callindex, -1, -1)
        self.js8net.startTimer(first, True)
        if( self.js8net.getCurrentRound() == self.window['option_currentround'].get() ):
          self.js8net.incRound()
        self.debug.info_message("decodeTriggers. First: " + first)

  """
  process end of round

  general format 1: WH6NCS: @HINET ... THE END OF ROUND ...
  example: WH6NCS: @HINET OK WE ARE AT THE END OF ROUND 1
  example: WH6NCS: @HINET OK WE HAVE REACHED THE END OF ROUND 1

  general format 2: WH6NCS: @HINET ... THE END OF THIS ROUND ...
  example: WH6NCS: @HINET OK WE ARE AT THE END OF THIS ROUND

  general format 3: WH6NCS: @HINET ... THE END OF THE ROUND ...
  example: WH6NCS: @HINET OK WE ARE AT THE END OF THE ROUND
  example: WH6NCS: @HINET OK WE HAVE REACHED THE END OF THE ROUND

  """
  def decodeEndRoundTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage(" THE END OF ROUND ", text) ):
      """ OK this is format 1: WH6NCS: @HINET ... THE END OF ROUND ... """
      self.js8net.setCurrentRound( self.window['option_currentround'].get() )
      self.debug.info_message("decodeTriggers. END ROUND")
    elif( self.js8client.isTextInMessage(" THE END OF THIS ROUND", text) ):
      """ OK this is format 2: WH6NCS: @HINET ... THE END OF THIS ROUND ... """
      self.js8net.setCurrentRound( self.window['option_currentround'].get() )
      self.debug.info_message("decodeTriggers. END ROUND")
    elif( self.js8client.isTextInMessage(" THE END OF THE ROUND", text) ):
      """ OK this is format 3: WH6NCS: @HINET ... THE END OF THE ROUND ... """
      self.js8net.setCurrentRound( self.window['option_currentround'].get() )
      self.debug.info_message("decodeTriggers. END ROUND")


  """
  process OVER TO message  
  general format 1: WH6NCS: @HINET ... OVER TO <CALLSIGN>. ...
  example: WH6NCS: @HINET NEXT OVER TO WH6ABC. GE FRED TAKE A TURN PLS 
  
  please note message must have a period at the end of the call sign.
  """
  def decodeNextOverToTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage(" OVER TO ", text) ):
      self.debug.info_message("decodeTriggers. NEXT")

      split1 = text.split(' OVER TO ', 1)
      next_call = split1[1].split('.', 1)[0].strip()
      self.debug.info_message("decodeTriggers. OVER TO: " + next_call)

      self.js8net.startTimer(next_call, True)
      callindex = self.js8net.findRoster(next_call)
      self.js8net.incrementStatus(callindex, -1, -1)

  """
  process QRT message  
  general format: WH6ABC: @HINET ... GOING QRT...
  example: WH6ABC: @HINET THANKS FOR THE NET IM GOING QRT. ALOHA!
  """
  def decodeQrtTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage(" GOING QRT", text) ):
      self.debug.info_message("decodeTriggers. 'QRT'")
      index = self.js8net.findRoster(last_call)
      self.js8net.updateRosterStatus(index, '<QRT>')

  """
  process Back To Net message  
  general format 1: WH6ABC: @HINET ... BACK TO NET
  general format 2: WH6ABC: @HINET ... BTN
  general format 3: WH6ABC: @HINET ... BTU
  example: WH6ABC: @HINET THANKS FOR DOING THE NET BTU
  """
  def decodeBackToNetTrigger(self, dict_obj, text, last_call, mode):
    if( self.js8client.isTextInMessage(" BACK TO NET", text) ):
      index = self.js8net.findRoster(last_call)
      self.js8net.updateRosterStatus(index, '<DONE>')
      self.debug.info_message("decodeTriggers. 'BACK TO NET'")
    elif( self.js8client.isTextInMessage(" BTU", text) ):
      index = self.js8net.findRoster(last_call)
      self.js8net.updateRosterStatus(index, '<DONE>')
      self.debug.info_message("decodeTriggers. 'BACK TO NET'")
    elif( self.js8client.isTextInMessage(" BTN", text) ):
      index = self.js8net.findRoster(last_call)
      self.js8net.updateRosterStatus(index, '<DONE>')
      self.debug.info_message("decodeTriggers. 'BACK TO NET'")

  """
  decode the text triggers in incoming and outgoing messages
  the triggers are used to alter the state of the state machine
  """    
  def decodeTriggers(self, dict_obj, text, last_call, mode):

    try:
      """ only allow certain decodes if the sending station is net control"""
      ncsname = self.window['input_ncs'].get().strip()

      """ ordinarily triggers are only processed for receive messages"""
      if(self.js8net.getOperatingMode() == cn.PARTICIPANT):
        self.debug.info_message("decodeTriggers. PARTICIPANT")
        if( mode == cn.RCV):
          self.debug.info_message("decodeTriggers. RCV")
          """ all of the text triggers are for the client stations only"""
          if( self.window['option_menu'].get().strip() == 'Round Table'):
            """ for a roundtable net, stations can decode next stn triggers from any station"""
            self.decodeNextOverToTrigger(dict_obj, text, last_call, mode)

          """ do strict check to make sure station sending these messages is net control"""
          if( ncsname == last_call):
            self.debug.info_message("decodeTriggers. cal match with: " + ncsname)
            self.decodeRosterTrigger(dict_obj, text, last_call, mode)
            self.decodeStartRoundTrigger(dict_obj, text, last_call, mode)
            self.decodeEndRoundTrigger(dict_obj, text, last_call, mode)
            self.decodeCheckInsRequestTrigger(dict_obj, text, last_call, mode)
            self.decodeQsyTrigger(dict_obj, text, last_call, mode)
            self.decodeOffsetsPlanTrigger(dict_obj, text, last_call, mode)
            if( self.window['option_menu'].get().strip() == 'Directed'):
              self.decodeNextOverToTrigger(dict_obj, text, last_call, mode)
      
          """ The following triggers can be processed regardless of sending station"""
          self.decodeQstTrigger(dict_obj, text, last_call, mode)
          self.decodeOpenNetTrigger(dict_obj, text, last_call, mode)
          self.decodeQrtTrigger(dict_obj, text, last_call, mode)
          self.decodeCheckInsTrigger(dict_obj, text, last_call, mode)
          self.decodeBackToNetTrigger(dict_obj, text, last_call, mode)
          if( self.window['option_menu'].get().strip() == 'Round Table'):
            self.decodeNextOverToTrigger(dict_obj, text, last_call, mode)

        elif( mode == cn.TX):
          self.debug.info_message("decodeTriggers. TX")
          self.decodeNextOverToTrigger(dict_obj, text, last_call, mode)
          self.decodeBackToNetTrigger(dict_obj, text, last_call, mode)
          self.decodeCheckInsTrigger(dict_obj, text, last_call, mode)

      elif(self.js8net.getOperatingMode() == cn.NETCONTROL):
        self.debug.info_message("decodeTriggers. NETCONTROL")
        if( mode == cn.RCV):
          self.decodeCheckInsTrigger(dict_obj, text, last_call, mode)
          self.decodeBackToNetTrigger(dict_obj, text, last_call, mode)
          if( self.window['option_menu'].get().strip() == 'Round Table'):
            self.decodeNextOverToTrigger(dict_obj, text, last_call, mode)
        elif( mode == cn.TX):
          self.decodeOffsetsPlanTrigger(dict_obj, text, last_call, mode)
    
      self.debug.info_message("decodeTriggers. Completed")

    except:
      self.debug.error_message("method: decode triggers. " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    return ()

  """
  in line replace of the % fields in ougoing messages
  """
  def replaceFields(self, message, incSeq):
    """
    %CN - current stn op name
    %NN - next stn op name
    %ROSTER
    """
    try:
      """ the full roster """
      if '%ROSTER' in message:
        roster_text=""
        for x in range(1, len(self.js8net.roster)):
          splitstr = self.js8net.roster[x].split(" ")
          call   = splitstr[0]
          name   = splitstr[1]
          status = splitstr[2]
          
          if(x==1):
            self.view.updateNextField(call)
          
          if(status != "<IGNORE>" and status != "<HEARD>"):
            if(name != "-"):
              roster_text += call + " " + name 
            else:
              roster_text += call 
            if(x < len(self.js8net.roster)-1):
              roster_text += ", " 

        message = message.replace('%ROSTER', roster_text)

      """ conditional 'GOOD EVENING' checkbox. format %IFGOODEVE my text %GOODEVE and %ENDIFGOODEVE """
      message = self.parseIt(message, 'cb_goodeve', True, '%IFGOODEVE', '%ENDIFGOODEVE', '%GOODEVE', 'option_goodeve')

      """ conditional 'OTHER' checkbox. format %IFOTHER my text %OTHERMSG and %ENDIFOTHER """
      message = self.parseIt(message, 'cb_other', True, '%IFOTHER', '%ENDIFOTHER', '%OTHERMSG', 'multi_other')

      """ conditional 'FURTHER' checkbox. format %IFFURTHER my text and %ENDIFFURTHER """
      message = self.parseIt(message, 'cb_further', True, '%IFFURTHER', '%ENDIFFURTHER', None, None)

      """ conditional 'FURTHER' checkbox not selected. format %IFNFURTHER my text and %ENDIFNFURTHER """
      message = self.parseIt(message, 'cb_further', False, '%IFNFURTHER', '%ENDIFNFURTHER', None, None)
      
      """ conditional 'SNR' checkbox. format %IFSNR my text and %ENDIFSNR """
      message = self.parseIt(message, 'cb_snr', True, '%IFSNR', '%ENDIFSNR', None, None)
      
      """ conditional 'tks' checkbox. format %IFTKS my text and %TKSMSG %ENDIFTKS """
      message = self.parseIt(message, 'cb_rep', True, '%IFTKS', '%ENDIFTKS', '%TKSMSG', 'option_tks')
      
      """ conditional 'UR Welcome ' checkbox. format %IFURW my text and  %ENDIFURW """
      message = self.parseIt(message, 'cb_welcome', True, '%IFURW', '%ENDIFURW', None, None)
      
      """ conditional 'tks' checkbox not checked. format %IFNTKS my text %ENDIFNTKS """
      message = self.parseIt(message, 'cb_rep', False, '%IFNTKS', '%ENDIFNTKS', None, None)

      """ conditional test for checkins and heard stations in the roster. format %IFCHECKIN my %CHECKINCALL text %ENDIFCHECKIN """
      while '%IFCHECKIN' in message:
        try:		
          self.debug.info_message("replaceFields. Decoding %IFCHECKIN: " + message)
          split1 = message.split('%IFCHECKIN', 1)
          pre_text = split1[0].strip()
          split2 = split1[1].split('%ENDIFCHECKIN', 1)
          post_text = split2[1].strip()

          self.js8net.setRosterStandbyCalls("")
          found = 0
          replace_text = ""
          for x in range(len(self.js8net.roster) ):
            if (self.js8net.roster[x].split(' ')[2] == "<CHECKIN>" or self.js8net.roster[x].split(' ')[2] == "<HEARD>"):
              if(found == 1):
                self.js8net.setRosterStandbyCalls( self.js8net.getRosterStandbyCalls() + "," + self.js8net.roster[x].split(' ')[0] )
              else:              
                self.js8net.setRosterStandbyCalls( self.js8net.roster[x].split(' ')[0] )
              
              """ add the call sign """				
              if(found == 1):
                replace_text = replace_text + ", " + self.js8net.roster[x].split(' ')[0]
              else:              
                replace_text = replace_text + self.js8net.roster[x].split(' ')[0]
              """ add the name in if it exists """
              if(self.js8net.roster[x].split(' ')[1] != "-"):
                replace_text = replace_text + " " + self.js8net.roster[x].split(' ')[1]
              
              found = 1			  
          if(found == 1):
            include_text = split2[0].strip().replace('%CHECKINCALL', replace_text )
            message = pre_text + ' ' + include_text + ' ' + post_text
          else:
            message = pre_text + ' ' + post_text

          self.debug.info_message("replaceFields. processed message: " + message)
        except:
          self.debug.error_message("method: replaceFields. " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

      if (self.js8net.utc_time_now != None):
        message = self.parseIt3(message, '%ZULUTIME', "{hours:02d}:{minutes:02d}".format(hours=self.js8net.utc_time_now.hour, minutes=self.js8net.utc_time_now.minute) )
      if (self.js8net.time_now != None):
        message = self.parseIt3(message, '%LOCALTIME', "{hours:02d}:{minutes:02d}".format(hours=self.js8net.time_now.hour, minutes=self.js8net.time_now.minute) )
      
      message = self.parseIt3(message, '%NCSNAME', self.js8net.nameFromSavedCalls(self.window['input_ncs'].get().strip() ) )
      message = self.parseIt3(message, '%NCSCALL', self.window['input_ncs'].get().strip())
      message = self.parseIt3(message, '%NETNAME', self.window['input_netname'].get().strip())
      message = self.parseIt3(message, '%NETTYPE', self.window['option_menu'].get().strip())
      message = self.parseIt3(message, '%NETSTARTTIME', self.window['input_starttime'].get().strip())
      message = self.parseIt3(message, '%NETFRE', self.window['input_netfre'].get().strip())
      message = self.parseIt3(message, '%NUMROUNDS', self.window['input_rounds'].get().strip())
      message = self.parseIt3(message, '%CURRENTROUND', self.window['option_currentround'].get().strip())
      message = self.parseIt3(message, '%GROUPNAME', self.window['input_netgroup'].get().strip())
      message = self.parseIt3(message, '%OFFSETSPLAN', self.js8net.getOffsetsList() )
      
      message = self.parseIt2(message, self.window['prev_stn'].get().strip(), '%LBADFRAMES', 5)
      message = self.parseIt2(message, self.window['prev_stn'].get().strip(), '%LTIMEDELTA', 6)
        
      """ last station call sign """
      message = self.parseIt2(message, self.window['prev_stn'].get().strip(), '%LC', 0)

      """ last station name """
      message = self.parseIt2(message, self.window['prev_stn'].get().strip(), '%LN', 1)

      """ last station signal report """
      message = self.parseIt2(message, self.window['prev_stn'].get().strip(), '%LSR', 4)
      
      """ next station call sign """
      message = self.parseIt2(message, self.view.getNextCall(), '%NC', 0)
      
      """ next station name """
      message = self.parseIt2(message, self.view.getNextCall(), '%NN', 1)
      
      message = self.parseIt4(message, '%IFNETSTARTED', '%ENDIFNETSTARTED', self.js8net.net_started)
      message = self.parseIt4(message, '%IFNNETSTARTED', '%ENDIFNNETSTARTED', False if self.js8net.net_started else True)
      message = self.parseIt4(message, '%IFPREV', '%ENDIFPREV', True if (self.view.getPrevCall() !="-") else False )
      message = self.parseIt4(message, '%IFNEXT', '%ENDIFNEXT', True if (self.view.getNextCall() !="-") else False)
      message = self.parseIt4(message, '%IFNPREV', '%ENDIFNPREV', True if (self.view.getPrevCall() =="-") else False)
      message = self.parseIt4(message, '%IFNNEXT', '%ENDIFNNEXT', True if (self.view.getNextCall() =="-") else False)

      message = self.parseWeakSignalStnAward(message, '%WEAKSIGNALAWARD')
      message = self.parseSyncStnAward(message, '%SYNCAWARD')

      """ conditional test the profile string. format e.g. %PROF(Tuesday) include txt to the next %ENDPROF """
      while '%PROF(' in message:
        split1 = message.split('%PROF(', 1)
        pre_text = split1[0].strip()
        split2 = split1[1].split('%ENDPROF', 1)
        post_text = split2[1].strip()
        split3 = split2[0].split(')',1)

        if(self.view.getProfileString() == split3[0]):
          message = pre_text + ' ' + split3[1].strip() + ' ' + post_text
        else:
          message = pre_text + ' ' + post_text

        self.debug.info_message("replaceFields. Decoding %PROF() " + message)

      """ include profile text only format e.g. welcome to %PROF """
      while '%PROF' in message:
        self.debug.info_message("replaceFields. Decoding %PROF")
        split1 = message.split('%PROF', 1)
        pre_text = split1[0].strip()
        post_text = split1[1].strip()

        message = pre_text + ' ' + self.view.getProfileString().strip() + ' ' + post_text

        self.debug.info_message("replaceFields. Decoding %PROF. Profile is: " + message)

      """ select only one of the choices by random. format e.g. %CHOICE I am choice 1 %CHOICE I am choice 2 %ENDCHOICE """
      while '%CHOICE' in message:
        split1 = message.split('%CHOICE', 1)
        pre_text = split1[0].strip()
        split2 = split1[1].split('%ENDCHOICE', 1)
        post_text = split2[1].strip()
        split3 = split2[0].split('%CHOICE')
        message = pre_text + ' ' + random.choice(split3).strip() + ' ' + post_text        
        
        self.debug.info_message("replaceFields. processed message: " + message)
        
      """ select only one of the sequence items by sequencing thru them one by one. format e.g. %SEQ I am choice 1 %SEQ I am choice 2 %ENDSEQ """
      while '%SEQ' in message:
        split1 = message.split('%SEQ', 1)
        pre_text = split1[0].strip()
        split2 = split1[1].split('%ENDSEQ', 1)
        post_text = split2[1].strip()
        split3 = split2[0].split('%SEQ')

        if(self.js8net.seqnum > len(split3)-1):
          self.js8net.seqnum = 0
        message = pre_text + ' ' + split3[self.js8net.seqnum].strip() + ' ' + post_text        

        self.js8net.seqnum = self.js8net.seqnum + 1
        if(self.js8net.seqnum > len(split3)-1):
          self.js8net.seqnum = 0

        self.debug.info_message("replaceFields. processed message: " + message)

    except:
      self.debug.error_message("method: replaceFields. Check syntax. " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))

    self.debug.info_message("replaceFields. returning: " + message)

    return(message)

  """
  generic parse function. usage example parseIt(message, 'cb_goodeve', '%IFGOODEVE', '%ENDIFGOODEVE', '%GOODEVE', 'option_goodeve' ) 
  """
  def parseIt(self, message, checkbox, state, beginmarker, endmarker, replacestring, replacefield):
    while beginmarker in message:
      checked = self.window[checkbox].get()
      split1 = message.split(beginmarker, 1)
      pre_text = split1[0].strip()
      split2 = split1[1].split(endmarker, 1)
      post_text = split2[1].strip()

      if (checked == state):
        if(replacestring != None and replacefield != None):
          include_text = split2[0].strip().replace(replacestring, self.window[replacefield].get().strip() )
          message = pre_text + ' ' + include_text + ' ' + post_text
        else:
         include_text = split2[0].strip()
         message = pre_text + ' ' + include_text + ' ' + post_text

      else:
        message = pre_text + ' ' + post_text
        
    return message

  """
  generic parse function. usage parseIt2(message, self.view.getNextCall(), '%NN', 1)
  """
  def parseIt2(self, message, call, replacestring, col_index):
    if replacestring in message:
      if call != "":
        index = self.js8net.findRoster(call)
        if(index != -1):
          name = self.js8net.roster[index].split(' ')[col_index]
          if name != "-":
            message = message.replace(replacestring, name )
          else:
            message = message.replace(replacestring, '' )
        else:
          message = message.replace(replacestring, '' )
      else:
        message = message.replace(replacestring, '' )
        
    return message

  """
  generic parse function. usage parseIt3(message, '%NETNAME', self.window['input_netname'].get().strip() )
  """
  def parseIt3(self, message, replacestring, value):
    if replacestring in message :
      message = message.replace(replacestring, value )
        
    return message

  """
  generic parse function. usage example parseIt4(message, %IFNETSTARTED', %ENDIFNETSTARTED', True)
  """
  def parseIt4(self, message, beginmarker, endmarker, state):
    while beginmarker in message:
      split1 = message.split(beginmarker, 1)
      pre_text = split1[0].strip()
      split2 = split1[1].split(endmarker, 1)
      post_text = split2[1].strip()

      if (state):
        include_text = split2[0].strip()
        message = pre_text + ' ' + include_text + ' ' + post_text
      else:
        message = pre_text + ' ' + post_text
        
    return message

  """
  special function to parse weakest station signal award
  usage parseWeakSignalStnAward(message, '%WEAKSIGNALAWARD')
  """
  def parseWeakSignalStnAward(self, message, replacestring):
    self.debug.info_message("parseWeakSignalStnAward")

    lowest_snr = 100
    replace_with = ""
    if replacestring in message :
      for x in range(len(self.js8net.roster)):
        roster_split_string = self.js8net.roster[x].split(" ")
        roster_call      = roster_split_string[0]     
        roster_status    = roster_split_string[2]
        roster_SNR       = roster_split_string[4]
        roster_BadFrm    = roster_split_string[5]
        if(roster_status != "<SWL>" and roster_status != "<IGNORE>" and roster_status != "<NONE>" and roster_status != "<HEARD>" and roster_call != self.js8net.getStationCallSign()):
          if(roster_BadFrm == "0"):
            int_snr = int(roster_SNR)
            if(int_snr < lowest_snr):
              lowest_snr = int_snr
              self.debug.info_message("parseWeakSignalStnAward. lowest SNR:" + str(lowest_snr) )
        
      if(lowest_snr < 100):  
        got_one = 0		  
        for x in range(len(self.js8net.roster)):
          roster_split_string = self.js8net.roster[x].split(" ")
          roster_call      = roster_split_string[0]     
          roster_name      = roster_split_string[1]
          roster_status    = roster_split_string[2]
          roster_SNR       = roster_split_string[4]
          roster_BadFrm    = roster_split_string[5]
          if(roster_status != "<SWL>" and roster_status != "<IGNORE>" and roster_status != "<NONE>" and roster_status != "<HEARD>" and roster_call != self.js8net.getStationCallSign()):
            int_snr = int(roster_SNR)
            if(roster_BadFrm == "0" and int_snr == lowest_snr):
              if(got_one == 1):
                replace_with = replace_with + ' AND ' + roster_call + ' ' + roster_name
              else:
                replace_with = replace_with + roster_call + ' ' + roster_name
              got_one = 1				
        if(got_one > 0):
          replace_with = replace_with + ' WITH AN SNR OF ' + '{:+03d}'.format(lowest_snr) 
			
      message = message.replace(replacestring, replace_with )
        
    return message

  """
  special function to parse best syncd station award
  usage parseSyncStnAward(message, '%SYNCSTNAWARD')
  """
  def parseSyncStnAward(self, message, replacestring):
    self.debug.info_message("parseSyncStnAward")

    lowest_sync=1000
    replace_with = ""
    if replacestring in message :
      for x in range(len(self.js8net.roster)):
        roster_split_string = self.js8net.roster[x].split(" ")
        roster_call      = roster_split_string[0]     
        roster_status    = roster_split_string[2]
        roster_offset    = roster_split_string[3]
        roster_SNR       = roster_split_string[4]
        roster_BadFrm    = roster_split_string[5]
        roster_timedlt   = roster_split_string[6]
        if(roster_status != "<SWL>" and roster_status != "<IGNORE>" and roster_status != "<NONE>" and roster_status != "<HEARD>" and roster_call != self.js8net.getStationCallSign()):
          if(roster_BadFrm == "0"):
            int_sync = abs( int(roster_timedlt) )
            if(int_sync < lowest_sync):
              lowest_sync = int_sync
              self.debug.info_message("parseSyncStnAward. lowest sync:" + str(lowest_sync) )

      if(lowest_sync < 1000):  
        got_one = 0		  
        for x in range(len(self.js8net.roster)):
          roster_split_string = self.js8net.roster[x].split(" ")
          roster_call      = roster_split_string[0]     
          roster_name      = roster_split_string[1]
          roster_status    = roster_split_string[2]
          roster_SNR       = roster_split_string[4]
          roster_BadFrm    = roster_split_string[5]
          roster_timedlt   = roster_split_string[6]
          if(roster_status != "<SWL>" and roster_status != "<IGNORE>" and roster_status != "<NONE>" and roster_status != "<HEARD>"  and roster_call != self.js8net.getStationCallSign()):
            int_sync = abs( int(roster_timedlt) )
            if(roster_BadFrm == "0" and int_sync == lowest_sync):
              if(got_one == 1):
                replace_with = replace_with + ' AND ' + roster_call + ' ' + roster_name
              else:
                replace_with = replace_with + roster_call + ' ' + roster_name
              got_one = 1				
        if(got_one > 0):
          replace_with = replace_with + ' WITH A TIME DELTA OF ' + str(lowest_sync)
			
      message = message.replace(replacestring, replace_with )
        
    return message

