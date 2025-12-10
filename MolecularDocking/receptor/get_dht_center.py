import numpy as np

pdb_file = "1T5Z.pdb"
resname_lig = "DHT"   # ajustar si el residuo se llama distinto en este PDB

coords = []

with open(pdb_file) as f:
    for line in f:
        if line.startswith("HETATM"):
            if line[17:20].strip() == resname_lig:
                x = float(line[30:38])
                y = float(line[38:46])
                z = float(line[46:54])
                coords.append((x, y, z))

coords = np.array(coords)
center = coords.mean(axis=0)
print("Centro del ligando DHT:", center.tolist())
