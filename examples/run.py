# run.py
from  MixtureMetrics import mixture_descriptors_to_csv

# Example usage
# 1- Change the file path of descriptors and concentrations files and output files directory accordingly.    
# 2- Please note that input files should have only one row as header and one column as row labels. if you have more than one header or row label, remove the redundent before using the code.
# 3- Please note that the number of components and their order in both file should be the same, you can also use id number for them.

if __name__ == '__main__':  
    desc_file_path = r'Descriptors.csv'
    concent_file_path = r'Components.csv'
    output_path = r'Output'
    
    
    result = mixture_descriptors_to_csv(desc_file_path, concent_file_path, output_path)
    print (result)

