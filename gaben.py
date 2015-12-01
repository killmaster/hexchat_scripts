#!/usr/bin/env python
# -*- coding: utf-8 -*-
__module_name__ = 'gaben'
__module_version__ = '1.0'
__module_description__ = 'gaben'

import hexchat
import time

with open('C:/Users/carlo/AppData/Roaming/HexChat/addons/gaben') as f:
    lines = f.read().splitlines()

def RateLimited(maxPerSecond):
    minInterval = 1.0 / float(maxPerSecond)
    def decorate(func):
        lastTimeCalled = [0.0]
        def rateLimitedFunction(*args,**kargs):
            elapsed = time.clock() - lastTimeCalled[0]
            leftToWait = minInterval - elapsed
            if leftToWait>0:
                time.sleep(leftToWait)
            ret = func(*args,**kargs)
            lastTimeCalled[0] = time.clock()
            return ret
        return rateLimitedFunction
    return decorate

@RateLimited(5)  # 5 per second at most
def flood(line):
    hexchat.command('say {}'.format(line))

def gaben(word, word_eol, userdata):
    for line in lines:
        flood(line)
    return hexchat.EAT_ALL

hexchat.hook_command('gaben', gaben, help='gaben is love gaben is life')
