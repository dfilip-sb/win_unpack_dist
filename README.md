# Overview

The script purpose is to consume the contents of folder `dist` usually used by Python package builders to store the newly created packages (`.whl` files).

# Usage

-   Place the script `unpack_dist.py` in the root of your project, the folder `dist`, containing your package files must be also there.
-   Execute the script with or without arguments:

          Simple `python unpack_dist.py` will check your `dist` folder for all non-dev packages and install them in your current environment.

          Extend with `-p <package1_name> <package2_name>` if you want only specified packages to be installed.

          Extend with `-f True` or `-f Yes` or `-f <any_character_except_zero>` if you want to force the installation of the package(s) even if the same versions of them are already installed in your environment.

# TODO

What needs to be improved:

-   rewrite with OOP and DRY approach
-   add checking the OS type and setting the version verification based on it
-   add more version identifiers to be skipped by the whole installation step, except of `.dev`
-   make the version skipping partly optional
