Using the PELICAN architecture with ATLAS Z+jets data

## Environment
I use the conda environment we create in [Zjets_omnifold analysis](https://github.com/kgreif24/zjets_omnifold?tab=readme-ov-file#environment-setup-on-perlmutter)
## Procedure
### Step 1
1. Create HDF5 files from the input root files which are located here: `$CFS/m3246/ZjetOmnifold/data/slimmed_files/`

| Dataset | Location|
|---------|----------|
| Train MC | WithTracks_ZjetOmnifold_May19_MGPy8FxFxRew_syst_train_Mar1023.root|
| Test MC | WithTracks_ZjetOmnifold_May19_MGPy8FxFxRew_syst_test_Mar0723.root| 
| Pseudodata | WithTracks_ZjetOmnifold_Aug5_PseudoDataSRew_Apr8_1_All.root|
| Truth Pseudodata | WithTracks_TruthPseudodata_Combined_1-18.root|

eg:
```
python addvars.py /global/cfs/cdirs/m3246/ZjetOmnifold/data/slimmed_files/WithTracks_ZjetOmnifold_May19_MGPy8FxFxRew_syst_test_Mar0723.root testmc mc
python addvars.py /global/cfs/cdirs/m3246/ZjetOmnifold/data/slimmed_files/WithTracks_ZjetOmnifold_Aug5_PseudoDataSRew_Apr8_1_All.root pd pd
```

This is quite fast and I run this step interactively.

2. Create final HDF5 files with the format expected by PELICAN / LorentzNet. We do this with the help of the conversion process developed in [LorentzGroupNetwork](https://github.com/fizisist/LorentzGroupNetwork#1-converting-the-dataset).
