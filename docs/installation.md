## Installation

!!!note
    This guide describes typical installations of PlantCV Geospatial.
    PlantCV Geospatial can be installed from source for developers or users who want to test the latest features.
    Please see our [Contributing Guide](CONTRIBUTING.md) for more information.

### Table of contents
1. [Supported platforms and dependencies](#dependencies)
2. [Install via a package manager](#install)
    1. [PyPI](#pypi)
3. [Installing PlantCV-Geospatial for contributors](#contributors)

### Supported platforms and dependencies <a name="dependencies"></a>
- Linux 64-bit, x86 processors
- macOS x86 (Intel) and M (ARM) processors
- Windows 64-bit, x86 processors

PlantCV Geospatial requires Python (tested with versions 3.11, 3.12, and 3.13), PlantCV v5, and these
[Python packages](https://github.com/danforthcenter/plantcv-geospatial/blob/main/pyproject.toml).
Additionally, we recommend installing [JupyterLab](https://jupyter.org/).

!!!note
    We recommend installing PlantCV Geospatial in a virtual environment, which is a self-contained Python environment that
    includes PlantCV Geospatial and its dependencies. Virtual environments are used to avoid conflicts between packages and
    can increase the reproducibility of your work by isolating package versions for specific projects.

### Install via a package manager  <a name="install"></a>

#### PyPI <a name="pypi"></a>

```bash
pip install plantcv-geospatial

```

Or with optional (but recommended) dependencies:

```bash
pip install plantcv-geospatial jupyterlab ipympl

```

### Installing PlantCV-Geospatial for contributors <a name="contributors"></a>
Before getting started, please read our [contributor guidelines](CONTRIBUTING.md) and [code of conduct](CODE_OF_CONDUCT.md).

You can follow the
[PlantCV Installation for Contributor Guide](https://plantcv.readthedocs.io/en/latest/installation/#contributors) and then
continue with the instructions below to add PlantCV-Geospatial to your development environment.

Follow the [PlantCV Installation](https://plantcv.readthedocs.io/en/latest/installation/#conda) guide. Then, install
PlantCV-Geospatial in editable mode so that it updates as you work on new features/updates.

```bash
# Activate the plantcv environment (you will have to do this each time you start a new session)
conda activate plantcv
# Install plantcv-geospatial in editable mode so that it updates as you work on new features/updates
git clone https://github.com/danforthcenter/plantcv-geospatial.git 
cd plantcv-geospatial 
pip install -e .

```
