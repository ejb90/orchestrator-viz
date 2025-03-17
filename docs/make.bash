#!/bin/bash

sphinx-apidoc -o . ../viz
sphinx-build -b html . out/