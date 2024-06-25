import matplotlib as plt
import pandas as pd
import fileinput
import numpy as np
import os




class MedCoders():
        def __init__(self):
                pass
       # @abstractedmethod
        def Usage(self):
            print("hello")




class Stewart_analysis():


    def __init__(self) -> None:
        self.sid_list = list()
        self.atot_list = list()
        self._NumberOfParams = 12
        self.Analysis_Data = {"Na": 0, "K": 0, "Ca": 0, "Mg": 0, "Cl":0, "Lactate": 0, 
                        "other_anitons": 0, "albumin": 0, "phosphate": 0,
                        "pH":0, "hCO3": 0, "pCO3": 0}
        self.result = str()


    diagnosis_labels = {
        0: "Normal acid-base status",
        1: "Respiratory alkalosis",
        2: "Respiratory acidosis",
        3: "Metabolic acidosis",
        4: "Metabolic alkalosis",
        5: "Respiratory alkalosis and metabolic alkalosis",
        6: "Respiratory acidosis and metabolic acidosis",
        7: "Respiratory alkalosis and metabolic acidosis",
        8: "Respiratory acidosis and metabolic alkalosis",
        9: "Undefined"
    }


    def calculate_sid(self, sid_list):
         na = sid_list[0]
         k = sid_list[1]
         ca = sid_list[2]
         mg = sid_list[3]
         cl = sid_list[4]
         lactate = sid_list[5]
         other_anions = sid_list[6]

         sid = (na + k + ca + mg) - (cl + lactate + other_anions)
         return sid



    def calculate_atot(self, atot_list: list[any])-> None:
        ph = atot_list[2]
        albumin = atot_list[0]
        phosphate = atot_list[1]
        atot = (albumin * 0.123 * ph) + (phosphate * (0.309 * ph + 0.469))
        return atot



    def run(self,input_data):
        #preproces the ordering
        
        if (len(input_data.values()) == self._NumberOfParams) and all(isinstance(value, (int,float))
                                                            for value in input_data.values()):
                self.Analysis_Data = input_data.copy()
                self.sid_list = (list(self.Analysis_Data.values())[:7])
                self.atot_list = (list(self.Analysis_Data.values())[7:10])
                
                self.result = self.diagnosis_labels.get(
                    self.classify_acid_base_disturbance(
                        self.Analysis_Data.get("ph"),
                        self.Analysis_Data.get("pco2"),
                        self.Analysis_Data.get("hco3"),
                        self.calculate_atot(self.atot_list),
                        self.calculate_sid(self.sid_list)
                    )
                )
        else:
            print("Assert parameters list\nSee .Usage() for help\n")
            return

        
            


    def classify_acid_base_disturbance(self,ph, pco2, hco3, sid, atot):
        if 7.35 <= ph <= 7.45 and 35 <= pco2 <= 45 and 22 <= hco3 <= 26:
            return 0  # Normal acid-base status
        elif ph > 7.45 and pco2 < 35:
            if hco3 < 22:
                return 7  # Respiratory alkalosis and metabolic acidosis
            elif hco3 > 26:
                return 5  # Respiratory alkalosis and metabolic alkalosis
            else:
                return 1  # Respiratory alkalosis
        elif ph < 7.35 and pco2 > 45:
            if hco3 < 22:
                return 6  # Respiratory acidosis and metabolic acidosis
            elif hco3 > 26:
                return 8  # Respiratory acidosis and metabolic alkalosis
            else:
                return 2  # Respiratory acidosis
        elif ph < 7.35 and hco3 < 22:
            if pco2 < 35:
                return 7  # Respiratory alkalosis and metabolic acidosis
            elif pco2 > 45:
                return 6  # Respiratory acidosis and metabolic acidosis
            else:
                return 3  # Metabolic acidosis
        elif ph > 7.45 and hco3 > 26:
            if pco2 < 35:
                return 5  # Respiratory alkalosis and metabolic alkalosis
            elif pco2 > 45:
                return 8  # Respiratory acidosis and metabolic alkalosis
            else:
                return 4  # Metabolic alkalosis
        else:
            return 9  # Undefined



    def Get(self):
        return self.result
        
    def File_Import(self, File_Name: str):
        try:
            file_path = os.path.join("diagnose_sets", "Steward_sets")
            csv_Path = os.path.join(file_path, File_Name)
            return pd.read_csv(csv_Path)
        except:
            print("File not found\n")
        
    def Usage():
        print("MedCoders::Steward_analysis -> Requiers arguments of the following order:\n")
        print("\tNa - mmol/L,\n\tK - mmol/L\n\tCa - mmol/L\n\tMg - mmol/L,\n\t",
              "Cl - mmol/L,\n\tLactate - mmol/L, Other_Anions -mmol/L,\n\t,albumin -g/dL,\n\t",
              "phosphate - mmol/L,\n\tpH - %, hCO3 - mmol/L, pCO2 - mmol/L")
    def Show(self):
        print(self.result)
        
    






