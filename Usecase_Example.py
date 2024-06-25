import pandas as pd


def Example_Sterward():
    from MedCoders import Stewart_analysis

    Steward = Stewart_analysis()
    Steward_Args = {"na": 135, "k": 3.8, "ca": 2.5, "mg": 1.5, "cl":115, "Lactate": 1.0, 
                        "other_anitons": 2, "albumin": 4.5, "Phosphate": 1.0,
                        "ph":7.28, "hco3": 18, "pco2": 39}

    Steward.run(Steward_Args)
    print(Steward.Get())



def Example_Henderson():    
    from MedCoders import Henderson_Hasselbalch
    Henderson_args = dict()
    Henderson_args = {"measured_ph": 7.4, "pco2": 40, "hco3": 24}

    Henderson = Henderson_Hasselbalch()
    Henderson.run(Henderson_args)
    print(Henderson.Get())


def Example_Adimlari():
    from MedCoders import Adimlari
    Adim = Adimlari()
    Adim_Params = dict()
    Adim_Params = {"measured_ph": 7.1, "pco2": 50, "hco3": 34}

    Adim.Run(Adim_Params)
    print(Adim.Get())



def Example_Description():
    from MedCoders import Description
    desc = Description()
    print(desc.calculate_ag(4,2,3))



def Example_Physiological():
    from MedCoders import Physiological_ACID_Based
    Example = Physiological_ACID_Based()
    print(Example.classify_acid_base_disorder(0,0,0,0,0,0,0,0,0))

# Usecase and File Imports


def Example_FileImport(File_Name: str):
    from MedCoders import Stewart_analysis
    File_test = Stewart_analysis()

    diagnosis_data = File_test.File_Import(File_Name)
    print(diagnosis_data.describe())
    


if __name__ == "__main__":
    Example_Henderson()
    Example_Description()
    Example_Physiological()
    Example_FileImport("Steward_test.csv")

