import argparse
import glob
import os
import subprocess


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--packages", nargs="+", required=False)
    parser.add_argument("-f", "--force", type=bool,
                        default=False, required=False)
    args: argparse.Namespace = parser.parse_args()

    packages = args.packages
    force = args.force

    # setting trusted hosts for whole pip
    os.system(
        'pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"')

    if packages is None:
        # install all packages in dist without .dev packages
        for file in glob.glob("dist/*.whl"):
            # filetring DEV versions from the whole dist installation
            if '.dev' not in file:
                # get package name from filename
                package_name: str = os.path.basename(file).split("-")[0]
                # get version from filename
                file_version: str = os.path.basename(file).split("-")[1]
                # get version from pip in system if exists
                try:
                    version_from_system: str = subprocess.check_output(
                        ["powershell.exe", f"pip show {package_name.replace('_', '-')} | Select-String -Pattern 'Version'"]).decode().split(" ")[1].strip()
                except subprocess.CalledProcessError:
                    version_from_system: str = "Not installed"
                # compare versions
                if file_version != version_from_system:
                    print(
                        f"Version mismatch for {package_name}! File version: {file_version}, system version: {version_from_system}.")
                    os.system(f"pip install {file}")
                else:
                    if not force:
                        print(
                            f"The same version {version_from_system} of the {package_name} is installed, skipping.")
                    else:
                        print(
                            f"The same version {version_from_system} of the {package_name} is installed, but FORCE flag set, reinstalling.")
                        os.system(f"pip install {file} --force-reinstall")
    else:
        for package in packages:
            package_files: list[str] = glob.glob(f"dist/{package}*.whl")
            if len(package_files) == 0:
                raise ValueError(
                    f"Could not find package named '{package}' in dist folder."
                )
            else:
                # get package name from filename
                package_name: str = os.path.basename(
                    package_files[0]).split("-")[0]
                # get version from filename
                file_version: str = os.path.basename(
                    package_files[0]).split("-")[1]
                # get version from pip in system if exists
                try:
                    version_from_system: str = subprocess.check_output(
                        ["powershell.exe", f"pip show {package_name.replace('_', '-')} | Select-String -Pattern 'Version'"]).decode().split(" ")[1].strip()
                except subprocess.CalledProcessError:
                    version_from_system: str = "Not installed"
                # compare versions
                if file_version != version_from_system:
                    print(
                        f"Version mismatch for {package_name}! File version: {file_version}, system version: {version_from_system}.")
                    os.system(f"pip install {package_files[0]}")
                else:
                    if not force:
                        print(
                            f"The same version {version_from_system} of the {package_name} is installed, skipping.")
                    else:
                        print(
                            f"The same version {version_from_system} of the {package_name} is installed, but FORCE flag set, reinstalling.")
                        os.system(
                            f"pip install {package_files[0]} --force-reinstall")
