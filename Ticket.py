import discord
from discord.ext import commands


PREFIX = ""
TOKEN = ""


client = commands.Bot(command_prefix=f"{PREFIX}")

@client.event
async def on_raw_reaction_add(payload):
  #msg = await ctx.fetch_message(payload.channel)
  #print(payload.message_id)
  channel = client.get_channel(payload.channel_id)
  msg = await channel.fetch_message(payload.message_id)
  emoji = payload.emoji.name
  user = payload.member
  guild = discord.utils.find(lambda g : g.id == payload.guild_id, client.guilds)
  if channel.name.startswith("support-"):
    if emoji == "🔒":
      if not user.bot:
        await msg.remove_reaction(emoji, user)
        await channel.send("Ticket closing in 5 seconds!")
        time.sleep(5)
        await channel.delete()
  if msg.id == 840685832800043088:
    print("creating ticket!")
    getID = random.randint(1,5000)
    ticketEmbed = discord.Embed(
      title=f"Ticket {getID} Created!",
      description = f"{user}'s Ticket Has Been Opened! \nReact with 🔒 to close the ticket!",
      color = discord.Color.dark_gold())
      #timestamp=payload.created_at)
    admin_role = get(guild.roles, name="Admin")
    overwrites = {
      guild.default_role: discord.PermissionOverwrite(read_messages=False),
      guild.me: discord.PermissionOverwrite(read_messages=True),
      admin_role: discord.PermissionOverwrite(read_messages=True),
      user: discord.PermissionOverwrite(read_messages=True)
    }
    channel = await guild.create_text_channel(f'Support-{user.display_name}', overwrites=overwrites)
    ticMsg = await channel.send(embed=ticketEmbed)
    await ticMsg.add_reaction("🔒")
    await msg.remove_reaction(emoji, user)

@client.command()
@has_permissions(administrator=True)
async def ticketAdm(ctx):
  embed = discord.Embed(title="Create a Ticket!", description="Create a ticket to talk to staff!", color=0x0059f2)
  embed.set_image(url="https://www.freeiconspng.com/thumbs/hd-tickets/download-ticket-ticket-free-entertainment-icon-orange-ticket-design-0.png")

  emMsg = await ctx.send(embed=embed)
  await emMsg.add_reaction("🎟")
  
  client.run(TOKEN)
