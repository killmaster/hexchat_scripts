#!/usr/bin/env python
# -*- coding: utf-8 -*-
__module_name__ = 'denzel\'s script'
__module_version__ = '1.1'
__module_description__ = 'agora com frases'

import hexchat
import itertools
import time

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

@RateLimited(2)  # 2 per second at most
def flood(line):
    hexchat.command('say {}'.format(line))

def denzel(word, word_eol, userdata):
	if len(word) > 1:
		flood(word_eol[1])
		for letter in word_eol[1][1:]:
			flood(letter)
	else:
		hexchat.command('help denzel')
	return hexchat.EAT_ALL

hexchat.hook_command('denzel', denzel, help='DENZEL <palavra>')
