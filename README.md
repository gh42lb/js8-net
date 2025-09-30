## Overview

JS8_Net v1.1 Beta release de WH6GGO

Designed and developed by Lawrence Byng

JS8 net is designed to provide a set of ehanced features for running a JS8 net.
The design concept is both experimental and unique. 

This application is for use in conjunction with JS8Call

To utilize these features, at the very least net control should use js8 net application.
It is possible for participant stations to participate without using js8 net application
however, those stations will not have any of the js8 net application enhanced functionality 
available to them.

All stations on the net that use js8 net application will have the enhanced functionality.
This functionality is similar to what might be provided by an internet based application, however this 
is achieved by using JS8 HF text mode communication only and without the use of any internet connections. 

#### Features
* Roster to display participating station call signs, operator name, net status and offset
* Point and click style of net operation
* Can be run as net control view or as participant station view
* Convenient notepad area to pre-type various communications prior to the net
* Auto save feature 
* Built in macro language allowing construction of wide variety of point and click messages with macros that are hooked into the various tracking aspects of JS8Net
* customization feature allowing customization of all point and click message
* state machine and text mode parser that allows participant stations to view up to date net information as if connected via internet
* no internet connection required. Uses only text mode communication allowing stations
* Use of application is optional. Any station using at a minimum JS8 mode only are still able to participate in the net.
* tracking of SNR, bad frames and time delta for each station. 
* Ability to distribute an offsets list to other stations running JS8Net


## Quick start guide


### JS8call configuration:

make sure JS8Call is configured as follows

1) Mode menu/Enable Auto Reply - checked
This setting is required for the text transfers between js8call and js8net to function correctly

2) File/Settings/Reporting tab
    • under the API section:
    • TCP Server Hostname: 127.0.0.1   Enable TCP Server API - checked
    • TCP Server Port:     2442        Accept TCP Requests   - checked
    • TCP Max Connections: 1 or 2

3) When you are ready to transmit, adjust the mode speed in JS8 as required (normal, fast, turbo) and make sure
 the TX button at the top right is enabled


### Downloading pre-built binaries

note: The software is incorporated in the HRRM suite. Tested on raspberry pi, ubuntu/linux mint and windows platforms
   
    
### Download and run from .py files

    • download the js8net python files into your chosen directory

    • make sure python is installed along with the following mudules...

FreeSimpleGui, sys, threading, json, random, getopt, datetime, socket, time, select, calendar


i.e.
python 3: pip3 install freesimplegui

    • now run the application: python ./js8_net_client.py --interface=netcontrol

    • or: python ./js8_net_client.py --interface=participant --frequency='fromjs8call' --group='@MYGROUP'



if everything is installed correctly, js8 net will connect to js8call and display the main window

if you wish to use a different ip or port these can be specified on the command line as follows...

    • python ./js8_net_client.py --interface=netcontrol --js8call='127.0.0.1:2442'



for more information please refer to user_guide.pdf



enjoy :)

73 de WH6GGO



## Copyright/License

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


