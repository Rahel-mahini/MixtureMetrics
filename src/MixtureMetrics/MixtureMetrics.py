# -*- coding: utf-8 -*-
"""
Created on Tue Aug 15 13:57:58 2023

@author: RASULEVLAB
"""


import pandas as pd
import numpy as np
import os
import sys

# Load data from the CSV file which exclude the header and first column 
def load_csv_data(descriptors_file_path, concentrations_file_path):
    
    try:
        # Load data from the first CSV file which exclude the header 
        df1 = pd.read_csv(descriptors_file_path, sep=',')

        # Load data from the second CSV file which exclude the header
        df2 = pd.read_csv(concentrations_file_path, sep=',')
        
        # exclude the first column 
        df1 = df1.iloc[:, 1:]
        df2 = df2.iloc[:, 1:]

        # Convert the dataframes to numpy 2D arrays
        descriptors = df1.values
        concentrations = df2.values
        descriptors = descriptors.astype(np.float64)
        concentrations = concentrations.astype(np.float64)     

        return descriptors, concentrations

    except Exception as e:
        print("Error occurred while loading CSV data:", e)
        
    
# load data from the CSV  file including header and including first column
def load_csv_all(descriptors_file_path, concentrations_file_path): 
    
    # read concentration file include the header
    df1 = pd.read_csv(descriptors_file_path, sep=',' , header = None)
    df2 = pd.read_csv(concentrations_file_path, sep=',', header = None)  
    descriptors = df1.values
    concentrations = df2.values
    print ("descriptors ",  descriptors.shape) 
    print ("concentrations ",  concentrations.shape) 
    
    descriptors[1:, 1:].astype(np.float64)
    concentrations[1:, 1:].astype(np.float64)
    return descriptors, concentrations


# Return a tuple including two numpy array of sorted_concentrations, sorted_descripors, which are ordered based on MW   
def order_mw (descriptors_file_path, concentrations_file_path):
    
    #Load data from the  CSV file which include the header 
    output = load_csv_all(descriptors_file_path, concentrations_file_path)
    descriptors = output[0]
    concentrations = output[1]
    
    descriptors_name = descriptors[0]
    mixtures_name = concentrations [:, 0]         
    
    # Sort Descriotors based on the MW (descending)
    column_index = np.where(descriptors_name== 'MW')[0][0]


    descriptor_no_header = descriptors[1:]

    
    sorted_descriptors_no_header = sorted (descriptor_no_header, key = lambda x : float (x [column_index]), reverse = True)   
    
    sorted_descriptors = np.vstack((descriptors_name, sorted_descriptors_no_header))         
 
  
    sorted_descriptors_nd = np.array(sorted_descriptors)
    
    # Check if the elements in the first row are numeric
    is_concentrations_header_numeric = all(isinstance(val, (int, float)) for val in concentrations[0, 1:])

    is_descriptors_1stcolumn_numeric = all(isinstance(val, (int, float)) for val in sorted_descriptors_nd[1:, 0])
      
    
    # Check if the 1st Column of descriptors file is numeric (contains only digits) first Convert to integers and then convert to str
    if is_descriptors_1stcolumn_numeric:
        sorted_descriptors_nd[1:, 0] = [int(col) for col in  sorted_descriptors_nd[1:, 0]]  
        sorted_descriptors_nd[1:, 0] = [str(col) for col in  sorted_descriptors_nd[1:, 0]]  
    else:
        sorted_descriptors_nd[1:, 0] = [str(col) for col in  sorted_descriptors_nd[1:, 0]]  # Convert to strings otherwise
  
    
    # Check if the 1st row of concentrations file is numeric (contains only digits), first Convert to integers and then  convert to str
    if is_concentrations_header_numeric:
        concentrations[0, 1:] = [int(row) for row in concentrations[0, 1:]]  
        concentrations[0, 1:] = [str(row) for row in concentrations[0, 1:]]  
        
    else:
        concentrations[0, 1:] = [str(row) for row in concentrations[0, 1:]]  # Convert to strings otherwise
    
    
    # Get the indices of the sorted_descriptors matrix first column that match the concentration matrix first row elememnt
    column_order = np.where(sorted_descriptors_nd[:, 0 , np.newaxis] == concentrations[np.newaxis, 0, :])[1]
   

    # Sort concentrations rows based on the components in the sorted descriptors
    sorted_concentrations = concentrations[:,  column_order ] 

    
    
    sorted_concentrations = np.column_stack((mixtures_name, sorted_concentrations))
    
   
       
    # exclude the first column (component names) and header (descriptors name) from descriptors matrix 
    sorted_descriptors = sorted_descriptors_nd[1:, 1:]    
    
    # exclude the first row (component names) and first column (mixtures name) from concentration matrix
    sorted_concentrations = sorted_concentrations[1:, 1:] 
    
            
    return sorted_descriptors, sorted_concentrations

    

