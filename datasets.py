import geopandas
import pandas
import rasterio
import rasterio.io
import shapely.geometry
import re

def geochemical_analysis_2022_09_11(target_element: str) -> pandas.DataFrame:
    data_frame = pandas.read_excel("Data/Geochemical Analysis 20220911.xlsx")

    x_mass=["SIO2", "TIO2", "AL2O3","FE2O3T","FEOT","MNO","MGO","CAO","NA2O","K2O","P2O5","H2O", "CR2O3"]
    x_impurities=["LI", "SC", "V","CR","CO","NI","CU","ZN","GA","MO","W","SN","SB","RB","SR","Y","NB","ZR","CS","CD","BA","LA","CE","PR","ND","SM","EU","GD","TB","DY","HO","ER","TM","YB","LU","HF","TA","PB","TH","U","AU","AG","S","AS_","SE","TE","GE","BI","TL","BE","B","F","CL","INDIUM"]
    x_ratios=["Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn", "Rb_MnO", "MnO_MgO"]
    x_impurities.remove(target_element)

    x_labels = x_mass + x_impurities + x_ratios
    y_labels = [target_element]

    data_frame = clean(data_frame, x_mass + x_impurities, y_labels)
    data_frame = compute_ratios(data_frame, x_ratios, x_mass + x_impurities + [target_element])

    data_frame.x_labels = lambda : x_labels
    data_frame.y_labels = lambda : y_labels

    return data_frame

def geochemical_analysis_2023_01_23(target_element: str) -> pandas.DataFrame:
    data_frame = pandas.read_excel("Data/Andes Master Geochem for ML 20Jan23 LSRGB subset.xlsx")

    x_mass=["SIO2", "TIO2", "AL2O3","FE2O3T","FEOT","MNO","MGO","CAO","NA2O","K2O","P2O5","H2O", "CR2O3"]
    x_impurities=["LI", "SC", "V","CR","CO","NI","CU","ZN","GA","MO","W","SN","SB","RB","SR","Y","NB","ZR","CS","CD","BA","LA","CE","PR","ND","SM","EU","GD","TB","DY","HO","ER","TM","YB","LU","HF","TA","PB","TH","U","AU","AG","S","AS_","SE","TE","GE","BI","TL","BE","B","F","CL","INDIUM"]
    x_ratios=["Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn", "Rb_MnO", "MnO_MgO"]
    x_impurities.remove(target_element)

    x_labels = x_mass + x_impurities + x_ratios
    y_labels = [target_element]

    data_frame = clean(data_frame, x_mass + x_impurities, y_labels)
    data_frame = compute_ratios(data_frame, x_ratios, x_mass + x_impurities + [target_element])

    data_frame.x_labels = lambda : x_labels
    data_frame.y_labels = lambda : y_labels

    return data_frame

def geochemical_analysis_2023_07_16(target_element: str) -> pandas.DataFrame:
    data_frame = pandas.read_excel("Data/Andes Master Geochem 16 July 2023.xlsx")

    x_mass = ["SIO2_wt%", "TIO2_wt%", "AL2O3_wt%", "FE2O3T_wt%", "FEOT_wt%", "MNO_wt%", "MGO_wt%", "CAO_wt%", "NA2O_wt%", "K2O_wt%", "P2O5_wt%", "H2O_wt%", "CR2O3_wt%"]
    x_impurities=["Li_ppm", "Sc_ppm", "V_ppm", "Cr_ppm", "Co_ppm", "Ni_ppm", "Cu_ppm", "Zn_ppm", "Ga_ppm", "Mo_ppm", "W_ppm", "Sn_ppm", "Sb_ppm", "Rb_ppm", "Sr_ppm", "Y_ppm", "Nb_ppm", "Zr_ppm", "Cs_ppm", "Cd_ppm", "Ba_ppm", "La_ppm", "Ce_ppm", "Pr_ppm", "Nd_ppm", "Sm_ppm", "Eu_ppm", "Gd_ppm", "Tb_ppm", "Dy_ppm", "Ho_ppm", "Er_ppm", "Tm_ppm", "Yb_ppm", "Lu_ppm", "Hf_ppm", "Ta_ppm", "Pb_ppm", "Th_ppm", "U_ppm", "Au_ppb", "Ag_ppm", "S_%", "As_ppm", "Se_ppm", "Te_ppm", "Ge_ppm", "Bi_ppm", "Tl_ppm", "Be_ppm", "B_ppm", "F_ppm", "Cl_ppm", "In_ppm"]
    x_ratios=["Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn", "Rb_MnO", "MnO_MgO"]
    x_impurities.remove(target_element)

    x_labels = x_mass + x_impurities + x_ratios
    y_labels = [target_element]

    data_frame.x_labels = lambda : x_labels
    data_frame.y_labels = lambda : y_labels

    data_frame = clean(data_frame, x_mass + x_impurities, y_labels)
    data_frame = compute_ratios(data_frame, x_ratios, x_mass + x_impurities + [target_element])

    return data_frame

