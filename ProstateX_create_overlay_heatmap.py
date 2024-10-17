import os
import nibabel as nib
import numpy as np

# Define the directory containing the mask files
mask_directory = r"E:\Grand Challenge Data\prostateX_raw_Files_2\PEx0220\nifti\mask_3"
output_file = os.path.join(mask_directory, 'wp_dl_3_overlay.nii.gz')

# Initialize a variable to store the summed mask data
summed_mask_data = None

# Loop over the range 0-18 to process each file
for i in range(19):
    mask_file = os.path.join(mask_directory, f'wp_dl_3_{i}.nii.gz')

    # Load the current mask file
    mask_img = nib.load(mask_file)
    mask_data = mask_img.get_fdata()  # Get the voxel data

    # If this is the first file, initialize the summed_mask_data
    if summed_mask_data is None:
        summed_mask_data = np.zeros_like(mask_data)

    # Add the current mask data to the summed_mask_data
    summed_mask_data += mask_data

# Save the summed data as a new NIfTI file
summed_mask_img = nib.Nifti1Image(summed_mask_data, mask_img.affine)
nib.save(summed_mask_img, output_file)

print(f"Summed mask saved as {output_file}")
