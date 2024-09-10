import h5py

def split_h5_file_by_entries(input_file, output_prefix, split_sizes):
    """
    Split an HDF5 file into smaller files based on specified entry sizes.

    Args:
    - input_file (str): Path to the input HDF5 file.
    - output_prefix (str): Prefix for the output files.
    - split_sizes (list of int): List specifying the number of entries for each output file.
    """
    with h5py.File(input_file, 'r') as f:
        total_entries = list(f.values())[0].shape[0]  # Get total entries from any dataset (assuming all keys have the same length)
        start_idx = 0
        
        # Verify if the split sizes are consistent with the dataset
        if sum(split_sizes) != total_entries:
            raise ValueError("The sum of split sizes must equal the total number of entries in the dataset.")
        
        # Iterate over each split size
        for i, size in enumerate(split_sizes):
            end_idx = start_idx + size
            output_file = f"{output_prefix}_part{i}.h5"
            
            with h5py.File(output_file, 'w') as out_f:
                # Copy each dataset for the given range
                for key in f.keys():
                    out_f.create_dataset(key, data=f[key][start_idx:end_idx])
                    
            print(f"Created {output_file} with {size} entries.")
            start_idx = end_idx

# Example usage
input_file = '/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/combinedfiles/trainmc_combined_v2.h5'  # Path to your input HDF5 file
output_prefix = 'trainmc'  # Prefix for the output files
split_sizes = [928120, 232030]#, 49450]  # Sizes for each split

split_h5_file_by_entries(input_file, output_prefix, split_sizes)