def geochemical_analysis_2023_10_17(target_element: str) -> pandas.DataFrame:
    data_frame = pandas.read_excel("Data/Andes Master Geochem 17 Oct 2023.xlsx")

    x_mass = ["SIO2_wt%", "TIO2_wt%", "AL2O3_wt%", "FE2O3T_wt%", "FEOT_wt%", "MNO_wt%", "MGO_wt%", "CAO_wt%", "NA2O_wt%", "K2O_wt%", "P2O5_wt%", "H2O_wt%", "CR2O3_wt%"]
    x_impurities=["Li_ppm", "Sc_ppm", "V_ppm", "Cr_ppm", "Co_ppm", "Ni_ppm", "Cu_ppm", "Zn_ppm", "Ga_ppm", "Mo_ppm", "W_ppm", "Sn_ppm", "Sb_ppm", "Rb_ppm", "Sr_ppm", "Y_ppm", "Nb_ppm", "Zr_ppm", "Cs_ppm", "Cd_ppm", "Ba_ppm", "La_ppm", "Ce_ppm", "Pr_ppm", "Nd_ppm", "Sm_ppm", "Eu_ppm", "Gd_ppm", "Tb_ppm", "Dy_ppm", "Ho_ppm", "Er_ppm", "Tm_ppm", "Yb_ppm", "Lu_ppm", "Hf_ppm", "Ta_ppm", "Pb_ppm", "Th_ppm", "U_ppm", "Au_ppb", "Ag_ppm", "S_%", "As_ppm", "Se_ppm", "Te_ppm", "Ge_ppm", "Bi_ppm", "Tl_ppm", "Be_ppm", "B_ppm", "F_ppm", "Cl_ppm", "In_ppm"]
    x_ratios=["Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn", "Rb_MnO", "MnO_MgO"]
    x_impurities.remove(target_element)

    x_labels = x_mass + x_impurities + x_ratios
    y_labels = [target_element]

    data_frame.x_labels = lambda : x_labels
    data_frame.y_labels = lambda : y_labels

    data_frame = clean(data_frame, x_mass + x_impurities, y_labels)
    data_frame = compute_ratios(data_frame, x_ratios, x_mass + x_impurities + [target_element])

    return data_frame

def geochemical_analysis_2023_12_19(target_element: str) -> pandas.DataFrame:
    data_frame = pandas.read_excel("Data/Andes Master Geochem 19 Dec 2023_revised.xlsx")

    x_mass = ["SIO2_wt%", "TIO2_wt%", "AL2O3_wt%", "FE2O3T_wt%", "FEOT_wt%", "MNO_wt%", "MGO_wt%", "CAO_wt%", "NA2O_wt%", "K2O_wt%", "P2O5_wt%", "H2O_wt%", "CR2O3_wt%"]
    x_impurities=["Li_ppm", "Sc_ppm", "V_ppm", "Cr_ppm", "Co_ppm", "Ni_ppm", "Cu_ppm", "Zn_ppm", "Ga_ppm", "Mo_ppm", "W_ppm", "Sn_ppm", "Sb_ppm", "Rb_ppm", "Sr_ppm", "Y_ppm", "Nb_ppm", "Zr_ppm", "Cs_ppm", "Cd_ppm", "Ba_ppm", "La_ppm", "Ce_ppm", "Pr_ppm", "Nd_ppm", "Sm_ppm", "Eu_ppm", "Gd_ppm", "Tb_ppm", "Dy_ppm", "Ho_ppm", "Er_ppm", "Tm_ppm", "Yb_ppm", "Lu_ppm", "Hf_ppm", "Ta_ppm", "Pb_ppm", "Th_ppm", "U_ppm", "Au_ppb", "Ag_ppm", "S_%", "As_ppm", "Se_ppm", "Te_ppm", "Ge_ppm", "Bi_ppm", "Tl_ppm", "Be_ppm", "B_ppm", "F_ppm", "Cl_ppm", "In_ppm"]
    x_ratios=["Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn", "Rb_MnO", "MnO_MgO"]
    x_impurities.remove(target_element)

    x_labels = x_mass + x_impurities + x_ratios
    y_labels = [target_element]

    data_frame.x_labels = lambda : x_labels
    data_frame.y_labels = lambda : y_labels

    data_frame = clean(data_frame, x_mass + x_impurities, y_labels)
    data_frame = compute_ratios(data_frame, x_ratios, x_mass + x_impurities + [target_element])

    return data_frame

