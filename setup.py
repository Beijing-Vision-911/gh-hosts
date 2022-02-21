from setuptools import find_packages, setup  # type: ignore

import versioneer

setup(
    name="gh-hosts",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    packages=find_packages(),
    entry_points={"gui_scripts": ["gh-hosts=gh_hosts.dns:main"]},
    setup_requires=["wheel", "nuitka"],
    install_requires=["ping3>=3.0.2"],
    command_options={
        "nuitka": {
            "--show-scons": True,
            "--enable-plugin": ["anti-bloat"],
            "--clang": True,
        }
    },
    build_with_nuitka=True,
)
