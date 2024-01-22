# AESA methods implemented for use in [Brightway](https://github.com/brightway-lca/brightway2)

- [AESA methods implemented for use in Brightway](#aesa-methods-implemented-for-use-in-brightway)
  - [Implemented methods and impact categories](#implemented-methods-and-impact-categories)
    - [AESA (PBs-LCIA)](#aesa-pbs-lcia)
      - [Changelog](#changelog)
  - [Usage](#usage)
  - [Installation](#installation)
  - [References](#references)
  - [Maintainer](#maintainer)
  - [License](#license)

## Implemented methods and impact categories
### AESA (PBs-LCIA)
  - climate change
    - atmospheric CO2 concentration
    - energy imbalance at top-of-atmosphere
  - ozone depletion
    - stratospheric O3 concentration
  - ocean acidification
    - carbonate ion concentration
  - biogeochemical flows
    - phosphorus
    - nitrogen
      - inverse modelling, surface water
      - directly fixated
  - land-system change
    - global
  - freshwater use
    - global
  - change in biosphere integrity
    - functional diversity
      - total
      - direct land use
      - CO2eq emissions
  - atmospheric aerosol loading

#### Changelog
See [CHANGELOG](CHANGELOG.md)
## Usage
```python
import brightway2 as bw
import aesa_pbs

aesa_pbs.__version__ # optionally check current version

# open an existing bw project or create a new one
bw.projects.set_current("<YOUR-PROJECT-NAME>")

# install AESA PBs methods
aesa_pbs.add_aesa_pbs(verbose=True)
# (optionally set `verbose=False` to avoid seeing the applied strategies)

# adapt a database for quantification of directly fixated nitrogen
# 1. retrieve list of nitrogenous fertilizers from "<DATABASE-NAME>"
nflow_activities = aesa_pbs.get_nitrogenous_fertilizers("<DATABASE-NAME>")

# 2. create exchanges for 'nitrogen fertilizer' in `activities` if they don't exist already.
aesa_pbs.update_nitrogen_fertilizer_exchanges(nflow_activities, show_updated=True)
```
See [example](notebooks/examples/how-to-use-aesa-methods.ipynb) for more detailed explanation of the usage.

## Installation
Currently this package can be only installed locally.  
To do so one option can be:

1. Download the zip file of the package
2. Un-zip to a folder on your machine (copy path to folder)
3. Open CLI:

```bash
# in the activated environment
pip install "<PATH-TO-PACKAGE-FOLDER>"
# Note: if pip<21.3, use `--use-feature=in-tree-build` flag
```

## References
[Ryberg, M. W.; Owsianiak, M.; Richardson, K.; Hauschild, M. Z.](https://doi.org/10.1016/j.ecolind.2017.12.065) developed CFs for the following categories of AESA (PBs-LCIA): "climate change", "ozone depletion", "ocean acidification", "biogeochemical flows", "land-system change" and "freshwater use".  
[Galán-Martín, Á.; Tulus, V.; Díaz, I.; Pozo, C.; Pérez-Ramírez, J.; Guillén-Gosálbez, G.](https://doi.org/10.1016/j.oneear.2021.04.001) developed CFs for "change in biosphere integrity, functional diversity" of AESA (PBs-LCIA)

## Maintainer
- [V.Tulus](https://github.com/vtulus)

## License
[BSD 3-Clause License](LICENSE). Copyright (c) 2022, Victor Tulus. All rights reserved.
