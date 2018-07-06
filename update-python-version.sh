#!/bin/bash

# update the .python-version file to match pyenv installed versions
pyenv whence python > .python-versions
