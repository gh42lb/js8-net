
JS8_net v1.0 Beta release de WH6GGO

designed and developed by Lawrence Byng, WH6GGO

This software is released under the MIT license


JS8 net is designed to provide a set of ehanced features for running a JS8 net.
The design concept is both experimental and unique. 

This application is for use in conjunction with JS8Call

to utilize these features, at the very least net control should use js8 net appliation.
it is possible for participant stations to participate without using js8 net application
however those stations will not have any of the js8 net application enhanced functionality 
available to them

all stations on the net that use js8 net application will have the benfeit of the enhanced functionality.
This functionality is similar to what might be provided by an internet based application, however this 
is achieved by using JS8 HF text mode communication only and without the use of any internet connections. 


Quick start guide
=================

STEP 1 JS8call configuration:
============================
make sure JS8Call is configured as follows

1) Mode menu/Enable Auto Reply - checked
This setting is required for the text transfers between js8call and js8net to function correctly

2) File/Settings/Reporting tab
under the API section:
TCP Server Hostname: 127.0.0.1   Enable TCP Server API - checked
TCP Server Port:     2442        Accept TCP Requests   - checked
TCP Max Connections: 1

3) When you are ready to transmit, adjust the mode speed in JS8 as required (normal, fast, turbo) and make sure
 the TX button at the top right is enabled


STEP 2 installing python and the modules. 
==========================================
make sure python 2.7 is installed along with the following mudules...

PySimpleGUI27, sys, threading, json, random, getopt, datetime, socket, time, select, calendar


STEP 3 downloading js8 net. 
===========================
download the js8net python files into your chosen directory

set js8_net_client.py as executeable

sudo chmod +x js8_net_client.py


step 4 run the application
==========================

There are two main modes of operation, one as net control...

python ./js8_net_client.py --interface=netcontrol --net_file=js8net_save_data.txt

--net_file specifies the name and location of the file to save data from js8 net


and one as a client or participant station...

python ./js8_net_client.py --interface=participant --net_file=js8net_save_data.txt --frequency='fromjs8call' --group='@MYGROUP'

--frequency and --group are required to participate. these can be acquired in several ways
--frequency='fromjs8call' this will use the frequency setting of jas8 call as the setting for the js8 net application
--group='@MYGROUP' this provides a manual override for the group field of the application

if everything is installed correctly, js8 net will connect to js8call and display the main window


if you wish to use a different ip or port these can be specified on the command line as follows...

python ./js8_net_client.py --interface=netcontrol --js8call='127.0.0.1:2442'


step 5 customization
====================

1) offsets plan
an offsets plan can be assigned to all stations as follows...
python ./js8_net_client.py --interface=netcontrol --offsets='1337,400,500,600,700,800,900'
please note only participant stations using the js8 net application will be able to use this feature


2) combo box messages
the two drop down combos can be customized with different messages as follows...
python ./js8_net_client.py --interface=netcontrol --combo_tks='comments,heads up,info' --combo_aloha='have a great morning,have a nice day,enjoy your day'


3) button messages
js8 net has a built in macro language and allows customization of the messages behind each of the main buttons
to activate the edit feature run js8 net in edit mode
python ./js8_net_client.py --interface=netcontrol --edit


4) screen colors
colors can be changed as follows...
python ./js8_net_client.py --interface=netcontrol --visual='background:yellow,main:pink,side:blue,flash1:green,flash2:cyan'

the default colors are set equivalent to...
python ./js8_net_client.py --interface=netcontrol --visual='background:LightGray,main:SeaGreen1,side:LightBlue1,flash1:red,flash2:blue'




enjoy :)

73 de WH6GGO
