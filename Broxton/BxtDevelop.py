# -*- coding: utf-8 -*-
"""
Created on Tue Jul  3 11:28:28 2018

@author: Byng.Zeng
"""

import commands
import subprocess
import sys
import re
import os

class AndroidBase(object):
    def help(self, cmd=''):
        #print('Class AndroidBase help.')
        print('make:[xxx,[xxx]]    : make xxx image')
        print('flash:[xxx,[xxx]]   : flash xxx image')
        
    def waitADB(self):
        cmd = r'adb wait-for-device'
        subprocess.call(cmd, shell=True)
        
    def rebootToBootloader(self):
        cmd = r'adb reboot bootloader'
        subprocess.call(cmd, shell=True)       

    def flashImage(self, pt, image):
        cmd = r'fastboot flash %s %s' % (pt, image)
        print(cmd)
        subprocess.call(cmd, shell=True)

    def unlockDevice(self):
        cmd = r'fastboot flashing unlock'
        print(cmd)
        subprocess.call(cmd, shell=True)        

    def lockDevice(self):
        cmd = r'fastboot flashing lock'
        print(cmd)
        subprocess.call(cmd, shell=True)

    def makeImages(self, images):
        bd = BxtDevelop()
        for image in images.values():
            bd.buildImage(image)


        
class AvbImage(object):
    def __init__(self,
            name= 'pdt',
            pdt='gordon_peak',
            opt='userdebug',
            usr='yingbin'):
        #print('AvbImage init now.')
        self._name = name
        self._pdt = pdt
        self._opt = opt
        self._user = usr
        self._out = r'out/target/product/%s' % self._pdt
        self._flashfiles = r'%s/%s-flashfiles-eng.%s' % (self._out, self._pdt, self._user)

    def help(self, cmd=''):
        #print('Class AvbImage help.')
        pass

    def avbMakeImage(self, image):
        # copy image to flashfiles folder
        cmd = r'cp %s/%s.img %s/%s.img' % (self._out, image, self._flashfiles, image)
        print(cmd)
        subprocess.call(cmd, shell=True)
        
        # uses avbtool to build image
        cmd = r'''
            out/host/linux-x86/bin/avbtool make_vbmeta_image --output %s/vbmeta.img \
            --include_descriptors_from_image %s/boot.img \
            --include_descriptors_from_image %s/system.img \
            --include_descriptors_from_image %s/vendor.img \
            --include_descriptors_from_image %s/tos.img \
            --key $TEST_KEY_PATH/testkey_rsa4096.pem --algorithm SHA256_RSA4096
            ''' % (self._flashfiles,
                   self._flashfiles,
                   self._flashfiles,
                   self._flashfiles,
                   self._flashfiles)
        #print(cmd)
        subprocess.call(cmd, shell=True)        
    
    def updateImages(self, images):
        # avb make images.
        for image in images.values():
            print('update image %s' % image)
            self.avbMakeImage(image)
        # setup flash env
        self.waitADB()
        self.rebootToBootloader()
        self.unlockDevice()
        # flash image now
        ab = AndroidBase()
        for image in images.values():
            fimage = r'%s/%s.img' % (self._flashfiles, image)
            ab.flashImage(image, fimage)
        # lock device.
        self.lockDevice()


class BIOS(object):
    def __init__(self,
            name= 'pdt',
            pdt='gordon_peak',
            opt='userdebug',
            usr='yingbin'):
        #print('BIOS init now.')
        self._name = name
        self._pdt = pdt
        self._opt = opt
        self._user = usr
        self._out = r'out/target/product/%s' % self._pdt
        self._flashfiles = r'%s/%s-flashfiles-eng.%s' % (self._out, self._pdt, self._user) 
        self._fw = '%s/%s' % (self._flashfiles, 'ifwi_gr_mrb_b1.bin')  
        self._ioc = '%s/%s' % (self._flashfiles, 'ioc_firmware_gp_mrb_fab_e_slcan.ias_ioc')

    def help(self, cmd=''):
        #print('Class BIOS help.')
        print('fw:xxx     : update firmware with xxx')
        print('ioc:xxx    : update ioc with xxx')

    def flashFW(self, fw):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ias-spi-programmer --write %s' % fw
        subprocess.call(cmd, shell=True)

    def flashIOC(self, ioc):
        cmd = r'sudo /opt/intel/platformflashtool/bin/ioc_flash_server_app -s /dev/ttyUSB2 -grfabc -t %s' % ioc
        subprocess.call(cmd, shell=True)
        
    def flash(self, cmds):
        for val in cmds.values():
            if val == 'fw':
                fw = r'%s/%s' % (self._flashfiles, self._fw)
                self.flashFW(fw)
            elif val == 'ioc':
                ioc = r'%s/%s' % (self._flashfiles, self._ioc)
                self.flashIOC(ioc)

