"""
The goal is to read the Z+jets input root files, add variables that are required as input by the PELICAN architecture and produce intermediate h5 files with those additional variables: 4-vector: E, px, py, pz and a label used for classification, is_signal. We set is_signal to 1 for MC and to 0 for pseudodata. 
This is done by reading the root files using uproot, loading them as a pandas dataframe, adding the new information and converting the pandas dataframe to h5 files.

python addvars.py /global/cfs/cdirs/m3246/ZjetOmnifold/data/slimmed_files/WithTracks_ZjetOmnifold_May19_MGPy8FxFxRew_syst_test_Mar0723.root testmc mc
python addvars.py /global/cfs/cdirs/m3246/ZjetOmnifold/data/slimmed_files/WithTracks_ZjetOmnifold_Aug5_PseudoDataSRew_Apr8_1_All.root pd pd
"""
import sys, os, time
import numpy as np
import uproot
import awkward as ak
import matplotlib.pyplot as plt
import pandas as pd

from tqdm.notebook import tqdm
import h5py

def pad_array(arr, max_tracks):
    # arr = ak.pad_none(arr, max_tracks, axis=1, clip=True)
    arr = ak.pad_none(arr, 400, axis=1, clip=True)
    arr = ak.to_numpy(ak.fill_none(arr, 0, axis=1))    
    return arr

def add_track_df(track_arr, label, df):
    for i in range(track_arr.shape[1]):    
        track_i = np.transpose(track_arr)[i]
        column_name = f"{label}_{i+2}"
        df[column_name] = track_i

    # return track_i    

def convert_to_h5(f_in, f_out, f_type):
    f_in = uproot.open(f_in)
    tree_in = f_in['OmniTree']

    pass190_mc = ak.to_numpy(tree_in['pass190'].array())
    flag_190 = pass190_mc

    l1_pt = ak.unflatten(tree_in["pT_l1"].array(), 1, axis=0)
    l1_eta = ak.unflatten(tree_in["eta_l1"].array(), 1, axis=0)
    l1_phi = ak.unflatten(tree_in["phi_l1"].array(), 1, axis=0)
    l1_px = l1_pt*np.cos(l1_phi)
    l1_py = l1_pt*np.sin(l1_phi)
    l1_pz = l1_pt*np.sinh(l1_eta)
    l1_e = np.sqrt(l1_px**2+l1_py**2+l1_pz**2)

    l2_pt = ak.unflatten(tree_in["pT_l2"].array(), 1, axis=0)
    l2_eta = ak.unflatten(tree_in["eta_l2"].array(), 1, axis=0)
    l2_phi = ak.unflatten(tree_in["phi_l2"].array(), 1, axis=0)
    l2_px = l2_pt*np.cos(l2_phi)
    l2_py = l2_pt*np.sin(l2_phi)
    l2_pz = l2_pt*np.sinh(l2_eta)
    l2_e = np.sqrt(l2_px**2+l2_py**2+l2_pz**2)

    tracks_pt = tree_in["pT_tracks"].array()
    tracks_eta = tree_in["eta_tracks"].array()
    tracks_phi = tree_in["phi_tracks"].array()
    tracks_pt = tracks_pt[flag_190 == True,...]
    tracks_eta = tracks_eta[flag_190 == True,...]
    tracks_phi = tracks_phi[flag_190 == True,...]

    tracks_px = tracks_pt*np.cos(tracks_phi)
    tracks_py = tracks_pt*np.sin(tracks_phi)
    tracks_pz = tracks_pt*np.sinh(tracks_eta)
    tracks_e = np.sqrt(tracks_px**2+tracks_py**2+tracks_pz**2)
     
    ak.count(tracks_pt, axis=1)
    max_tracks = int(ak.max(ak.count(tracks_pt, axis=1)))
    # print(max_tracks)
    tracks_e = pad_array(tracks_e, max_tracks)
    tracks_px = pad_array(tracks_px, max_tracks)
    tracks_py = pad_array(tracks_py, max_tracks)
    tracks_pz = pad_array(tracks_pz, max_tracks)

    df = ak.to_dataframe({"E_0": ak.flatten(l1_e[flag_190 == True, ...]),"PX_0": ak.flatten(l1_px[flag_190 == True, ...]), "PY_0": ak.flatten(l1_py[flag_190 == True, ...]), "PZ_0": ak.flatten(l1_pz[flag_190 == True, ...])} )
    df["E_1"] = ak.flatten(l2_e[flag_190 == True, ...])
    df["PX_1"] = ak.flatten(l2_px[flag_190 == True, ...])
    df["PY_1"] = ak.flatten(l2_py[flag_190 == True, ...])
    df["PZ_1"] = ak.flatten(l2_pz[flag_190 == True, ...])

    add_track_df(tracks_e, "E", df)
    add_track_df(tracks_px, "PX", df)
    add_track_df(tracks_py, "PY", df)
    add_track_df(tracks_pz, "PZ", df)

    # is_signal = pd.Series(np.ones(len(df)))
    # df["is_signal"] = np.ones(len(df))
    if (f_type=="mc"):
        df["is_signal"] = np.zeros(len(df))
    else:    df["is_signal"] = np.ones(len(df))
    # result = [df, is_signal]

    # result_df = pd.concat(result)

    # print(result_df)
    print(df.shape)
    df.to_hdf(f"{f_out}.h5", key='table')    

def main(args):

        f_in = str(sys.argv[1])
        f_out = str(sys.argv[2])
        f_type = str(sys.argv[3])
        convert_to_h5(f_in, f_out, f_type)
        return 

if __name__ == "__main__":
    main(sys.argv)    
