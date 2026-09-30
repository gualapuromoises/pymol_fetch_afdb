import os
import json
import urllib.request
from pymol import cmd

def fetchaf(uniprot_id, name=None):
    """
    DESCRIPTION
        Fetches the AlphaFold structure from EBI AlphaFold DB using a UniProt ID,
        saves the file locally as <uniprot_id>.cif, loads it into PyMOL as <uniprot_id>,
        and colors it by pLDDT confidence.
        
    USAGE
        fetchaf uniprot_id [, name]
        
    EXAMPLE
        fetchaf O84146
    """
    uniprot_id = str(uniprot_id).upper().strip()
    
    if not name:
        name = uniprot_id
        
    fetch_path = cmd.get("fetch_path") or "."
    output_file = os.path.join(fetch_path, f"{name}.cif")
    
    api_url = f"https://alphafold.ebi.ac.uk/api/prediction/{uniprot_id}"
    print(f"Querying AlphaFold API for {uniprot_id}...")
    
    try:
        req = urllib.request.Request(api_url, headers={"Accept": "application/json"})
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read().decode("utf-8"))
            
        if not data:
            print(f"Error: No AlphaFold prediction found for {uniprot_id}.")
            return
            
        cif_url = data[0].get("cifUrl")
        if not cif_url:
            print("Error: No CIF URL returned by the AlphaFold API.")
            return
            
        print(f"Downloading as {output_file}...")
        urllib.request.urlretrieve(cif_url, output_file)
        
        cmd.load(output_file, name)
        
        # Apply pLDDT coloring via cascading overrides to avoid '<=' parser errors.
        # We also use 'model {name}' to prevent namespace collisions.
        cmd.color("orange", f"model {name}")
        cmd.color("yellow", f"model {name} and b > 50")
        cmd.color("cyan",   f"model {name} and b > 70")
        cmd.color("blue",   f"model {name} and b > 90")
        
        cmd.orient(name)
        print(f"Success! Saved as '{output_file}' and loaded as object '{name}'.")
        
    except urllib.error.HTTPError as e:
        if e.code == 404:
            print(f"Error: UniProt ID '{uniprot_id}' not found in AlphaFold DB.")
        else:
            print(f"HTTP Error {e.code}: Could not fetch structure.")
    except Exception as e:
        print(f"Connection Error: {str(e)}")

cmd.extend("fetchaf", fetchaf)
