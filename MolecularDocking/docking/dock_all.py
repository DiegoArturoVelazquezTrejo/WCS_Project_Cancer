from vina import Vina
import os

# Sustituye estos valores por el centro que calculaste con get_dht_center.py
CENTER = [0.022571428571428527, 64.09828571428572, 3.921333333333334]
BOX = [20, 20, 20]         # puedes ajustar si quieres una caja más grande

RECEPTOR_PDBQT = "../receptor/AR_noDHT.pdbqt"
LIGANDS = ["DHT", "ARN", "BIC", "ENZ"]

def run(name, center, box,
        receptor_pdbqt=RECEPTOR_PDBQT,
        lig_dir="../ligands",
        out_dir="results",
        exhaustiveness=32,
        n_poses=20,
        seed=42):

    os.makedirs(out_dir, exist_ok=True)

    v = Vina(sf_name='vina', seed=seed, cpu=8)

    # Receptor
    v.set_receptor(receptor_pdbqt)

    # Definir mapas de afinidad en la caja (pocket de DHT)
    v.compute_vina_maps(center=center, box_size=box)

    # Ligando
    lig_path = os.path.join(lig_dir, f"{name}.pdbqt")
    v.set_ligand_from_file(lig_path)

    print(f"\n===== {name} =====")

    # IMPORTANTE: NO llamamos v.score() ni v.optimize() aquí
    # porque el ligando viene en un sistema de coordenadas arbitrario.
    # Dejamos que Vina lo coloque durante el docking:

    v.dock(exhaustiveness=exhaustiveness, n_poses=n_poses)

    # Energías de las poses (kcal/mol)
    energies = v.energies(n_poses=n_poses)
    # energies es un array Nx3: [E, rmsd_lb, rmsd_ub]
    best = energies[0, 0]
    print(f"Best binding energy: {best:.3f} kcal/mol")
    print("All pose energies (kcal/mol):", energies[:, 0])

    # Guardar poses
    out_pdbqt = os.path.join(out_dir, f"{name}_out.pdbqt")
    v.write_poses(out_pdbqt, n_poses=5, overwrite=True)
    print("Saved poses →", out_pdbqt)

if __name__ == "__main__":
    os.makedirs("results", exist_ok=True)
    for name in LIGANDS:
        run(name, CENTER, BOX)