def satellite_analysis_2023_01_20(target_element: str) -> pandas.DataFrame:
    data_frame = pandas.read_excel("Data/Andes Master Geochem for ML 20Jan23 LSRGB subset.xlsx")
    
    return satellite_analysis(data_frame, target_element)

def satellite_analysis_2023_10_17(target_element: str) -> pandas.DataFrame:
    data_frame = pandas.read_excel("Data/Andes Master Geochem 17 Oct 2023 LSRGB subset.xlsx")
    
    return satellite_analysis(data_frame, target_element)

def satellite_analysis(data_frame: pandas.DataFrame, target_element: str) -> pandas.DataFrame:

    x_labels = [f"{color}{scale}" for scale in ["30", "90", "210"] for color in ["R", "G", "B"]]
    y_labels = [target_element]

    data_frame.x_labels = lambda : x_labels
    data_frame.y_labels = lambda : y_labels

    data_frame = clean(data_frame, x_labels, y_labels)

    return data_frame


def satellite_image_2019() -> rasterio.io.DatasetReader:
    return satellite_image(r"./Data/2019_Mosaic_30m_Nclip_4o2_6o7_PC3_v4_SUTM19.tif")

def satellite_image_2023() -> rasterio.io.DatasetReader:
    return satellite_image(r"./Data/MapBox_Image_Corani3.tif")

def satellite_image(satellite_image_file_path) -> rasterio.io.DatasetReader:
    satellite_image = rasterio.open(satellite_image_file_path)

    satellite_image.x_resolution = (satellite_image.bounds.right - satellite_image.bounds.left) / satellite_image.width
    satellite_image.y_resolution = (satellite_image.bounds.top - satellite_image.bounds.bottom) / satellite_image.height

    satellite_image_bands = []

    for i in range(0, satellite_image.count):
        satellite_image_bands.append(satellite_image.read(i + 1))

    satellite_image.bands = satellite_image_bands

    return satellite_image


def geochemical_satellite_analysis_2023_01_20(satellite_image: rasterio.io.DatasetReader, target_column: str, positive_threshold: float=None, drop_out_of_bounds: bool=True) -> geopandas.GeoDataFrame:
    satellite_data_frame = pandas.read_excel("Data/Andes Master Geochem for ML 20Jan23 LSRGB subset.xlsx")
    
    satellite_data_frame.x_labels = lambda : ["EAST", "NORTH", "ALTITUDE", "SIO2", "TIO2", "AL2O3", "FE2O3T", "FEOT", "MNO", "MGO", "CAO", "NA2O", "K2O", "P2O5", "H2O", "CR2O3", "LOI", "TOTAL", "SC", "V", "CR", "CO", "NI", "CU", "ZN", "GA", "MO", "W", "SN", "SB", "RB", "SR", "Y", "NB", "ZR", "CS", "CD", "BA", "LA", "CE", "PR", "ND", "SM", "EU", "GD", "TB", "DY", "HO", "ER", "TM", "YB", "LU", "HF", "TA", "PB", "TH", "U", "AU", "AG", "S", "AS_", "SE", "TE", "GE", "BI", "TL", "BE", "B", "F", "CL", "INDIUM", "Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn"]
    satellite_data_frame.y_labels = lambda : [target_column]
    
    satellite_data_frame = clean(satellite_data_frame, satellite_data_frame.x_labels(), satellite_data_frame.y_labels())
    
    return geochemical_satellite_analysis(satellite_data_frame, satellite_image, target_column, positive_threshold, drop_out_of_bounds)

