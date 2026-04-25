from __future__ import annotations
from argparse import Namespace, ArgumentParser
from ..services.batch_service import run_batch_service


def add_batch_parser(parser: ArgumentParser) -> None:
    parser.add_argument("-i", "--cleaned_input_path",required=True,help="Path to input cleaned CIF/PDB file. The file needs to already be cleaned.")
    parser.add_argument("-m", "--input_msa",required=True,help="Path to input MSA file (STO/aligned FASTA/A3M format). The MSA file needs to be generated using the cleaned FASTA sequence.")
    parser.add_argument("-s","--substrate_names",required=False,default=None,help="Optional substrate names or SMILES strings. Multiple substrates should be separated by ','. If not provided, substrate, dock, and protein-substrate interaction steps will be skipped.")
    parser.add_argument("-o", "--output_dir",required=True,help="Path to output directory. If --save_extra_outputs is False, only final integrate JSON files and log.txt will be kept here.")
    parser.add_argument("--save_extra_outputs", dest="save_extra_outputs", action="store_true",help="Enable keeping extra output files such as HMM, substrate SDFs, docked SDFs, and complex CIF files (default: Disabled).")
    parser.set_defaults(save_extra_outputs=False)
    parser.add_argument("--hydrocluster_cutoff",type=float,default=10.0,help="Minimum contact area cutoff for hydrophobic cluster residue-residue connection (default: 10.0).")
    parser.add_argument("--no_minimize_energy",action="store_false",dest="minimize_energy",help="Disable performing an energy minimization before energy evaluation (default: enabled).")
    parser.set_defaults(minimize_energy=True)
    parser.add_argument("--energy_minimization_iteration",type=int,default=1000,help="Maximum number of iterations for energy minimization (default: 1000).")
    parser.add_argument("--flexibility_method",type=str,choices=["ANM", "GNM"],default="ANM",help="Method for RMSF calculation: ANM or GNM (default: ANM).")
    parser.add_argument("--flexibility_cutoff",type=float,default=15.0,help="Distance cutoff used to determine the residue connection in ProDy (default: 15.0).")
    parser.add_argument("--flexibility_n_modes",type=int,default=20,help="Number of low-frequency normal modes used for RMSF calculation (default: 20).")
    parser.add_argument("--disorder_window_size",type=int,default=11,help="Sliding window size for FoldIndex-like disorder score calculation (default: 11).")
    parser.add_argument("--disorder_min_region_length",type=int,default=5,help="Minimum number of consecutive residues required to define a disordered region (default: 5).")
    parser.add_argument("--embedding_model_name",type=str,choices=["esm2_t6_8M_UR50D", "esm2_t12_35M_UR50D", "esm2_t30_150M_UR50D"],default="esm2_t6_8M_UR50D",help="Model for embedding generation: esm2_t6_8M_UR50D, esm2_t12_35M_UR50D, esm2_t30_150M_UR50D.")
    parser.add_argument("--pocket_min_rad",type=float,default=1.8,help="Minimum probe radius used by PyVOL for cavity detection (default: 1.8).")
    parser.add_argument("--pocket_max_rad",type=float,default=6.2,help="Maximum probe radius used by PyVOL for cavity detection (default: 6.2).")
    parser.add_argument("--pocket_min_volume",type=int,default=50,help="Minimum pocket volume threshold (default: 50).")
    parser.add_argument("--substrate_max_synonyms",type=int,default=20,help="Maximum number of substrate synonyms retried when fetching SMILES from a substrate name (default: 20).")
    parser.add_argument("--substrate_fp_radius",type=int,default=2,help="Radius used for Morgan fingerprint generation (default: 2).")
    parser.add_argument("--substrate_n_bits",type=int,default=512,help="Bit size of the Morgan fingerprint vector (default: 512).")
    parser.add_argument("--substrate_num_confs",type=int,default=5,help="Maximum number of 3D structures to generate for each substrate (default: 5).")
    parser.add_argument("--substrate_prune_rms",type=float,default=0.5,help="RMS threshold used to prune highly similar conformers during 3D conformer generation (default: 0.5).")
    parser.add_argument("--dock_max_attempt_num",type=int,default=20,help="Maximum number of docking attempts (default: 20).")
    parser.add_argument("--dock_no_early_stop", action="store_false", dest="dock_early_stop",help="Disable stopping immediately after the first successful docking result (default: enabled).")
    parser.set_defaults(dock_early_stop=True)
    parser.add_argument("--dock_exhaustiveness",type=int,default=16,help="Exhaustiveness of AutoDock Vina search (default: 16).")
    parser.add_argument("--dock_cpu",type=int,default=0,help="Number of CPUs used by AutoDock Vina (default: 0).")
    parser.add_argument("--hbond_bonded_h_min_distance",type=float,default=0.8,help="Minimum bonded heavy atom-hydrogen distance used for hydrogen bond donor detection (default: 0.8).")
    parser.add_argument("--hbond_bonded_h_max_distance",type=float,default=1.3,help="Maximum bonded heavy atom-hydrogen distance used for hydrogen bond donor detection (default: 1.3).")
    parser.add_argument("--hbond_da_max_distance",type=float,default=3.9,help="Maximum donor-acceptor distance cutoff for hydrogen bond detection (default: 3.9).")
    parser.add_argument("--hbond_ha_max_distance",type=float,default=2.5,help="Maximum hydrogen-acceptor distance cutoff for hydrogen bond detection (default: 2.5).")
    parser.add_argument("--hbond_angle",type=float,default=90.0,help="Minimum donor-hydrogen-acceptor angle cutoff for hydrogen bond detection (default: 90.0).")
    parser.add_argument("--ionic_distance_cutoff",type=float,default=4.0,help="Maximum distance cutoff for ionic bond detection (default: 4.0).")
    parser.add_argument("--vdw_mu",type=float,default=0.01,help="Mu parameter used in van der Waals interaction detection (default: 0.01).")
    parser.add_argument("--ppstack_center_distance_cutoff",type=float,default=6.5,help="Maximum ring-center distance cutoff for pi-pi stacking detection (default: 6.5).")
    parser.add_argument("--pication_distance_cutoff",type=float,default=5.0,help="Maximum ring-cation distance cutoff for pi-cation interaction detection (default: 5.0).")
    parser.add_argument("--pication_angle_cutoff",type=float,default=45.0,help="Maximum angle cutoff for pi-cation interaction detection (default: 45.0).")
    parser.add_argument("--ssbond_max_distance",type=float,default=2.5,help="Maximum sulfur-sulfur distance cutoff for disulfide bond detection (default: 2.5).")


    parser.set_defaults(func=run_batch)


