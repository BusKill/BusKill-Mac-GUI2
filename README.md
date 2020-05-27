# BusKill-Mac-GUI
A GUI implementation of the BusKill Project 

# buskill-mac
BusKill Laptop Kill Cord for Macbooks

# Press

As seen on [PCMag](https://www.forbes.com/sites/daveywinder/2020/01/03/this-20-usb-cable-is-a-dead-mans-switch-for-your-linux-laptop/), [Forbes](https://www.pcmag.com/news/372806/programmers-usb-cable-can-kill-laptop-if-machine-is-yanked), [ZDNet](https://www.zdnet.com/article/new-usb-cable-kills-your-linux-laptop-if-stolen-in-a-public-place/), & [Tom's Hardware](https://www.tomshardware.com/news/the-buskill-usb-cable-secures-your-laptop-against-thieves).

# For more Information

See https://tech.michaelaltfield.net/2020/01/02/buskill-laptop-kill-cord-dead-man-switch/

# Build Instructions 

Requirements:
    -> [py2app] (https://pypi.org/project/py2app/) This can also be installed via pip
    
    -> [MacPorts] (https://www.macports.org/ports.php?by=variant&substr=qt5)
    -> Installing Macports Python as well as the dependencies 
        -> PyQt5 is mainly

Once you have checked all these boxes you are ready to generate the .app


run the following commands
    
'''console
python3 setup.py py2app
'''
    
    This will then generate a dist/ and build/ folder 

    -> you now need to add the data files to the .app

    '''console
      mkdir dist/BusKill\ -\ Mac.app/Contents/Resources/Triggers
      mkdir dist/BusKill\ -\ Mac.app/Contents/Resources/Resources
      mkdir dist/BusKill\ -\ Mac.app/Contents/Resources/Config
      mkdir dist/BusKill\ -\ Mac.app/Contents/Resources/Logging
      cp -r Resources/ dist/BusKill\ -\ Mac.app/Contents/Resources/Resources/
      cp -r Triggers/ dist/BusKill\ -\ Mac.app/Contents/Resources/Triggers/
    '''

    -> you will now have a fully working .app package

    _**please note**_
    once you have generated the .app (or have downloaded from developer) you can navigate to 
    
    BusKill\ -\ Mac.app/Contents/Resources

    all the source code remains here in **plain text** code here can be changed still. this is not a binary. it is a package 


# Known Issues

-> .py Triggers are no longer supported 

-> permissions require resetting on the triggers 


chmod a+x BusKill\ -\ Mac/Contents/Resources/Triggers/lock/Trigger.sh

chmod a+x Buskill\ -\ Mac/Contents/Resources/Triggers/shutdown/Trigger.sh


Configuration and Logging not thourghly tested yet!!!


This is an alpha release only
