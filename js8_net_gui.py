#!/usr/bin/env python
import PySimpleGUI27 as sg
import sys
import JS8_Client
import threading
import json
import constant
import calendar
import constant as cn

from datetime import datetime, timedelta
from datetime import time


class MainWindow(object):

  """
  define a set of standard hardcoded messages
  """
       
  message_list_buttons = {'QST'   :'@ALLCALL QST QST THE %NETNAME NET STARTS AT %NETSTARTTIME ZULU ON %NETFRE MHZ. %SEQ PLS FEEL FREE TO JOIN US. %SEQ DX STATIONS ARE WELCOME TO JOIN US. %SEQ %ENDSEQ PLS USE %GROUPNAME GRP',\
                          'PreCK' : '%GROUPNAME %IFNNETSTARTED %SEQ ANY PRE-CHKS? %SEQ ANY MORE PRE-CHKS? %ENDSEQ %ENDIFNNETSTARTED '\
                                    '%IFNETSTARTED %SEQ ANY CK-INS? %SEQ ANY MORE CK-INS? %SEQ LAST CALL FOR CK-INS %ENDSEQ %ENDIFNETSTARTED',\
                          'Open'  :'%SEQ'\
                                   '%GROUPNAME IT IS %LOCALTIME IN THE HAWAIIAN ISLANDS AND TIME FOR THE %PROF EDITION OF THE %NETNAME NET. GE THIS IS %NCSNAME UR HOST. THIS IS A %NUMROUNDS ROUND '\
                                   'DIRECTED NET TO TEST JS8. PLS '\
                                   'USE %GROUPNAME GRP FOR ALL MSGS TO THE NET. '\
                	               '%SEQ '\
                                   '%GROUPNAME IT IS %LOCALTIME IN THE HAWAIIAN ISLANDS AND TIME FOR THE %PROF EDITION OF THE %NETNAME NET. '\
                                    'GE THIS IS %NCSNAME UR HOST. THIS IS A %NETTYPE NET GOING %NUMROUNDS ROUNDS. PLS '\
                                   'USE %GROUPNAME GRP FOR ALL MSGS TO THE NET.'\
                	               '%ENDSEQ ',\
                          'CKin'  : '%GROUPNAME %IFNNETSTARTED %SEQ ANY PRE-CHECKS? %SEQ ANY MORE PRE-CHECKS? %ENDSEQ %ENDIFNNETSTARTED '\
                                    '%IFNETSTARTED %SEQ ARE THERE ANY CHECK-INS? %SEQ ANY MORE CHECK-INS FOR THE NET CALL NOW? %SEQ LAST CALL FOR CHECK-INS %ENDSEQ %ENDIFNETSTARTED',\
                          'Gotu'  : '%GROUPNAME'\
                                    '%SEQ %IFCHECKIN OK I HAVE ADDED %CHECKINCALL TO THE ROSTER. GE TKS FOR CHECKING IN. %ENDIFCHECKIN'\
                                    '%SEQ %IFCHECKIN OK I HEARD %CHECKINCALL. GE TKS FOR CHECKING IN.%ENDIFCHECKIN '\
                                    '%ENDSEQ'\
                                    '%IFNNETSTARTED ARE THERE ANY MORE PRE-CHKS? %ENDIFNNETSTARTED '\
                                    '%IFNETSTARTED ARE THERE ANY MORE CHECK-INS? %ENDIFNETSTARTED ',\
                          'Roster': '%GROUPNAME %SEQ OK THE ROSTER IS: %ROSTER '\
                                               '%SEQ OK SO FAR THE ROSTER IS: %ROSTER '\
                                               '%SEQ OK THE UPDATED ROSTER IS: %ROSTER  %ENDSEQ',\
                          'First' : '%GROUPNAME %SEQ OK LETS GET STARTED. FIRST ON THE ROSTER IS %NC. GE %NN START US OUT PLS'\
                                               '%SEQ OK LETS START ROUND %CURRENTROUND. FIRST ON THE LIST IS %NC. GE %NN TAKE A TURN PLS'\
                                               '%SEQ OK WE START WITH %NC. GE %NN HOW ARE YOU DOING?'\
                                               '%SEQ OK WE BEGIN WITH %NC. GE %NN TAKE A TURN PLS'\
                                               '%SEQ OK %NC IS FIRST ON THE LIST. GE %NN YOUR REPORT PLS'\
                                               '%ENDSEQ',\
                          'Next'  :        '%SEQ'\
							               '%GROUPNAME '\
							               '%IFURW UR VERY WELCOME. %ENDIFURW '\
                                           '%IFTKS Thanks %LN for the %TKSMSG. %ENDIFTKS '\
                                           '%IFNTKS Thanks %LN. %ENDIFNTKS '\
                                           '%IFSNR Your SNR IS %LSR WITH %LBADFRAMES DROPPED FRAMES AND A TIME DELTA OF %LTIMEDELTA. '\
                                           '%ENDIFSNR'\
                                           '%IFOTHER %OTHERMSG. %ENDIFOTHER '\
                                           '%IFFURTHER Anything further for the net %LN? %ENDIFFURTHER '\
                                           '%IFGOODEVE have a %GOODEVE %LN. %ENDIFGOODEVE '\
                                           '%IFNFURTHER '\
                                           '%IFNEXT Next over to %NC. GE %NN TAKE A TURN PLS %ENDIFNEXT'\
                                           '%ENDIFNFURTHER '\
							               '%SEQ '\
							               '%GROUPNAME '\
							               '%IFURW UR VERY WELCOME. %ENDIFURW '\
                                           '%IFTKS Thanks for the %TKSMSG. %ENDIFTKS '\
                                           '%IFNTKS Thanks %LN. %ENDIFNTKS '\
                                           '%IFSNR Your SNR is %LSR '\
                                           '%ENDIFSNR'\
                                           '%IFOTHER %OTHERMSG. %ENDIFOTHER '\
                                           '%IFFURTHER Anything further for the net %LN? %ENDIFFURTHER '\
                                           '%IFGOODEVE have a %GOODEVE %LN. %ENDIFGOODEVE '\
                                           '%IFNFURTHER '\
                                           '%IFNEXT Next over to %NC. GE %NN TAKE A TURN PLS %ENDIFNEXT'\
                                           '%ENDIFNFURTHER '\
							               '%SEQ '\
                                           '%IFNEXT %GROUPNAME Next over to %NC. GE %NN TAKE A TURN PLS %ENDIFNEXT'\
                                           '%IFNNEXT OK looks like we are at the end of the list. Any late check ins? %ENDIFNNEXT'\
							               '%SEQ '\
                                           '%IFNEXT %GROUPNAME OK LETS TRY GOING OVER TO %NC ONE MORE TIME. GE %NN TAKE A TURN PLS. %ENDIFNEXT'\
                                           '%IFNNEXT OK we are at the end of the roster. Are there any late check ins? %ENDIFNNEXT'\
							               '%ENDSEQ ',\
                          'End'   :        '%SEQ'\
							               '%GROUPNAME '\
							               '%IFURW UR VERY WELCOME. %ENDIFURW '\
                                           '%IFTKS Thanks %LN for the %TKSMSG. %ENDIFTKS '\
                                           '%IFNTKS Thanks %LN. %ENDIFNTKS '\
                                           '%IFSNR Your SNR IS %LSR WITH %LBADFRAMES DROPPED FRAMES AND A TIME DELTA OF %LTIMEDELTA. '\
                                           '%ENDIFSNR'\
                                           '%IFOTHER %OTHERMSG. %ENDIFOTHER '\
                                           '%IFFURTHER Anything further for the net %LN? %ENDIFFURTHER '\
                                           '%IFGOODEVE have a %GOODEVE %LN. %ENDIFGOODEVE '\
                                           '%IFNFURTHER '\
                                           'TKS ALL FOR UR COMMENTS ON ROUND %CURRENTROUND. OK WE ARE AT THE END OF THE ROUND ARE THERE ANY LATE CHECK-INS?'\
                                           '%ENDIFNFURTHER '\
							               '%SEQ '\
							               '%GROUPNAME '\
							               '%IFURW UR VERY WELCOME. %ENDIFURW '\
                                           '%IFTKS Thanks for the %TKSMSG. %ENDIFTKS '\
                                           '%IFNTKS Thanks %LN. %ENDIFNTKS '\
                                           '%IFSNR Your SNR is %LSR '\
                                           '%ENDIFSNR'\
                                           '%IFOTHER %OTHERMSG. %ENDIFOTHER '\
                                           '%IFFURTHER Anything further for the net %LN? %ENDIFFURTHER '\
                                           '%IFGOODEVE have a %GOODEVE %LN. %ENDIFGOODEVE '\
                                           '%IFNFURTHER '\
                                           'OK WE ARE AT THE END OF THIS ROUND. ARE THERE ANY LATE CHECK-INS?'\
                                           '%ENDIFNFURTHER '\
							               '%SEQ '\
                                           'TKS ALL FOR UR COMMENTS. OK WE ARE AT THE END OF ROUND %CURRENTROUND. ARE THERE ANY LATE CHECK-INS?'\
							               '%SEQ '\
                                           'TKS ALL FOR UR COMMENTS. OK IT LOOKS LIKE WE ARE AT THE END OF THE ROUND.'\
							               '%ENDSEQ ',\
                          'Skip'  : '%GROUPNAME OK well come back to %LN. %IFNEXT Next over to %NN. GE %NN UR REPORT PLS %ENDIFNEXT',\
                          'Prompt': '%GROUPNAME %SEQ HI %NN ur turn %SEQ %NN ur turn %SEQ %NN? %SEQ %NN take a turn pls %ENDSEQ',\
                          'Over To': '%GROUPNAME %SEQ OK lets try %NC again. GE %NN take a turn pls %SEQ OK Now over to %NC. go ahead %NN %SEQ over to %NN %ENDSEQ',\
                          'Cmnt'  : '%GROUPNAME %SEQ ARE THERE ANY QUESTIONS OR COMMENTS? %SEQ ANY MORE QUESTIONS OR COMMENTS BEFORE I CLOSE? %SEQ LAST CALL FOR QUESTIONS OR COMMENTS BEFORE I CLOSE %ENDSEQ',\
                          'Close' : '%GROUPNAME THIS CONCLUDES TODAYS NET. TKS ALL FOR SUPPORTING JS8 IN HAWAII. THE NET IS NOW CLOSED AT %LOCALTIME HST AND THIS FRE RETURNED TO RGLR AMTR RADIO USE. 73 TO ALL AND ALOHA DE %NCSCALL',\
                          'NCS_Cust1' : '%GROUPNAME OK ITS AWARD TIME! '\
                                            '%SEQ OK THE AWARD FOR PERFECT COPY WEAKEST SIGNAL STN GOES TO %WEAKSIGNALAWARD. AWESOME! HAVE THREE GOLD STARS! '\
                                            '%SEQ OK THE AWARD FOR BEST TIME SYNCED STN WITH NET CONTROL GOES TO %SYNCAWARD AWESOME! HAVE THREE GOLD STARS! '\
                                            '%SEQ '\
                                            'THE AWARD FOR PERFECT COPY WEAKEST SIGNAL STN GOES TO %WEAKSIGNALAWARD. AWESOME! HAVE THREE GOLD STARS! '\
                                            'AND THE AWARD FOR BEST TIME SYNCED STN WITH NET CONTROL GOES TO %SYNCAWARD AWESOME! THREE GOLD STARS ALSO!'\
                                            '%ENDSEQ.',\
                          'NCS_Cust2' : '%SEQ'\
                                        '%GROUPNAME OK THE NEW OFFSETS PLAN IS: %OFFSETSPLAN '\
                                        '%SEQ'\
                                        '%GROUPNAME QSY TO 7.078 '\
                                        '%ENDSEQ ',\
                          'CkMeIn' : '%GROUPNAME %SEQ CHECKING IN'\
                                                '%SEQ CHECK ME IN PLS'\
                                                '%SEQ CHECK ME IN SWL ONLY PLS'\
                                                '%SEQ CHECK-IN'\
                                                '%SEQ CHECKING IN TO THE NET %ENDSEQ',\
                          'Alert'  : '%GROUPNAME %SEQ BREAK BREAK'\
                                               '%SEQ EMER TRAFFIC REQUEST'\
                                               '%SEQ ALERT ALERT %ENDSEQ',\
                          'QRT'    : '%GROUPNAME %SEQ I AM GOING QRT TKS'\
                                             '%SEQ GOING QRT ALOHA ALL %ENDSEQ',\
                          'POST'   : '%GROUPNAME POSTING TO SIDEBAR %IFOTHER %OTHERMSG. %ENDIFOTHER ',\
                          'TKS'    : '%GROUPNAME '\
                                           '%IFTKS Thanks %LN for the %TKSMSG. %ENDIFTKS '\
                                           '%IFNTKS Thanks %LN. %ENDIFNTKS '\
                                           '%IFSNR %SEQ Your FULL Signal report is SNR:%LSR, BAD FRAMES:%LBADFRAMES, TIME DELTA:%LTIMEDELTA '\
                                           '%SEQ Your SNR is %LSR '\
                                           '%ENDSEQ %ENDIFSNR'\
                                           '%IFOTHER %OTHERMSG. %ENDIFOTHER '\
                                           '%IFGOODEVE have a %GOODEVE %LN. %ENDIFGOODEVE ',\
                          'MyComment' : '%GROUPNAME My Comment %IFOTHER %OTHERMSG. %ENDIFOTHER ',\
                          'CliCust1' : '%GROUPNAME SIDE-POST COMMENT %IFOTHER %OTHERMSG. %ENDIFOTHER ',\
                          'CliCust2' : '%GROUPNAME OK THE AWARD FOR '\
                                            '%SEQ PERFECT COPY WEAKEST SIGNAL STN GOES TO %WEAKSIGNALAWARD. AWESOME! HAVE THREE GOLD STARS! '\
                                            '%SEQ BEST TIME SYNCED STN WITH NET CONTROL GOES TO %SYNCAWARD AWESOME! HAVE THREE GOLD STARS! %ENDSEQ.'}


  message_list_buttons_edited = {}

  """ Create some test callsigns for the simulated messages """  
  test_callsign_ncs  = "WH6NCS"
  test_name_ncs      = "GERONIMO"
  test_callsign_stn1 = "WH6ABC"
  test_name_stn1     = "FRED"
  test_callsign_stn2 = "WH6DEF"
  test_name_stn2     = "TOM"
  test_callsign_stn3 = "WH6GHI"
  test_name_stn3     = "MARC"
  test_callsign_stn4 = "WH6JKL"
  test_name_stn4     = "BILL"

  """ create simulated messages """
  message_side_list_client = {'QST'             : test_callsign_ncs + ': @ALLCALL QST QST THE HAWAII JS8 NET STARTS AT 04:30 ZULU ON 7.095 MHZ. PLS USE @HINET GRP',\
                              'ROSTER-1'        : test_callsign_ncs + ': @HINET THE ROSTER IS: ' + test_callsign_stn1 + ' ' + test_name_stn1 + ', '\
                                                                                                 + test_callsign_stn2 + ' ' + test_name_stn2 + ', '\
                                                                                                 + test_callsign_stn3 + ' ' + test_name_stn3 + ', '\
                                                                                                 + test_callsign_stn4 + ' ' + test_name_stn4, \
                              'ROSTER-2'        : test_callsign_ncs + ': @HINET THE ROSTER IS: ' + test_callsign_stn1 + ' ' + test_name_stn1 + ', '\
                                                                                                 + test_callsign_stn2 + ', ' \
                                                                                                 + test_callsign_stn3 + ', ' \
                                                                                                 + test_callsign_stn4 + ' ' + test_name_stn4, \
                              'OPEN DIRECT 1'   : test_callsign_ncs + ': @HINET WELCOME TO THE TUESDAY EDITION OF THE HAWAII JS8 NET. GE THIS IS GERONIMO UR HOST. THIS IS A ONE ROUND DIRECTED NET TO TEST JS8. PLS USE @HINET GRP.',\
                              'OPEN DIRECT 2'   : test_callsign_ncs + ': @HINET WELCOME TO THE TUESDAY EDITION OF THE HAWAII JS8 NET. GE THIS IS GERONIMO UR HOST. THIS IS A DIRECTED NET GOING TWO ROUNDS. PLS USE @HINET GRP.',\
                              'OPEN RNDTABLE 1' : test_callsign_ncs + ': @HINET WELCOME TO THE TUESDAY EDITION OF THE HAWAII JS8 NET. GE THIS IS GERONIMO UR HOST. THIS IS A ONE ROUND ROUND TABLE NET TO TEST JS8. PLS USE @HINET GRP.',\
                              'OPEN RNDTABLE 2' : test_callsign_ncs + ': @HINET WELCOME TO THE TUESDAY EDITION OF THE HAWAII JS8 NET. GE THIS IS GERONIMO UR HOST. THIS IS A ROUND TABLE NET GOING THREE ROUNDS. PLS USE @HINET GRP.',\
                              'CKIN REQ'        : test_callsign_ncs + ': @HINET ANY CHECK-INS?',\
                              'CKIN 1'          : test_callsign_ncs + ': @HINET CHECK ME IN PLS',\
                              'CKIN 2'          : test_callsign_ncs + ': @HINET CHECK ME IN SWL ONLY PLS',\
                              'CKIN 3'          : test_callsign_ncs + ': @HINET CHECKING IN TO THE NET',\
                              'CKIN 4'          : test_callsign_ncs + ': @HINET CKIN',\
                              'CKIN 5'          : test_callsign_ncs + ': @HINET CK-IN FOR THE NET',\
                              'CKIN 6'          : test_callsign_ncs + ': @HINET CK IN',\
                              'CKIN 7'          : test_callsign_ncs + ': @HINET BLAH BLAH BLAH',\
                              'CKIN 8'          : test_callsign_ncs + ': @HINET CHECK IN',\
                              'QSY'             : test_callsign_ncs + ': @HINET QSY TO 3.562',\
                              'OFFSETPLAN1'     : test_callsign_ncs + ': @HINET OK THE NEW OFFSETS PLAN IS: %OFFSETSPLAN',\
                              'OFFSETPLAN2'     : test_callsign_ncs + ': @HINET OK THE NEW OFFSETS PLAN IS: 1100,500,600,700,800,900',\
                              'FIRST 1'         : test_callsign_ncs + ': @HINET OK FIRST ON THE ROSTER IS WH6DEF',\
                              'FIRST 2'         : test_callsign_ncs + ': @HINET OK FIRST ON THE LIST IS WH6ABC',\
                              'FIRST 3'         : test_callsign_ncs + ': @HINET OK WE START WITH WH6ABC',\
                              'FIRST 4'         : test_callsign_ncs + ': @HINET OK WE BEGIN WITH WH6DEF',\
                              'FIRST 5'         : test_callsign_ncs + ': @HINET OK SO WH6ABC IS FIRST ON THE LIST',\
                              'END 1'           : test_callsign_ncs + ': @HINET OK WE ARE AT THE END OF ROUND 1',\
                              'END 2'           : test_callsign_ncs + ': @HINET OK WE ARE AT THE END OF THIS ROUND',\
                              'END 3'           : test_callsign_ncs + ': @HINET OK WE ARE AT THE END OF THE ROUND',\
                              'OVER TO 1'       : test_callsign_ncs + ': @HINET NEXT WE GO OVER TO WH6DEF',\
                              'OVER TO 2'       : test_callsign_ncs + ': @HINET OK THANKS FRED. NEXT OVER TO WH6DEF. GE TOM TAKE A TURN PLS',\
                              'BTU 1'           : test_callsign_ncs + ': @HINET THANKS FOR THE NET BACK TO NET',\
                              'BTU 2'           : test_callsign_ncs + ': @HINET THANKS FOR THE NET BTU',\
                              'BTU 3'           : test_callsign_ncs + ': @HINET THANKS FOR THE NET BTN',\
                              'QRT'             : test_callsign_ncs + ': @HINET TKS FOR DOING THE NET IM GOING QRT. ALOHA'}


  def __init__(self):  
    self.next_flash_buttons = None
    self.currently_editing  = None
    self.delayed_send = 0
    self.delay_value = 25
    self.btn_clr1 = 'white'
    self.btn_clr2 = 'green'
    self.btn_flashclr1 = 'red'
    self.btn_flashclr2 = 'blue'
                            
  def setDelayValue(self, value):
    self.delay_value = value

  def getDelayValue(self):
    return self.delay_value

  def updateEditedMessage(self, key, value):
    self.message_list_buttons_edited[key] = value
    return
    
  def getEditedMessage(self, key):
    if(key not in self.message_list_buttons_edited):
      return self.message_list_buttons[key]
    else:
      return self.message_list_buttons_edited[key]

  def deleteEditedMessage(self, key):
    return self.message_list_buttons_edited.pop(key, None)

  def getDefaultMessage(self, key):
    return self.message_list_buttons[key]

  def isEditedMessage(self, key):
    if(key in self.message_list_buttons_edited):
      return True 
    else:
      return False


  def deleteEditedMessage(self, key):
    if(key in self.message_list_buttons_edited):
      del self.message_list_buttons_edited[key]
    return

  def zulutime_as_string(self):
    mytime = datetime.utcnow().strftime("%H:%M:%S")
    return mytime

  def stopFlash(self, timeout):
    self.window['multiRcv'].Update(background_color='SeaGreen1')
    self.window['multiSide'].Update(background_color='LightBlue1')
    self.window['slider_timeout'].Update(timeout)
    return()

  def writeMsgToScreen(self, dict_obj, text, js8client, last_call):

    self.js8net.debug.info_message("writeMsgToScreen")

    insert_string = ""
    name = self.js8net.getRosterName( self.js8net.findRoster(last_call) )

    if(name!="" and name!="-"):
      insert_string = " " + last_call + "-" + name

    """ update main offset and sidebar offset fields"""
    prev_offset_main    = self.js8net.main_offset
    prev_offset_sidebar = self.js8net.sidebar_offset
    
    offset = js8client.getParam(dict_obj, "OFFSET")
    this_offset = int(offset)

    if(this_offset > (self.js8net.getSideMainOffsetBoundary()-85) ):
      self.js8net.main_offset = this_offset
    else:
      self.js8net.sidebar_offset = this_offset

    """
    update the main received text fields
    figure out which channel and write text to screen
    """
    if(this_offset > (self.js8net.getSideMainOffsetBoundary()-170) ):
      if(this_offset > prev_offset_main-10 and this_offset < prev_offset_main+10):
        self.window['multiRcv'].Update(value=text, append=True)
      else:
        self.window['multiRcv'].Update(value="\n<" + self.zulutime_as_string() + insert_string + "> " + text, append=True)
    else: 
      if(this_offset > prev_offset_sidebar-10 and this_offset < prev_offset_sidebar+10):
        self.window['multiSide'].Update(value=text, append=True)
      else:
        self.window['multiSide'].Update(value="\n<" + self.zulutime_as_string() + insert_string + "> " + text, append=True)

    self.js8net.debug.info_message("writeMsgToScreen complete")

    return()

  def refreshRoster(self, roster):
    self.js8net.setRoster(roster)
    self.window['roster'].Update(roster)

  def getStatus(self, values):
    name = values['rstr_status'].strip()
    if(name == None or name == ""):
      name = "-"
    return(name)

  def getCall(self, values):
    name = values['roster_choose'].strip()
    if(name == None or name == ""):
      name = "-"
    return(name)

  def getCallAlt(self):
    call = self.window['roster_choose'].get().strip()
    if(call == None or call == ""):
      call = "-"
    return(call)

  def getName(self, values):
    name = values['rstr_name'].strip()
    if(name == None or name == ""):
      name = "-"
    return(name)

  def getNextCall(self):
    call = self.window['next_stn'].get().strip()
    if(call == None or call == ""):
      call = "-"
    return(call)

  def getPrevCall(self):
    call = self.window['prev_stn'].get().strip()
    if(call == None or call == ""):
      call = "-"
    return(call)
    
  def getProfileString(self):
	return (self.window['option_profile'].get() )

  def getSelectedIndex(self, values):
    return (values['roster'][0])

  def getSelected(self, values):
    return (values['roster'])

  def updateNextField(self, text):
    self.window['next_stn'].Update(text)

  def updatePrevField(self, text):
    self.window['prev_stn'].Update(text)

  def flashcolor(self, values, color1, color2):
    self.window['multiRcv'].Update(background_color=color1)
    self.window['multiSide'].Update(background_color=color2)
    return

  def updateCallNameStatus(self, values, call, name, status):
    self.window['roster_choose'].Update(value=call)
    self.window['rstr_name'].Update(name)
    self.window['rstr_status'].Update(status)
    return

  def removestn(self, values, roster):
    self.refreshRoster(roster)
    self.window['roster_choose'].Update('')
    self.window['rstr_name'].Update('')
    self.window['rstr_status'].Update('')
    return

  def clearall(self, values):
    self.refreshRoster([])
    self.updateCallNameStatus(None, '', '', '<NONE>')
    return

  def populateall(self, values):
    js = self.js8net.getNcsData()
    netgrp = js.get("params").get("NetGroup")
    netfre = js.get("params").get("Frequency")
    
    self.window['input_rounds'].Update(value='')
    self.window['input_ncs'].Update(value='')
    self.window['input_netgroup'].Update(value=netgrp)
    self.window['input_netfre'].Update(value=netfre)
    self.window['input_netname'].Update(value='')
    self.window['input_starttime'].Update(value='')
    return

  def run(self, js8client, js8net, dispatcher):

    self.js8client = js8client
    self.js8net = js8net

    try:
      while True:
        event, values = self.window.read(timeout=100)
       
        try:
          dispatcher.dispatch[event](dispatcher, values)
        except:
          dispatcher.event_catchall(values)

        if event in ('Exit', None):
          break

      self.window.close()
    except:
      self.event_exit(None)
      self.window.close()

    self.window.close()

  def event_exit(self, values):

    try:
      self.writeDictToFile("js8net_save_data.txt")
      self.js8client.stopThreads()
    except:
      self.debug.error_message("method: event_exit. " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))
      
    return()

  def readDictFromFile(self, filename):
    with open(filename) as f:
      data = f.read()
  
    """  
    reconstructing the data as a dictionary
    """
    js = json.loads(data)

    """ now add the edited data object """	  
    self.message_list_buttons_edited = js.get("editdata")
   
    return(js)


  def writeDictToFile(self, filename):
	  
    ncs_fields = False
    client_fields = False
    if(self.js8net.getOperatingMode() == cn.PARTICIPANT):
      client_fields = True		
    elif(self.js8net.getOperatingMode() == cn.NETCONTROL):
      ncs_fields = True		
	
    netname = ""  
    edition = ""
    netgroup = ""
    nettype = ""
    netstart = ""
    netfre = ""
    ncs = ""    
    
    checked = self.window['cb_savedetails'].get()

    if(self.js8net.getOperatingMode() == cn.PARTICIPANT):
      netname  = self.js8net.getNcsData().get("params").get("NetName")
      edition  = self.js8net.getNcsData().get("params").get("Edition")
      netgroup = self.js8net.getNcsData().get("params").get("NetGroup")
      nettype  = self.js8net.getNcsData().get("params").get("DirectedRnd")
      netstart = self.js8net.getNcsData().get("params").get("StartTime")
      netfre   = self.js8net.getNcsData().get("params").get("NetFre")
      ncs      = self.js8net.getNcsData().get("params").get("NCS")
	  
    """ individual fields first """	  
    details = { 'params': {'NetName'    : self.window['input_netname'].get() if (ncs_fields or checked) else netname,
                           'Edition'    : self.window['option_profile'].get() if (ncs_fields or checked) else edition,
                           'NetGroup'   : self.window['input_netgroup'].get() if (ncs_fields or checked) else netgroup,
                           'DirectRnd'  : self.window['option_menu'].get() if (ncs_fields or checked) else nettype,
                           'StartTime'  : self.window['input_starttime'].get() if (ncs_fields or checked) else netstart,
                           'NetFre'     : self.window['input_netfre'].get() if (ncs_fields or checked) else netfre,
                           'NCS'        : self.window['input_ncs'].get() if (ncs_fields or checked) else ncs,
                           'Rounds'     : self.window['input_rounds'].get(),
                           'AutoCheckin': self.window['cb_autocheckin'].get(),
                           'PrevStn'    : self.window['prev_stn'].get(),
                           'NextStn'    : self.window['next_stn'].get(),
                           'SendOption' : self.window['option_postsend'].get(),
                           'MainOffset' : self.window['main_offset'].get(),
                           'SideOffset' : self.window['sidebar_offset'].get(),
                           'AutoHandoff': self.window['cb_autohandoff'].get(),
                           'FlashBtn'   : self.window['cb_flashbtn'].get(),
                           'Announce'   : self.window['multi_announce'].get().strip(),
                           'Report'     : self.window['multi_myreport'].get().strip(),
                           'Other'      : self.window['multi_other'].get().strip() } }

    """ now add the edited data object """	  
    details['editdata']=self.message_list_buttons_edited

    """ now add the roster data object """	  
    if(self.js8net.getOperatingMode() == cn.NETCONTROL):
      details['roster']=self.js8net.getRoster()
    elif(self.js8net.getOperatingMode() == cn.PARTICIPANT):
      details['roster']=self.js8net.getNcsData().get("roster")

    """ now add the call sign lookups data object  """
    details['callsigns']=self.js8net.getKnownCalls()
 
    with open(filename, 'w') as convert_file:
              convert_file.write(json.dumps(details))
    return()

  """
  handle the net control buttons across the screen
  """
  def handle_button(self, values, key, btnname):

    rettext = ''
    if(self.window['input_netgroup'].get().strip() == ""):
      self.js8net.debug.error_message("group field is empty. please specify a group name")
    else:		
      mainside = cn.PREVIEW_MAIN 
      rettext = self.handle_button_common(values, key, btnname, mainside, False)
    return rettext
    
  def handle_button_common(self, values, key, btnname, mainside, handoff):

    rettext = ''
    if(self.window['input_netgroup'].get().strip() == ""):
      self.js8net.debug.error_message("group field is empty. please specify a group name")
    else:		
      rettext = self.handle_button_common2(values, key, btnname, mainside, handoff)

    return rettext

  def handle_button_common2(self, values, key, btnname, mainside, handoff):

    action_window = 'multi_select'
    if( mainside == cn.PREVIEW_MAIN):
      action_window = 'multi_select'
      offset = int(self.window['main_offset'].get().split("Hz")[0])
      freq_text = self.window['input_netfre'].get().strip()
      if(freq_text != ""):
        freq = float(freq_text.split("MHz")[0])
        int_freq = int(freq * 1000000)
        self.js8net.setDialAndOffset(int_freq, offset)
      
    elif( mainside == cn.PREVIEW_SIDE):
      action_window = 'multi_side'
      offset = int(self.window['sidebar_offset'].get().split("Hz")[0])
      freq_text = self.window['input_netfre'].get().strip()
      if(freq_text != ""):
        freq = float(freq_text.split("MHz")[0])
        int_freq = int(freq * 1000000)
        self.js8net.setDialAndOffset(int_freq, offset)
	  
    if(self.js8net.getEditMode() == False):
      text = self.getEditedMessage(key).strip()
      self.js8net.saved_send_string = self.js8net.parser.replaceFields(text, True).strip()
      self.window[action_window].update(self.js8net.saved_send_string)
      send_type = self.window['option_postsend'].get()
      
      if(self.js8net.saved_send_string != ""):
       
        if(send_type != "Post to JS8Call + send"):
          self.js8net.sendIt(self.js8net.saved_send_string, handoff)
        else:
          self.delayed_send = self.getDelayValue()

      else:
        self.stopFlashingAllButtons()
        self.startFlashButtons(self.next_flash_buttons)
        self.next_flash_buttons = []
    else:
      try:		
        if(self.js8net.getEditState() == cn.SAVED):
          """ going into the EDIT state """			
          self.stopFlashingButtons(['button_qst', 'button_open', 'button_ckin', 'button_roster', 'button_first', 'button_next', 'button_prompt', 'button_skip', 'button_end', 'button_cmnt', 'button_close'])
          self.startFlashButtons([btnname])
          """ move the text into the edit window and change the flashing buttons """		
          text = self.getEditedMessage(key)

          if(self.isEditedMessage(key)):
            self.window['cb_edited'].update(True)
          else:		
            self.window['cb_edited'].update(False)
          self.currently_editing = key
          self.window[action_window].update(text)
        else:
          """ going into the SAVED state """			
          """ save the edited data and set the flashing buttons again  """        
          self.startFlashAllButtons()
          text = self.window[action_window].get().strip()
          
          if(self.window['cb_edited'].get() ):
            self.updateEditedMessage(key, text)
          else: 
            self.deleteEditedMessage(key)	
          self.window[action_window].update("")
          self.window['cb_edited'].update(False)
      except:
        self.debug.error_message("method: handle_button_common2. " + str(sys.exc_info()[0]) + str(sys.exc_info()[1] ))
      self.js8net.toggleEditState()
      
    return(text)
    
  def handle_msgselectside(self, values):
    selected = values['option_selectside']
    myrpt = self.window['multi_side'].update(self.message_side_list_client[values['option_selectside']])
    return()        

  def checkDisableAllButtons(self):
    self.js8net.debug.info_message("method: checkDisableAllButtons.")
    if( self.window['input_netgroup'].get().strip() == "" or self.window['input_netfre'].get().strip() == ""):
      self.js8net.debug.info_message("method: checkDisableAllButtons. True")
      """ disable all of the ncs buttons """
      self.disableEnableAllButtons(True, ['button_qst', 'button_open', 'button_ckin', 'button_gotu', 'button_roster', 'button_first', 'button_next', 'button_prompt', 'button_skip', 'button_end', 'button_cmnt', 'button_close', 'button_ncs_cust1', 'button_ncs_cust2'])
      """ disable all of the client buttons """
      self.disableEnableAllButtons(True, ['btncli_ckmein', 'btncli_alert', 'btncli_qrt', 'btncli_post', 'btncli_tks', 'btncli_cust1', 'btncli_cust2'])
      """ disable all of the GO buttons """
      self.disableEnableAllButtons(True, ['send_announce', 'send_report', 'send_comment', 'send_really'])
      
      checked = self.window['cb_simulate'].get()
      if(not checked):
        self.disableEnableAllButtons(True, ['send_side'])
      
    elif( self.window['input_netgroup'].get().strip() != "" and self.window['input_netfre'].get().strip() != ""):
      self.js8net.debug.info_message("method: checkDisableAllButtons. False")
      """ enable all of the ncs buttons """
      self.disableEnableAllButtons(False, ['button_qst', 'button_open', 'button_ckin', 'button_gotu', 'button_roster', 'button_first', 'button_next', 'button_prompt', 'button_skip', 'button_end', 'button_cmnt', 'button_close', 'button_ncs_cust1', 'button_ncs_cust2'])
      """ enable all of the client buttons """
      self.disableEnableAllButtons(False, ['btncli_ckmein', 'btncli_alert', 'btncli_qrt', 'btncli_post', 'btncli_tks', 'btncli_cust1', 'btncli_cust2'])
      """ enable all of the GO buttons """
      self.disableEnableAllButtons(False, ['send_announce', 'send_report', 'send_comment', 'send_really', 'send_side'])

    if( self.window['input_netgroup'].get().strip() == ""):
      self.window['text_netgrp'].update(text_color='red')
    else:  
      self.window['text_netgrp'].update(text_color='black')

    if( self.window['input_netfre'].get().strip() == ""):
      self.window['text_netfre'].update(text_color='red')
    else:  
      self.window['text_netfre'].update(text_color='black')

  def disableEnableAllButtons(self, disable_state, buttons):
    for x in range(len(buttons)):
      self.js8net.debug.info_message("disabling button " + buttons[x])
      self.window[buttons[x]].update(disabled=disable_state)
    return

  def startFlashButtons(self, flashButtons):
    self.js8net.flash_win = flashButtons
    return

  def startFlashAllButtons(self):
    self.startFlashButtons(['button_qst', 'button_open', 'button_ckin', 'button_gotu', 'button_roster', 'button_first', 'button_next', 'button_prompt', 'button_skip', 'button_end', 'button_cmnt', 'button_close', 'button_ncs_cust1', 'button_ncs_cust2'])

  def flashButtons(self):
    if(self.js8net.flash_state ==0):
      for x in range(len(self.js8net.flash_win)):
        flashwin = self.window[self.js8net.flash_win[x]]
        self.js8net.flash_state=1
        flashwin.Update(button_color=(self.btn_flashclr1, self.btn_flashclr2))
    else:
      for x in range(len(self.js8net.flash_win)):
        flashwin = self.window[self.js8net.flash_win[x]]
        self.js8net.flash_state=0
        flashwin.Update(button_color=(self.btn_flashclr2, self.btn_flashclr1))
    return
    
  def stopFlashingButtons(self, buttons_list):
    for x in range(len(buttons_list)):
      flashwin = self.window[buttons_list[x]]
      flashwin.Update(button_color=(self.btn_clr1, self.btn_clr2))

    self.js8net.flash_win = None
    return
    
  def stopFlashingAllButtons(self):
    self.stopFlashingButtons(['button_qst', 'button_open', 'button_ckin', 'button_gotu', 'button_roster', 'button_first', 'button_next', 'button_prompt', 'button_skip', 'button_end', 'button_cmnt', 'button_close', 'button_ncs_cust1', 'button_ncs_cust2', 'send_announce', 'send_report', 'send_comment', 'send_really'])
   
  """
  create the main GUI window
  """
  def createClientWindow(self, js, mode,simulation_mode, edit_mode, combo_list_1, combo_list_2, client_read_details, net_group, net_frequency, counter_value, show_counter, visuals, offsets_list, main_offset):
    
    btn_clr1 = self.btn_clr1
    btn_clr2 = self.btn_clr2

    side_list = []

    for x in range(len(self.message_side_list_client)):
      key, val = self.message_side_list_client.items()[x]
      side_list += [key]
      
    """ get today in english """  
    today_string = js.get("params").get("Edition")
    """ retrieve from the command line options """
    today_string = ""
    if(today_string == ""):
      today_string = calendar.day_name[datetime.today().weekday()]

    auto_handoff_default = js.get("params").get("AutoHandoff")
    roster = []
    if(mode == cn.NETCONTROL):
      roster = js.get("roster")
      auto_handoff_default = False
    elif(mode == cn.PARTICIPANT):
      roster = []
      auto_handoff_default = True
      
    first_call = ""
    first_name = ""
    if(roster != None and len(roster)>0):
      first_call = roster[0].split(" ")[0]
      first_name = roster[0].split(" ")[1]
      
    client_fields = False
    ncs_fields = False
    show_edit_buttons = False
    if(mode == cn.NETCONTROL):
      ncs_fields = True
    else:
      client_fields = True
   
    disable_buttons = False
    netgrp_value = js.get("params").get("NetGroup") if (ncs_fields or client_read_details) else net_group
    netfre_value = js.get("params").get("NetFre") if (ncs_fields or client_read_details) else net_frequency
    if(netgrp_value == "" or netfre_value == ""):
      disable_buttons = True

    disable_sendside = disable_buttons
    if(simulation_mode):
      disable_sendside = False

    side_offset = js.get("params").get("SideOffset") 
    side_offset = 537

    netgrp_text_color='black'
    netfre_text_color='black'
    if(netgrp_value == ""):
      netgrp_text_color='red'

    if(netfre_value == ""):
      netfre_text_color='red'
      
    background = 'LightGray'
    main_color = 'SeaGreen1'
    side_color = 'LightBlue1'
   
    visuals_split = visuals.split(',')
    
    btn_flashclr1 = 'red'
    btn_flashclr2 = 'green'
    
    for x in range(len(visuals_split) ):
      vis_field=visuals_split[x].split(':')[0]
      vis_value=visuals_split[x].split(':')[1]
      if(vis_field == 'background'):
        background = vis_value
      elif(vis_field == 'main'):
        main_color = vis_value
      elif(vis_field == 'side'):
        side_color = vis_value
      elif(vis_field == 'flash1'):
        btn_flashclr1 = vis_value
      elif(vis_field == 'flash2'):
        btn_flashclr2 = vis_value

    self.btn_flashclr1 = btn_flashclr1
    self.btn_flashclr2 = btn_flashclr2

   
    layout = [
        [sg.Text('Net:', size=(3, 1), font=("Helvetica", 20), background_color=background), 
             sg.InputText(js.get("params").get("NetName") if (ncs_fields or client_read_details) else "" , size=(15, 1), font=("Helvetica", 15), key='input_netname'), 
             sg.Text('Edition:', size=(6, 1), font=("Helvetica", 20), background_color=background), 
             sg.InputText(today_string if (ncs_fields or client_read_details) else "" , size=(11, 1), key='option_profile'),
             sg.Text('Timer:', size=(5, 1), font=("Helvetica", 20), background_color=background), 
             sg.Text('----', size=(9, 1), font=("Helvetica", 20), key='clock', background_color=background)],
        [sg.Text('Net Group:', size=(9, 1), font=("Helvetica", 15), key='text_netgrp', text_color=netgrp_text_color, background_color=background), 
             sg.InputText(netgrp_value , key='input_netgroup', size=(16, 1), enable_events=True), 
             sg.Text('Type:', size=(5, 1), font=("Helvetica", 15), background_color=background), 
             sg.Combo(('Directed', 'Round Table', '-'), default_value=js.get("params").get("DirectRnd") if (ncs_fields or client_read_details) else "-" , key='option_menu', size=(15, 1)), 
             sg.Text('Start:', size=(4, 1), font=("Helvetica", 15), key='stn_call', background_color=background),
             sg.InputText(js.get("params").get("StartTime") if (ncs_fields or client_read_details) else "00:00" , size=(5, 1), font=("Helvetica", 15), key='input_starttime'),
             sg.Text('Zulu', size=(4, 1), font=("Helvetica", 15), key='zulu', background_color=background),
             sg.CBox('Save', key='cb_savedetails', default=ncs_fields or client_read_details, disabled = ncs_fields, background_color=background)],

        [sg.Text('Frequency:', size=(9, 1), font=("Helvetica", 15), key='text_netfre', text_color=netfre_text_color, background_color=background), 
             sg.InputText(netfre_value , key='input_netfre', size=(16, 1), enable_events=True), 
             sg.Text('NCS:', size=(5, 1), font=("Helvetica", 15), background_color=background), 
             sg.InputText(js.get("params").get("NCS") if (ncs_fields or client_read_details) else "" , key='input_ncs', size=(9, 1), font=("Helvetica", 15)),
             sg.Text('Round:', size=(6, 1), font=("Helvetica", 15), background_color=background),
             sg.Combo(('ONE', 'TWO', 'THREE'), key='option_currentround', size=(8, 1)), 
             sg.Text('of:', size=(2, 1), font=("Helvetica", 15), background_color=background),
             sg.Combo(('-', 'ONE', 'TWO', 'THREE'), key='input_rounds', size=(8, 1), default_value=js.get("params").get("Rounds") if (ncs_fields or client_read_details) else "-")], 

        [sg.Text('_' * 100, background_color=background, visible=ncs_fields)],

        [sg.InputText(first_call, key='roster_choose', size=(17, 1), enable_events=True, visible=ncs_fields),
         sg.InputText(first_name, key='rstr_name', size=(16, 1), enable_events=True, visible=ncs_fields),
         sg.Combo((cn.HEARD, cn.STANDBY, cn.NEXT, cn.TALKING, cn.SKIP, cn.DONE, cn.QRT, cn.SWL, cn.IGNORE, cn.NONE, cn.CHECKIN, cn.NCS), key='rstr_status', size=(13, 1), enable_events=True, visible=ncs_fields),
         sg.Button('Update', size=(5, 1), key='add_stn', visible=ncs_fields),
         sg.Button('Delete', size=(5, 1), key='remove_stn', visible=ncs_fields),
         sg.Button('Clear', size=(5, 1), key='clear_all', visible=ncs_fields),
         sg.CBox('Auto Check-In', key='cb_autocheckin', enable_events=True, visible=ncs_fields, default=js.get("params").get("AutoCheckin"), background_color=background )], 

        [                   sg.Table(values=roster, headings=['Callsign', 'Name', 'Status', 'Offset', 'SNR', 'Bad Frm', 'Time Dlt'],
                            max_col_width=65,
                            col_widths=[12, 12, 9, 8, 8, 7, 7],
                            auto_size_columns=False,
                            justification='left',
                            enable_events=True,
                            select_mode=sg.TABLE_SELECT_MODE_EXTENDED,
                            num_rows=5, key='roster')],

        [sg.CBox('Prev', key='cb_prevstn', visible=ncs_fields, background_color=background, enable_events=True),
         sg.Text('Prev', size=(8, 1), visible=client_fields, background_color=background), 
         sg.InputText(js.get("params").get("PrevStn"), key='prev_stn', size=(12, 1), enable_events=True, disabled=True), 
         sg.CBox('Next', key='cb_nextstn', visible=ncs_fields, background_color=background, enable_events=True),
         sg.Text('Next', size=(8, 1), visible=client_fields, background_color=background), 
         sg.InputText(js.get("params").get("NextStn"), key='next_stn', size=(12, 1), enable_events=True, disabled=True), 
         sg.Button('Reset', key='reset_roster', visible=ncs_fields),
         sg.Text('', size=(10, 1), visible=ncs_fields, background_color=background ),
         sg.Button('Clear', size=(5, 1), key='btncli_clear', visible=client_fields),
         sg.Combo(('Post to JS8Call only', 'Post to JS8Call + send'), key='option_postsend', enable_events=True, default_value=js.get("params").get("SendOption"))],

        [sg.MLine(default_text='', size=(98, 5), key='multiRcv', autoscroll=True, background_color=main_color)],
        [sg.MLine(default_text='', size=(98, 3), key='multiSide', autoscroll=True, background_color=side_color)],

        [sg.Slider(range=(1, counter_value), orientation='h', size=(64, 15), key='slider_timeout', default_value=counter_value, visible=show_counter, background_color=background)],
         
        [sg.CBox('Offset:', key='cb_presetoffset', default = False , background_color=background, enable_events=True),
         sg.InputText(main_offset, key='main_offset', size=(10, 1), background_color=main_color, disabled=True),
         sg.Text('Side Offset:', size=(12, 1), visible=client_fields, background_color=background),
         sg.InputText(side_offset, key='sidebar_offset', size=(10, 1), background_color=side_color, visible=client_fields, disabled = True),
         sg.CBox('Auto hand off', key='cb_autohandoff', visible=client_fields, default=auto_handoff_default, background_color=background),
         sg.CBox('Flash buttons', key='cb_flashbtn', enable_events=True, default = js.get("params").get("FlashBtn") , background_color=background),
         sg.CBox('Auto clear', key='cb_clronsnd', default = True, background_color=background )],

        [sg.Text('Announce', size=(8, 1), background_color=background), 
         sg.MLine(default_text=js.get("params").get("Announce"), size=(77, 3), key='multi_announce', enable_events=True, background_color=main_color),
         sg.Button('Go', key='send_announce', disabled = disable_buttons)],
        [sg.Text('My report', size=(8, 1), background_color=background),
         sg.MLine(default_text=js.get("params").get("Report"), size=(77, 5), key='multi_myreport', enable_events=True, background_color=main_color), 
         sg.Button('Go', key='send_report', disabled = disable_buttons)],
        [sg.Text('Other', size=(8, 1), background_color=background),
         sg.MLine(default_text=js.get("params").get("Other"), size=(77, 2), key='multi_other', enable_events=True, background_color=main_color), 
         sg.Button('Go', key='send_comment', disabled = disable_buttons)],

        [sg.Text('', size=(8, 1), visible=ncs_fields, background_color=background), 
         sg.Button('QST',   key='button_qst', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Got u', key='button_gotu', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('CKin?',  key='button_ckin', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Open',  key='button_open', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Roster',key='button_roster', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('First', key='button_first', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Next',  key='button_next', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons )], 
        [sg.Text('', size=(8, 1), visible=ncs_fields, background_color=background), 
         sg.Button('Nudge',key='button_prompt', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Skip',  key='button_skip', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('End Rnd',   key='button_end', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Awards!', key='button_ncs_cust1', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Comment',  key='button_cmnt', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Close', key='button_close', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons ), 
         sg.Button('Extras', key='button_ncs_cust2', size=(6, 1), button_color=(btn_clr1, btn_clr2), visible=ncs_fields, disabled = disable_buttons )], 

        [sg.CBox('UR Welcome', key='cb_welcome', enable_events=True, visible=ncs_fields, background_color=background),
         sg.Text('', size=(8, 1), visible=client_fields, background_color=background), 
         sg.CBox('Tks',   key='cb_rep', background_color=background),
         sg.Combo(combo_list_1, key='option_tks', enable_events=True, visible=ncs_fields),
         sg.CBox('SNR',      key='cb_snr', background_color=background),
         sg.Button('Edit', key='edit_firstcombo', visible=show_edit_buttons),
         sg.CBox('Other', key='cb_other', background_color=background),
         sg.CBox('More?', key='cb_further', enable_events=True, visible=ncs_fields, background_color=background),
         sg.CBox('', key='cb_goodeve', enable_events=True, background_color=background),
         sg.Combo(combo_list_2, key='option_goodeve', enable_events=True),
         sg.Button('Edit', key='edit_secondcombo', visible=show_edit_buttons)],

        [sg.Text('Preview', size=(8, 1), background_color=background ),
         sg.MLine(' ', key='multi_select', size=(77, 4), enable_events=True, background_color=main_color), 
         sg.Button('Go', key='send_really', disabled = disable_buttons)],

        [sg.Text('', size=(8, 1), visible=client_fields, background_color=background ),
         sg.Button('CKin', key='btncli_ckmein', size=(5, 1), button_color=(btn_clr1, btn_clr2), visible=client_fields, disabled = disable_buttons ), 
         sg.Button('ALERT', key='btncli_alert', size=(5, 1), button_color=(btn_clr1, btn_clr2), visible=client_fields, disabled = disable_buttons ), 
         sg.Button('QRT', key='btncli_qrt', size=(5, 1), button_color=(btn_clr1, btn_clr2), visible=client_fields, disabled = disable_buttons ), 
         sg.Button('Post', key='btncli_post', size=(5, 1), button_color=(btn_clr1, btn_clr2), visible=client_fields, disabled = disable_buttons ), 
         sg.Button('Tks', key='btncli_tks', size=(5, 1), button_color=(btn_clr1, btn_clr2), visible=client_fields, disabled = disable_buttons ), 
         sg.Button('Custom1', key='btncli_cust1', size=(5, 1), button_color=(btn_clr1, btn_clr2), visible=client_fields, disabled = disable_buttons ), 
         sg.Button('Custom2', key='btncli_cust2', size=(5, 1), button_color=(btn_clr1, btn_clr2), visible=client_fields, disabled = disable_buttons )], 
        [sg.Text('', size=(8, 1), visible=edit_mode, background_color=background ),
         sg.CBox('Edit Macros', key='cb_editbtn', visible=edit_mode , enable_events=True, background_color=background),
         sg.CBox('Modified', key='cb_edited', visible=edit_mode, enable_events=True, background_color=background)],
        [sg.Text('Preview', size=(8, 1), visible=(client_fields or simulation_mode), background_color=background ),
         sg.MLine(' ', key='multi_side', size=(77, 3), enable_events=True, background_color=side_color, visible=(client_fields or simulation_mode) ), 
         sg.Button('Go', key='send_side', visible=(client_fields or simulation_mode), disabled = disable_sendside )],
         
        [sg.Button('Exit'), 
         sg.Combo(side_list, key='option_selectside', size=(21, 1), enable_events=True, visible=simulation_mode ),
         sg.CBox('Simulate', key='cb_simulate', visible=simulation_mode, default=False, background_color=background)],
    ]
    self.window = sg.Window('JS8Net de WH6GGO (v1.0 Beta)', layout, default_element_size=(40, 1), grab_anywhere=False, disable_close=True, background_color=background)
    return (self.window)

