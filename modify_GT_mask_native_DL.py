'''import os
import nibabel as nib
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion


def modify_mask(case_dir, margin_mm):
    base_dir = os.path.join(case_dir, "nifti")
    t2_file = os.path.join(base_dir, "t2", "t2.nii.gz")
    mask_file = os.path.join(base_dir, "mask", "wp_ts.nii.gz")
    output_dir = os.path.join(base_dir, f"mask_{margin_mm}")
    output_file = os.path.join(output_dir, f"wp_dl_{margin_mm}.nii.gz")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the T2 and mask images
    t2_img = nib.load(t2_file)
    mask_img = nib.load(mask_file)

    mask_data = mask_img.get_fdata()

    # Get voxel dimensions
    voxel_dims = t2_img.header.get_zooms()

    # Calculate the number of iterations needed for a 20mm dilation or erosion
    iterations = int(margin_mm / voxel_dims[0])  # assuming isotropic voxel dimensions

    # Initialize the expanded mask data
    modified_mask_data = np.zeros_like(mask_data)

    # Iterate through each z-slice and apply the alternating modifications
    for z in range(mask_data.shape[2]):
        slice_mask = mask_data[:, :, z]
        if np.sum(slice_mask) == 0:
            continue

        if z % 4 == 0:  # Apply 20mm outer radial margin (dilation)
            modified_slice_mask = binary_dilation(slice_mask, iterations=iterations)
        elif z % 4 == 2:  # Apply 20mm inner radial margin (erosion)
            modified_slice_mask = binary_erosion(slice_mask, iterations=iterations)
        else:  # No modification
            modified_slice_mask = slice_mask

        modified_mask_data[:, :, z] = modified_slice_mask

    # Save the modified mask
    new_mask_img = nib.Nifti1Image(modified_mask_data, mask_img.affine, mask_img.header)
    nib.save(new_mask_img, output_file)


def main(margin_mm=20):
    master_folder = "/home/curasight/Downloads/prostateX_raw_Files_test2"

    # Iterate through all subdirectories in the master folder
    for case_dir in os.listdir(master_folder):
        case_path = os.path.join(master_folder, case_dir)
        if os.path.isdir(case_path) and case_dir.startswith("PEx0"):
            print(f"Processing case: {case_dir} for {margin_mm}")
            modify_mask(case_path, margin_mm)


if __name__ == '__main__':
    # Set the default margin to 20mm, can be modified by the user
    preferred_margin_mm = 20
    for preferred_margin_mm in range(0,21):
        main(margin_mm=preferred_margin_mm)'''

#use above if alternating expand, same, contract

#use below if random expand, same, contract

import os
import nibabel as nib
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion
import random

import os
import nibabel as nib
import numpy as np
from scipy.ndimage import binary_dilation, binary_erosion
import random


def modify_mask(case_dir, margin_mm, output_dir,i):
    base_dir = os.path.join(case_dir, "nifti")
    t2_file = os.path.join(base_dir, "t2", "t2.nii.gz")
    mask_file = os.path.join(base_dir, "mask", "wp_ts.nii.gz")
    output_file = os.path.join(output_dir, f"wp_dl_{margin_mm}_{i}.nii.gz")

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)

    # Load the T2 and mask images
    t2_img = nib.load(t2_file)
    mask_img = nib.load(mask_file)

    mask_data = mask_img.get_fdata()

    # Get voxel dimensions
    voxel_dims = t2_img.header.get_zooms()

    # Calculate the number of iterations needed for the specified dilation or erosion
    iterations = int(margin_mm / voxel_dims[0])  # assuming isotropic voxel dimensions

    # Initialize the expanded mask data
    modified_mask_data = np.zeros_like(mask_data)

    # Iterate through each z-slice and randomly apply one of the modifications
    for z in range(mask_data.shape[2]):
        slice_mask = mask_data[:, :, z]
        if np.sum(slice_mask) == 0:
            continue

        choice = random.choice(['expand', 'contract', 'none'])

        if choice == 'expand':  # Apply outer radial margin (dilation)
            modified_slice_mask = binary_dilation(slice_mask, iterations=iterations)
        elif choice == 'contract':  # Apply inner radial margin (erosion)
            modified_slice_mask = binary_erosion(slice_mask, iterations=iterations)
        else:  # No modification
            modified_slice_mask = slice_mask

        modified_mask_data[:, :, z] = modified_slice_mask

    # Save the modified mask
    new_mask_img = nib.Nifti1Image(modified_mask_data, mask_img.affine, mask_img.header)
    nib.save(new_mask_img, output_file)

    if margin_mm==0:
        nib.save(mask_img,output_file)

def main():
    master_folder = "E:\Grand Challenge Data\prostateX_raw_Files_2"

    # Iterate through all subdirectories in the master folder
    for i in range (0,19):
        for case_dir in os.listdir(master_folder):
            case_path = os.path.join(master_folder, case_dir)
            if os.path.isdir(case_path) and case_dir.startswith("PEx0"):
                for margin_mm in range(0,11):
                    output_dir = os.path.join(case_path,"nifti", f"mask_{margin_mm}")
                    print(f"Processing case: {case_dir}, margin: {margin_mm}")
                    modify_mask(case_path, margin_mm, output_dir,i)


if __name__ == '__main__':
    main()