import argparse
import glob
import os
import platform
import subprocess


class PackageInstaller:
    def __init__(self, packages: str = "", force: bool = False) -> None:
        self.packages: str = packages
        self.force: bool = force

    def install(self) -> None:
        self._set_trusted_hosts()
        if self.packages is None:
            self._install_all_packages()
        else:
            self._install_selected_packages()

    def _set_trusted_hosts(self) -> None:
        os.system(
            'pip config set global.trusted-host "pypi.org files.pythonhosted.org pypi.python.org"')

    def _install_all_packages(self) -> None:
        for file in glob.glob("dist/*.whl"):
            if '.dev' not in file:
                package_name, file_version = self._get_package_info(file)
                version_from_system: str = self._get_version_from_system(
                    package_name)
                if file_version != version_from_system:
                    self._install_package(file)
                else:
                    self._print_skip_message(package_name, version_from_system)

    def _install_selected_packages(self) -> None:
        for package in self.packages:
            package_files: list[str] = glob.glob(f"dist/{package}*.whl")
            if len(package_files) == 0:
                raise ValueError(
                    f"Could not find package named '{package}' in dist folder."
                )
            else:
                package_name, file_version = self._get_package_info(
                    package_files[0])
                version_from_system: str = self._get_version_from_system(
                    package_name)
                if file_version != version_from_system:
                    self._install_package(package_files[0])
                else:
                    self._print_skip_message(package_name, version_from_system)

    def _get_package_info(self, file):
        package_name = os.path.basename(file).split("-")[0]
        file_version = os.path.basename(file).split("-")[1]
        return package_name, file_version

    def _get_version_from_system(self, package_name) -> str:
        system_type: str = platform.system()
        if system_type == 'Windows':
            cmd: str = f"pip show {package_name.replace(
                '_', '-')} | Select-String -Pattern 'Version'"
            shell_cmd: list[str] = ["powershell.exe", cmd]
        elif system_type in ['Linux', 'Darwin']:
            cmd: str = f"pip show {
                package_name.replace('_', '-')} | grep 'Version'"
            shell_cmd: list[str] = cmd.split()
        else:
            raise NotImplementedError(
                f"Unsupported system type: {system_type}")
        try:
            version_from_system: str = subprocess.check_output(
                shell_cmd).decode().split(" ")[1].strip()
        except subprocess.CalledProcessError:
            version_from_system = "Not installed"
        return version_from_system

    def _install_package(self, file) -> None:
        package_name, file_version = self._get_package_info(file)
        print(
            f"Version mismatch for {package_name}! File version: {file_version}, system version: \
                {self._get_version_from_system(package_name)}.")
        if self.force:
            os.system(f"pip install {file} --force-reinstall")
        else:
            os.system(f"pip install {file}")

    def _print_skip_message(self, package_name, version_from_system) -> None:
        if self.force:
            print(
                f"The same version {version_from_system} of the {package_name} is installed, but FORCE \
                    flag set, reinstalling.")
        else:
            print(
                f"The same version {version_from_system} of the {package_name} is installed, skipping.")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--packages", nargs="+", required=False)
    parser.add_argument("-f", "--force", type=bool,
                        default=False, required=False)
    args: argparse.Namespace = parser.parse_args()

    installer = PackageInstaller(args.packages, args.force)
    installer.install()