# Returns the numpy array of header of the descriptors matrix (1, num_descriptors) and the first column (num_mixtures,1) of the concentration matrix     
def get_header_firstcolumn (descriptors_file_path, concentrations_file_path):
    
    try:
        # Load data from the first CSV file as pandas dataframe
        df1 = pd.read_csv(descriptors_file_path)
 
      
        # Load data from the second CSV file as pandas dataframe
        df2 = pd.read_csv(concentrations_file_path)
    
        # store header of descriptor names as list size of (num_descriptors + 1)
        header_descriptor = df1.columns.tolist()
       
        #convert list to numpy array
        header_descriptor_ndarray = np.array (header_descriptor).astype(str)
    
        # store mixture name column as pandas series
        first_column_mixture = df2.iloc[:, 0]
        
        # convert pandas series to numpy array 
        first_column_mixture_ndarray = first_column_mixture.values
        
        
        num_descriptors = df1.shape[1]
        num_mixture = df2.shape[0]     
 
        # reshape the header_descriptor_ndarray, first_column_mixture_ndarray from (num_descriptors + 1, ) and (num_mixtures, ) to (1, num_descriptors + 1) and (num_mixtures, 1)
        header_descriptors_reshape = np.reshape(header_descriptor_ndarray, (1, num_descriptors ))
        column_mixtures_reshape = np.reshape(first_column_mixture_ndarray, (num_mixture, 1))
        

        return header_descriptors_reshape, column_mixtures_reshape
    
    except Exception as e:
        print("Error occurred while loading CSV data:", e)     




     
