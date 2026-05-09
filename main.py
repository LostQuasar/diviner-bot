import discord
from discord import app_commands
import dotenv
import os
import pubchem
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

if not GUILD_ID:
    exit()

MY_GUILD = discord.Object(id=int(GUILD_ID))

class MyClient(discord.Client):
    # Suppress error on the User attribute being None since it fills up later
    user: discord.ClientUser

    def __init__(self, *, intents: discord.Intents):
        super().__init__(intents=intents)
        # A CommandTree is a special type that holds all the application command
        # state required to make it work. This is a separate class because it
        # allows all the extra state to be opt-in.
        # Whenever you want to work with application commands, your tree is used
        # to store and work with them.
        # Note: When using commands.Bot instead of discord.Client, the bot will
        # maintain its own tree instead.
        self.tree = app_commands.CommandTree(self)

    # In this basic example, we just synchronize the app commands to one guild.
    # Instead of specifying a guild to every command, we copy over our global commands instead.
    # By doing so, we don't have to wait up to an hour until they are shown to the end-user.
    async def setup_hook(self):
        # This copies the global commands over to your guild.
        self.tree.copy_global_to(guild=MY_GUILD)
        await self.tree.sync(guild=MY_GUILD)

intents = discord.Intents.default()
client = MyClient(intents=intents)

@client.event
async def on_ready():
    print(f'Logged in as {client.user} (ID: {client.user.id})')
    print('------')


@client.tree.command()
async def compound(interaction: discord.Interaction, name: str):
    """Get information about a compound!"""
    compound_info = pubchem.compound()
    await compound_info.create(name)
    if compound_info.cid == 0:
        await interaction.response.send_message(f"Your search did not return any results", ephemeral=True)
        return

    embed = discord.Embed(
        title=compound_info.title,
        url=compound_info.url,
        color=discord.Colour.random(seed=compound_info.cid)
    )

    embed.add_field(name="Molecular Formula", value=compound_info.molecular_formula, inline=True)
    embed.add_field(name="Molecular Weight", value=f"{compound_info.molecular_weight} mol", inline=True)
    if compound_info.description != "":
        embed.add_field(name="Description", value=compound_info.description, inline=False)

    embed.set_footer(text="Data provided by NIH PubChem Database", icon_url="https://pubchem.ncbi.nlm.nih.gov/pcfe/favicon/favicon-32x32.png")
    embed.set_image(url=compound_info.image_url)

    await interaction.response.send_message("",embed=embed)

client.run(TOKEN)

