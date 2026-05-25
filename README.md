[![DOI](https://zenodo.org/badge/1219039183.svg)](https://doi.org/10.5281/zenodo.19709395)
# Command: enzywizard-batch

EnzyWizard-Batch is a command-line tool for running a complete EnzyWizard
analysis workflow from a cleaned protein structure and a matched MSA file.
It performs multiple EnzyWizard modules, including residue property analysis, 
hydrophobic cluster detection, energy evaluation, flexibility analysis, 
disordered region detection, conservation analysis, residue embedding generation, 
binding pocket detection, optional substrate
feature generation, optional enzyme-substrate docking, molecular interaction calculation,
and final graph integration.
If substrate names or SMILES strings are provided, the full enzyme-substrate
workflow will be executed, including substrate preparation, docking,
enzyme-substrate molecular interaction detection, and strict graph integration.
If no substrate input is provided, the program generates a protein-only integrated graph 
based on residue-level features and intra-enzyme molecular interactions.
The final output is an integrated graph dataset that can be directly used for
graph-based analysis, machine learning, and enzyme function studies.


# example usage:

Example command:

enzywizard-batch -i examples/input/cleaned_3GP6.cif -m examples/input/jhmm_3GP6.sto -s "glucose;fructose" -o examples/output/


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

Multiple substrates should be separated by ';'.

If provided, the following additional workflows will be executed:
- substrate feature generation
- substrate 3D structure generation
- enzyme-substrate docking
- enzyme-substrate molecular interaction calculation
- strict graph integration

If substrate generation or docking fails, these additional workflows are skipped
for the final integration and the program continues with the protein-only route.

If not provided, substrate, docking, and enzyme-substrate molecular interaction steps
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
files, docked substrate files, and enzyme-substrate complex files may be saved.

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
Distance cutoff used to determine residue-residue connections in ProDy.
Default: 15.0.

--flexibility_n_modes
Optional.
Number of low-frequency normal modes used for RMSF calculation.
Default: 20.

--disorder_window_size
Optional.
Sliding window size for FoldIndex-like disordered region score calculation.
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
Minimum probe radius used by PyVOL for binding pocket detection.
Default: 1.8.

--pocket_max_rad
Optional.
Maximum probe radius used by PyVOL for binding pocket detection.
Default: 6.2.

--pocket_min_volume
Optional.
Minimum binding pocket volume threshold.
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

--dock_catalytic_residue
Optional.
Cleaned protein residue index used as the docking box center.

Example:
  121

This parameter is an integer residue index from the cleaned single-chain protein
structure. The CA atom coordinate of this residue is used as the docking box
center. When this parameter is provided, --dock_box_size is required.
This parameter cannot be used together with --dock_catalytic_site_coord.
When this parameter is provided, the docking step does not use PyVOL pocket
detection or the global docking box fallback to build Vina docking boxes.

--dock_catalytic_site_coord
Optional.
Catalytic site center coordinate separated by ','.

Example:
  12.5,8.0,-3.2

When this parameter is provided, --dock_box_size is required.
This parameter cannot be used together with --dock_catalytic_residue.
When this parameter is provided, the docking step does not use PyVOL pocket
detection or the global docking box fallback to build Vina docking boxes.

--dock_box_size
Optional.
Docking box size separated by ','.

Example:
  20,20,20

This parameter is required when --dock_catalytic_residue or
--dock_catalytic_site_coord is provided. All three values must be positive
numbers.

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

   The report follows the JSON schema file:
   - resources/enzywizard_integrate_report_schema.json

   The JSON report contains the following fields:

   - "report_type"
     - Data type: string
     - Expected value: "enzywizard_integrate"
     - Description: The field 'report_type' indicates the type ('type': http://purl.org/dc/terms/type) of report ('report': http://purl.obolibrary.org/obo/IAO_0000088) generated by the EnzyWizard-Integrate software ('software': https://schema.org/SoftwareApplication).

   - "overall_statistics"
     - Data type: object
     - Description: The field 'overall_statistics' indicates the overall summary statistics ('statistics': http://purl.obolibrary.org/obo/STATO_0000039) integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088).

     The "overall_statistics" object may contain:

     - "residue_name_count"
       - Data type: array
       - Description: The field 'residue_name_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue names ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name), represented in the order of one-letter amino acid codes ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html).

     - "residue_chemical_classification_count"
       - Data type: array
       - Description: The field 'residue_chemical_classification_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue chemical classifications ('classification': http://purl.obolibrary.org/obo/NCIT_C25161).

     - "residue_secondary_structure_count"
       - Data type: array
       - Description: The field 'residue_secondary_structure_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of residue secondary structures ('secondary structure': http://edamontology.org/operation_1847), represented using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "hydrophobic_cluster_count"
       - Data type: integer
       - Description: The field 'hydrophobic_cluster_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "max_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'max_hydrophobic_cluster_area' indicates the maximum area ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "total_hydrophobic_cluster_area"
       - Data type: number
       - Description: The field 'total_hydrophobic_cluster_area' indicates the total area ('area': http://purl.obolibrary.org/obo/PATO_0001323) of hydrophobic clusters ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "disordered_region_count"
       - Data type: integer
       - Description: The field 'disordered_region_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

     - "max_disordered_region_length"
       - Data type: integer
       - Description: The field 'max_disordered_region_length' indicates the maximum sequence length ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

     - "total_disordered_region_length"
       - Data type: integer
       - Description: The field 'total_disordered_region_length' indicates the total sequence length ('sequence length': http://edamontology.org/data_1249) of intrinsically disordered regions ('intrinsically disordered region': https://disprot.org/ontology).

     - "binding_pocket_count"
       - Data type: integer
       - Description: The field 'binding_pocket_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/pocket_specification.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL).

     - "max_binding_pocket_volume"
       - Data type: number
       - Description: The field 'max_binding_pocket_volume' indicates the maximum volume ('maximum': http://purl.obolibrary.org/obo/STATO_0000150; 'volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL).

     - "total_binding_pocket_volume"
       - Data type: number
       - Description: The field 'total_binding_pocket_volume' indicates the total volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of binding pockets ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html) calculated by PyVOL software ('PyVOL': https://bio.tools/PyVOL).

     - "total_potential_energy"
       - Data type: number
       - Description: The field 'total_potential_energy' indicates the total potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) calculated from the protein structure ('protein structure': http://edamontology.org/data_1537).

     - "harmonic_bond_potential_energy"
       - Data type: number
       - Description: The field 'harmonic_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic bond force term ('harmonic bond force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicbondforce).

     - "harmonic_angle_potential_energy"
       - Data type: number
       - Description: The field 'harmonic_angle_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the harmonic angle force term ('harmonic angle force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#harmonicangleforce).

     - "custom_bond_potential_energy"
       - Data type: number
       - Description: The field 'custom_bond_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom bond force term ('custom bond force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#custombondforce).

     - "custom_torsion_potential_energy"
       - Data type: number
       - Description: The field 'custom_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom torsion force term ('custom torsion force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customtorsionforce).

     - "custom_nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'custom_nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the custom nonbonded force term ('custom nonbonded force term': https://docs.openmm.org/latest/userguide/theory/03_custom_forces.html#customnonbondedforce).

     - "nonbonded_potential_energy"
       - Data type: number
       - Description: The field 'nonbonded_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the nonbonded force term ('nonbonded force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#nonbondedforce).

     - "periodic_torsion_potential_energy"
       - Data type: number
       - Description: The field 'periodic_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the periodic torsion force term ('periodic torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#periodictorsionforce).

     - "cmap_torsion_potential_energy"
       - Data type: number
       - Description: The field 'cmap_torsion_potential_energy' indicates the potential energy ('potential energy': https://goldbook.iupac.org/terms/view/P04778) contributed by the CMAP torsion force term ('CMAP torsion force term': https://docs.openmm.org/latest/userguide/theory/02_standard_forces.html#cmaptorsionforce).

     - "enzyme_substrate_binding_affinity"
       - Data type: number
       - Description: The field 'enzyme_substrate_binding_affinity' indicates the predicted binding affinity ('binding affinity': https://vina.scripps.edu/manual/#output) calculated by AutoDock Vina software ('AutoDock Vina': https://bio.tools/autodock_vina) from docking ('docking': https://goldbook.iupac.org/terms/view/11437) of the enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

     - "hydrogen_bond_count"
       - Data type: integer
       - Description: The field 'hydrogen_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of hydrogen bonds ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899).

     - "ionic_bond_count"
       - Data type: integer
       - Description: The field 'ionic_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of ionic bonds ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058).

     - "van_der_waals_contact_count"
       - Data type: integer
       - Description: The field 'van_der_waals_contact_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of van der Waals contacts ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597).

     - "pi_pi_stacking_count"
       - Data type: integer
       - Description: The field 'pi_pi_stacking_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-pi stacking interactions ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861).

     - "pi_cation_interaction_count"
       - Data type: integer
       - Description: The field 'pi_cation_interaction_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of pi-cation interactions ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154).

     - "disulfide_bond_count"
       - Data type: integer
       - Description: The field 'disulfide_bond_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of disulfide bonds ('disulfide bond': https://www.uniprot.org/help/disulfid).

   - "integrated_graph"
     - Data type: array
     - Description: The field 'integrated_graph' indicates the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/) containing molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between source nodes and target nodes, and isolated nodes ('isolated node': https://mathworld.wolfram.com/IsolatedPoint.html) integrated from EnzyWizard reports ('report': http://purl.obolibrary.org/obo/IAO_0000088).

     Each item in "integrated_graph" is one of the following entry objects:

     Interaction graph entry:

     - "molecular_interaction"
       - Data type: object
       - Description: The field 'molecular_interaction' indicates a molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

       The "molecular_interaction" object contains:

       - "molecular_interaction_type"
         - Data type: string
         - Description: The field 'molecular_interaction_type' indicates the type ('interaction type': http://purl.obolibrary.org/obo/MI_0190) of molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI), using RING interaction codes ('RING interaction type': https://ring.biocomputingup.it/help/interactions): hydrogen bond ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899; value: HBOND), ionic bond ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058; value: IONIC), van der Waals contact ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597; value: VDW), pi-pi stacking ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861; value: PIPISTACK), pi-cation interaction ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154; value: PICATION), and disulfide bond ('disulfide bond': https://www.uniprot.org/help/disulfid; value: SSBOND).

       - "molecular_interaction_one_hot_encoding"
         - Data type: array
         - Description: The field 'molecular_interaction_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the molecular interaction type ('interaction type': http://purl.obolibrary.org/obo/MI_0190).

       - "interaction_count"
         - Data type: integer
         - Description: The field 'interaction_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node.

     - "source_node"
       - Data type: object
       - Description: The field 'source_node' indicates the source node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) corresponding to a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

     - "target_node"
       - Data type: object
       - Description: The field 'target_node' indicates the target node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) corresponding to a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

     Isolated node graph entry:

     - "isolated_node"
       - Data type: object
       - Description: The field 'isolated_node' indicates an isolated residue node ('isolated point': https://mathworld.wolfram.com/IsolatedPoint.html; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) or a substrate node ('substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph.

     Node objects used in "source_node", "target_node", and "isolated_node" may contain residue node fields or substrate node fields.

     Residue node fields:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     - "node_type"
       - Data type: string
       - Expected value: "residue"
       - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'residue' indicating a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "node_type_one_hot_encoding"
       - Data type: array
       - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

     - "residue_index"
       - Data type: integer
       - Description: The field 'residue_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_name"
       - Data type: string
       - Description: The field 'residue_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using one-letter code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

     - "residue_name_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name).

     - "residue_alpha_carbon_coordinate"
       - Data type: array
       - Description: The field 'residue_alpha_carbon_coordinate' indicates the three-dimensional coordinate ('coordinate': http://purl.obolibrary.org/obo/NCIT_C44477) of the alpha carbon atom ('alpha carbon': https://www.rcsb.org/docs/general-help/glossary; 'atom': http://purl.obolibrary.org/obo/CHMO_0001075) in the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_chemical_classification"
       - Data type: string
       - Description: The field 'residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_chemical_classification_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_chemical_classification_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_secondary_structure"
       - Data type: string
       - Description: The field 'residue_secondary_structure' indicates the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

     - "residue_secondary_structure_one_hot_encoding"
       - Data type: array
       - Description: The field 'residue_secondary_structure_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue secondary structure ('secondary structure': http://edamontology.org/operation_1847).

     - "residue_relative_solvent_accessibility"
       - Data type: number
       - Description: The field 'residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_backbone_phi_angle"
       - Data type: number
       - Description: The field 'residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

     - "residue_backbone_psi_angle"
       - Data type: number
       - Description: The field 'residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

     - "residue_net_charge"
       - Data type: number
       - Description: The field 'residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_pka"
       - Data type: number
       - Description: The field 'residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_volume"
       - Data type: number
       - Description: The field 'residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_hydrophobicity"
       - Data type: number
       - Description: The field 'residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_molecular_weight"
       - Data type: number
       - Description: The field 'residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_isoelectric_point"
       - Data type: number
       - Description: The field 'residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_root_mean_square_fluctuation"
       - Data type: number
       - Description: The field 'residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_sequence_conservation_score"
       - Data type: number
       - Description: The field 'residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448; 'score': http://edamontology.org/data_1772) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

     - "residue_embedding"
       - Data type: array
       - Description: The field 'residue_embedding' indicates the embedding ('embedding': https://developers.google.com/machine-learning/crash-course/embeddings) generated by the ESM-2 protein language model ('ESM-2': https://docs.nvidia.com/bionemo-framework/2.0/models/esm2/; 'protein language model': https://synbiointel.com/glossary/protein-language-model/) for the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), represented as a numerical vector ('numerical vector': https://mathworld.wolfram.com/Vector.html).

     - "is_in_hydrophobic_cluster"
       - Data type: boolean
       - Description: The field 'is_in_hydrophobic_cluster' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a hydrophobic cluster ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

     - "is_in_disordered_region"
       - Data type: boolean
       - Description: The field 'is_in_disordered_region' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in an intrinsically disordered region ('intrinsically disordered region': https://disprot.org/ontology).

     - "is_in_binding_pocket"
       - Data type: boolean
       - Description: The field 'is_in_binding_pocket' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a binding pocket ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html).

     Substrate node fields:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     - "node_type"
       - Data type: string
       - Expected value: "substrate"
       - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'substrate' indicating a substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "node_type_one_hot_encoding"
       - Data type: array
       - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

     - "substrate_index"
       - Data type: integer
       - Description: The field 'substrate_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_name"
       - Data type: string
       - Description: The field 'substrate_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_smiles"
       - Data type: string
       - Description: The field 'substrate_smiles' indicates the SMILES representation ('SMILES': https://opensmiles.org/opensmiles.html) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_atom_count"
       - Data type: integer
       - Description: The field 'substrate_atom_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of atoms ('atom': https://goldbook.iupac.org/terms/view/A00493) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_molecular_weight"
       - Data type: number
       - Description: The field 'substrate_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "substrate_logp"
       - Data type: number
       - Description: The field 'substrate_logp' indicates the calculated logP value ('LogP': https://doktormike.gitlab.io/posts/navigating-logp-logd-pka-and-logs-a-physicists-guide/) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

     - "docked_substrate_center_coordinate"
       - Data type: array
       - Description: The field 'docked_substrate_center_coordinate' indicates the center coordinate ('coordinate': https://mathworld.wolfram.com/Coordinates.html) of the docked substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

     - "substrate_fingerprint_encoding"
       - Data type: array
       - Description: The field 'substrate_fingerprint_encoding' indicates the molecular fingerprint encoding ('molecular fingerprint': https://www.rdkit.org/docs/GettingStartedInPython.html#fingerprinting-and-molecular-similarity) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

2. A node-only JSON file
   - integrate_nodes_{protein_name}.json

   The node-only JSON file follows the JSON schema file:
   - resources/integrated_graph_nodes_schema.json

   The node-only JSON file contains an array of integrated graph node records.

   Each item is one of the following node objects:

   Residue node object:

   - Data type: object
   - Description: This object indicates a residue node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node; 'residue': http://purl.obolibrary.org/obo/GENO_0000782) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   The residue node object contains:

   - "node_index"
     - Data type: integer
     - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   - "node_type"
     - Data type: string
     - Expected value: "residue"
     - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'residue' indicating a residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "node_type_one_hot_encoding"
     - Data type: array
     - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

   - "residue_index"
     - Data type: integer
     - Description: The field 'residue_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_name"
     - Data type: string
     - Description: The field 'residue_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using one-letter code ('one-letter code': https://iupac.qmul.ac.uk/AminoAcid/A2021.html) to represent.

   - "residue_name_one_hot_encoding"
     - Data type: array
     - Description: The field 'residue_name_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue name ('residue': http://purl.obolibrary.org/obo/GENO_0000782; 'name': http://xmlns.com/foaf/0.1/name).

   - "residue_alpha_carbon_coordinate"
     - Data type: array
     - Description: The field 'residue_alpha_carbon_coordinate' indicates the three-dimensional coordinate ('coordinate': http://purl.obolibrary.org/obo/NCIT_C44477) of the alpha carbon atom ('alpha carbon': https://www.rcsb.org/docs/general-help/glossary; 'atom': http://purl.obolibrary.org/obo/CHMO_0001075) in the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_chemical_classification"
     - Data type: string
     - Description: The field 'residue_chemical_classification' indicates the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_chemical_classification_one_hot_encoding"
     - Data type: array
     - Description: The field 'residue_chemical_classification_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the chemical classification ('classification': http://purl.obolibrary.org/obo/NCIT_C25161) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_secondary_structure"
     - Data type: string
     - Description: The field 'residue_secondary_structure' indicates the secondary structure ('secondary structure': http://edamontology.org/operation_1847) assigned to the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), using DSSP secondary-structure codes ('DSSP': https://manual.gromacs.org/current/onlinehelp/gmx-dssp.html).

   - "residue_secondary_structure_one_hot_encoding"
     - Data type: array
     - Description: The field 'residue_secondary_structure_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the residue secondary structure ('secondary structure': http://edamontology.org/operation_1847).

   - "residue_relative_solvent_accessibility"
     - Data type: number
     - Description: The field 'residue_relative_solvent_accessibility' indicates the relative solvent accessibility ('solvent accessibility': http://edamontology.org/data_1542) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_backbone_phi_angle"
     - Data type: number
     - Description: The field 'residue_backbone_phi_angle' indicates the backbone phi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

   - "residue_backbone_psi_angle"
     - Data type: number
     - Description: The field 'residue_backbone_psi_angle' indicates the backbone psi torsion angle ('torsion angle': https://goldbook.iupac.org/terms/view/T06406) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) in the protein backbone ('protein backbone': http://edamontology.org/operation_1825).

   - "residue_net_charge"
     - Data type: number
     - Description: The field 'residue_net_charge' indicates the net electric charge ('net electric charge': https://goldbook.iupac.org/terms/view/N04111) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_pka"
     - Data type: number
     - Description: The field 'residue_pka' indicates the pKa value ('pKa': https://goldbook.iupac.org/terms/view/15441) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_volume"
     - Data type: number
     - Description: The field 'residue_volume' indicates the volume ('volume': http://purl.obolibrary.org/obo/PATO_0000918) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_hydrophobicity"
     - Data type: number
     - Description: The field 'residue_hydrophobicity' indicates the hydrophobicity ('hydrophobicity': https://goldbook.iupac.org/terms/view/HT06964) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_molecular_weight"
     - Data type: number
     - Description: The field 'residue_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_isoelectric_point"
     - Data type: number
     - Description: The field 'residue_isoelectric_point' indicates the isoelectric point ('isoelectric point': https://goldbook.iupac.org/terms/view/I03275) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_root_mean_square_fluctuation"
     - Data type: number
     - Description: The field 'residue_root_mean_square_fluctuation' indicates the root mean square fluctuation ('root mean square fluctuation': https://manual.gromacs.org/current/onlinehelp/gmx-rmsf.html) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_sequence_conservation_score"
     - Data type: number
     - Description: The field 'residue_sequence_conservation_score' indicates the sequence conservation score ('sequence conservation': http://edamontology.org/operation_0448; 'score': http://edamontology.org/data_1772) of the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782).

   - "residue_embedding"
     - Data type: array
     - Description: The field 'residue_embedding' indicates the embedding ('embedding': https://developers.google.com/machine-learning/crash-course/embeddings) generated by the ESM-2 protein language model ('ESM-2': https://docs.nvidia.com/bionemo-framework/2.0/models/esm2/; 'protein language model': https://synbiointel.com/glossary/protein-language-model/) for the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782), represented as a numerical vector ('numerical vector': https://mathworld.wolfram.com/Vector.html).

   - "is_in_hydrophobic_cluster"
     - Data type: boolean
     - Description: The field 'is_in_hydrophobic_cluster' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a hydrophobic cluster ('hydrophobic cluster': https://proteintools.uni-bayreuth.de/clusters/).

   - "is_in_disordered_region"
     - Data type: boolean
     - Description: The field 'is_in_disordered_region' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in an intrinsically disordered region ('intrinsically disordered region': https://disprot.org/ontology).

   - "is_in_binding_pocket"
     - Data type: boolean
     - Description: The field 'is_in_binding_pocket' indicates whether the residue ('residue': http://purl.obolibrary.org/obo/GENO_0000782) is included in a binding pocket ('binding pocket': https://schlessinger-lab.github.io/pyvol/index.html).

   Substrate node object:

   - Data type: object
   - Description: This object indicates a substrate node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node; 'substrate': https://purl.dsmz.de/schema/Substrate) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   The substrate node object contains:

   - "node_index"
     - Data type: integer
     - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   - "node_type"
     - Data type: string
     - Expected value: "substrate"
     - Description: The field 'node_type' indicates the type ('type': http://purl.org/dc/terms/type) of node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node), with value 'substrate' indicating a substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "node_type_one_hot_encoding"
     - Data type: array
     - Description: The field 'node_type_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the node type ('type': http://purl.org/dc/terms/type).

   - "substrate_index"
     - Data type: integer
     - Description: The field 'substrate_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_name"
     - Data type: string
     - Description: The field 'substrate_name' indicates the name ('name': http://xmlns.com/foaf/0.1/name) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_smiles"
     - Data type: string
     - Description: The field 'substrate_smiles' indicates the SMILES representation ('SMILES': https://opensmiles.org/opensmiles.html) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_atom_count"
     - Data type: integer
     - Description: The field 'substrate_atom_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of atoms ('atom': https://goldbook.iupac.org/terms/view/A00493) in the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_molecular_weight"
     - Data type: number
     - Description: The field 'substrate_molecular_weight' indicates the molecular weight ('molecular weight': https://goldbook.iupac.org/terms/view/R05271) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "substrate_logp"
     - Data type: number
     - Description: The field 'substrate_logp' indicates the calculated logP value ('LogP': https://doktormike.gitlab.io/posts/navigating-logp-logd-pka-and-logs-a-physicists-guide/) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate).

   - "docked_substrate_center_coordinate"
     - Data type: array
     - Description: The field 'docked_substrate_center_coordinate' indicates the center coordinate ('coordinate': https://mathworld.wolfram.com/Coordinates.html) of the docked substrate ('substrate': https://purl.dsmz.de/schema/Substrate) in the enzyme-substrate complex ('enzyme': https://purl.dsmz.de/schema/Enzyme; 'substrate': https://purl.dsmz.de/schema/Substrate; 'complex': https://goldbook.iupac.org/terms/view/C01203).

   - "substrate_fingerprint_encoding"
     - Data type: array
     - Description: The field 'substrate_fingerprint_encoding' indicates the molecular fingerprint encoding ('molecular fingerprint': https://www.rdkit.org/docs/GettingStartedInPython.html#fingerprinting-and-molecular-similarity) of the substrate ('substrate': https://purl.dsmz.de/schema/Substrate) calculated by RDKit software ('RDKit': https://www.rdkit.org/docs/index.html).

3. An edge-only JSON file
   - integrate_edges_{protein_name}.json

   The edge-only JSON file follows the JSON schema file:
   - resources/integrated_graph_edges_schema.json

   The edge-only JSON file contains an array of integrated graph edge records.

   Each item is an object containing:

   - "molecular_interaction"
     - Data type: object
     - Description: The field 'molecular_interaction' indicates a molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

     The "molecular_interaction" object contains:

     - "molecular_interaction_type"
       - Data type: string
       - Description: The field 'molecular_interaction_type' indicates the type ('interaction type': http://purl.obolibrary.org/obo/MI_0190) of molecular interaction ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI), using RING interaction codes ('RING interaction type': https://ring.biocomputingup.it/help/interactions): hydrogen bond ('hydrogen bond': https://goldbook.iupac.org/terms/view/H02899; value: HBOND), ionic bond ('ionic bond': https://goldbook.iupac.org/terms/view/IT07058; value: IONIC), van der Waals contact ('van der Waals forces': https://goldbook.iupac.org/terms/view/V06597; value: VDW), pi-pi stacking ('pi-pi stacking': https://goldbook.iupac.org/terms/view/13861; value: PIPISTACK), pi-cation interaction ('cation-pi interaction': https://goldbook.iupac.org/terms/view/08154; value: PICATION), and disulfide bond ('disulfide bond': https://www.uniprot.org/help/disulfid; value: SSBOND).

     - "molecular_interaction_one_hot_encoding"
       - Data type: array
       - Description: The field 'molecular_interaction_one_hot_encoding' indicates the one-hot encoding ('one-hot encoding': https://developers.google.com/machine-learning/glossary#one-hot_encoding) of the molecular interaction type ('interaction type': http://purl.obolibrary.org/obo/MI_0190).

     - "interaction_count"
       - Data type: integer
       - Description: The field 'interaction_count' indicates the count ('count': http://purl.obolibrary.org/obo/STATO_0000047) of molecular interactions ('molecular interaction': https://bioportal.bioontology.org/ontologies/MI) between the source node and the target node.

   - "source_node"
     - Data type: object
     - Description: The field 'source_node' indicates the source node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph.

     The "source_node" object contains:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).

   - "target_node"
     - Data type: object
     - Description: The field 'target_node' indicates the target node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph.

     The "target_node" object contains:

     - "node_index"
       - Data type: integer
       - Description: The field 'node_index' indicates the index ('index': http://purl.obolibrary.org/obo/NCIT_C25390) of the node ('node': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/#graphdb-node) in the integrated graph ('graph': https://neo4j.com/docs/getting-started/appendix/graphdb-concepts/).


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
   - Check flexibility and disordered region parameters.
   - Check binding pocket detection parameters.
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
   - Build an identity residue mapping between old residues and new residues.
   - Generate an enzywizard_clean-style report for downstream integration.

7. Prepare OpenMM and sequence objects
   - Convert the cleaned structure into an OpenMM-compatible structure.
   - Build an OpenMM Modeller object.
   - Extract the cleaned protein sequence.

8. Run residue property analysis
   - Load DSSP information.
   - Calculate residue-level properties.
   - Generate the enzywizard_aaprops report.

9. Run hydrophobic cluster analysis
   - Detect hydrophobic clusters.
   - Generate the enzywizard_hydrocluster report.

10. Run energy analysis
   - Optionally minimize the protein structure.
   - Calculate energy terms using the selected force field.
   - Generate the enzywizard_energy report.

11. Run flexibility analysis
   - Calculate residue-level RMSF using ANM or GNM.
   - Generate the enzywizard_flexibility report.

12. Run disordered region analysis
   - Calculate FoldIndex-like disordered region scores.
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

15. Run binding pocket analysis
   - Detect binding pockets using PyVOL.
   - Generate the enzywizard_pocket report.

16. Optionally run substrate analysis
   - Parse substrate names or SMILES strings.
   - Retrieve or complete SMILES information.
   - Generate substrate fingerprints and 3D conformers.
   - Save substrate structure files.
   - Generate the enzywizard_substrate report.
   - If substrate parsing, SMILES completion, conformer generation, structure saving,
     or report generation fails, log a warning and continue with the protein-only route.

17. Optionally run docking analysis
   - If --dock_catalytic_residue is provided, use the CA coordinate of that cleaned protein residue as the docking box center.
   - If --dock_catalytic_site_coord is provided, use that coordinate as the docking box center.
   - In either manual docking box mode, use --dock_box_size as the docking box size and skip docking-specific PyVOL pocket detection and the global docking box fallback.
   - If no manual docking box parameter is provided, dock generated substrate structures into automatically generated pocket and global fallback docking boxes.
   - Save docking results.
   - Generate the enzywizard_dock report.
   - Load docked substrate structures for molecular interaction analysis.
   - If docking, dock report generation, or docked substrate loading fails,
     log a warning and continue with the protein-only route.

18. Run molecular interaction analysis
   - If substrate input is provided and docking completed, filter valid docked substrates.
   - Calculate intra-enzyme molecular interactions.
   - Calculate enzyme-substrate molecular interactions when valid docked substrates exist.
   - Summarize molecular interaction counts.
   - Generate the enzywizard_interaction report.

19. Run graph integration
   - Collect all generated reports into report_dict.
   - Use strict integration when substrate input is provided and substrate/docking
     workflows complete successfully.
   - Use non-strict integration when no substrate input is provided or the workflow
     falls back to the protein-only route.
   - Merge residue-level, substrate-level, and molecular interaction-level information
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