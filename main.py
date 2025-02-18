import discord
import dotenv
import os
import pubchempy as pcp
import requests
import re 

bot = discord.Bot()
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")
PUBCHEM_URL = "https://pubchem.ncbi.nlm.nih.gov"

@bot.command(description="Get information about a compound")
async def compound(ctx, name):
    compound_info = pcp.get_compounds(name, 'name')
    if compound_info == []:
        await ctx.respond(f"Your search did not return any results", ephemeral=True)
        return
    compound_info = compound_info[0]
    description = requests.get(f"{PUBCHEM_URL}/rest/pug/compound/cid/{compound_info.cid}/description/json").json()["InformationList"]["Information"][1]["Description"]
    embed = discord.Embed(
        title=str(compound_info.synonyms[0]).title(),
        url=f"{PUBCHEM_URL}/compound/{compound_info.cid}",
        color=discord.Colour.random(seed=compound_info.cid),
    )
    
    embed.add_field(name="Molecular Formula", value=compound_info.molecular_formula, inline=True)
    embed.add_field(name="Molecular Weight", value=f"{compound_info.molecular_weight} mol")
    embed.add_field(name="Description", value=description, inline=False)

    embed.set_footer(text="Data provided by NIH PubChem Database", icon_url=f"{PUBCHEM_URL}/favicon.ico")
    embed.set_image(url=f"{PUBCHEM_URL}/image/imgsrv.fcgi?cid={compound_info.cid}&t=l")

    await ctx.respond(embed=embed)
bot.run(TOKEN)