def geochemical_satellite_analysis_2023_10_17(satellite_image: rasterio.io.DatasetReader, target_column: str, positive_threshold: float=None, drop_out_of_bounds: bool=True) -> geopandas.GeoDataFrame:
    satellite_data_frame = pandas.read_excel("Data/Andes Master Geochem 17 Oct 2023.xlsx")
    
    x_mass = ["SIO2_wt%", "TIO2_wt%", "AL2O3_wt%", "FE2O3T_wt%", "FEOT_wt%", "MNO_wt%", "MGO_wt%", "CAO_wt%", "NA2O_wt%", "K2O_wt%", "P2O5_wt%", "H2O_wt%", "CR2O3_wt%"]
    x_impurities=["Li_ppm", "Sc_ppm", "V_ppm", "Cr_ppm", "Co_ppm", "Ni_ppm", "Cu_ppm", "Zn_ppm", "Ga_ppm", "Mo_ppm", "W_ppm", "Sn_ppm", "Sb_ppm", "Rb_ppm", "Sr_ppm", "Y_ppm", "Nb_ppm", "Zr_ppm", "Cs_ppm", "Cd_ppm", "Ba_ppm", "La_ppm", "Ce_ppm", "Pr_ppm", "Nd_ppm", "Sm_ppm", "Eu_ppm", "Gd_ppm", "Tb_ppm", "Dy_ppm", "Ho_ppm", "Er_ppm", "Tm_ppm", "Yb_ppm", "Lu_ppm", "Hf_ppm", "Ta_ppm", "Pb_ppm", "Th_ppm", "U_ppm", "Au_ppb", "Ag_ppm", "S_%", "As_ppm", "Se_ppm", "Te_ppm", "Ge_ppm", "Bi_ppm", "Tl_ppm", "Be_ppm", "B_ppm", "F_ppm", "Cl_ppm", "In_ppm"]
    x_ratios=["Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn", "Rb_MnO", "MnO_MgO"]

    satellite_data_frame.x_labels = lambda : ["EAST", "NORTH", "ALTITUDE", ] + x_mass + ["LOI_wt%", "TOTAL_wt%"] + x_impurities + x_ratios
    satellite_data_frame.y_labels = lambda : [target_column]
    
    satellite_data_frame = clean(satellite_data_frame, x_mass + x_impurities, satellite_data_frame.y_labels())
    satellite_data_frame = compute_ratios(satellite_data_frame, x_ratios, x_mass + x_impurities + [target_column])

    return geochemical_satellite_analysis(satellite_data_frame, satellite_image, target_column, positive_threshold, drop_out_of_bounds)

def geochemical_satellite_analysis_2023_12_19(satellite_image: rasterio.io.DatasetReader, target_column: str, positive_threshold: float=None, drop_out_of_bounds: bool=True) -> geopandas.GeoDataFrame:
    satellite_data_frame = pandas.read_excel("Data/Andes Master Geochem 19 Dec 2023_revised.xlsx")
    
    x_mass = ["SIO2_wt%", "TIO2_wt%", "AL2O3_wt%", "FE2O3T_wt%", "FEOT_wt%", "MNO_wt%", "MGO_wt%", "CAO_wt%", "NA2O_wt%", "K2O_wt%", "P2O5_wt%", "H2O_wt%", "CR2O3_wt%"]
    x_impurities=["Li_ppm", "Sc_ppm", "V_ppm", "Cr_ppm", "Co_ppm", "Ni_ppm", "Cu_ppm", "Zn_ppm", "Ga_ppm", "Mo_ppm", "W_ppm", "Sn_ppm", "Sb_ppm", "Rb_ppm", "Sr_ppm", "Y_ppm", "Nb_ppm", "Zr_ppm", "Cs_ppm", "Cd_ppm", "Ba_ppm", "La_ppm", "Ce_ppm", "Pr_ppm", "Nd_ppm", "Sm_ppm", "Eu_ppm", "Gd_ppm", "Tb_ppm", "Dy_ppm", "Ho_ppm", "Er_ppm", "Tm_ppm", "Yb_ppm", "Lu_ppm", "Hf_ppm", "Ta_ppm", "Pb_ppm", "Th_ppm", "U_ppm", "Au_ppb", "Ag_ppm", "S_%", "As_ppm", "Se_ppm", "Te_ppm", "Ge_ppm", "Bi_ppm", "Tl_ppm", "Be_ppm", "B_ppm", "F_ppm", "Cl_ppm", "In_ppm"]
    x_ratios=["Rb_K2O", "Rb_Yb", "Rb_La", "K2O_MgO", "Rb_MgO", "U_Ba", "Ba_La", "U_Th", "Rb_Sn", "K2O_Sn", "Rb_MnO", "MnO_MgO"]

    satellite_data_frame.x_labels = lambda : ["EAST", "NORTH", "ALTITUDE", ] + x_mass + ["LOI_wt%", "TOTAL_wt%"] + x_impurities + x_ratios
    satellite_data_frame.y_labels = lambda : [target_column]
    
    satellite_data_frame = clean(satellite_data_frame, x_mass + x_impurities, satellite_data_frame.y_labels())
    satellite_data_frame = compute_ratios(satellite_data_frame, x_ratios, x_mass + x_impurities + [target_column])

    return geochemical_satellite_analysis(satellite_data_frame, satellite_image, target_column, positive_threshold, drop_out_of_bounds)


