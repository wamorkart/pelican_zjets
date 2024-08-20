import h5py
import numpy as np
import os, time, uuid
import pandas as pd


def concat2(file1, file2, file3, compress = True, comp_level = 5):
    f1 = h5py.File(file1,'r')
    f2 = h5py.File(file2,'r')
    keys1 = [str(x) for x in f1.keys()]
    keys2 = [str(x) for x in f2.keys()]
    
    # --- Checks --- #
    # check that keys match
    if(sorted(keys1) != sorted(keys2)):
        print('Keys don\'t match for ', file1, ', ', file2, ' .')
        print(file1, ' keys: ', sorted(keys1))
        print(file2, ' keys: ', sorted(keys2))
        raise ValueError('Key mismatch.')
        return
        
    # check that dimensions match (except for lengths) for each dataset
    for key in keys1:
        shape1 = f1[key].shape
        shape2 = f2[key].shape
        # check number of dimensions
        if(len(shape1) != len(shape2)):
            print('# of dimensions don\'t match for dataset ', key, ' .')
            print(file1, '[', key, '] ndim = ', len(shape1))
            print(file2, '[', key, '] ndim = ', len(shape2))
            raise ValueError('Number of dimensions mismatch.')
            return
            
        # check each dimension, except for the first (length allowed to mismatch)
        n_mismatch = 0
        for i in range(len(shape1)-1):
            if (shape1[i+1] != shape2[i+1]):
                print (shape1[i+1])
                print (shape2[i+1])
                print('Dimension', i+1, ' mismatch for dataset ', key, ' .')
                n_mismatch = n_mismatch + 1
        if(n_mismatch > 0):
            dimension_error = ' dimension mismatch'
            if(n_mismatch > 1): dimension_error = ' dimension mismatches.'
            raise ValueError(str(n_mismatch) + dimension_error)
    
    # --- Finished checks --- #
    # get final shapes of each dataset
    shape_dict = {}
    for key in keys1:
        length = f1[key].shape[0] + f2[key].shape[0]
        shape = (length,) + f1[key].shape[1:]
        shape_dict[key] = shape
    f3 = h5py.File(file3,'w')
    for key in keys1:
        a = f1[key][:]
        b = f2[key][:]
        c = np.concatenate((a,b),axis=0) # concatenate along length axis
        if(compress): dset = f3.create_dataset(key, data=c, compression='gzip', compression_opts=comp_level)
        else: dset = f3.create_dataset(key, data=c)
    f3.close()
    f1.close()
    f2.close()

def concatN(list_of_files, output_name = 'out.h5', comp_level = 5, debug = False):
    if len(list_of_files) <= 1: return
    list_of_files_dynamic = list_of_files
    tempname = ''
    tempname_old = ''
    while(len(list_of_files_dynamic) > 1):
        if(debug):
            print(len(list_of_files_dynamic), ' files left to concatenate.')
        tempname = str(uuid.uuid4().hex) + '.h5' # highly unlikely to cause namespace conflict
        concat2(list_of_files_dynamic[-1], list_of_files_dynamic[-2], tempname, True, comp_level)
        if tempname_old != '': os.remove(tempname_old)
        list_of_files_dynamic.pop()
        list_of_files_dynamic.pop()
        list_of_files_dynamic.append(tempname)
        tempname_old = tempname
    os.rename(tempname,output_name)


files_pd = [f"/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/pd_chunk_{i}_c_14082024.h5" for i in range(1, 49)]
files_testmc = [f"/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/testmc_chunk_{i}_c_14082024.h5" for i in range(1, 77)]
files_trainmc = [f"/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/trainmc_chunk_{i}_c_14082024.h5" for i in range(1, 233)]


# files_train = ["/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/pd_chunk_1_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/pd_chunk_2_c.h5","/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/pd_chunk_3_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/pd_chunk_4_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/trainmc_chunk_1_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/trainmc_chunk_2_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/trainmc_chunk_3_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/trainmc_chunk_4_c.h5"]
# files_test = ["/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/pd_chunk_5_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/testmc_chunk_1_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/testmc_chunk_2_c.h5"]
# files_valid = ["/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/pd_chunk_6_c.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzGroupNetwork/data/toptag/conversion/raw2h5/utils/condor/trainmc_chunk_5_c.h5" ]

files_train = ["/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/pelican_zjets/scripts/trainmc_part0.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/pelican_zjets/scripts/pd_part0.h5"]
files_test = ["/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/zjets_14082024/testmc_combined.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/pelican_zjets/scripts/pd_part1.h5"]
files_valid = ["/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/pelican_zjets/scripts/trainmc_part1.h5", "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/pelican_zjets/scripts/pd_part2.h5"]

#concatN([x for x in files_pd], "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/zjets_14082024/pd_combined.h5", debug=True)
#concatN([x for x in files_testmc], "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/zjets_14082024/testmc_combined.h5", debug=True)
# concatN([x for x in files_trainmc], "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/zjets_14082024/trainmc_combined.h5", debug=True)

# concatN([x for x in files_train], "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/zjets_14082024/train_c.h5")
# concatN([x for x in files_test], "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/zjets_14082024/test_c.h5")
concatN([x for x in files_valid], "/global/cfs/cdirs/m3246/twamorka/omnifold_atlas/LorentzNet-release/data/zjets_14082024/valid_c.h5")

