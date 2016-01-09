#!/usr/bin/env python
# -*- coding: utf-8 -*-
__module_name__ = 'memes'
__module_version__ = '1.0'
__module_description__ = 'shitposting'

import hexchat
from itertools import combinations_with_replacement
import random

spiga_ogui = "juro que quando a ouvi a voz do {}pela primeira vez pensava que ele era atrasado mental. passado uns dias cheguei que há conclusão que ele é mesmo isso. deve ter alguma doença mental e não estou a brincar"
spiga_narcisista = "{}, não sei se estas a satirizar mas és extremamente narcisista, inclusive vens aqui tentar corrigir os teus problemas de autoestima, num canal onde tens autistas que não fodem conas, só para veres o quão no fundo a tua vida está"
strong_words = {
    'strongismos',
    'strongismo'
}

def ogui(word, word_eol, userdata):
  res = spiga_ogui.format(word_eol[1])
  hexchat.command('say {}'.format(res))
  return hexchat.EAT_ALL

def narcisista(word, word_eol, userdata):
  res = spiga_narcisista.format(word_eol[1])
  hexchat.command('say {}'.format(res))

def strongismos(word, word_eol, userdata):
    with open('C:/Users/carlo/AppData/Roaming/HexChat/addons/strongismos', encoding='utf-8') as f:
        lines = f.read().splitlines()
    if any(substring in word_eol[2] for substring in strong_words):
        res = ' '.join(str(x) for x in random.sample(lines,10))
        hexchat.command('say ' + res)

def strongismos_cmd(word, word_eol, userdata):
    with open('C:/Users/carlo/AppData/Roaming/HexChat/addons/strongismos', encoding='utf-8') as f:
        lines = f.read().splitlines()
    res = ' '.join(str(x) for x in random.sample(lines,10))
    hexchat.command('say ' + res)

hexchat.hook_command('ogui', ogui, help='OGUI <nick>')
hexchat.hook_command('narcisista', narcisista, help='NARCISISTA <nick>')
hexchat.hook_server('PRIVMSG', strongismos)
hexchat.hook_command('strong', strongismos_cmd, help='STRONGISMOS')
