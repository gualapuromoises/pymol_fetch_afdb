Markdown
# PyMOL AlphaFold Fetch Plugin (`fetchaf.py`)

A lightweight, robust PyMOL plugin to dynamically fetch, load, and color AlphaFold protein structure predictions directly from the EBI AlphaFold Database (https://alphafold.ebi.ac.uk/).

## Features
* **Dynamic API Querying:** Automatically queries the EBI AlphaFold API to find the latest available prediction version (e.g., v4, v6) for a given UniProt ID, preventing broken links.
* **Smart Coloring:** Automatically applies the standard AlphaFold pLDDT confidence color scheme (Blue > 90, Cyan > 70, Yellow > 50, Orange ≤ 50) using a cascading selection method that bypasses PyMOL parser errors.
* **Zero Dependencies:** Built entirely with Python's standard libraries (`urllib`, `json`, `os`). Requires no `pip` or Conda installations, avoiding environment conflicts.
* **Clean Organization:** Saves the `.cif` file locally to your current working directory and loads it into the PyMOL workspace using the clean UniProt ID (or a custom name).

## Installation
1. Download or copy the `fetchaf.py` script.
2. Move the script into your PyMOL startup directory:
   ```bash
   mv fetchaf.py ~/.pymol/startup/
   ```
Restart PyMOL. The command is now permanently integrated.

# Usage
Inside the PyMOL command line, use the native command syntax:

```bash
# Fetch a structure and use the UniProt ID as the object name
fetchaf O84553

# Fetch a structure and assign a custom object name
fetchaf O84553, rsbw
```

It can not overwrite, if need to download again, delete first the existing structure: 

```bash
# Delete existing structure to fetch a new structure with the same name 
delete rsbw

# Fetch again and assign a custom object name
fetchaf O84553, rsbw
```

