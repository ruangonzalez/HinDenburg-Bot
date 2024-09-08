import discord
from discord.ext import commands, tasks
from bs4 import BeautifulSoup
import requests
import json
import re

with open ('token.txt','r') as f:
    discord_token = f.readline()

intents = discord.Intents.default()
intents.members = True
intents.message_content = True

client = commands.Bot(command_prefix='!',intents=intents)

@tasks.loop(seconds=60)
async def heartbeat():
    print("ainda vivo...")

@client.event
async def on_ready():
    
    print(f'{client.user} energizado e pronto para servir')
    
    heartbeat.start()
    
    channel = client.get_user(925356567832977418)
    await channel.send(':robot: **ENERGIZADO E PRONTO PARA SERVIR** :robot:')
    await channel.send('https://tenor.com/view/goblin-world-of-warcraft-dance-gif-15507982')
    
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
       
        await message.channel.send("Olá, qual item quer pesquisar hoje? Digite '/wiki <item>' para pesquisar!")
        
   else:
       
        await client.process_commands(message)
@client.tree.command(description="só o passinho do gauchinho")
async def passinho(interact:discord.Interaction):
    await interact.response.send_message('https://tenor.com/view/goblin-world-of-warcraft-dance-gif-15507982')

@client.tree.command(description="pesquisa no WoWHead sobre o >item< que você deseja.")
async def wiki(interact:discord.Interaction, search: str):
    await interact.response.defer()
    
    pesquisa = search.replace(' ', '+')
    url = f'https://www.wowhead.com/pt/search?q={pesquisa}'

    try:
        response = requests.get(url)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        print("Página carregada")
        script = soup.find('script', string=re.compile('WH.SearchPage.showTopResults'))
        
        link = None
        
        if script: 
            script_text = script.string
            
            try:  
                          
                json_text = re.search(r'\[.*?\]', script_text)
                if json_text:
                    json_string = json_text.group(0)
                    
                    # print(f"JSON encontrado: {json_string}")
                    
                    open_braces = 0
                    open_brackets = 0 
                    
                    for char in json_string:
                        
                        if char == '[':
                            open_brackets += 1
                        elif char == ']':
                            open_brackets -= 1
                        elif char == '{':
                            open_braces += 1
                        elif char == '}':
                            open_braces -= 1
                    
                    if open_brackets > open_braces:
                        if open_brackets - open_braces == 1:
                            
                            json_string += '}' * open_braces
                            json_string += ']' * open_brackets
                            
                        else:
                            
                            json_string += ']' * (open_brackets - 1)
                            json_string += '}' * open_braces
                            json_string += ']'
                            
                    elif open_braces > open_brackets:
                        if open_brackets == 1:
                            
                            json_string += '}' * open_braces
                            json_string += ']' * open_brackets
                            
                        else:
                            
                            json_string += ']' * (open_brackets - 1)
                            json_string += '}' * open_braces
                            json_string += ']'
                    else: 
                        
                        json_string += ']' * (open_brackets - 1)
                        json_string += '}' * open_braces
                        json_string += ']'
                                                               
                    # print(f"JSON corrigido: {json_string}")
                    
                    try:
                        items = json.loads(json_string)
                        item_found = False
                        
                        for item in items:
                            
                            item_name = item.get('lvjson', {}).get('name', '')
                            if search.lower() in item_name.lower():
                                
                                item_id = item['typeId']
                                item_name = item['lvjson']['name']
                                url = f'https://www.wowhead.com/pt/item={item_id}/{item_name.replace(" ", "-").lower()}'
                                print(f"Link encontrado para {item_name}: {url}")
                                await interact.followup.send(f"Link encontrado para {item_name}: {url}")
                                item_found = True
                                break
                            
                            elif search.lower() in item_name.lower():
                                
                                try:
                                    
                                    item_id = item['typeId']
                                    item_name = pesquisa
                                    url = f'https://www.wowhead.com/pt/item={item_id}/{item_name.replace(" ", "-").lower()}'
                                    await interact.followup.send(f"Link encontrado para {item_name}: {url}")
                                    item_found = True
                                    break
                                
                                except:
                                        print(f'Item {search} não encontrado.')
                                        await interact.followup.send(f'Item {search} não encontrado.')
                            
                        if not item_found:
                            try:
                                    
                                    item_id = item['typeId']
                                    item_name = pesquisa
                                    url = f'https://www.wowhead.com/pt/item={item_id}/{item_name.replace(" ", "-").lower()}'
                                    await interact.followup.send(f"Link encontrado para {search}: {url}")
                                    item_found = True
                                    
                                
                            except:
                                    print(f'Item {search} não encontrado.')
                                    await interact.followup.send(f'Item {search} não encontrado.')
                
                    except json.JSONDecodeError as e:
                        print(f"Erro ao decodificar JSON: {e}")
                        await interact.followup.send('Erro ao processar dados.')
                        
            except Exception as e:
                print(f"Erro geral: {e}")
                await interact.followup.send('Erro ao processar dados.') 
        else:
            print(f'Item {search} não encontrado.')
            await interact.followup.send(f'Item {search} não encontrado.')
            
    except requests.RequestException as e:
        print(f"Erro na requisição: {e}")
        await interact.followup.send('Erro ao carregar página.')            
        
client.run(discord_token)