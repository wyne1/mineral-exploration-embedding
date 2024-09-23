from __future__ import annotations

from pathlib import Path
from typing import Optional

import geopandas
import geopandas.datasets
import pandas
import shapely.geometry
from universal_common import first

ELEMENTS: list[str] = ["Au", "Ag", "Al", "As", "B", "Ba", "Be", "Bi", "Ca", "Cd", "Ce", "Co", "Cr", "Cs", "Cu", "Fe", "Ga", "Ge", "Hf", "Hg", "In", "K", "La", "Li", "Mg", "Mn", "Mo", "Na", "Nb", "Ni", "P", "Pb", "Rb", "Re", "S", "Sb", "Sc", "Se", "Sn", "Sr", "Ta", "Te", "Th", "Ti", "Tl", "U", "V", "W", "Y", "Zn", "Zr"]


def string_equals(a: Optional[str], b: Optional[str], case_sensitive: bool = True):
    if a is None and b is None:
        return True
    elif (a is None and b is not None) or (a is not None and b is None):
        return False

    if not case_sensitive:
        return a.casefold() == b.casefold()
    
    return a == b

def rename_column(column_name):
    map: dict = {
        "Sample_Number": "SampleNumber",
        "UTM_Easting": "Easting",
        "UTM_Northing": "Northing",
        "(2Ca+Na+K)/Al_(molar)": "(2Ca+Na+K)/Al",
        "K/Al_(molar)": "K/Al",
        "K/(Al-Na)_(molar)": "K/(Al-Na)",
        "Na/Al_(molar)": "Na/Al"
    }

    if column_name in map.keys():
        return map[column_name]
    
    if "_" in column_name:
        parts: list[str] = column_name.split("_")

        if len(parts) == 2:
            element: str = parts[0]
            unit: str = parts[1]

            if string_equals(unit, "perc"):
                unit = "%"
            
            if element.casefold() in [x.casefold() for x in ELEMENTS]:
                element = first(ELEMENTS, lambda x: x.casefold() == element.casefold())
                return f"{element} ({unit})"
                
    
    return column_name

def augment_domain_series(point: shapely.Point) -> tuple[Optional[int], Optional[str], Optional[int]]:
    if (547750 <= point.x and point.x <= 550250 and 3355000 <= point.y and point.y <= 3359000) or (549500 <= point.x and point.x <= 551250 and 3353250 <= point.y and point.y <= 3355000):
        return (1, "Mercedes", 1)
    elif 550750 <= point.x and point.x <= 553850 and 3356250 <= point.y and point.y <= 3359250:
        return (2, "Klondike-Rey de Oro", 1)
    elif 551000 <= point.x and point.x <= 557000 and 3359500 <= point.y and point.y <= 3366000:
        return (3, "San Martin-Lupita-Diluvio", 1)
    elif 550000 <= point.x and point.x <= 565000 and 3372500 <= point.y and point.y <= 3382000:
        return (4, "La Mesa", 2)
    
    return (None, None, None)

class Mercedes:
    DOMAIN_ID_COLUMN: str = "DomainId"
    DOMAIN_NAME_COLUMN: str = "DomainName"
    AREA_ID_COLUMN = "AreaId"
    GEOMETRY_COLUMN: str = "Geometry"
    ID_COLUMN: str = "SampleNumber"

    @classmethod
    def latest(cls, directory: Path) -> geopandas.GeoDataFrame:
        return cls.version(directory, "2024-05-30")

    @classmethod
    def version(cls, directory: Path, version: str) -> geopandas.GeoDataFrame:
        path: Path = directory / f"Mercedes - {version}.xlsx"
        sheet_name: str = "Mercedes BC Geochem working"

        return cls.load_dataset(path, sheet_name)

    @classmethod
    def load_dataset(cls, path: Path, sheet_name: str) -> geopandas.GeoDataFrame:
        data_frame: pandas.DataFrame = pandas.read_excel(path, sheet_name = sheet_name)
        data_frame = data_frame.rename(mapper = rename_column, axis = "columns")
        data_frame = data_frame.dropna(subset=["Easting", "Northing", "Au (ppm)"])
        data_frame = data_frame[data_frame["SampleNumber"] != 695715][data_frame["SampleNumber"] != 696377][data_frame["SampleNumber"] != "MRS-019"][data_frame["SampleNumber"] != 697159][data_frame["SampleNumber"] != 697161][data_frame["SampleNumber"] != 697163][data_frame["SampleNumber"] != 696453][data_frame["SampleNumber"] != 696517]

        def create_geometry(row: pandas.core.series.Series) -> shapely.geometry.Point:
            return shapely.geometry.Point(row["Easting"], row["Northing"])

        data_frame[cls.GEOMETRY_COLUMN] = data_frame.apply(create_geometry, axis=1)
        data_frame = geopandas.GeoDataFrame(data_frame, geometry = cls.GEOMETRY_COLUMN)

        data_frame[cls.DOMAIN_ID_COLUMN], data_frame[cls.DOMAIN_NAME_COLUMN], data_frame[cls.AREA_ID_COLUMN] = zip(*data_frame[cls.GEOMETRY_COLUMN].apply(augment_domain_series))

        return data_frame
    
__all__ = [Mercedes]