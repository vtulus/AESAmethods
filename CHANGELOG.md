# Changelog
## 0.9.0 (2022-07-25)
- Files containing CFs information are now stored in .yaml format (instead of .xlsx)
  - `add_aesa_pbs()` still reads .xlsx files, which are generated in the background on execution with the help of the functionality added by the `DataConverter` class
- Add check for duplicated CFs in .yaml files

## 0.8.8 (2022-06-13)
- Add notebooks with use examples
- ---
- Sync `premise`-based branch with this version (v0.8.8+premise)

## 0.8.7 (2022-05-16)
- Add usage and installation instructions to README
- Add **method for quantification of direct N fixation**
---
- Sync `premise`-based branch with this version (v0.8.7+premise)

## 0.8.6 (2022-05-11)
- Split **CBI method** into 3 subcategories:
   - total
   - direct land use
   - CO2eq emissions
---
- Sync `premise`-based branch with this version (v0.8.6+premise) 

## 0.8.5 (2022-04-19)
- Add `__version__` to method name
- Correct `solve_lca()`

## 0.8.4 (2022-04-13)
- Add "Occupation, lake, artificial" (land) CF to **CBI method** (CF =  7.69231E-13)

## 0.8.3 (2022-04-13)
Change/Add CFs of **FWU method**:
- Add "Water, unspecified natural origin" (fossil well and in ground) (CF = 1E-9)
- Add "Water, cooling, unspecified natural origin" (CF = 1E-9)
- Add "Water, turbine use, unspecified natural origin" (CF = -1E-9)
- Add "Water" (fossil well and ground- long-term) (CF = 1E-9)

## 0.8.2 (2022-04-11)
- Add `checkPBsmethod.ipynb` to `notebooks\test` folder
- Add `utils.py`
- Add strategies to generate "subcategories" for **CBI method**
- Add strategy `add_subcategory_methane_air` for **CBI method**
---
- Add branch for `premise`-based version of the AESA methods
  - Add CFs for specific CO2 flows to account for NETs, see e44988eeba336

## 0.8.1 (2022-03-25)
- Move notebooks to `notebooks\dev` folder
- Move source code to `src` folder
- Add package setup files
- Add option to suppress output of `aesa_pbs.add_aesa_pbs()`

## 0.8.0 (2022-03-22)
AESA (PBs-LCIA) method converted to Brightway-readable format.

> **NOTE**: Changelog for versions `<0.8.0` refers to the implementation of the method in SimaPro

## 0.7.2 (2020-09-09)
CFs for CO2 associated with land transformation are modified consistently with the IPCC recommendations and considering the ecoinvent approach, in which pulse CO2 emissions for Land Use Change are already "amortized" over the plantation lifetime.

The characterization factors for CO2 fossil and CO2, land transformation, are now the same, consistently with other common LCA methodologies.

### **Climate change - CO2 concentration**
CF for "Carbon dioxide, land transformation" has been changed from 8.97E-14 to 2.69E-11 (ppm / kg CO2)

### **Climate change - Energy imbalance**
CF for "Carbon dioxide, land transformation" has been changed from 1.18E-15 to 3.53E-13 (Wm-2 / kg CO2)

### **Ocean acidification**
CF for "Carbon dioxide, land transformation" has been changed from 2.74E-16 to 8.22E-14 (Omega Aragon / kg CO2)