def geochemical_satellite_analysis(satellite_data_frame, satellite_image: rasterio.io.DatasetReader, target_column: str, positive_threshold: float=None, drop_out_of_bounds: bool=True) -> geopandas.GeoDataFrame:

    if drop_out_of_bounds:
        def is_out_of_bounds(row: pandas.core.series.Series) -> bool:
            return row["EAST"] < satellite_image.bounds.left or row["EAST"] > satellite_image.bounds.right or row["NORTH"] > satellite_image.bounds.top or row["NORTH"] < satellite_image.bounds.bottom

        satellite_data_frame["OutOfBounds"] = satellite_data_frame.apply(is_out_of_bounds, axis=1)
        satellite_data_frame = satellite_data_frame[satellite_data_frame["OutOfBounds"] == False]
        satellite_data_frame = satellite_data_frame.drop(columns=["OutOfBounds"])

    def create_geometry(row: pandas.core.series.Series) -> shapely.geometry.Point:
        return shapely.geometry.Point(row["EAST"], row["NORTH"])

    satellite_data_frame["Geometry"] = satellite_data_frame.apply(create_geometry, axis=1)
    if positive_threshold is not None:
        satellite_data_frame[f"{target_column}_THRESHOLD"] = satellite_data_frame[target_column].ge(positive_threshold)
    satellite_data_frame = geopandas.GeoDataFrame(satellite_data_frame, crs=satellite_image.crs, geometry="Geometry")
    return satellite_data_frame

def clean(data_frame: pandas.DataFrame, x_labels, y_labels) -> pandas.DataFrame:
    def coerce_float(x: any) -> float:
        try:
            return float(x)
        except:
            return None

    def apply_unmeasured(x: float) -> bool:
        return x if x != 0 else None

    def replace_lessthan(x: any) -> int:
        try:        
            return float(x[1:]) / 2 if re.search(r'^<\d?\.?\d+', x) else x
        except TypeError:
            return x    
        
    for column in x_labels + y_labels:
        data_frame[column] = data_frame[column].apply(coerce_float).apply(apply_unmeasured).apply(replace_lessthan)

    return data_frame

def compute_ratios(data_frame: pandas.DataFrame, ratios, mass_impurities_labels) -> pandas.DataFrame:
    def lowercase_nth(x: str, n=1):
        return x if len(x) == 1 else x[:n] + x[n].lower() + x[n + 1:]

    for ratio in ratios:
        tokens = ratio.split("_")
        first_element, second_element = tokens[0], tokens[1]
        
        first_element_match = [x for x in mass_impurities_labels if first_element in x or lowercase_nth(first_element) in x or first_element.upper() in x]
        first_element_match.sort(key = lambda x : 1 if x.lower() == first_element.lower() else 0, reverse = True)
        second_element_match = [x for x in mass_impurities_labels if second_element in x or lowercase_nth(second_element) in x or second_element.upper() in x]
        second_element_match.sort(key = lambda x : 1 if x.lower() == second_element.lower() else 0, reverse = True)

        compute_ratio(data_frame, ratio, first_element_match[0], second_element_match[0])

    return data_frame

def compute_ratio(data_frame: pandas.DataFrame, ratio: str, numerator: str, denominator: str) -> None:
    data_frame[ratio] = (data_frame[numerator] / data_frame[denominator]).where(data_frame[denominator] != 0, data_frame[numerator].where(data_frame[numerator] == 0, float("inf")))

__all__ = ["geochemical_analysis_2022_09_11", "geochemical_analysis_2023_07_16", "geochemical_analysis_2023_01_23" "geochemical_analysis", "satellite_analysis", "satellite_image", "geochemical_satellite_analysis", "compute_ratios"]