# This function, get the dictionary of 12 matrices, and return the dictionary of 12 csv files path       
def write_matrices_to_csv(tabels_dict, output_path=None):
    
    average = tabels_dict["centroid"] 
    sqrdiff = tabels_dict["sqr_diff"]  
    absdiff = tabels_dict["abs_diff"]  
    fmolsum = tabels_dict["fmol_sum"]
    fmoldiff = tabels_dict["fmol_diff"] 
    sqrfmol = tabels_dict["sqr_fmol"] 
    rootfmol = tabels_dict["root_fmol"] 
    sqrfmolsum = tabels_dict["sqr_fmol_sum"] 
    normcont = tabels_dict["norm_cont"] 
    moldev = tabels_dict["mol_dev"] 
    sqrmoldev = tabels_dict["sqr_mol_dev"] 
    moldevsqr = tabels_dict["mol_dev_sqr"]                                                                                                                                                                                                                                                       
    
    # convert the numpy array to dataframe
    average_df = pd.DataFrame(average)
    sqrdiff_df = pd.DataFrame(sqrdiff)
    absdiff_df = pd.DataFrame(absdiff)
    fmolsum_df = pd.DataFrame(fmolsum)
    fmoldiff_df = pd.DataFrame(fmoldiff)
    sqrfmol_df = pd.DataFrame(sqrfmol)
    rootfmol_df = pd.DataFrame(rootfmol)
    sqrfmolsum_df = pd.DataFrame(sqrfmolsum)
    normcont_df = pd.DataFrame(normcont)
    moldev_df = pd.DataFrame(moldev)
    sqrmoldev_df = pd.DataFrame(sqrmoldev)
    moldevsqr_df = pd.DataFrame(moldevsqr)
      
    try:
        if output_path is None or output_path == "":
            output_path = os.getcwd()

        # Create the output directory if it doesn't exist
        os.makedirs(output_path, exist_ok=True)

        # Generate file names
        file_name1 = 'centroid.csv'
        file_name2 = 'sqr_diff.csv'
        file_name3 = 'abs_diff.csv'
        file_name4 = 'fmol_sum.csv'
        file_name5 = 'fmol_diff.csv'
        file_name6 = 'sqr_fmol.csv'
        file_name7 = 'root_fmol.csv'
        file_name8 = 'sqr_fmol_sum.csv'
        file_name9 = 'norm_cont.csv'
        file_name10 = 'mol_dev.csv'
        file_name11 = 'sqr_mol_dev.csv'
        file_name12 = 'mol_dev_sqr.csv'


        # Save matrix 1-12 as CSV filess
        file_path1 = os.path.join(output_path, file_name1)
        average_df.to_csv(file_path1, sep=',' , header=False, index=False)
      
        file_path2 = os.path.join(output_path, file_name2)
        sqrdiff_df.to_csv(file_path2, sep=',' , header=False, index=False)
        
        file_path3 = os.path.join(output_path, file_name3)
        absdiff_df.to_csv(file_path3, sep=',' , header=False, index=False)
        
        file_path4 = os.path.join(output_path, file_name4)
        fmolsum_df.to_csv(file_path4, sep=',' , header=False, index=False)
        
        file_path5 = os.path.join(output_path, file_name5)
        fmoldiff_df.to_csv(file_path5, sep=',' , header=False, index=False)
        
        file_path6 = os.path.join(output_path, file_name6)
        sqrfmol_df.to_csv(file_path6, sep=',' , header=False, index=False)

        file_path7 = os.path.join(output_path, file_name7)
        rootfmol_df.to_csv(file_path7, sep=',' , header=False, index=False)

        file_path8 = os.path.join(output_path, file_name8)
        sqrfmolsum_df.to_csv(file_path8, sep=',' , header=False, index=False)
        
        file_path9 = os.path.join(output_path, file_name9)
        normcont_df.to_csv(file_path9, sep=',' , header=False, index=False)
        
        file_path10 = os.path.join(output_path, file_name10)
        moldev_df.to_csv(file_path10, sep=',' , header=False, index=False)
        
        file_path11 = os.path.join(output_path, file_name11)
        sqrmoldev_df.to_csv(file_path11, sep=',' , header=False, index=False)
        
        file_path12 = os.path.join(output_path, file_name12)
        moldevsqr_df.to_csv(file_path12, sep=',' , header=False, index=False)
        
        
        file_path_dict = {
        'centroid': file_path1,
        'sqr_diff': file_path2,
        'abs_diff': file_path3,
        'fmol_sum': file_path4,
        'fmol_diff': file_path5,
        'sqr_fmol': file_path6,
        'root_fmol': file_path7,
        'sqr_fmol_sum': file_path8,
        'norm_cont': file_path9,
        'mol_dev': file_path10,
        'sqr_mol_dev': file_path11,
        'mol_dev_sqr': file_path12, 
        
        }

        # Return the file paths dictionary
        return file_path_dict
    
    except (FileNotFoundError, NotADirectoryError, PermissionError, ValueError) as e:
        print(f"Error: {e}")
    
    except Exception as e:
        print("Error occurred while writing matrices to CSV:", e)


# Return the matrix (numpy array) which has 0 for any zero value and 1 for non-szero values of the input matrix
def mask_concentration(concentrations):
    
    mask = np.where(concentrations == 0, 0, 1)
    
    return mask


