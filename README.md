[![DOI](https://zenodo.org/badge/1219039183.svg)](https://doi.org/10.5281/zenodo.19709395)

# Command: enzywizard-batch

EnzyWizard-Batch is a command-line tool for running a complete EnzyWizard
analysis workflow from a cleaned protein structure and a matched MSA file.
It performs multiple EnzyWizard modules, including amino acid property analysis, 
hydrophobic cluster detection, energy evaluation, flexibility analysis, 
disorder prediction, conservation analysis, protein embedding generation, 
pocket detection, optional substrate
feature generation, optional molecular docking, interaction network calculation,
and final graph integration.
If substrate names or SMILES strings are provided, the full protein-substrate
workflow will be executed, including substrate preparation, docking,
protein-substrate interaction detection, and strict graph integration.
If no substrate input is provided, the program generates a protein-only integrated graph 
based on protein-level features and intra-protein interactions.
The final output is an integrated graph dataset that can be directly used for
graph-based analysis, machine learning, and enzyme function studies.


# example usage:

Example command:

enzywizard-batch -i examples/input/cleaned_3GP6.cif -m examples/input/jhmm_3GP6.sto -s glucose,fructose -o examples/output/


# input parameters:

-i, --cleaned_input_path
Required.
Path to the input cleaned protein structure file in CIF or PDB format.

The file must:
- already be cleaned
- contain a valid single protein chain
- contain hydrogen atoms
- match the sequence used to generate the input MSA

-m, --input_msa
Required.
Path to the input MSA file.

Supported MSA formats include:
- Stockholm (.sto)
- aligned FASTA
- A3M

The MSA must be generated using the cleaned protein FASTA sequence.

-s, --substrate_names
Optional.
Substrate names or SMILES strings.

Multiple substrates should be separated by ','.

If provided, the following additional workflows will be executed:
- substrate feature generation
- substrate 3D structure generation
- molecular docking
- protein-substrate interaction calculation
- strict graph integration

If not provided, substrate, docking, and protein-substrate interaction steps
will be skipped.

-o, --output_dir
Required.
Directory to save batch outputs.

--save_extra_outputs
Optional.
Enable keeping intermediate and side output files.

By default, this option is disabled, and only the final integrated JSON outputs
and log.txt are kept.

When enabled, additional files such as cleaned MSA, HMM profile, substrate SDF
files, docked substrate files, and protein-ligand complex files may be saved.

--hydrocluster_cutoff
Optional.
Minimum contact area cutoff for hydrophobic cluster residue-residue connection.
Default: 10.0.

--no_minimize_energy
Optional.
Disable energy minimization before energy evaluation.
By default, energy minimization is enabled.

--energy_minimization_iteration
Optional.
Maximum number of iterations for energy minimization.
Default: 1000.

--flexibility_method
Optional.
Normal mode method for RMSF calculation.
Choices:
- ANM
- GNM
Default: ANM.

--flexibility_cutoff
Optional.
Distance cutoff used to determine residue connections in ProDy.
Default: 15.0.

--flexibility_n_modes
Optional.
Number of low-frequency normal modes used for RMSF calculation.
Default: 20.

--disorder_window_size
Optional.
Sliding window size for FoldIndex-like disorder score calculation.
Default: 11.

--disorder_min_region_length
Optional.
Minimum number of consecutive residues required to define a disordered region.
Default: 5.

--embedding_model_name
Optional.
ESM2 model used for residue embedding generation.

Choices:
- esm2_t6_8M_UR50D
- esm2_t12_35M_UR50D
- esm2_t30_150M_UR50D

Default: esm2_t6_8M_UR50D.

--pocket_min_rad
Optional.
Minimum probe radius used by PyVOL for cavity detection.
Default: 1.8.

--pocket_max_rad
Optional.
Maximum probe radius used by PyVOL for cavity detection.
Default: 6.2.

--pocket_min_volume
Optional.
Minimum pocket volume threshold.
Default: 50.

--substrate_max_synonyms
Optional.
Maximum number of substrate synonyms retried when fetching SMILES from a
substrate name.
Default: 20.

--substrate_fp_radius
Optional.
Radius used for Morgan fingerprint generation.
Default: 2.

--substrate_n_bits
Optional.
Bit size of the Morgan fingerprint vector.
Default: 512.

--substrate_num_confs
Optional.
Maximum number of 3D conformers generated for each substrate.
Default: 5.

--substrate_prune_rms
Optional.
RMS threshold used to prune highly similar conformers during 3D conformer
generation.
Default: 0.5.

--dock_max_attempt_num
Optional.
Maximum number of docking attempts.
Default: 20.

--dock_no_early_stop
Optional.
Disable stopping immediately after the first successful docking result.

By default, early stopping is enabled.

--dock_exhaustiveness
Optional.
Exhaustiveness of AutoDock Vina search.
Default: 16.

--dock_cpu
Optional.
Number of CPUs used by AutoDock Vina.
Default: 0.

--hbond_bonded_h_min_distance
Optional.
Minimum bonded heavy atom-hydrogen distance used for hydrogen bond donor
detection.
Default: 0.8.

--hbond_bonded_h_max_distance
Optional.
Maximum bonded heavy atom-hydrogen distance used for hydrogen bond donor
detection.
Default: 1.3.

--hbond_da_max_distance
Optional.
Maximum donor-acceptor distance cutoff for hydrogen bond detection.
Default: 3.9.

--hbond_ha_max_distance
Optional.
Maximum hydrogen-acceptor distance cutoff for hydrogen bond detection.
Default: 2.5.

--hbond_angle
Optional.
Minimum donor-hydrogen-acceptor angle cutoff for hydrogen bond detection.
Default: 90.0.

--ionic_distance_cutoff
Optional.
Maximum distance cutoff for ionic bond detection.
Default: 4.0.

--vdw_mu
Optional.
Mu parameter used in van der Waals interaction detection.
Default: 0.01.

--ppstack_center_distance_cutoff
Optional.
Maximum ring-center distance cutoff for pi-pi stacking detection.
Default: 6.5.

--pication_distance_cutoff
Optional.
Maximum ring-cation distance cutoff for pi-cation interaction detection.
Default: 5.0.

--pication_angle_cutoff
Optional.
Maximum angle cutoff for pi-cation interaction detection.
Default: 45.0.

--ssbond_max_distance
Optional.
Maximum sulfur-sulfur distance cutoff for disulfide bond detection.
Default: 2.5.


# output content:

The program outputs the following files into the output directory:

1. An integrated JSON report
   - integrate_report_{protein_name}.json

   The JSON report contains:

   - "output_type"
     A string identifying the report type:
     "enzywizard_integrate"

   - "integrated_graph"
     A list describing the integrated graph entries.

     Each entry is stored in one of the following formats:

     Node entry:
     - "node_1"
       A single integrated node record representing:
       - an amino acid residue
       - or a substrate, if substrate input is provided

     Edge entry:
     - "node_1"
       Information of the first node

     - "edge"
       Information of the relationship between nodes

     - "node_2"
       Information of the second node

   The integrated graph represents:
   - protein-level residue features
   - residue-residue relationships
   - intra-protein interaction networks
   - optional substrate nodes
   - optional protein-substrate docking and interaction information

2. A node-only JSON file
   - integrate_nodes_{protein_name}.json

   Contains all node records extracted from the integrated graph.

3. An edge-only JSON file
   - integrate_edges_{protein_name}.json

   Contains all edge records extracted from the integrated graph.

If --save_extra_outputs is enabled, additional intermediate or side output files
may also be saved, including:
- cleaned MSA STO file
- HMM profile file
- substrate SDF files
- docked substrate files
- protein-substrate complex files


# Process:

This command processes the input cleaned structure and MSA as follows:

1. Validate input files
   - Check that cleaned_input_path exists.
   - Check that input_msa exists.
   - Create output_dir if needed.

2. Resolve names
   - Extract protein_name from the cleaned structure filename.
   - Extract msa_name from the MSA filename.
   - Validate filename length.

3. Validate parameters
   - Check parameter ranges for hydrophobic cluster detection.
   - Check energy minimization parameters.
   - Check flexibility and disorder parameters.
   - Check pocket detection parameters.
   - Check substrate generation parameters.
   - Check docking parameters.
   - Check interaction detection parameters.

4. Prepare output mode
   - If --save_extra_outputs is enabled, run directly in output_dir.
   - If disabled, run in a temporary directory and only copy final outputs.

5. Load cleaned structure
   - Read the cleaned CIF or PDB file.
   - Validate that it is a valid cleaned protein structure.
   - Check that hydrogen atoms are present.

6. Build identity clean report
   - Treat the input structure as already cleaned.
   - Build an identity residue mapping between old and new residues.
   - Generate an enzywizard_clean-style report for downstream integration.

7. Prepare OpenMM and sequence objects
   - Convert the cleaned structure into an OpenMM-compatible structure.
   - Build an OpenMM Modeller object.
   - Extract the cleaned protein sequence.

8. Run amino acid property analysis
   - Load DSSP information.
   - Calculate residue-level amino acid properties.
   - Generate the enzywizard_aaprops report.

9. Run hydrophobic cluster analysis
   - Detect hydrophobic residue clusters.
   - Generate the enzywizard_hydrocluster report.

10. Run energy analysis
   - Optionally minimize the protein structure.
   - Calculate energy terms using the selected force field.
   - Generate the enzywizard_energy report.

11. Run flexibility analysis
   - Calculate residue-level RMSF using ANM or GNM.
   - Generate the enzywizard_flexibility report.

12. Run disorder analysis
   - Calculate FoldIndex-like disorder scores.
   - Detect disordered regions.
   - Generate the enzywizard_disorder report.

13. Run conservation analysis
   - Load and validate the input MSA.
   - Clean the MSA into Stockholm format.
   - Build an HMM profile.
   - Calculate residue-level conservation scores.
   - Generate the enzywizard_conservation report.

14. Run embedding analysis
   - Generate residue-level ESM2 embeddings.
   - Generate the enzywizard_embedding report.

15. Run pocket analysis
   - Detect protein pockets using PyVOL.
   - Generate the enzywizard_pocket report.

16. Optionally run substrate analysis
   - Parse substrate names or SMILES strings.
   - Retrieve or complete SMILES information.
   - Generate substrate fingerprints and 3D conformers.
   - Save substrate structure files.
   - Generate the enzywizard_substrate report.

17. Optionally run docking analysis
   - Dock generated substrate structures into predicted protein pockets.
   - Save docking results.
   - Generate the enzywizard_dock report.
   - Load docked ligand structures for interaction analysis.

18. Run interaction analysis
   - If substrate input is provided, filter valid docked substrates.
   - Calculate intra-protein interactions.
   - Calculate protein-substrate interactions when valid docked substrates exist.
   - Summarize interaction counts.
   - Generate the enzywizard_interaction report.

19. Run graph integration
   - Collect all generated reports into report_dict.
   - Use strict integration when substrate input is provided.
   - Use non-strict integration when no substrate input is provided.
   - Merge residue-level, substrate-level, and interaction-level information
     into a unified integrated graph.

20. Save integrated outputs
   - Write integrate_report_{protein_name}.json.
   - Split integrated_graph into node and edge lists.
   - Write integrate_nodes_{protein_name}.json.
   - Write integrate_edges_{protein_name}.json.

21. Finalize outputs
   - If --save_extra_outputs is disabled, copy only the final integrated JSON
     outputs and log.txt from the temporary directory to output_dir.
   - Finish the batch workflow.


# dependencies:

- Biopython
- NumPy
- OpenMM
- DSSP
- ProDy
- ESM
- HMMER
- PyVOL
- RDKit
- AutoDock Vina
- Meeko
- JSON


# references:

- Biopython:
  https://biopython.org/

- OpenMM:
  https://openmm.org/

- DSSP:
  https://github.com/PDB-REDO/dssp

- ProDy:
  http://prody.csb.pitt.edu/

- ESM:
  https://github.com/facebookresearch/esm

- HMMER:
  http://hmmer.org/

- PyVOL:
  https://github.com/schlessinger-lab/pyvol

- RDKit:
  https://www.rdkit.org/

- AutoDock Vina:
  https://vina.scripps.edu/

- Meeko:
  https://github.com/forlilab/Meeko

- JSON:
  https://www.json.org/
