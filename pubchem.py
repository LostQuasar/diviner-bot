import requests
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

    def __init__(self, name):
        resp = requests.get(f"{API_URL}/name/{name}/cids/json").json()
        if "Fault" in resp:
            return
        self.cid = int(resp["IdentifierList"]["CID"][0])

        properties = ["Title","MolecularWeight","MolecularFormula"]
        resp = requests.get(f"{API_URL}/cid/{self.cid}/property/{",".join(properties)}/json").json()
        if "Fault" in resp:
            return
        data = resp["PropertyTable"]["Properties"][0]
        self.title = data["Title"]
        self.molecular_weight = float(data["MolecularWeight"])
        self.molecular_formula = data["MolecularFormula"]

        resp = requests.get(f"{API_URL}/cid/{self.cid}/description/json").json()
        if "Fault" in resp:
            return
        if len(resp["InformationList"]["Information"]) > 1:
            self.description = resp["InformationList"]["Information"][1]["Description"]      

        self.image_url = f"{API_URL}/cid/{self.cid}/png"
        self.url = f"{LINK_URL}/{self.cid}"

#TEST API
if __name__ == "__main__":
    compound_data = compound("advil")
    print(compound_data.cid)
    print(compound_data.title)
    print(compound_data.molecular_weight)
    print(compound_data.molecular_formula)
    print(compound_data.image_url)
    print(compound_data.url)

    