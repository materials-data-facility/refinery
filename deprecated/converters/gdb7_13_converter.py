import json
import sys
import os
from tqdm import tqdm
from mdf_forge.toolbox import find_files
from mdf_refinery.parsers.ase_parser import parse_ase
from mdf_refinery.validator import Validator

# VERSION 0.3.0

# This is the GDB7-13(QM7b) dataset: Machine learning of molecular electronic properties in chemical compound space
# Arguments:
#   input_path (string): The file or directory where the data resides.
#       NOTE: Do not hard-code the path to the data in the converter (the filename can be hard-coded, though). The converter should be portable.
#   metadata (string or dict): The path to the JSON dataset metadata file, a dict or json.dumps string containing the dataset metadata, or None to specify the metadata here. Default None.
#   verbose (bool): Should the script print status messages to standard output? Default False.
#       NOTE: The converter should have NO output if verbose is False, unless there is an error.
def convert(input_path, metadata=None, verbose=False):
    if verbose:
        print("Begin converting")

    # Collect the metadata
    if not metadata:
        dataset_metadata = {
            "mdf": {
                "title": "Machine learning of molecular electronic properties in chemical compound space",
                "acl": ['public'],
                "source_name": "gdb7_13",
                "citation": ["Gr\'egoire Montavon, Matthias Rupp, Vivekanand Gobre, Alvaro Vazquez-Mayagoitia, Katja Hansen, Alexandre Tkatchenko, Klaus-Robert M\"uller, O. Anatole von Lilienfeld: Machine learning of molecular electronic properties in chemical compound space, New Journal of Physics, 15(9): 095003, IOP Publishing, 2013.DOI: 10.1088/1367-2630/15/9/095003"],
                "data_contact": {
    
                    "given_name": "O. Anatole",
                    "family_name": "von Lilienfeld",
    
                    "email": "anatole@alcf.anl.gov",
                    "institution": "Argonne National Laboratory",
                    },
    
                "author": [{
                    
                    "given_name": "O. Anatole",
                    "family_name": "von Lilienfeld",
                    
                    "email": "anatole@alcf.anl.gov",
                    "instituition": "Argonne National Laboratory"
                    
                    },
                    {
                        
                    "given_name": "Grégoire",
                    "family_name": "Montavon",
                    
                    "institution": "Technical University of Berlin"
                    
                    },
                    {
                    
                    "given_name": "Matthias",
                    "family_name": "Rupp",
                    
                    "instituition": "Institute of Pharmaceutical Sciences, ETH Zurich",
                    
                    },
                    {
                    
                    "given_name": "Vivekanand",
                    "family_name": "Gobre",
                    
                    "instituition": "Fritz-Haber-Institut der Max-Planck-Gesellschaft",
                    
                    },
                    {
                    
                    "given_name": "Alvaro",
                    "family_name": "Vazquez-Mayagoitia",
                    
                    "instituition": "Argonne National Laboratory",
                    
                    },
                    {
                    
                    "given_name": "Katja",
                    "family_name": "Hansen",
                    
                    "instituition": "Fritz-Haber-Institut der Max-Planck-Gesellschaft",
                    
                    },
                    {
                    
                    "given_name": "Alexandre",
                    "family_name": "Tkatchenko",
                    
                    "email": "tkatchen@fhi-berlin.mpg.de",
                    "instituition": "Fritz-Haber-Institut der Max-Planck-Gesellschaft, Pohang University of Science and Technology",
                    
                    },
                    {
                    
                    "given_name": "Klaus-Robert",
                    "family_name": "Müller",
                    
                    "email": "klaus-robert.mueller@tu-berlin.de",
                    "instituition": "Technical University of Berlin, Korea University",
                    
                    }],
    
                "license": "https://creativecommons.org/licenses/by/3.0/",
    
                "collection": "gdb7_13",
    #            "tags": ,
    
                "description": "7k small organic molecules, in their ground state, 14 combinations of properties and theory levels. 7,211 small organic molecules composed of H, C, N, O, S, Cl, saturated with H, and up to 7 non-H atoms. Molecules relaxed using DFT with PBE functional. Properties are atomization energy (DFT/PBE0), averaged polarizability (DFT/PBE0, SCS), HOMO and LUMO eigenvalues (GW, DFT/PBE0, ZINDO), and, ionization potential, electron affinity, first excitation energy, frequency of maximal absorption (all ZINDO).",
                "year": 2013,
    
                "links": {
    
                    "landing_page": "http://qmml.org/datasets.html#gdb7-13",
    
                    "publication": ["http://dx.doi.org/10.1088/1367-2630/15/9/095003"],
                    #"data_doi": "",
    
    #                "related_id": ,
    
                    "zip": {
                    
                        #"globus_endpoint": ,
                        "http_host": "http://qmml.org",
    
                        "path": "/Datasets/gdb7-13.zip",
                        }
                    },
    
    #            "mrr": ,
    
                "data_contributor": [{
                    "given_name": "Evan",
                    "family_name": "Pike",
                    "email": "dep78@uchicago.edu",
                    "institution": "The University of Chicago",
                    "github": "dep78"
                    }]
                }
            }
        
    elif type(metadata) is str:
        try:
            dataset_metadata = json.loads(metadata)
        except Exception:
            try:
                with open(metadata, 'r') as metadata_file:
                    dataset_metadata = json.load(metadata_file)
            except Exception as e:
                sys.exit("Error: Unable to read metadata: " + repr(e))
    elif type(metadata) is dict:
        dataset_metadata = metadata
    else:
        sys.exit("Error: Invalid metadata parameter")



    # Make a Validator to help write the feedstock
    # You must pass the metadata to the constructor
    # Each Validator instance can only be used for a single dataset
    # If the metadata is incorrect, the constructor will throw an exception and the program will exit
    dataset_validator = Validator(dataset_metadata)


    # Get the data
    #    Each record should be exactly one dictionary
    #    You must write your records using the Validator one at a time
    #    It is recommended that you use a parser to help with this process if one is available for your datatype
    #    Each record also needs its own metadata
    for data_file in tqdm(find_files(input_path, "xyz"), desc="Processing files", disable=not verbose):
        record = parse_ase(os.path.join(data_file["path"], data_file["filename"]), "xyz")
        record_metadata = {
            "mdf": {
                "title": "gdb7_13 " + data_file["filename"],
                "acl": ['public'],
    
    #            "tags": ,
    #            "description": ,
                
                "composition": record["chemical_formula"],
    #            "raw": ,
    
                "links": {
                    #"landing_page": ,
    
    #                "publication": ,
    #                "data_doi": ,
    
    #                "related_id": ,
    
                    "xyz": {
                        "globus_endpoint": "82f1b5c6-6e9b-11e5-ba47-22000b92c6ec",
                        "http_host": "https://data.materialsdatafacility.org",
    
                        "path": "/collections/gdb7_13/gdb7_13_data/" + data_file["filename"],
                        },
                    },
    
    #            "citation": ,
    #            "data_contact": {
    
    #                "given_name": ,
    #                "family_name": ,
    
    #                "email": ,
    #                "institution":,
    
    #                },
    
    #            "author": ,
    
    #            "license": ,
    #            "collection": ,
    #            "year": ,
    
    #            "mrr":
    
    #            "processing": ,
    #            "structure":,
                }
            }

        # Pass each individual record to the Validator
        result = dataset_validator.write_record(record_metadata)

        # Check if the Validator accepted the record, and print a message if it didn't
        # If the Validator returns "success" == True, the record was written successfully
        if result["success"] is not True:
            print("Error:", result["message"])

    # You're done!
    if verbose:
        print("Finished converting")
