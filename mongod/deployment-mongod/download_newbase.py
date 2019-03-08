

import os
import tarfile

all_compressed_files = [
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-a.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-d.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-g.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-h.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-n-A-D.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-n-E-J.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-n-K-O.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-n-P-S.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-n-T-Z.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-p.tar',
    'ftp://ftp.nrg.eu/pub/www/talys/libraries/libraries-t.tar'
]

# #ftp://ftp.nrg.eu/pub/www/talys/newbase.tar

# files_complete = []
# for file in all_compressed_files:
#     os.system('wget '+ file)

for file in all_compressed_files:
    filename = os.path.split(file)[-1]
    print(filename)
    filepath = os.path.join('compressed_data',filename)

    with tarfile.open(filepath,'r') as tgz:
        print('Extracting {0}...'.format(filepath))
        tgz.extractall('xs2')