class Henderson_Hasselbalch():
    def __init__(self)-> None:
        self.Analysis_Data = list()
        self.Paramers_count = 3
        self.result = str()
    
        self.diganosis_lable = {
            0: "Nominal",
            1: "Respiratory alkalosis",
            2: "Respiratory acidosis",
            3: "Metabolic acidosis",
            4: "Metabolic alkalosis",
            5: "Respiratory alkalosis and metabolic alkalosis",
            6: "Respiratory acidosis and metabolic acidosis",
            7: "Respiratory alkalosis and metabolic acidosis",
            8: "Respiratory acidosis and metabolic alkalosis",
            9: "Undefined"
        }



    def Usage():
        print("MedCoders::Henderson_Hasselbalch -> Requiers arguments of the following order:\n")
        print("\tpH - %,\n\tpCO2 - mmHg,\n\thCO3 - mmol/L")


    def run(self,Henderson_args):
        if (len(Henderson_args.values())==
            self.Paramers_count) and all(isinstance(value, (int,float))
            for value in Henderson_args.values()):
            
            self.Analysis_Data = Henderson_args.copy()
            del Henderson_args
            
            self.result = self.diganosis_lable.get(self.classify_acid_base_disturbance(
                self.Analysis_Data.get("measured_ph"),
                self.Analysis_Data.get("pco2"),
                self.Analysis_Data.get("hco3")
            ))

        else:
            print("Assert parameters list\nUse .Usage() for help")
            return


    
    
    def calculate_ph(self, hco3, pco2):
        calculated_ph = 6.1 + np.log10(hco3 / (0.03 * pco2))
        return calculated_ph


    def classify_acid_base_disturbance(self, measured_ph, pco2, hco3):
        self.calculated_ph = self.calculate_ph(hco3, pco2)


        if 7.35 <= measured_ph <= 7.45 and 35 <= pco2 <= 45 and 22 <= hco3 <= 26:
            return 0  # Normal acid-base status
        elif measured_ph > 7.45 and pco2 < 35:
            if hco3 < 22:
                return 7  # Respiratory alkalosis and metabolic acidosis
            elif hco3 > 26:
                return 5  # Respiratory alkalosis and metabolic alkalosis
            else:
                return 1  # Respiratory alkalosis
        elif measured_ph < 7.35 and pco2 > 45:
            if hco3 < 22:
                return 6  # Respiratory acidosis and metabolic acidosis
            elif hco3 > 26:
                return 8  # Respiratory acidosis and metabolic alkalosis
            else:
                return 2  # Respiratory acidosis
        elif measured_ph < 7.35 and hco3 < 22:
            if pco2 < 35:
                return 7  # Respiratory alkalosis and metabolic acidosis
            elif pco2 > 45:
                return 6  # Respiratory acidosis and metabolic acidosis
            else:
                return 3  # Metabolic acidosis
        elif measured_ph > 7.45 and hco3 > 26:
            if pco2 < 35:
                return 5  # Respiratory alkalosis and metabolic alkalosis
            elif pco2 > 45:
                return 8  # Respiratory acidosis and metabolic alkalosis
            else:
                return 4  # Metabolic alkalosis
        else:
            return 9  # I am not sure

        
    def Get(self):
        return self.result

    def File_Import(self, File_Name: str):
            
        try:
            file_path = os.path.join("diagnose_sets", "Henderson_Hasselbalch")
            csv_Path = os.path.join(file_path, File_Name)
            return pd.read_csv(csv_Path)
        except:
            print("File not found\n")
        

    def Show(self):
        print(self.result)
        pass




