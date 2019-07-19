# -*- coding: utf-8 -*-
"""
Created on Mon May 27 15:39:13 2019

@author: Tobias Wolff

This function checks the SNR of the white and the gray matter. The white matter 
segmentation is taken from the aparc+aseg image and the gray matter from the 
aseg image. The white matter is eroded by three voxels in order to ignore 
partial volumes. For the gray matter this is not possible, because the layer 
is aready very thin. An erosion would eliminate nearly the whole signal. 

Required arguments:
    - subjects_dir : path to the subjects directory 
    - subject : subject ID

Optional arguments:
    - nb_erode : the number of erosions, default = 3
    - ref_image : the reference image, default = "norm.mgz", can be changed to "orig.mgz"
    
"""

def wm_gm_anat_snr_checker(subjects_dir, subject, nb_erode=3, ref_image="norm.mgz"):

    import os
    import numpy as np
    import nibabel as nib
    from skimage.morphology import binary_erosion
    
    # Get the path to the different files
    path_aparc_aseg  = os.path.join(subjects_dir,subject,"mri","aparc+aseg.mgz")
    path_aseg = os.path.join(subjects_dir,subject,"mri","aseg.mgz")
    
    path_reference_image = os.path.join(subjects_dir,subject,"mri",ref_image)
    print("The SNR is computed for the "+ref_image+" image")
            
    # Reading the image to identify the itensities of the white and gray matter at the different locations. 
    norm = nib.load(path_reference_image)
    norm_data = norm.get_fdata()    

    # Reading the aparc+aseg image to locate the white matter    
    inseg = nib.load(path_aparc_aseg)
    data_aparc_aseg = inseg.get_fdata()    

    # Create 3D binary data where the white matter locations are encoded with 1, all the others with zero
    b_wm_data = np.zeros((256,256,256))
    
    # The following keys represent the white matter labels in the aparc+aseg image
    wm_labels = [2, 41, 7, 46, 251, 252, 253, 254, 255, 77, 78, 79]
    
    # Find the wm labels in the aparc+aseg image and set the locations in the binary image to one 
    for i in wm_labels:
        x, y, z = np.where(data_aparc_aseg == i)      
        b_wm_data[x,y,z] = 1 

    print("The number of erosions for the white matter SNR is: ", int(nb_erode))
    nb_erode = int(nb_erode) + 4 # this must be some obscure bugfix
    b_wm_data = binary_erosion(b_wm_data,np.ones((nb_erode, nb_erode,nb_erode)))
    
    # Computation of the SNR of the white matter
    x, y, z = np.where(b_wm_data == 1)
    signal_wm = []
    signal_wm.append(norm_data[x,y,z])
    signal_wm_mean = np.mean(signal_wm)
    signal_wm_std = np.std(signal_wm)
    wm_snr = signal_wm_mean/signal_wm_std
    print("The signal to noise ratio of the white matter is", wm_snr) 

    # Reading the aparc+aseg image to locate the gray matter    
    aseg = nib.load(path_aseg)
    data_aseg = aseg.get_fdata()
    
    # Create binary data where the gray matter locations are encoded with 1, all the others with zero
    b_gm_data = np.zeros((256,256,256))
    
    # The following keys represent the gray matter labels in the aseg image    
    gm_labels = [ 3, 42 ]
    
    # Find the gm labels in the aseg image and set the locations in the binary image to one 
    for i in gm_labels:
        x, y, z = np.where(data_aseg == i)
        b_gm_data[x, y, z] = 1
    
    # Computation of the SNR of the gray matter
    x, y, z = np.where(b_gm_data == 1)
    signal_gm =[]
    signal_gm.extend(norm_data[x,y,z])
    signal_gm_mean = np.mean(signal_gm)
    signal_gm_std = np.std(signal_gm)
    gm_snr =signal_gm_mean/signal_gm_std
    print ("The signal to noise ratio of the gray matter is:", gm_snr)        

    # Return
    return wm_snr, gm_snr