def run_batch(args: Namespace) -> None:
    run_batch_service(
        cleaned_input_path=args.cleaned_input_path,
        input_msa=args.input_msa,
        substrate_names=args.substrate_names,
        output_dir=args.output_dir,
        save_extra_outputs=args.save_extra_outputs,
        cutoff_area=args.hydrocluster_cutoff,
        minimize_energy=args.minimize_energy,
        minimization_iteration=args.energy_minimization_iteration,
        flexibility_cutoff=args.flexibility_cutoff,
        n_modes=args.flexibility_n_modes,
        flexibility_method=args.flexibility_method,
        window_size=args.disorder_window_size,
        min_region_length=args.disorder_min_region_length,
        embedding_model_name=args.embedding_model_name,
        pocket_min_rad=args.pocket_min_rad,
        pocket_max_rad=args.pocket_max_rad,
        pocket_min_volume=args.pocket_min_volume,
        max_synonyms=args.substrate_max_synonyms,
        fp_radius=args.substrate_fp_radius,
        n_bits=args.substrate_n_bits,
        num_confs=args.substrate_num_confs,
        prune_rms=args.substrate_prune_rms,
        max_docking_attempt_num=args.dock_max_attempt_num,
        early_stop=args.dock_early_stop,
        exhaustiveness=args.dock_exhaustiveness,
        cpu=args.dock_cpu,
        dock_min_rad=args.pocket_min_rad,
        dock_max_rad=args.pocket_max_rad,
        dock_min_volume=args.pocket_min_volume,
        bonded_h_min_distance_A=args.hbond_bonded_h_min_distance,
        bonded_h_max_distance_A=args.hbond_bonded_h_max_distance,
        da_max_distance_A=args.hbond_da_max_distance,
        ha_max_distance_A=args.hbond_ha_max_distance,
        dha_min_angle_deg=args.hbond_angle,
        ionic_distance_cutoff_A=args.ionic_distance_cutoff,
        mu=args.vdw_mu,
        ring_center_distance_cutoff_A=args.ppstack_center_distance_cutoff,
        ring_cation_distance_cutoff_A=args.pication_distance_cutoff,
        ring_cation_angle_cutoff_deg=args.pication_angle_cutoff,
        ss_max_distance_A=args.ssbond_max_distance,
    )

# ==============================
# Command: enzywizard-batch
# ==============================

# brief introduction:
'''
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
'''

# example usage:
'''
Example command:

enzywizard-batch -i examples/input/cleaned_3GP6.cif -m examples/input/jhmm_3GP6.sto -s glucose,fructose -o examples/output/
'''

# input parameters:
'''
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
'''

# output content:
'''
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
'''

# Process:
'''
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
'''

# dependencies:
'''
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
'''

# references:
'''
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
'''