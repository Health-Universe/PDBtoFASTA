import streamlit as st
import subprocess
import os
import time
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), "PDBtoFASTA"))

from pdb_to_fasta import Pdb, AMINO_ACIDS_3TO1


st.markdown("## PDB to FASTA")
st.divider()

# File uploader
pdb_file = st.file_uploader(
    "Upload",
    type="pdb",
    help="**Input:** Protein PDB \n\n**Output:** FASTA string"
)

# Optional
hetatm_residues = st.checkbox("HETATM Residues",
                              value=False,
                              help="If checked, output will include HETATM Residue."
                              )

# Check if a PDB file is uploaded
if pdb_file is not None:

    # Show the "Run" button
    if st.button("Run", help="Convert PDB to FASTA"):
        with st.spinner("Running..."):
            time.sleep(2)
            # Save the PDB file to a temporary location
            temp_pdb_file_path = os.path.join("/tmp", pdb_file.name)
            with open(temp_pdb_file_path, "wb") as f:
                f.write(pdb_file.getvalue())

            # Define the command-line arguments for the external script
            cmd_args = ["python", "pdb_to_fasta.py", temp_pdb_file_path]
            if hetatm_residues:
                cmd_args.append("--ligand")

            # Call the external script using subprocess
            result = subprocess.run(cmd_args, capture_output=True, text=True)

            # Display the output
            st.code(result.stdout)

            # Save the FASTA output to a temporary file
            temp_fasta_file_path = os.path.join("/tmp", "output.fasta")
            with open(temp_fasta_file_path, "w") as f:
                f.write(result.stdout)

            # Download the FASTA file using st.download
            st.markdown("## Download FASTA File")
            st.download_button(label="Download FASTA", data=temp_fasta_file_path, file_name="output.fasta")

            # Remove the temporary PDB and FASTA files
            os.remove(temp_pdb_file_path)
            os.remove(temp_fasta_file_path)
