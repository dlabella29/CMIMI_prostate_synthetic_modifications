import os
import numpy as np
import nibabel as nib
from itertools import combinations

def compute_dice_coefficient(mask1, mask2):
    intersection = np.sum((mask1 > 0) & (mask2 > 0))
    volume_sum = np.sum(mask1 > 0) + np.sum(mask2 > 0)
    if volume_sum == 0:
        return 1.0  # Both masks are empty
    else:
        return 2.0 * intersection / volume_sum

def main():
    root_dir = 'E:\Grand Challenge Data\prostateX_raw_Files_2'
    case_dirs = [d for d in os.listdir(root_dir) if d.startswith('PEx0') and os.path.isdir(os.path.join(root_dir, d))]
    overall_dice_scores = []
    case_averages = {}

    for case in case_dirs:
        mask_dir = os.path.join(root_dir, case, 'nifti', 'mask_10')
        if not os.path.exists(mask_dir):
            continue  # Skip if mask directory doesn't exist

        # Collect all wp_dl_&&& files
        mask_files = [f for f in os.listdir(mask_dir) if f.startswith('wp_dl_10_') and (f.endswith('.nii') or f.endswith('.nii.gz'))]
        mask_files_full = [os.path.join(mask_dir, f) for f in mask_files]

        if len(mask_files_full) < 2:
            continue  # Need at least two masks to compute pairwise Dice

        dice_scores = []

        # Generate all unique pairs
        for file1, file2 in combinations(mask_files_full, 2):
            try:
                img1 = nib.load(file1)
                img2 = nib.load(file2)
                data1 = img1.get_fdata()
                data2 = img2.get_fdata()

                if data1.shape != data2.shape:
                    print(f"Shape mismatch between {file1} and {file2}. Skipping these files.")
                    continue

                dice = compute_dice_coefficient(data1, data2)
                dice_scores.append(dice)
                overall_dice_scores.append(dice)
            except Exception as e:
                print(f"Error processing {file1} and {file2}: {e}")
                continue

        if dice_scores:
            average_dice = np.mean(dice_scores)
            case_averages[case] = average_dice
            print(f"Case {case}: Average Dice = {average_dice:.4f}")

    if overall_dice_scores:
        overall_average = np.mean(overall_dice_scores)
        print(f"\nOverall Average Dice = {overall_average:.4f}")
    else:
        print("No pairwise Dice scores computed.")

if __name__ == "__main__":
    main()