class Code(object):
    def __init__(self, url=''):
        #print('create Code')
        self._url = url

    def help(self, cmd=''):
        #print('Class Code help.')
        print('url:ssh_xxx    : init source code')
        print('sync:xxx    : sync source code')
        if cmd == 'cfg':
            print('url:')


    def initURL(self):
        cmd = r'repo init -u %s' % self._url
        print(cmd)
        subprocess.call(cmd, shell=True)

    def syncURL(self):
        linux = LinuxBase()
        cpus = linux.getCPUs
        if cpus > 5:
            cpus = 5
        
        cmd = r'repo sync -j{num}'.format(num=cpus)
        print(cmd)
        subprocess.call(cmd, shell=True)
        
    def urlHandler(self, cmds):
        t = type(cmds)
        if t == dict:
            for cmd in cmds.values():
                if cmd == 'init':
                    self.initURL()
                elif cmd == 'sync':
                    self.syncURL()
        elif t == list:
            for i in range(cmds):
                if cmds[i] == 'init':
                    self.initURL()
                elif cmds[i] == 'sync':
                    self.syncURL()
        elif t == str:
            if cmds == 'init':
                self.initURL()
            elif cmds == 'sync':
                self.syncURL()
            
class LinuxBase(object):
    def help(self, cmd=''):
        #print('Class linuxBase help.')
        print('rm:[xxx,[xxx]]    : remove xxx file')
        #pass
    
    def getCPUs(self):
        cmd = r'cat /proc/cpuinfo | grep "processor"| wc -l'
        return commands.getoutput(cmd)
   
    def delete(self, f):
        cmd = r'rm -rf %s' % f
        subprocess.call(cmd, shell=True)


class Parser(object):
    def help(self, cmd=''):
        #print('Class Parser help.')
        pass
        
    def parserCMDArgs(self, cmds):
        reCmd = re.compile(r'^([a-z]{1,8}):([a-z,_]{0,32})$')
        output = {}
        for cmd in cmds:
            try:
                k, v = reCmd.match(cmd).groups()
                #print k,v
                output[k]= self.parserArgs(k, v)
            except AttributeError as e:
                print('Invalid input: %s' % e)
                
        return output
        
    def parserArgs(self, cmd, argv):
        reArgv = re.compile(r'^([a-z]{1,8}),([a-z,_]{0,32})$')
        index = 0
        output = {}
        temp = argv
        while temp:
            if re.search(',', temp) == None:
                output[index] = temp
                temp = 0
            else:
                k, v = reArgv.match(temp).groups()
                temp = v
                output[index] = k
            index += 1

        return output 

class BxtDevelop(AndroidBase,
                 AvbImage,
                 BIOS,
                 Code,
                 LinuxBase):
    def __init__(self):
        #print('BxtDevelop init now.')
        super(AndroidBase, self).__init__()
        super(AvbImage, self).__init__()
        super(BIOS, self).__init__()
        super(Code, self).__init__()
        super(LinuxBase, self).__init__()

    def help(self, cmd=''):
        #print('Class BxtDevelop help.')
        super(AndroidBase, self).help(cmd)
        super(BIOS,self).help(cmd)
        super(Code,self).help(cmd)
        super(AvbImage,self).help(cmd)
        #super(LinuxBase,self).help(cmd)

    def buildImage(self, image):
        # create buildImage.sh to make image.
        builds = r'''#!/bin/bash
device/intel/mixins/mixin-update
. build/envsetup.sh
lunch {pdt}-{opt}
make {image} -j{cpu}'''.format(pdt=self._pdt, opt=self._opt, image=image, cpu=self.getCPUs())
        buildsh = r'.buildImage.sh'
        with open(buildsh, 'w') as f:
            f.write(builds)
        # run buildImage.sh
        os.system(r'chmod a+x {sh}'.format(sh=buildsh))
        cmd = r'./{sh}'.format(sh=buildsh)
        print(cmd)
        subprocess.call(cmd, shell=True)

class CmdHandler(Parser, BxtDevelop):
    # list of support cmd, value: function.
    supportCmds = {
        'help'  : None,
        'url'   : None,
        'flash' : None,
        'make'  : None,
        'rm'    : None,
        'fw'    : None,
        'ioc'   : None,
    }

    def __init__(self):
        super(Parser, self).__init__()
        super(BxtDevelop, self).__init__()

    def getCMD(self):
        #print('parse all of cmds.')
        parser = Parser()
        return parser.parserCMDArgs(sys.argv[1:])   

    def checkCMD(self, cmds):
        for key in cmds.keys():
            if self.supportCmds.has_key(key) == False:
                return False
        return True

    def configCMD(self, cmds):
        for key in cmds.iterkeys():
            if key == 'help':
                self.supportCmds['help'] = self.help
            elif key == 'make':
                #android = AndroidBase()
                self.supportCmds['make'] = self.makeImages
            elif key == 'flash':
                self.supportCmds['flash'] = self.updateImages
            elif key == 'fw':
                self.supportCmds['fw'] = self.flashFW
            elif key == 'ioc':
                self.supportCmds['ioc'] = self.flashIOC
            elif key == 'url':
                self.supportCmds['url'] = self.urlHandler
            elif key == 'rm':
                self.supportCmds['rm'] = self.delete
                
    def runCMD(self, cmds):
        for key in cmds.iterkeys():
            if self.supportCmds[key] != None:
                #print cmds[key]
                f = self.supportCmds[key]
                f(cmds[key])

    def main(self, cmds):
        cmdResult = self.getCMD()
        if self.checkCMD(cmdResult) == False:
            print('Found invalid input, exit!')
            exit()

        self.configCMD(cmdResult)
        self.runCMD(cmdResult)


if __name__ == '__main__':
    hdr = CmdHandler()
    hdr.main(sys.argv[1:])