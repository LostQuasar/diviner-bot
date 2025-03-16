import discord
import dotenv
import os
import pubchem

bot = discord.Bot()
dotenv.load_dotenv()
TOKEN = os.getenv("TOKEN")

@bot.command(description="Get information about a compound")
async def compound(ctx, name):
    compound_info = pubchem.compound(name)
    if compound_info.cid == 0:
        await ctx.respond(f"Your search did not return any results", ephemeral=True)
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

    await ctx.respond(embed=embed)

bot.run(TOKEN)