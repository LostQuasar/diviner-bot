import aiohttp
import asyncio

API_URL = "https://pubchem.ncbi.nlm.nih.gov/rest/pug/compound"
LINK_URL = "https://pubchem.ncbi.nlm.nih.gov/compound"

class compound:
    cid = 0
    title = ""
    molecular_weight = 0.0
    molecular_formula = ""
    description = ""
    image_url = ""
    url = ""

    def __init__(self):
        return
    
    async def create(self, name):
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{API_URL}/name/{name}/cids/json") as r:
                if r.status == 200:
                    js = await r.json()
                    self.cid = int(js["IdentifierList"]["CID"][0])

            properties = ["Title","MolecularWeight","MolecularFormula"]
            async with session.get(f"{API_URL}/cid/{self.cid}/property/{",".join(properties)}/json") as r:
                if r.status == 200:
                    js = await r.json()
                    data = js["PropertyTable"]["Properties"][0]
                    self.title = data["Title"]
                    self.molecular_weight = float(data["MolecularWeight"])
                    self.molecular_formula = data["MolecularFormula"]
            async with session.get(f"{API_URL}/cid/{self.cid}/description/json") as r:
                if r.status == 200:
                    js = await r.json()
                    if len(js["InformationList"]["Information"]) > 1:
                        self.description = js["InformationList"]["Information"][1]["Description"]      
            self.image_url = f"{API_URL}/cid/{self.cid}/png"
            self.url = f"{LINK_URL}/{self.cid}"

async def main():
    compound_data = compound()
    await compound_data.create("advil")
    print(compound_data.cid)
    print(compound_data.title)
    print(compound_data.molecular_weight)
    print(compound_data.molecular_formula)
    print(compound_data.image_url)
    print(compound_data.url)

#TEST API
if __name__ == "__main__":
    asyncio.run(main())



    