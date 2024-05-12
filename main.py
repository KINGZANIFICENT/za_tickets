import discord
from discord.ext import commands
from discord.ui import Button, View
from discord import Intents

intents = discord.Intents.default()
intents.messages = True
intents.guilds = True
intents.reactions = True

bot = commands.Bot(command_prefix='$', intents=Intents.all())

class TicketMenu(View):
    def __init__(self):
        super().__init__()
        self.add_item(Button(style=discord.ButtonStyle.green, label="Create Ticket", custom_id="create_ticket"))

@bot.event
async def on_ready():
    print('Logged in as {0.user}'.format(bot))

@bot.event
async def on_button_click(interaction):
    print(f"Button interaction detected: {interaction.custom_id}")
    if interaction.custom_id == "create_ticket":
        await interaction.response.send_message("Creating ticket...")
        await interaction.followup.send("Ticket created!")

@bot.command()
async def create_ticket(ctx):
    player_reports_channel_id = 1238350635104211006 # your player reports channel here
    player_reports_channel = bot.get_channel(player_reports_channel_id)
    if not player_reports_channel or not isinstance(player_reports_channel, discord.TextChannel):
        return await ctx.send("Player reports channel not found. Please provide a valid channel ID.")

    thread_name = f'ticket-{ctx.author}'
    thread = await player_reports_channel.create_thread(name=thread_name, auto_archive_duration=1440)  # 1440 minutes (24 hours)

    
    await thread.add_user(ctx.author)

   
    staff_role_id = 1238350632197558314 #your staff id here
    staff_role = ctx.guild.get_role(staff_role_id)
    if staff_role:
        for member in ctx.guild.members:
            if staff_role in member.roles:
                await thread.add_user(member)

    await ctx.send(f'Ticket created in thread: {thread.name}')

@bot.command()
async def close_ticket(ctx):
    if isinstance(ctx.channel, discord.Thread):
        await ctx.channel.delete()
        await ctx.send("Ticket closed.")
    else:
        await ctx.send("This command can only be used in a ticket thread.")

@bot.command()
async def setup_menu(ctx, channel_id: int):
    channel = bot.get_channel(channel_id)
    if channel:
        message = await channel.send("Click the button below to create a ticket:", view=TicketMenu())
    else:
        await ctx.send("Invalid channel ID.")

bot.run('MTIzOTEyNzM5NzcxMDgyMzQ1NQ.GI4bLg.WVVSN6N5ojdSETWz4C6BAMD3bo4CvzisLohPik') # your bot token here

