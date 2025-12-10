for lig in DHT ARN BIC ENZ; do
    obabel -ipdbqt ${lig}_out.pdbqt -opdb -O ${lig}_poses.pdb
done