# Return the matrix (numpy array) of differences of concentration weighted descriptors of all components for each mixture (Xa*Da-Xb*Db) 
def diff_mult ( descriptors, concentrations ):
    
    concentrations = concentrations.astype(float)
    descriptors  = descriptors.astype(float)
    
    num_mixtures = concentrations.shape[0]
    num_components= descriptors.shape[0]
    num_descriptors = descriptors.shape[1]
    
    mult = concentrations[:, np.newaxis, :] * descriptors.T[np.newaxis, :, :]
    
      
    difference = np.zeros(( num_mixtures, num_descriptors ))
        

    # Add epsilon to the descriptor's component  with zero value which have a non-zero concentration
    epsilon = sys.float_info.epsilon

    for i in range(num_mixtures):
         mix = mult [i]
         for j in range (num_descriptors):
             row =  mix[j]
             for k in range (num_components):
                 if row[k] == 0 and concentrations [i][k] > 0:
                    mult [i][j][k] += epsilon 


    
    
    # Iterate through the rows (num_mixtures) of mult array and if they have more than 2 non-zero concentration values use for loop over num_descriptors and do np.subtract.reduce() of descriptors in mult array with non-epsilon 
    # And elif there is only one non-zero concentration values, copy paste the descriptors value of that component, HomoPolymer.
    for i in range(num_mixtures): 

        row =  concentrations[i]
        non_zero_indices = np.nonzero(row)  # Find non-zero indices in the row (in each mixture)

        
        num_non_zero_component = len(non_zero_indices[0])
      
        mult_row =  mult[i]
 
        mult_non_zero_indices = np.nonzero(mult_row)  # Find non-zero indices in the mult row
 
       
        # Check if the row has 2 or more non-zero elements
        if num_non_zero_component >= 2:   
              
            non_zero_values = mult[i][mult_non_zero_indices] 
           
                     
            non_zero_values_reshape = np.reshape(non_zero_values , ( num_descriptors, -1 ) ) 
            
            non_zero_values_reshape = non_zero_values_reshape.astype(float)   
            
            sub_diff = np.zeros(( num_descriptors, 1 ))
            
            for j in range (num_descriptors):
                
                # Checks if there is at least one element in the array non_zero_values_reshape[j] that is not equal to epsilon
                if np.any(non_zero_values_reshape[j] != epsilon):    # or if np.all(non_zero_values_reshape[j] == epsilon): 
                    
                    sub_sub_diff = np.subtract.reduce([x for x in non_zero_values_reshape[j] if x != epsilon])                     
                    
                else:
                     sub_sub_diff = 0   
                
                sub_diff [j] = sub_sub_diff 
                
            sub_diff  = sub_diff.reshape (( num_descriptors, ))            
            difference[i]  = difference[i].reshape (( num_descriptors, ) )
            
            difference[i] = sub_diff
            
        # Check if the row  has only 1 non-zero element (HomoPolymer)                  
        elif num_non_zero_component == 1:
                 
            # Find the index row  of the component  in descriptors
            non_zero_index = non_zero_indices[0]
         
            
            # Find the index of the non-zero element in homopolymer and copy paste the descriptors of the component int the diff output
            difference[i] = descriptors [ non_zero_index]
            
    
    return difference
    

# Return the matrix (numpy array) of differences of descriptors of all components (nonzero values) of each mixture  (Da-Db) 
def diff_descriptors (descriptors, concentrations): 
    
    concentrations = concentrations.astype(float)
    descriptors  = descriptors.astype(float)
       
    mask = mask_concentration(concentrations)   
    difference = diff_mult ( descriptors, mask )
        
    return difference

# Return the mean ( (Da + Db)/ 2 ) of all pure components descriptors of each mixtures
def centroid(descriptors, concentrations):
    
    num_mixtures = concentrations.shape[0]
    mask = mask_concentration(concentrations)
    sum_descriptors = np.dot(mask, descriptors)   
    num_nonzero_components = np.sum(mask, axis = 1)
    
    # In order to broadcast, one of the dimension should be 1, then reshape the  (num_mixtures, ) to (num_mixtures, 1) dimension 
    num_nonzero_components_reshaped = np.reshape(num_nonzero_components, (num_mixtures, 1))
    average = np.divide(sum_descriptors, num_nonzero_components_reshaped)  
    
    return average