class Adimlari(MedCoders):
       def __init__(self):
              self.Analisys_Data = dict()
              self.result = str()
              self.ParameterCount = 3
              
       def Get(self):
            return self.result
        
       def Usage():
           print("MedCoders::Adimlari-> Requiers arguments of the following order:\n")
           print("\tpH - %,\n\tpCO2 - mmHg,\n\thCO3 - mmol/L")
       
       
       def File_Import(self, File_Name: str):
            try:
                file_path = os.path.join("diagnose_sets", "Adimlari")
                csv_Path = os.path.join(file_path, File_Name)
                return pd.read_csv(csv_Path)
            except:
                print("File not found\n")
             

       def Show(self):
          print(self.result)
          pass
            


       def Run(self, Adimlari_param: dict):
            if(len(Adimlari_param.values()) == 
               self.ParameterCount and all(isinstance(value, (int,float))
               for value in Adimlari_param.values())):
                    
                    self.Analisys_Data = Adimlari_param.copy()
                    del Adimlari_param

                    self.result = (self.classify(
                        self.Analisys_Data.get("measured_ph"),
                        self.Analisys_Data.get("pco2"),
                        self.Analisys_Data.get("hco3")
                    ))
            else:
                print("Assert parameters list\nUse .Usage() for help")
                return
      
      
       def classify(self,measured_ph, pco2, hco3):
           
           expected_pco2_metabolic_acidosis = 40 - (24 - hco3)
           expected_pco2_metabolic_alkalosis = 40 + (hco3 - 24) * 0.7
           # Akut ve kronik solunumsal bozukluklar için kompansasyon kriterleri
           acute_resp_acidosis_h = 40 + (pco2 - 40) * 0.8
           chronic_resp_acidosis_h = 40 + (pco2 - 40) * 0.3
           acute_resp_alkalosis_h = 40 - (40 - pco2) * 0.8
           chronic_resp_alkalosis_h = 40 - (40 - pco2) * 0.5
           # Metabolik asidoz
           if hco3 < 22:
               if np.isclose(pco2, expected_pco2_metabolic_acidosis, atol=2):
                   return "Metabolic acidosis with appropriate compensation"
               elif pco2 < expected_pco2_metabolic_acidosis:
                   return "Metabolic acidosis with respiratory alkalosis"
               elif pco2 > expected_pco2_metabolic_acidosis:
                    return "Metabolic acidosis with respiratory acidosis"               
            # Metabolik alkaloz
           if hco3 > 26:
                if np.isclose(pco2, expected_pco2_metabolic_alkalosis, atol=2):
                    return "Metabolic alkalosis with appropriate compensation"
                elif pco2 < expected_pco2_metabolic_alkalosis:
                    return "Metabolic alkalosis with respiratory alkalosis"
                elif pco2 > expected_pco2_metabolic_alkalosis:
                    return "Metabolic alkalosis with respiratory acidosis"              
            # Akut solunum asidozu
           if pco2 > 45:
                if np.isclose(hco3, acute_resp_acidosis_h, atol=2):
                    return "Acute respiratory acidosis"
                elif np.isclose(hco3, chronic_resp_acidosis_h, atol=2):
                    return "Chronic respiratory acidosis"               
            # Akut solunum alkalozu
           if pco2 < 35:
                if np.isclose(hco3, acute_resp_alkalosis_h, atol=2):
                    return "Acute respiratory alkalosis"
                elif np.isclose(hco3, chronic_resp_alkalosis_h, atol=2):
                    return "Chronic respiratory alkalosis"              
                return "Undefined"



class Description():
    
    def __init__(self) -> None:
        pass
    

    def calculate_atot(self,albumin, phosphate, ph=7.4):
        # Toplam zayıf asit (Atot) hesaplanması
        albumin_component = albumin * 0.123 * (7.4 - ph)
        phosphate_component = phosphate * 0.309
        atot = albumin_component + phosphate_component
        return atot
    

    def calculate_sig(self,na, k, ca, mg, cl, lactate, hco3, albumin, phosphate):
        # Toplam zayıf asit (Atot) hesaplanması
        atot = self.calculate_atot(albumin, phosphate)
        # SIG hesaplaması
        sig = na + k + ca + mg - cl - lactate - hco3 - atot
        return sig
    

    def calculate_lactate_free_sig(self,na, k, ca, mg, cl, hco3, albumin, phosphate):
        # Toplam zayıf asit (Atot) hesaplanması
        atot = self.calculate_atot(albumin, phosphate)
        # Laktattan arındırılmış SIG hesaplaması
        lactate_free_sig = na + k + ca + mg - cl - hco3 - atot
        return lactate_free_sig
    

    def calculate_ag(self, na, cl, hco3):
        # Anion Gap (AG) hesaplaması
        ag = na - (cl + hco3)
        return ag
    

    def calculate_agc(self, na, cl, hco3, albumin):
        # Corrected Anion Gap (AGc) hesaplaması
        ag = self.calculate_ag(na, cl, hco3)
        agc = ag + 2.5 * (4.0 - albumin)
        return agc



