import webbrowser as wb
from discord.embeds import Embed
from discord.errors import DiscordServerError
import discord.ext as commands
import discord
import time

BOT = 'OTI3MzQzNTk1NjU1MTU1NzY0.YdI2Bg.yZLqR9uZNIjB50RGpkOmBUz9AQE'
client = discord.Client()

GameRunning = False
forca = ''
sentMessage = ''
class Game():

    def __init__ (self, word):
        global GameRunning
        self.finalWord = word
        self.secretWord = len(self.finalWord) * '-'
        self.lifes = 3
        GameRunning = True
   
    def EndGame(self, win):
        if win:
            str = 'you won'
        else:
            str = 'you lost'
            
        return self.final_EMBED(str)
        
        
    def Logic(self, guess, user):
        global GameRunning
        found = False
        for i in range(len(self.finalWord)):
            if self.finalWord[i] == guess:
                found = True
                self.secretWord = self.replacer(self.secretWord ,guess,i)
                if self.finalWord == self.secretWord:
                    GameRunning = False
                    return self.EndGame(True)
        if not found:
            if self.lifes <= 0:
                GameRunning = False
                return self.EndGame(False)
            else:
                self.lifes -=1
        return self.EMBED(user)       
                
    def EMBED(self, user):
        table = discord.Embed(
            title = 'Jogo da forca 🙈',
            description = (self.secretWord),
            colour = 8927650
        )
        table.add_field(name = 'Vidas: ', value = str(self.lifes) + ' ❤', inline = False)
        table.set_author(name = user, icon_url = 'https://i.pinimg.com/originals/e7/4b/38/e74b38cbb1cf9d5ddd4edf15557fedd1.gif')
        return table
    
    def final_EMBED(self, str):
        table = discord.Embed(
            title = 'Jogo da forca 🙉',
            description = 'Game over, ' + str + ', secret word was ' + self.finalWord,
            colour = 8921000
        )
        return table
    
    def replacer(self, s, newstring, index, nofail=False):
        if not nofail and index not in range(len(s)):
            raise ValueError("index outside given string")
        if index < 0:  
            return newstring + s
        if index > len(s): 
            return s + newstring
        return s[:index] + newstring + s[index + 1:]
    

    
@client.event
async def on_ready():
    print ("Bot is online 🙉") 
async def on_disconnect():
    print ("Bot is offline 🙈") 
    
@client.event
async def on_message(message):
    user = str(message.author).split('#')[0]
    user_message = str(message.content)
    channel = str(message.channel.name)
    
    global GameRunning 
    global forca #name of the class
    global sentMessage #embed table
    
    if message.channel.name == "bot-commands":
        
        #jogo da forca
        if user_message.startswith('!forca ') and not GameRunning:
            word = user_message.replace("!forca ", "", 1)
            await message.delete()
            table = Game(word).EMBED(user)
            sentMessage = await message.channel.send(embed = table)
            forca = Game(word) 
              
        elif user_message.startswith('?') and GameRunning:
            word = user_message.replace("?", "", 1)  
            await message.delete()
            table = forca.Logic(word, user)
            await sentMessage.edit(embed = table)
            
        #spam machine
        elif user_message.startswith("! "):
            input = Game.replacer(Game ,user_message.lower(), "", x)
            input = Game.replacer(Game, input, "", 0)
            for i in range(3):
                if input[1] == '@':
                    async with message.channel.typing():
                        await message.channel.send(input * 30 + ' ')
                        time.sleep(1)
            
        #cancel every game
        elif user_message.startswith('!cancel'):
            GameRunning = False
            await message.channel.send(f'Game cancelled by {user}')
    return            

client.run(BOT)