# Return the square of difference of all  descriptors of pure components of each mixtures ( (Da - Db)^2)
def sqr_diff(descriptors, concentrations):      
 
    concentrations = concentrations.astype(float)
    descriptors  = descriptors.astype(float)

    num_mixtures = concentrations.shape[0]
    num_components= descriptors.shape[0]
    num_descriptors = descriptors.shape[1]
    
    squared_diff = np.zeros ((num_mixtures, num_descriptors ))
   
    mask = mask_concentration(concentrations)

    
    mult = mask[:, np.newaxis, :] * descriptors.T[np.newaxis, :, :]

      
    difference = np.zeros(( num_mixtures, num_descriptors ))

    # Add epsilon to the descrptor's componet with zero value which have a non-zero concentration
    epsilon = sys.float_info.epsilon

    for i in range(num_mixtures):
        
         mix = mult [i]
         for j in range (num_descriptors):
             row =  mix[j]
             for k in range (num_components):
                 if row[k] == 0 and concentrations [i][k] > 0:
                    mult [i][j][k] += epsilon 
    
    # Iterate through the rows (num_mixtures) of mult array and if they have more than 2 non-zero concentration values use for loop over num_descriptors and do np.subtract.reduce() of descriptors in mult array with non-epsilon 
    # And elif there is only one non-zero concentration values, copy paste the descriptors value of that component, HomoPolymer,
    for i in range(num_mixtures): 
     
        row =  concentrations[i]
        non_zero_indices = np.nonzero(row)  # Find non-zero indices in the row
          
        num_non_zero_component = len(non_zero_indices[0])
               
        mult_row =  mult[i]
        
        mult_non_zero_indices = np.nonzero(mult_row)  # Find non-zero indices in the row
         
       
        #  Check if the row has 2 or more non-zero elements
        if num_non_zero_component >= 2:   
              
            non_zero_values = mult[i][mult_non_zero_indices]         
                     
            non_zero_values_reshape = np.reshape(non_zero_values , ( num_descriptors, -1 ) ) 
           
            
            non_zero_values_reshape = non_zero_values_reshape.astype(float)   
            
            sub_diff = np.zeros(( num_descriptors, 1 ))
            
            for j in range (num_descriptors):
                
                # Checks if there is at least one element in the array non_zero_values_reshape[j] that is not equal to epsilon
                if np.any(non_zero_values_reshape[j] != epsilon):   
                    
                    sub_sub_diff = np.subtract.reduce([x for x in non_zero_values_reshape[j] if x != epsilon]) 
                  
                    
                else:
                     sub_sub_diff = 0   
                
                sub_diff [j] = sub_sub_diff
         
                
            sub_diff  = sub_diff.reshape (( num_descriptors, ))            
            difference[i]  = difference[i].reshape (( num_descriptors, ) )
            
            difference[i] = sub_diff
            squared_diff [i]  = np.square(difference[i])  
            
               
       # Check if the row  has only 1 non-zero element (HomoPolymer)       
        elif num_non_zero_component == 1:
                 
            # Find the index row  of the component  in descriptors
            non_zero_index = non_zero_indices[0]
                                
            # Find the index of the non-zero element in homopolymer and copy paste the descriptors of the component int the diff output
            difference[i] = descriptors [ non_zero_index]
            squared_diff [i]  = difference[i]            
    
    return squared_diff     

# Return the absolute of difference of all descriptors of pure components of each mixtures (|Da - Db|)
def abs_diff(descriptors, concentrations): 
    
    num_mixtures = concentrations.shape[0]
    num_descriptors = descriptors.shape[1]    
    diffs = diff_descriptors (descriptors, concentrations)       
    absolute_diff = np.abs (diffs)
    absolute_diff = np.reshape(absolute_diff, (num_mixtures,num_descriptors))
    
    mask = mask_concentration(concentrations) 
    for i in range (num_mixtures):
        
        non_zero_indices = np.nonzero(mask[i])  # Find non-zero indices for each mixture mask array
        num_non_zero_component = len(non_zero_indices[0])
        
        # if HomoPolymer
        if num_non_zero_component == 1: 
                        
            non_zero_index = non_zero_indices[0]
            absolute_diff [i] = descriptors [ non_zero_index]
    
    return absolute_diff
        

# Return the sum of weighted descriptors of pure components of each mixtures (Xa*Da + Xb*Db)
def fmol_sum(descriptors, concentrations):
    
    dot_product = np.dot(concentrations, descriptors)
    
    return dot_product


