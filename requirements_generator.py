import os
import pkg_resources

# Set the local package directory
local_package_dir = 'packages'

# Get a list of all locally installed packages
distros = [d for d in pkg_resources.find_distributions(local_package_dir)]

# Open the requirements.txt file for writing
with open('requirements.txt', 'w') as f:
    # For each package, write its name and version to the file
    for distro in distros:
        f.write(f'{distro.project_name}=={distro.version}\n')