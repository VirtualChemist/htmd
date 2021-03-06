# (c) 2015-2018 Acellera Ltd http://www.acellera.com
# All Rights Reserved
# Distributed under HTMD Software License Agreement
# No redistribution in whole or part
#
import json
from subprocess import check_output
import sys
import os

workdir = sys.argv[1]

metatemplate = """
package:
  name: htmd-deps
  version: {{{{ environ.get('BUILD_VERSION') }}}}

source:
   path: .

requirements:
  build:
    - python
    - requests

  run:
{run}

  run_constrained:
{run_constrained}
"""

# Read in all dependencies
deps = []
with open(os.path.join(workdir, 'DEPENDENCIES'), 'r') as f:
    for line in f:
        # Remove comments and split
        packagematch = line.split('#')[0].split()
        # Append dict of the conda package match specification
        if packagematch:
            deps.append(dict(zip(['name', 'version', 'build_string'], packagematch)))

# Get all installed packages from conda
packages = check_output(['conda', 'list', '--json']).decode('utf8')
packages = json.loads(packages)

# Find the version of each dependency and add them to the meta.yaml file
rundeps = ''
runconstdeps = ''
depnames = [dep['name'] for dep in deps]
found = dict(zip(depnames, [False] * len(depnames)))
for p in packages:
    name = p['name'].lower()
    if name in depnames:
        dep = next(dep for dep in deps if dep['name'] == name)
        if 'version' not in dep:
            if name == 'htmd-data':
                text = '    - {} =={}\n'.format(name, p['version'])
            else:
                text = '    - {} >={}\n'.format(name, p['version'])
        else:
            text = '    - {} {}\n'.format(name, dep['version'])

        if name == 'htmd-data':
            runconstdeps += text
        else:
            rundeps += text
        found[name] = True

metatemplate = metatemplate.format(run=rundeps, run_constrained=runconstdeps)

# Check if all dependencies were found. If not print which and exit with error
if not all(found):
    for key in found:
        if not found[key]:
            print('Could not find dependency "{}". Exiting with error.'.format(key))
    sys.exit(1)

# Write htmd-deps meta.yaml file
with open(os.path.join(workdir, 'meta.yaml'), 'w') as f:
    f.write(metatemplate)
