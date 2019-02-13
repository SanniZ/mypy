#!/usr/bin/env python3

# ===========================================
#    Config ubuntu rxdp for remote desktop
# ===========================================
# --------------------------
# author: Byng Zeng
# Date  : 2018-11-30
# --------------------------

import os
import re
import subprocess
import shutil
import operator as op

class ConfigXubuntuDesktop(object):

    # install xrdp
    def install_xrdp(self):
         cmd = r'sudo apt-get install xrdp -y'
         subprocess.call(cmd, shell=True)

    # install xubuntu-desktop
    def install_xubuntu_desktop(self):
         cmd = r'sudo apt-get install xubuntu-desktop -y'
         subprocess.call(cmd, shell=True)

    # config .xsession
    def config_xsession(self):
         with open(os.path.abspath('%s/.xsession2' % os.getenv('HOME')), 'a') as f:
             f.write('xfce4-session')

    # config xfce startwm
    def config_startwp_sh(self):
         startwm = os.path.abspath('startwm.sh')
         shutil.copyfile('/etc/xrdp/startwm.sh', startwm)
         # read startwm for update.
         with open(startwm, 'r') as f:
             lines = f.readlines()
         # insert xfce4-session
         for i in range(len(lines)):
             if re.match('. /etc/X11/Xsessioin', lines[i]) != None:
                 lines.insert(i, 'xfce4-session\n')
                 break
         # update startwm.
         with open(startwm, 'w') as f:
             for line in lines:
                 f.write(line)
         # copy to /etc/xrdp/startwm.sh
         cmd = r'sudo cp %s /etc/xrdp/startwm.sh && sudo chmod 0755 /etc/xrdp/startwm.sh' % startwm
         subprocess.call(cmd, shell=True)
         # delete temp startwm
         os.remove(startwm)

    # restart xrdp
    def restart_xrdp(self):
         cmd = r'sudo service xrdp restart'
         subprocess.call(cmd, shell=True)

if __name__ == '__main__':
     xubuntu = ConfigXubuntuDesktop()
     xubuntu.install_xrdp()
     xubuntu.install_xubuntu_desktop()
     xubuntu.config_xsession()
     xubuntu.config_startwp_sh()
     xubuntu.restart_xrdp()