# Return the difference of weighted descriptors of pure components of each mixtures by mol fractions  (Xa*Da - Xb*Db)
def fmol_diff (descriptors, concentrations):
    

    descriptors = descriptors.astype(np.float64)
    concentrations = concentrations.astype(np.float64)
    
    fmoldiff = diff_mult ( descriptors, concentrations )
   
    return fmoldiff


# Return the  sum  of weighted descriptors of pure components of each mixtures by square of mol fractions (Xa^2*Da + Xb^2*Db)
def sqr_fmol(descriptors, concentrations):
    
    squar_conc = np.square(concentrations)
    sqrfmol = np.dot(squar_conc, descriptors)
    
    return sqrfmol


# Return the sum  of weighted descriptors of pure components of each mixtures by root of mol fractions (√Xa*Da + √Xb*Db)
def root_fmol(descriptors, concentrations):
    
    fmol_root = np.sqrt(concentrations)
    fmolroot = np.dot(fmol_root, descriptors)
    
    return fmolroot

# Return the square sum  of weighted descriptors of pure components of each mixtures by mol fractions (Xa*Da + Xb*Db)^2
def sqr_fmol_sum (descriptors, concentrations):
    
   
    dot_product = np.dot(concentrations, descriptors)
    num_mixtures = concentrations.shape[0]
    num_descriptors = descriptors.shape[1]
    
    sqrfmolsum = np.zeros ((num_mixtures, num_descriptors ))
    mask = mask_concentration(concentrations)    
  
  
    for i in range (num_mixtures):
        
        non_zero_indices = np.nonzero(mask[i])  # Find non-zero indices for each mixture mask array
        num_non_zero_component = len(non_zero_indices[0])
        
        if num_non_zero_component >= 2: 
            
            sqrfmolsum [i] = np.square(dot_product [i])
            
        # else HomoPolymer    
        else: 
            
             non_zero_index = non_zero_indices[0]
             sqrfmolsum [i] = descriptors [ non_zero_index]
    
    return sqrfmolsum

# returns √((Xa * Da)^2+ (Xb * Db)^2 )
def norm_cont (descriptors, concentrations):
    
    num_mixtures = concentrations.shape[0]
    num_components = concentrations.shape[1]
    num_descriptors = descriptors.shape[1]
    
    mult = concentrations[:, np.newaxis, :] * descriptors.T[np.newaxis, :, :]
    mult_reshape = np.reshape(mult, (num_mixtures, num_descriptors, num_components))
    square_mult = np.square(mult_reshape)
    sum_square_mult = np.sum(square_mult , axis= 2)
    
    normcont = np.sqrt(sum_square_mult)
    
    num_mixtures = concentrations.shape[0] 
      
    # Iterate through the rows
    for i in range(num_mixtures):
        
        row =  concentrations[i]
        non_zero_indices = np.nonzero(row)
        num_non_zero = np.count_nonzero(row)
        
        # Check if the row has only 1 non-zero element (HomoPolymer)   
        if num_non_zero == 1: 
            non_zero_index = non_zero_indices[0]
            normcont[i] = descriptors [non_zero_index]
    
    return normcont


# return the difference of the sorted components concentration by value of each mixture Xa -Xb
def diff_concentration (concentrations):
    
    concentrations = concentrations.astype(np.float64)
    num_mixtures = concentrations.shape[0]
    # num_component = concentrations.shape[1]
    
    difference = np.zeros((num_mixtures)) 
    
    
    # Iterate through the rows
    for i in range(num_mixtures):     
       
        row =  concentrations[i]
        
        # Find non-zero indices in the row  
        non_zero_indices = np.nonzero(row)  
        num_non_zero = len(non_zero_indices[0])
        
        # Check if the row has 2 or more non-zero elements
        if num_non_zero >= 2: 
              
            non_zero_values = concentrations[i][non_zero_indices]                               
            
            non_zero_values = non_zero_values.astype(float)
            diff = np.subtract.reduce(non_zero_values)         
            difference [i] = diff
            
        # Check if the row  has only 1 non-zero element (HomoPolymer)   
        elif  num_non_zero == 1: 
                
           difference[i] = num_non_zero 
                           
   
    
    return difference

