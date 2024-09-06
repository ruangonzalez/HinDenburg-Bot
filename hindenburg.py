import discord
from discord.ext import commands
from discord import app_commands
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

with open ('token.txt','r') as f:
    discord_token = f.readline()


intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = discord.Client(intents=intents)
client = commands.Bot(command_prefix='!',intents=intents)


@client.event
async def on_ready():
    
    print(f'{client.user} energizado e pronto para servir')
    
    channel = client.get_user(925356567832977418)
    await channel.send('to online beiçatron')
    
@client.command()
async def sincronizar(ctx:commands.Context):
    
    if ctx.author.id == 925356567832977418:
        
        sincs = await client.tree.sync()
        await ctx.reply(f'{len(sincs)} comandos sincronizados')
        
    else:
        
        await ctx.reply('voce nao pode faze essa merda')
        await ctx.reply('nois vai te mata')

@client.event
async def on_message(message):
    
   if client.user in message.mentions:
       
        await message.channel.send("oi")
        
   else:
       
        await client.process_commands(message)
    
@client.tree.command(description="pesquisa no WoWHead sobre o >item< que você deseja.")
async def wiki(interact:discord.Interaction, search: str):
    await interact.response.defer()
    
    pesquisa = search.replace(' ', '+')
    
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
    
    driver.get(f'https://www.wowhead.com/pt/search?q={pesquisa}')

    try:
       
        wait = WebDriverWait(driver, 10)
        
        for i in range(0,6):
            try:
                
                element = wait.until(EC.presence_of_element_located((By.CLASS_NAME, f'q{i}.listview-cleartext')))
                link = element.get_attribute('href')
                print(f"Link encontrado para q{i}: {link}")
                break
            
            except:
                print(f"Elemento não encontrado para q{i}")
                
        await interact.followup.send(f"Aqui está o link da wiki: " + link)
    
    except Exception as e:
       
        print(f"Erro: {e}")
    
    finally:
       
        driver.quit()
    
client.run(discord_token)