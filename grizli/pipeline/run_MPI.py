"""
Script to run all redshift fits in parallel with OpenMPI

Usage:  

    mpiexec -n 10 python -m mpi4py.futures $GRIZLICODE/grizli/pipeline/run_MPI.py
   
where "-n 8" indicates running 8 parallel threads.

Needs 'fit_args.py' created by `auto_script.generate_fit_params`.

"""
import time
import os
import glob

def find_ids():
    # Find objects that with extarcted spectra and that need to be fit
    all_files=glob.glob('*beams.fits')
    files = []
    for file in all_files:
        if not os.path.exists(file.replace('beams.fits', 'full.fits')):
            files.append(file)

    print('{0} files to fit'.format(len(files)))
        
    ids = [int(file.split('_')[1].split('.')[0]) for file in files]
    
    return ids
    
if __name__ == '__main__':

    import numpy as np
    import drizzlepac

    import matplotlib.pyplot as plt
    plt.ioff()

    from mpi4py.futures import MPIPoolExecutor

    from grizli.fitting import run_all_parallel
    from grizli import utils
    utils.set_warnings()
    
    t1 = time.time()
    
    ids = find_ids()
    if len(ids) == 0:
        exit()
        
    with MPIPoolExecutor() as executor:
        res = executor.map(run_all_parallel, ids)
        for ix in res:
            print('  Done, id={0} / status={1}, t={2:.1f}'.format(ix[0], ix[1], ix[2]))
        
    t2 = time.time()
    
    print('MPIPool: {0:.1f}'.format(t2-t1))
    
        
