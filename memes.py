#!/usr/bin/env python
# -*- coding: utf-8 -*-
__module_name__ = 'memes'
__module_version__ = '1.0'
__module_description__ = 'shitposting'

import hexchat

spiga_ogui = "juro que quando a ouvi a voz do {}pela primeira vez pensava que ele era atrasado mental. passado uns dias cheguei que há conclusão que ele é mesmo isso. deve ter alguma doença mental e não estou a brincar"
spiga_narcisista = "{}, não sei se estas a satirizar mas és extremamente narcisista, inclusive vens aqui tentar corrigir os teus problemas de autoestima, num canal onde tens autistas que não fodem conas, só para veres o quão no fundo a tua vida está"

def ogui(word, word_eol, userdata):
  res = spiga_ogui.format(word_eol[1])
  hexchat.command('say {}'.format(res))
  return hexchat.EAT_ALL 

def narcisista(word, word_eol, userdata):
  res = spiga_narcisista.format(word_eol[1])
  hexchat.command('say {}'.format(res))

hexchat.hook_command('ogui', ogui, help='OGUI <nick>')
hexchat.hook_command('narcisista', narcisista, help='NARCISISTA <nick>')
