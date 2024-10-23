#   -*- coding: utf-8 -*-
import os
import shutil

from pybuilder.core import depends, task, use_plugin, init

use_plugin("python.core")
use_plugin("python.unittest")
use_plugin("python.flake8")
use_plugin("python.distutils")


name = "ycappuccino_storage"
default_task = "publish"
version = "0.1.0"


@init
def set_properties(project):
    project.set_property("core", False)  # default is True
    project.depends_on_requirements("requirements.txt")
    project.depends_on(
        "ycappuccino_core", url="git+https://github.com/Y-Cappuccino/core.git"
    )
