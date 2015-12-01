__module_name__ = "stop SPAM" 
__module_version__ = "1.5 for xchat" 
__module_description__ = "stop SPAM: SAO is still bad"
import hexchat

botcommands = {
	':!find',
	':@find',
	':/msg',
	':/MSG',
	':!new',
	':!list',
	':!search',
	':!FIND',
	':@FIND',
	':!packlist',
	':!help'
}

badwords = {
	'sao',
	'SAO'
}

def stopSPAM(word,word_eol, userdata):
	if word[3].lower() in botcommands:
		return hexchat.EAT_ALL
	if any(substring in word_eol[2].lower() for substring in badwords):
		return hexchat.EAT_ALL
	else:
		return hexchat.EAT_NONE
			
hexchat.hook_server('PRIVMSG', stopSPAM)
