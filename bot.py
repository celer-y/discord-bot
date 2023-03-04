import os
import discord
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from discord.ext import commands

# Discord bot setup
intents = discord.Intents.all()
intents.members = True  # to enable member related events
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')

# Google Spreadsheet API setup
scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']
creds = ServiceAccountCredentials.from_json_keyfile_name('credentials', scope)
client_gspread = gspread.authorize(creds)
spreadsheet_id = '1mqTkELnm72KQ1V57c5-7qSDiI-gfrUhOFivRtzhaif8'
sheet = client_gspread.open_by_key(spreadsheet_id).sheet1

# Discord command to read data from the spreadsheet
@bot.command()
async def search(ctx, name):
    # Get headers
    headers = sheet.row_values(1)
    # Get data
    data = sheet.get_all_values()
    # Find the row index of the user with the given name
    name_column_index = headers.index('Name')
    for index, row in enumerate(data):
        if row[name_column_index] == name:
            break
    else:
        await ctx.send(f"Couldn't find a row with the name {name}.")
        return
    # Create embed
    embed = discord.Embed(title="Search Results", color=discord.Color.blue())
    # Add fields to embed
    for header, value in zip(headers, data[index]):
        embed.add_field(name=header, value=value, inline=True)
    await ctx.send(embed=embed)
    
bot.run('TOKEN')