# Return the square of the sorted components concentration by value of each mixture Xa-Xb
def sqr_concentration (concentrations):
    
    concentrations = concentrations.astype(float)    
    sqr = np.square(concentrations)
    
    return sqr


# Return | Da - Db| * [1- | (Xa -Xb)]  
def mol_dev ( descriptors, concentrations):
    
    descriptors = descriptors.astype (float)
    concentrations = concentrations.astype (float)
    
    abs_diff_desc = abs_diff (descriptors, concentrations)
    diff_concent = diff_concentration (concentrations)     
    abs_diff_conc = 1- (np.abs(diff_concent))
    moldev = abs_diff_desc.T * abs_diff_conc
    moldev = moldev.T
    
    num_mixtures = concentrations.shape[0]    
    
    # Iterate through the rows
    for i in range(num_mixtures):     

        row =  concentrations[i]
        num_non_zero = np.count_nonzero(row)
 
        
        # Check if the row has only 1 non-zero element (HomoPolymer)   
        if num_non_zero == 1: 
            
            moldev[i] = abs_diff_desc [i]                   
    
    return moldev
    

# returns |Da - Db| * [1-|(Xa^2 -Xb^2)|)]  
def sqr_mol_dev (descriptors, concentrations):
    

    descriptors = descriptors.astype (float)
    concentrations = concentrations.astype (float)
    
    abs_diff_desc = abs_diff (descriptors, concentrations) 
    square_conc = sqr_concentration (concentrations)    
    diff_concent = np.subtract.reduce(square_conc , axis= 1)        
    abs_diff_conc_subtract1 = 1- (np.abs(diff_concent))    
    sqrmoldev = abs_diff_desc.T * abs_diff_conc_subtract1
    sqrmoldev = sqrmoldev.T
    
    
    num_mixtures = concentrations.shape[0]    

    # Iterate through the rows
    for i in range(num_mixtures):     

        row =  concentrations[i]
        num_non_zero = np.count_nonzero(row)
        
        # Check if the row has only 1 non-zero element (HomoPolymer)   
        if num_non_zero == 1: 
            
            sqrmoldev[i] = abs_diff_desc [i] 
    
    return sqrmoldev


# returns |Da - Db| * [1- |(Xa -Xb)|]^2  
def mol_dev_sqr (descriptors, concentrations):
    
    descriptors = descriptors.astype (float)
    concentrations = concentrations.astype (float)
    
    abs_diff_desc = abs_diff (descriptors, concentrations)
    diff_concent = diff_concentration (concentrations)
    abs_diff_conc_subtract1 = 1- (np.abs(diff_concent))
    square_conc = np.square(abs_diff_conc_subtract1)
    moldevsqr = abs_diff_desc.T * square_conc
    moldevsqr = moldevsqr.T
    
    num_mixtures = concentrations.shape[0]    

    # Iterate through the rows
    for i in range(num_mixtures):     

        row =  concentrations[i]
        num_non_zero = np.count_nonzero(row)
        
        # Check if the row has only 1 non-zero element (HomoPolymer)   
        if num_non_zero == 1: 
            
            moldevsqr[i] = abs_diff_desc [i]
    
    return moldevsqr   

  

