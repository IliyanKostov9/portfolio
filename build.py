#   -*- coding: utf-8 -*-
import os

from pybuilder.core import init, use_plugin

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.coverage")
use_plugin("python.distutils")


name = "portfolio"
default_task = "publish"


@init
def set_properties(project):
    project.set_property("dir_source_main_python", "src")
    project.set_property("dir_source_unittest_python", "tests")
    project.set_property("dir_source_main_scripts", "scripts")

    # Install deps
    project.build_depends_on("mockito")
    project.build_depends_on("Django")
