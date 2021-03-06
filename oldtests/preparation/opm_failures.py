# (c) 2015-2018 Acellera Ltd http://www.acellera.com
# All Rights Reserved
# Distributed under HTMD Software License Agreement
# No redistribution in whole or part
#
from htmd import *
from htmd.util import opm
from htmd.builder.charmm import build

import sys

cases = """
1z98
2w2e
2z73
3cll
3jbr
3lut
3rhw
3spc
3spg
3syq
4csk
4hkr
4kfm
4pe5
4tlm
4uqj
5an8
""".split()

# Disable this as a test
# sys.exit(0)

# cases=["3cll"]

print(os.getcwd())

for p in cases:
    print("Working on --------------- " + p)
    m, th = opm(p)
    m.filter("protein")
    m.write("{:s}.pdb".format(p))

    mo, rd = proteinPrepare(m, returnDetails=True, verbose=True)
    mo.write("{:s}-prep.pdb".format(p))
    rd.data.to_excel("{:s}-data.xlsx".format(p))

    #mo.set('segid', 'P')
    #build(mo, outdir="build-" + p, ionize=False)
