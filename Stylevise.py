## StyleVise
## Kyle Booten, 2020

from Judge import Judge
import random

import cmd, sys, readline

import time

import argparse


class Game(cmd.Cmd):


	def __init__(self,output='sv_output.txt',level=0):
		super().__init__()
		self.intro = '\nStyle🗜Vise\nType "play" to start a new game.\nType "help" or "?" to list commands.\n'
		self.prompt = '>'
		self.file = None
		started = False
		dead = False
		self.space = "      "
		self.nice_comments = ["Nice!","Impressive.","Solid.","Right on.","Now THAT'S typing.","Yes, make it new!"]
		self.mean_comments = ["*Yawn*","Same old same old.","Is that all you got?","...zzzzz..."]
		self.level2name = {
			0:"EASY",
			1:"MEDIUM",
			2:"HARD",
			3:"EXPERT",
			4:"EVIL"
		}
		self.judge = Judge()
		self.started = False
		##
		##adjustable
		self.output_file = open(output,'a+')
		self.starting_level=level


	## internal events

	def special_print(self,text):
		"duplicates input---print and add to file"
		self.output_file.write(text+"\n")
		print(text)


	def restart(self):
		"set a bunch of variables for one attempt of the game. record time."
		self.level = self.starting_level
		self.old_sents = []
		self.total_points = 0
		self.level_points = 0
		self.points_to_next_level = 10
		self.life = 10
		self.started = False
		self.life_warned = False
		self.dead = False
		## time
		time_string = time.asctime( time.localtime(time.time()) )
		self.output_file.write("\n"+time_string+"\n") 


	def level_banner(self):
		banner="\u001b[32m*****************\u001b[0m\n"
		banner+="\u001b[32mLevel  %d: %s\u001b[0m\n" % (self.level+1,self.level2name[self.level])
		banner+="\u001b[32m*****************\u001b[0m\n"
		return banner


	def scratch_out(self,listoftokens):
		"return a string version with the 'boring' language crossed out"
		newstring = ""
		for token in listoftokens:
			if token.startswith("<"):
				inside = token[1:-1] ## get inside without brackets
				inside = "\u001b[9m%s\u001b[0m" % inside
				newstring+=(" "+inside)
			else:
				newstring+=(" "+token)
		return newstring


	def update_based_on_judgment(self,judgment):
		"""
		update state based on judgement and tell the player about it
		uniqueness is judged before interestingness
		cue other functions to reply to the player's input
		"""
		to_print = ""
		## not interesting
		if judgment['unique']==False:
			to_print+=self.space+"*Yawn*---you have already written:\n"
			to_print+=self.space+'"'+judgment['prevSent']+'"\n'
			to_print+=self.space+"💖-1\n"
			self.life-=1
		## not interesting
		elif judgment['interesting']==False:
			to_print+=self.space+self.scratch_out(judgment['markedUp'])+"\n"
			to_print+=self.space+random.choice(self.mean_comments)+"\n"
			to_print+=self.space+"💖-1\n"
			self.life-=1
		## interesting & unique
		else:
			if random.choice([True,True,True,False]):
				to_print+=self.space+"👍+1\n"
			else:
				to_print+=self.space+"👍"+random.choice(self.nice_comments)+"\n"
			self.old_sents.append(judgment['originalLine'])
			self.total_points+=1
			self.level_points+=1
		### now maybe change level
		if self.life==0:
			self.dead = True
			to_print += "%sOut of 💖s.\n%sGAME OVER\n%sYou earned %d points this time.\n%sType 'play' to start again\n" % (self.space,self.space,self.space,self.total_points,self.space)
		elif self.life==1:
			if self.life_warned==False:
				self.life_warned==True
			to_print+="%s\u001b[38;5;40;5;7m(Warning...only one 💖 left!)\u001b[0m\n" % self.space
		elif self.level_points==self.points_to_next_level:
			if self.level<self.judge.max_level: ## should be 5
				self.level+=1
				to_print+=self.level_banner()
		return to_print


	def win(self):
		"print celebration once player wins"
		self.special_print("%sYOU WIN\n%s~~~~~~~\n" % (self.space, self.space))
		elite_sentence = "elite sentence generator!".split()
		celebrations = list("       💫💫💫💫💯💯💯🙌🙌💪🧠🤟🎆🎉🎉")
		for i in range(9):
			self.special_print("%s%s%s" % (self.space," "*random.randrange(4),elite_sentence[0]))
			elite_sentence.append(elite_sentence.pop(0))
			self.special_print("%s%s" % (self.space," ".join(random.sample(celebrations,4))))



	## interpreted commands (using cmd)


	def do_quit(self,args):
		"Quit the game"
		try:
			self.special_print("%sYou earned %d points this time.\n" % (self.space,self.total_points))
			print("%sSession data saved to %s.\n" % (self.space,self.output_file.name)) ## don't record
			self.output_file.close()
		except:
			print("Goodbye.")  ## if not played
		return True


	def do_info(self,args):
		"Learn about the game"
		with open('readme.md','r') as f:
			readme = f.read()
		to_print = readme.split("***")[0].rstrip()
		self.special_print(to_print)


	def do_score(self,args):
		"Check your score"
		try:
			"print the player's current score and health"
			to_print = "%s👍 = %d\n%s💖 = %d\n" % (self.space*2,self.total_points,self.space*2,self.life)
		except:
			to_print = self.intro
		self.special_print(to_print)


	def do_play(self,args):
		"Start (or restart) the game"
		self.restart()
		self.started = True
		to_print=self.level_banner()
		to_print+="%sType 'score' to see your current points (👍) and your remaining life (💖).\n" % self.space
		to_print+="%sSee how many points you can get before you run out of life!\n" % self.space
		self.special_print(to_print)


	def default(self,args):
		"""
		handle any non-parsable input
		assume it is a sentence to be judged
		"""
		if self.started==True and self.dead==False:
			if args[-1] in ".?!":  ## make sure input ends in punctuation
				self.output_file.write(args+"\n") ## write user line to file
				judgment = self.judge.input_and_test_new_sent(args,self.level,self.old_sents)
				to_print = self.update_based_on_judgment(judgment)
			else:
				if len(args.split(" "))==1: ## if it looks like a special command
					to_print = "%sAre you trying to enter a command?\n%sIf so, type 'help' or '?'.\n" % (self.space,self.space)
				else: ## if no puntuation
					to_print = "%sPlease make sure to end your sentence with punctuation ('.', '?', or '!')\n" % self.space
		else:
			to_print = self.intro
		self.special_print(to_print)


def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-o", action='store', type=str, default="sv_output.txt",
                        help="Where the program will record interactions")
	parser.add_argument("-l", action='store', type=int, default=1,
						help="Initial level of difficulty (1-5)")
	args = parser.parse_args()
	sv = Game(output=args.o,level=args.l-1)
	sv.cmdloop()


if __name__ == '__main__':
	main()