# This function load the input files and run all the formulation of mixture descriptors 
# This function retun the dictionary of 12 mixture descriptors numpy arrays   
def mixture_descriptors (descriptors_file_path , concentrations_file_path):
    
    descriptors, concentrations  = load_csv_data (descriptors_file_path , concentrations_file_path)
   
    average = centroid(descriptors, concentrations)
    fmolsum = fmol_sum(descriptors, concentrations)
    sqrfmol = sqr_fmol(descriptors, concentrations)
    rootfmol = root_fmol(descriptors, concentrations)
    sqrfmolsum = sqr_fmol_sum (descriptors, concentrations)
    normcont = norm_cont (descriptors, concentrations)
    
    sorted_descriptors, sorted_concentrations = order_mw (descriptors_file_path, concentrations_file_path)
    
    
    sqrdiff = sqr_diff(sorted_descriptors, sorted_concentrations)
    absdiff = abs_diff(sorted_descriptors, sorted_concentrations)
    fmoldiff = fmol_diff (sorted_descriptors, sorted_concentrations)  
    moldev = mol_dev (sorted_descriptors, sorted_concentrations)
    sqrmoldev = sqr_mol_dev (sorted_descriptors, sorted_concentrations)
    moldevsqr= mol_dev_sqr (sorted_descriptors, sorted_concentrations)

    
    tabels_dict = {
        'centroid': average,
        'sqr_diff': sqrdiff,
        'abs_diff': absdiff,
        'fmol_sum': fmolsum,
        'fmol_diff': fmoldiff,
        'sqr_fmol': sqrfmol,
        'root_fmol': rootfmol,
        'sqr_fmol_sum': sqrfmolsum,
        'norm_cont': normcont,
        'mol_dev': moldev,
        'sqr_mol_dev': sqrmoldev,
        'mol_dev_sqr': moldevsqr, 
        }
    
    return  tabels_dict 

# This function concatenates the original descriptors name with the mixture descriptor names
def generate_new_descriptor_name (descriptors_file_path, concentrations_file_path):
    
    data  = load_csv_data (descriptors_file_path , concentrations_file_path)
    descriptors = data[0]
    
    num_descriptors = descriptors.shape[1]
    print ("num_descriptors", num_descriptors) 
    
    
    output = get_header_firstcolumn (descriptors_file_path, concentrations_file_path)
    
    header_name = output[0].reshape(1, -1)
    header_name = header_name[:, 1:]


    
    result = np.empty((12, num_descriptors) , dtype ='U29')
   
    Mixure_names = np.array(['centroid',  'sqr_diff', 'abs_diff',  'fmol_sum', 'fmol_diff', 'sqr_fmol', 'root_fmol', 'sqr_fmol_sum', 'norm_cont', 'mol_dev', 'sqr_mol_dev', 'mol_dev_sqr'])
   
    
    for i in range (len(Mixure_names)):
        for j, ele in enumerate(header_name[0]):

            result[i][j]= "-".join([ele, Mixure_names[i]] )   
            
    ID = np.array(['Mixture_ID/Descriptors'])   
    header_Id = np.repeat( ID, 12, axis=0)  
    result = np.c_[header_Id , result ]
    
    print ('result' , result.shape)
    pd_result = pd.DataFrame(result)
    
    result_dic = {key: values  for key , values in zip  (Mixure_names ,result )}
    
    return result_dic


# This function run mixture_descriptors function, gets header_descriptors, column_mixtures, and concatenate them to the output csv files
# Then run the write_matrices_to_csv function,    
# Retun the dictionary of 12  mixture descriptores csv files output path  
def mixture_descriptors_to_csv (descriptors_file_path , concentrations_file_path, output_path ):
    
    tabels_dict = mixture_descriptors (descriptors_file_path , concentrations_file_path)
    header_descriptors, column_mixtures = get_header_firstcolumn (descriptors_file_path, concentrations_file_path)
    Mixture_descriptors_name = generate_new_descriptor_name (descriptors_file_path, concentrations_file_path)
    
    # Add the header_descriptors, column_mixtures to the first row and first column of all dataframes instead of combiantorial in the dictionary
    # Add the combination_header, column_mixtures to the first row and first column of all dataframes instead of combiantorial in the dictionary
    # create new dictionary to store concatenated ones
    concatenated_dict = {}
    
    for key, arr in tabels_dict.items():

        # Concatenate the column to the beginning of the DataFrame
        concatenated = np.concatenate((column_mixtures, arr), axis=1)
  
        # Concatenate the header  vector size (1, num_descriptor+1) to the beginning of the DataFrame of (num_mixtures, num_descriptor+1), to get matrix of  (num_mixtures +1, num_descriptor+1)
        concatenated = np.vstack((Mixture_descriptors_name[key], concatenated))
        
        concatenated_dict[key] = concatenated
    
    output_path_dict= write_matrices_to_csv(concatenated_dict, output_path)
    
    return output_path_dict
