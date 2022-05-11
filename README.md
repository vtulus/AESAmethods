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
  - land-system change
    - global
  - freshwater use
    - global
  - change in biosphere integrity
    - functional diversity
      - total
      - direct land use
      - CO2eq emissions

#### Changelog
See [CHANGELOG](CHANGELOG.md)
## Usage
```python
import brightway2 as bw
import aesa_pbs

aesa_pbs.__version__ # optionally check current version

# open an existing bw project or create a new one
bw.projects.set_current("<YOURPROJECT NAME>")

# install AESA PBs methods
aesa_pbs.add_aesa_pbs(verbose=True)
# (optionally set `verbose=False` to avoid seeing the applied strategies)
```

## Installation
Currently this package can be only installed locally.  
To do so one option can be:

1. Download zip file of the package
2. Un-zip to a folder on your machine
3. Open CLI:

```bash
# in the activated environment
cd <PATH TO PACKAGE FOLDER>
pip install . --use-feature=in-tree-build
```

## References
[Ryberg, M. W.; Owsianiak, M.; Richardson, K.; Hauschild, M. Z.](https://doi.org/10.1016/j.ecolind.2017.12.065) developed CFs for the following categories of AESA (PBs-LCIA): "climate change", "ozone depletion", "ocean acidification", "biogeochemical flows", "land-system change" and "freshwater use".  
[Galán-Martín, Á.; Tulus, V.; Díaz, I.; Pozo, C.; Pérez-Ramírez, J.; Guillén-Gosálbez, G.](https://doi.org/10.1016/j.oneear.2021.04.001) developed CFs for "change in biosphere integrity, functional diversity" of AESA (PBs-LCIA)

## Maintainer
- [V.Tulus](https://github.com/vtulus)

## License
[BSD 3-Clause License](LICENSE). Copyright (c) 2022, Victor Tulus. All rights reserved.