class Physiological_ACID_Based():
    def __init__(self) -> None:
        pass

    def calculate_expected_pco2_metabolic_acidosis(self,hco3):
        return (1.5 * hco3) + 8

    def calculate_expected_pco2_metabolic_alkalosis(self,hco3):
        return 0.7 * hco3 + 20

    def calculate_anion_gap(self,na, k, cl, hco3, albumin=None):
        if albumin is not None:
            # Correcting for albumin
            albumin_correction = (4.0 - albumin) * 2.5
            anion_gap = (na + k) - (cl + hco3) + albumin_correction
        else:
            anion_gap = (na + k) - (cl + hco3)
        return anion_gap


    def classify_acid_base_disorder(self,pH, hco3, pco2, na, k, cl, urinary_cl=None, urinary_k=None, albumin=None):
        if pH < 7.38:
            # Acidemia
            if hco3 < 22:
                # Metabolic acidosis
                expected_pco2 = self.calculate_expected_pco2_metabolic_acidosis(hco3)
                if np.isclose(pco2, expected_pco2, atol=2):
                    respiratory_response = "appropriate respiratory compensation"
                elif pco2 < expected_pco2:
                    respiratory_response = "additional respiratory alkalosis"
                else:
                    respiratory_response = "additional respiratory acidosis"

                anion_gap = self.calculate_anion_gap(na, k, cl, hco3, albumin)
                if anion_gap > 12:
                    anion_gap_status = "high anion gap"
                else:
                    anion_gap_status = "normal anion gap"

                return f"Metabolic acidosis with {respiratory_response} and {anion_gap_status}."

            elif pco2 > 42:
                # Respiratory acidosis
                if hco3 < 24 + ((pco2 - 40) * 0.1):
                    metabolic_response = "acute respiratory acidosis"
                elif hco3 < 24 + ((pco2 - 40) * 0.3):
                    metabolic_response = "chronic respiratory acidosis"
                else:
                    metabolic_response = "additional metabolic alkalosis"

                return f"Respiratory acidosis with {metabolic_response}."


        elif pH > 7.42:
            # Alkalemia
            if hco3 > 26:
                # Metabolic alkalosis
                expected_pco2 = self.calculate_expected_pco2_metabolic_alkalosis(hco3)
                if np.isclose(pco2, expected_pco2, atol=2):
                    respiratory_response = "appropriate respiratory compensation"
                elif pco2 < expected_pco2:
                    respiratory_response = "additional respiratory alkalosis"
                else:
                    respiratory_response = "additional respiratory acidosis"

                diagnosis = f"Metabolic alkalosis with {respiratory_response}."

                if urinary_cl is not None:
                    if urinary_cl < 25:
                        chloride_response = "Chloride-responsive (responsive to NaCl, KCl)"
                        if "milk alkali syndrome" in diagnosis:
                            diagnosis += " Consider milk alkali syndrome (hypercalcemia in renal failure)."
                    else:
                        chloride_response = "Chloride-resistant (urinary Cl > 40 mmol/L)"
                        if urinary_k is not None:
                            if urinary_k < 20:
                                potassium_status = "Low urinary K+ (e.g., laxative abuse)"
                            else:
                                potassium_status = "High urinary K+ (e.g., diuretic use)"
                                if "low or normal blood pressure" in diagnosis:
                                    diagnosis += " Consider Gitelman syndrome (low urinary calcium) or Bartter syndrome (high urinary calcium)."
                                else:
                                    diagnosis += " High blood pressure indicates mineralocorticoid excess, often with hypokalemia."
                        else:
                            potassium_status = "Urinary K+ not provided"
                    diagnosis += f" {chloride_response}. {potassium_status}."
                return diagnosis

            elif pco2 < 38:
                # Respiratory alkalosis
                if hco3 < 24 - (pco2 - 40) * 0.2:
                    metabolic_response = "acute respiratory alkalosis"
                elif hco3 < 24 - (pco2 - 40) * 0.5:
                    metabolic_response = "chronic respiratory alkalosis"
                else:
                    metabolic_response = "additional metabolic acidosis"

                diagnosis = f"Respiratory alkalosis with {metabolic_response}."
                return diagnosis

        return "Normal or other acid-base disorder."