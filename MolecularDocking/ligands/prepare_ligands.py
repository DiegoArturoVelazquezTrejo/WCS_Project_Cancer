from rdkit import Chem
from rdkit.Chem import AllChem
from meeko import MoleculePreparation, PDBQTWriterLegacy
import os

# Diccionario: nombre -> SMILES
SMILES = {
    "DHT": "C[C@]12CCC(=O)C[C@@H]1CC[C@@H]3[C@@H]2CC[C@]4([C@H]3CC[C@@H]4O)C",
    "ARN": "NC(=O)C1=C(C=C(C=C1)N2C(=S)N(C(=O)C23CCC3)C4=CC(=C(N=C4)C#N)C(F)(F)F)F",
    "BIC": "CC(CS(=O)(=O)C1=CC=C(C=C1)F)(C(=O)NC2=CC(=C(C=C2)C#N)C(F)(F)F)O",
    "ENZ": "CC1(C(=O)N(C(=S)N1C2=CC(=C(C=C2)C(=O)NC)F)C3=CC(=C(C=C3)C#N)C(F)(F)F)C"
}

def smiles_to_3d_pdbqt(name, smiles, out_dir=".", ph=7.4):
    import os
    from rdkit import Chem
    from rdkit.Chem import AllChem
    from meeko import MoleculePreparation, PDBQTWriterLegacy

    # 1) Parsear SMILES y generar 3D
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        raise ValueError(f"No se pudo parsear el SMILES de {name}")

    mol = Chem.AddHs(mol)
    params = AllChem.ETKDGv3()
    params.randomSeed = 42
    AllChem.EmbedMolecule(mol, params)
    AllChem.UFFOptimizeMolecule(mol, maxIters=500)

    # (Opcional) guardar SDF
    sdf_path = os.path.join(out_dir, f"{name}.sdf")
    w = Chem.SDWriter(sdf_path)
    w.write(mol)
    w.close()

    # 2) Preparar para Vina con Meeko
    mk_prep = MoleculePreparation()
    molsetup_list = mk_prep.prepare(mol)
    molsetup = molsetup_list[0]

    # 3) Escribir PDBQT (manejar el caso str / tupla)
    result = PDBQTWriterLegacy.write_string(molsetup)

    if isinstance(result, tuple):
        pdbqt_string = result[0]   # nos quedamos con el string
    else:
        pdbqt_string = result

    pdbqt_path = os.path.join(out_dir, f"{name}.pdbqt")
    with open(pdbqt_path, "w") as f:
        f.write(pdbqt_string)

    print(f"{name}: escritos {sdf_path} y {pdbqt_path}")

if __name__ == "__main__":
    out_dir = "."
    os.makedirs(out_dir, exist_ok=True)
    for name, smi in SMILES.items():
        smiles_to_3d_pdbqt(name, smi, out_dir=out_dir)
