# README for the Quality checker scripts

## Overview

The main script, from which the functions are called is the "quality_checker.py". 

This script calls several function that compute: 

* The WM and GM SNR based on the norm.mgz image 
* The WM and GM SNR based on the orig.mgz image 
* The size of the Corpus Callosum 
* The number of holes in the LH and RH occured during the toplogy fixing 
* The number of defects in the LH and RH occured during the topology fixing
* The topological fixing time of the LH and the RH 
* The Contrast to Noise ratio of the LH and the RH 
* The outliers in relation to the segmentation volumes
* The Shape distances for several regions (optional)

## Usage

Required Arguments: 

* -sdir Subjects directory, 
* -recs Recon checker scripts 
* -rcsv path_data_file: CSV file in which the results will be saved
* -mch pat_manual_check_file: CSV file in which the critical subjects are saved. The reason why they are documented is also included 
    
Optional Arguments: 

* -subjects: If specified, not the whole directory will be processed 
* -fsh: Freesurfer Home Directory
* -sk, -sh, -scsv: Shape Key, Shape scripts home directory, results of the shape analysis. When specifying a shape_home directory, the script will compute the segmentation distances and save them into a csv file.
* -pname, -pkey: Plotly username, Plotly Key: You can sign up to plotly and then have a nice boxplot diagram of your results. This boxplot is semi-interactive as you can see the subject ID when sliding across the points.
* -stats: If one wants to have a file with the information treated in the outlier part. This file will be created in the subjects directory with the name mean_file.
* -lumeans: If one has already computed the means of the directory, there is an option to look up these means instead of computing them. 
* -nerode: If one wants to shorten the WM when computing the CNR, one can erode more than the default value of three pixel. 
        
Note: 

* If you do not specify some subjects, the scripts will execute the QC over the whole directory. 
* You need to define the subjects dir with a slash at the end. 

Example:
    
    python3 quality_checker.py \
        -sdir /path/to/your/subjects/dir/ \
        -recs /path/to/your/quality_checker/scripts/ \
        -rcsv /path/to/your/metrics_result_file.csv/ \
        -mch /path/to/your/manual_check_file.csv \
        -fsh /path/to/your/freesurfer/home/directory/ 
        -sk /path/to/your/shape/key.txt \
        -sh /path/to/your/shapeDNA/scripts/ 
        -scsv /path/to/your/shape_results_file.csv \
        -pname plotly_username \
        -pkey plotly_key
   
## Further extensions/modifications

A few issues remain with the current version of the scripts:

* At the moment the manual_checker function evaluates the holes, defects and Contrast to Noise ratio in order to evaluate if an image is bad. The corresponding thresholds have not been established in a professional manner. They are more intuitive and based on the ADNI 3T-Good dataset. Some modifications might be made in order to have less false positive or false negative subjects. 
* The shape metrics are only computed. There is no further evaluation if one segmenatation is well done or not. It could be interesting to look out for some way to detect segmentation outliers with the shape distances results. 
* It could be interesting to improve the report with screenshots of the possible bad subjects.
* Nearly all metrics are age and sex dependant. If available, this information should be included in the Quality check, which is not the case yet. 
* In the MRI QC (Poldrack Lab) paper, the metric that helped a lot in order to determine the quality of an image was the foreground/background energy ratio. This could be done by using mri_seghead function.
* Some images suffer from horizontal lines. These horizontal lines could be detected with the Hough Transform.
* Apart from one subprocess in the ShapeDNA postprocessing, the whole pipeline is done without subprocesses. In order to avoid version compatibility problems, it could be interesting to implement the functionality in a new python script.


## Technical notes

scripts:

quality_checker.py
|
|- wm_gm_anat_snr_checker
|- cc_size_checker.py
|- holes_topo_checker.py
|- contrast_control.py
|- shape_checker.py
|
|- write_information_to_file.py
|- write_shape_to_file.py
|
|- recon_all_aseg_outlier_checker.py
|  |- g_parc_mean_norm.py
|  |- g_parc_val_norm.py
|  |- read_parc_mean_from_table.py
|  |- segsfile2
|
|- manual_check.py
|
|- create_graph.py

scripts-unused:

- defects_checker.py
- get_relative_cc_size.py
- fore_back_energy_checker.py

scripts-unfinished:

- Hough_transform.py
