# Minimal makefile for Sphinx documentation
#

# You can set these variables from the command line.
SPHINXOPTS    =
SPHINXBUILD   = sphinx-build
SPHINXPROJ    = jsonmask
SOURCEDIR     = .
BUILDDIR      = _build

.DEFAULT_GOAL := html

help:
	@$(SPHINXBUILD) -M help "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)

test:
	@$(SPHINXBUILD) -nWT -b dummy . _build/html

.PHONY: help test Makefile

# Catch-all target: route all unknown targets to Sphinx using the new
# "make mode" option.  $(O) is meant as a shortcut for $(SPHINXOPTS).
%: Makefile
	@$(SPHINXBUILD) -M $(@F) "$(SOURCEDIR)" "$(BUILDDIR)" $(SPHINXOPTS) $(O)