## 0.7.1 (2020-08-14)
### **Damage assessment (% of BII loss)**
The following types of land are added (based on [Hanafiah et al.](https://doi.org/10.1016/j.jclepro.2012.06.016)):
- Occupation, pasture, man made, organic (CF: 0.3)
- Occupation, permanent crop, irrigated (CF: 0.9)
- Occupation, permanent crop, irrigated, extensive (CF: 0.7)
- Occupation, permanent crop, irrigated, intensive (CF: 0.9)
- Occupation, permanent crop, non-irrigated (CF: 0.9)
- Occupation, permanent crop, non-irrigated, extensive (CF: 0.7)
- Occupation, permanent crop, non-irrigated, intensive(CF: 0.9)
- Urban, green areas (0.95) . not in ecoinvent
- Occupation, annual crop, non-irrigated (CF: 0.9
- Occupation, lakes, artificial (CF: 1) . not in ecoinvent
- Occupation, forest, used (CF: 0.5) . not in ecoinvent
- Occupation, agriculture (CF: 0.9) . not in ecoinvent
- Occupation, annual crop, greenhouse (CF: 0.9) 

> Note: *land types and characterization factors added in "(not PBs) Biological footprint, LU**" (BIILoss.m2a)*

## 0.7.0 (2020-07-21)
Updates from v0.6.5

### **Biogeochemical flows - P**  
The following elementary flows are now taken into account:
- Phosphate, (CF = 2.81E-10) 
- Phosphorous, total, (8.61E-10)
- Phosphorous,  (8.61E-10)
  
> Emission to Lake and River are now considered.  
> In the v0.65 only Phosphorous,  (8.61E-10) to Lake was considered.

### **Biogeochemical flows - N**  
The following elementary flows are now taken into account:
- Nitrate, (CF = 5.51E-9)
- Nitrogen, (CF = 2.44E-8)
- Nitrogen, total, (CF = 2.44E-8)

> Emission to Lake and River are now considered.  
> In v0.65 only Nitrate,  (5.51E-9) to Lake/River was considered.

### **Damage assessment (% of BII loss)**  
`At` updated from 1.08E+14 to 1.30E+14 m2  

> In this version the total area is consistent with [IMAGE model](https://models.pbl.nl/image/index.php/Download_packages)  
> In 0.65 the Earth’s total Area considered was 1.08E+14 m2, according to ReCiPe2016.

Mean Species Abundance (MSA) is used as a proxy of Biological Intactness Index (BII)
> *"The main difference between MSA and BII is that every hectare is given equal weight in MSA, whereas BII gives more weight to species rich areas."*  
> \-[Alkemade et al. 2009](https://doi.org/10.1007/s10021-009-9229-5)

`GWP` (kg CO2 eq): Global Warming Potential (calculated using "ReCiPe 2016 (H) midpoint" characterization factors)  
`BF_LU` (BII loss*m2a): Biological footprint for Land Use  
`BF_CC` (BII loss*m2a): Biological footprint for Climate Change  
`At` (m2a): Earth’s total land (used in 1 yr) = 1.30E+14   
`MSA`: Mean species abundance
> (0: no species; 1: undisturbed biodiversity)  

`(1-MSA)`: Loss of mean species abundance
> (0: no loss of species; 1: complete loss of species)  

[Hanafiah et al.](https://doi.org/10.1016/j.jclepro.2012.06.016) provide `(1-MSA)` values for different land types present in SimaPro. These values are used as the characterization factors to assess "Biological footprint, LU". `(1-MSA)` values are applied to land use inventory flows (m2a).

`BF_LU` is calculated as `SUM[Ai*(1-MSAi)]` for "i-th" land use type.

According to [Hanafiah et al.](https://doi.org/10.1016/j.jclepro.2012.06.016), `BF_CC` can be calculated as `BF_CC = 0.27 * GWP`

"In damage assessment" `BII loss` is finally calculated as `% BII loss = 100 x (BF_LU+BF_CC)/At`

The factor applied to `GWP` is calculated as `100 x (0.27/At) = 2.07692E-13`  
The factor applied to `BF_LU` is calculated as `100 x (1/At) = 7.69231E-13`

> NOTE: **Indicators with the prefix "(not PBs)" are used exclusively for the damage assessment, where the final indicator is provided.**

### **N-flows to freshwater considers lake and river sub-compartments**
### **Alternative approaches to address PBs, Biodiversity and Nitrogen Flow**
Are available in the supplementary methods of SUPERLAB project

## < 0.6.5 (2019)
Add CF for N2O (dinitrogen monoxide) in **Ozone depletion PB**.  
From [Algunaibet et al. 2019](https://doi.org/10.1039/c8ee03423k): 
> "Although the existing method to compute PBs does not assign a characterization factor that quantifies the N2O impact on the stratospheric ozone depletion PB, N2O emissions do exert a noticeable pressure on the ozone layer. Therefore, we here expand the existing method developed by Ryberg et al. by designing a characterization factor that quantifies the impact of N2O emissions on the stratospheric ozone depletion PB. In essence, we first convert the N2O emissions to CFC-11 equivalent (i.e., 0.018 kg of CFC-11 equivalent per kg of N2O) and then apply the characterization factor that links CFC-11 to the stratospheric ozone depletion PB available in the existing framework."
- dinitrogen monoxide (air, all subcategories) (CF = 1.41E-10)
