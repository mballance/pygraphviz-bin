#****************************************************************************
#* setup.py for libvsc
#****************************************************************************
import os
import stat
import subprocess
import shutil
import sysconfig
from setuptools import setup
from distutils.extension import Extension
from distutils.command.build_clib import build_clib
from distutils.ccompiler import new_compiler
from distutils.spawn import find_executable
from setuptools.command.build_ext import build_ext as _build_ext
from wheel.bdist_wheel import bdist_wheel as _bdist_wheel
from setuptools.command.install import install
from distutils.file_util import copy_file

_DEBUG = False
_DEBUG_LEVEL = 0

version="0.0.1"

if "BUILD_NUM" in os.environ.keys():
    version += "." + os.environ["BUILD_NUM"]

class InstallCmd(install):
    def run(self):
        install.run(self)
#        dot = os.path.join(
#                self.install_lib, 
#                "graphviz_bin", 
#                "bin", 
#                "dot")
#        st = os.stat(dot)
#        os.chmod(dot, st.st_mode | stat.S_IEXEC)

class BdistWheel(_bdist_wheel):

    def finalize_options(self):
        _bdist_wheel.finalize_options(self)
        self.root_is_pure = False

class build_ext(_build_ext):
    def run(self):
        print("build_ext::run")
        super().run()
        self.copy_extensions_to_source()

    def copy_extensions_to_source(self):
        """ Like the base class method, but copy libs into proper directory in develop. """
        print("copy_extensions_to_source")
        super().copy_extensions_to_source()

        build_py = self.get_finalized_command("build_py")

        cwd = os.getcwd()
        ext = self.extensions[0]
        fullname = self.get_ext_fullname(ext.name)
        filename = self.get_ext_filename(fullname)
        modpath = fullname.split(".")
        package = ".".join(modpath[:-1])
        package_dir = build_py.get_package_dir(package)

        print("Copy dot")
        copy_file(
            os.path.join(cwd, "result", "dot"),
            os.path.join(package_dir, "dot"))

        dest_filename = os.path.join(package_dir, filename)

        print("package_dir: %s dest_filename: %s" % (package_dir, dest_filename))


setup(
  name="pygraphviz-bin",
  version=version,
  packages=['graphviz_bin'],
  package_dir = {'' : 'src'},
  package_data = {'graphviz_bin' : [ 'dot*']},
  author = "Matthew Ballance",
  author_email = "matt.ballance@gmail.com",
  description = ("Pre-compiled GraphViz wrapped in Python"),
  license = "Apache 2.0",
  keywords = ["GraphViz", "Dot"],
  url = "https://github.com/mballance/pygraphviz-bin",
  include_package_data=True,
  install_requires=[
  ],
  setup_requires=[
    'setuptools_scm',
    'cython'
  ],
  ext_modules=[
      Extension("graphviz_bin.stub",
          sources=["src/stub.pyx"])],
  cmdclass={
#      'install': InstallCmd,
#      'bdist_wheel': BdistWheel,
      'build_ext': build_ext}
)


