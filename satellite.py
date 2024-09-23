from __future__ import annotations
import geopandas
import math
import pandas
import pandas.core.series
import rasterio.io
import shapely.geometry

def get_layer_label(band_index: int, layer_index: int) -> str:
    return f"B{band_index}L{layer_index}"

def get_layer_coordinate_label(band_index: int, layer_index: int, layer_coordinate: int) -> str:
    return f"B{band_index}L{layer_index}C{layer_coordinate}"
        
def length_of_layer(layer_index: int) -> int:
    return (2 * layer_index) + 1

def size_of_layer(layer_index: int) -> int:
    if (layer_index == 0):
        return 1
    else:
        return int(pow(length_of_layer(layer_index), 2) - pow(length_of_layer(layer_index - 1), 2))

def get_layer_offsets(layer_index: int, layer_coordinate: int) -> tuple[int, int]:
    length_breakpoint = length_of_layer(layer_index) - 1

    if layer_coordinate <= layer_index:
        return layer_coordinate, layer_index
    elif layer_coordinate <= length_breakpoint + layer_index:
        return layer_index, layer_index - (layer_coordinate - layer_index)
    elif layer_coordinate <= (2 * length_breakpoint) + layer_index:
        return layer_index - (layer_coordinate - (length_breakpoint + layer_index)), -layer_index
    elif layer_coordinate <= (3 * length_breakpoint) + layer_index:
        return -layer_index, -layer_index + (layer_coordinate - ((2 * length_breakpoint) + layer_index))
    else:
        return -layer_index + (layer_coordinate - ((3 * length_breakpoint) + layer_index)), layer_index

def create_features(satellite_data_frame: geopandas.GeoDataFrame, satellite_image: rasterio.io.DatasetReader, pixel_layer_start: int = 0, pixel_layer_count: int = 3, aggregate_layer_start: int = 1, aggregate_layer_count: int = 3) -> None:
    def get_index_x(row: pandas.core.series.Series) -> int:
        east = row["EAST"]
        if not math.isnan(east):
            delta_x = east - satellite_image.bounds.left
            index_x = math.floor(delta_x / satellite_image.x_resolution)
            
            return int(index_x)

    def get_index_y(row: pandas.core.series.Series) -> int:
        north = row["NORTH"]
        if not math.isnan(north):
            delta_y = abs(north - satellite_image.bounds.top)
            index_y = math.floor(delta_y / satellite_image.y_resolution)
            
            return int(index_y)
        
    def get_pixel_by_east_north(row: pandas.core.series.Series, band_index: int, layer_index: int, layer_coordinate: int) -> float:
        east = row["EAST"]
        north = row["NORTH"]
        if not math.isnan(east) and not math.isnan(north):
            delta_x = east - satellite_image.bounds.left
            delta_y = abs(north - satellite_image.bounds.top)
            index_x = math.floor(delta_x / satellite_image.x_resolution)
            index_y = math.floor(delta_y / satellite_image.y_resolution)

            offset_x, offset_y = get_layer_offsets(layer_index, layer_coordinate)

            index_x += offset_x
            if index_x < 0:
                index_x = 0
            elif index_x > satellite_image.width - 1:
                index_x = satellite_image.width - 1

            index_y += offset_y
            if index_y < 0:
                index_y = 0
            elif index_y > satellite_image.height - 1:
                index_y = satellite_image.height - 1
            
            return satellite_image.bands[band_index][index_y][index_x]

    def get_aggregate_by_east_north(row: pandas.core.series.Series, band_index: int, layer_index: int) -> float:
        east = row["EAST"]
        north = row["NORTH"]
        if not math.isnan(east) and not math.isnan(north):
            delta_x = east - satellite_image.bounds.left
            delta_y = abs(north - satellite_image.bounds.top)
            index_x = math.floor(delta_x / satellite_image.x_resolution)
            index_y = math.floor(delta_y / satellite_image.y_resolution)

            count = 0
            total = 0
            for offset_x in range(-layer_index, layer_index + 1):
                for offset_y in range(-layer_index, layer_index + 1):
                    inner_index_x = index_x + offset_x
                    if inner_index_x < 0:
                        inner_index_x = 0
                    elif inner_index_x > satellite_image.width - 1:
                        inner_index_x = satellite_image.width - 1

                    inner_index_y = index_y + offset_y
                    if inner_index_y < 0:
                        inner_index_y = 0
                    elif inner_index_y > satellite_image.height - 1:
                        inner_index_y = satellite_image.height - 1

                    count += 1
                    total += satellite_image.bands[band_index][inner_index_y][inner_index_x]
            
            return total / count
    
    satellite_data_frame["INDEX_X"] = satellite_data_frame.apply(get_index_x, axis=1)
    satellite_data_frame["INDEX_Y"] = satellite_data_frame.apply(get_index_y, axis=1)

    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(pixel_layer_start, pixel_layer_count):
            for layer_coordinate in range(0, size_of_layer(layer_index)):
                satellite_data_frame[get_layer_coordinate_label(band_index, layer_index, layer_coordinate)] = satellite_data_frame.apply(lambda row : get_pixel_by_east_north(row, band_index, layer_index, layer_coordinate), axis=1)

    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(aggregate_layer_start, aggregate_layer_count):
            satellite_data_frame[get_layer_label(band_index, layer_index)] = satellite_data_frame.apply(lambda row: get_aggregate_by_east_north(row, band_index, layer_index), axis=1)

def create_summary_data_frame(satellite_data_frame: geopandas.GeoDataFrame, satellite_image: rasterio.io.DatasetReader, target_column: str, measurement_disambiguation_mode: callable[[geopandas.GeoDataFrame], pandas.core.series.Series], pixel_layer_start: int = 0, pixel_layer_count: int = 3, aggregate_layer_start: int = 1, aggregate_layer_count: int = 3):
    index_data_frame = satellite_data_frame.dropna(subset=[target_column]).groupby(["INDEX_X", "INDEX_Y"])
    index_data_frame = measurement_disambiguation_mode(index_data_frame).reset_index()

    def get_pixel_by_index(row: pandas.core.series.Series, band_index: int, layer_index: int, layer_coordinate: int) -> float:
        index_x = row["INDEX_X"]
        index_y = row["INDEX_Y"]

        offset_x, offset_y = get_layer_offsets(layer_index, layer_coordinate)

        index_x += offset_x
        if index_x < 0:
            index_x = 0
        elif index_x > satellite_image.width - 1:
            index_x = satellite_image.width - 1

        index_y += offset_y
        if index_y < 0:
            index_y = 0
        elif index_y > satellite_image.height - 1:
            index_y = satellite_image.height - 1
        
        return satellite_image.bands[band_index][int(index_y)][int(index_x)]

    def get_aggregate_by_index(row: pandas.core.series.Series, band_index: int, layer_index: int) -> float:
        index_x = row["INDEX_X"]
        index_y = row["INDEX_Y"]

        count = 0
        total = 0
        for offset_x in range(-layer_index, layer_index + 1):
            for offset_y in range(-layer_index, layer_index + 1):
                inner_index_x = index_x + offset_x
                if inner_index_x < 0:
                    inner_index_x = 0
                elif inner_index_x > satellite_image.width - 1:
                    inner_index_x = satellite_image.width - 1

                inner_index_y = index_y + offset_y
                if inner_index_y < 0:
                    inner_index_y = 0
                elif inner_index_y > satellite_image.height - 1:
                    inner_index_y = satellite_image.height - 1

                count += 1
                total += satellite_image.bands[band_index][int(inner_index_y)][int(inner_index_x)]
        
        return total / count

    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(pixel_layer_start, pixel_layer_count):
            for layer_coordinate in range(0, size_of_layer(layer_index)):
                index_data_frame[get_layer_coordinate_label(band_index, layer_index, layer_coordinate)] = index_data_frame.apply(lambda row : get_pixel_by_index(row, band_index, layer_index, layer_coordinate), axis=1)

    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(aggregate_layer_start, aggregate_layer_count):
            index_data_frame[get_layer_label(band_index, layer_index)] = index_data_frame.apply(lambda row : get_aggregate_by_index(row, band_index, layer_index), axis=1)

    x_labels = []
    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(pixel_layer_start, pixel_layer_count):
            for layer_coordinate in range(0, size_of_layer(layer_index)):
                x_labels.append(get_layer_coordinate_label(band_index, layer_index, layer_coordinate))
    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(aggregate_layer_start, aggregate_layer_count):
            x_labels.append(get_layer_label(band_index, layer_index))
    y_labels = [target_column]

    index_data_frame = index_data_frame[x_labels + y_labels]

    index_data_frame.x_labels = lambda : x_labels
    index_data_frame.y_labels = lambda : y_labels

    return index_data_frame

def create_grid_search_data_frame(satellite_image: rasterio.io.DatasetReader, step_x: int, step_y: int, pixel_layer_start: int = 0, pixel_layer_count: int = 3, aggregate_layer_start: int = 1, aggregate_layer_count: int = 3) -> geopandas.GeoDataFrame:    
    def create_geometry(row: pandas.core.series.Series) -> shapely.geometry.Point:
        return shapely.geometry.Point(row["EAST"], row["NORTH"])
    
    def get_pixel_by_index(row: pandas.core.series.Series, band_index: int, layer_index: int, layer_coordinate: int) -> float:
        index_x = row["INDEX_X"]
        index_y = row["INDEX_Y"]

        offset_x, offset_y = get_layer_offsets(layer_index, layer_coordinate)

        index_x += offset_x
        if index_x < 0:
            index_x = 0
        elif index_x > satellite_image.width - 1:
            index_x = satellite_image.width - 1

        index_y += offset_y
        if index_y < 0:
            index_y = 0
        elif index_y > satellite_image.height - 1:
            index_y = satellite_image.height - 1
        
        return satellite_image.bands[band_index][int(index_y)][int(index_x)]

    def get_aggregate_by_index(row: pandas.core.series.Series, band_index: int, layer_index: int) -> float:
        index_x = row["INDEX_X"]
        index_y = row["INDEX_Y"]

        count = 0
        total = 0
        for offset_x in range(-layer_index, layer_index + 1):
            for offset_y in range(-layer_index, layer_index + 1):
                inner_index_x = index_x + offset_x
                if inner_index_x < 0:
                    inner_index_x = 0
                elif inner_index_x > satellite_image.width - 1:
                    inner_index_x = satellite_image.width - 1

                inner_index_y = index_y + offset_y
                if inner_index_y < 0:
                    inner_index_y = 0
                elif inner_index_y > satellite_image.height - 1:
                    inner_index_y = satellite_image.height - 1

                count += 1
                total += satellite_image.bands[band_index][int(inner_index_y)][int(inner_index_x)]
        
        return total / count
    
    index_x_list = []
    index_y_list = []
    east_list = []
    north_list = []

    for x in range(0, satellite_image.width, step_x):
        for y in range(0, satellite_image.height, step_y):
            index_x_list.append(x)
            index_y_list.append(y)
            (east, north) = satellite_image.xy(y, x)
            east_list.append(east)
            north_list.append(north)


    grid_search_data_frame = pandas.DataFrame({
        "INDEX_X": index_x_list,
        "INDEX_Y": index_y_list,
        "EAST": east_list,
        "NORTH": north_list
    })

    grid_search_data_frame["Geometry"] = grid_search_data_frame.apply(create_geometry, axis=1)
    grid_search_data_frame = geopandas.GeoDataFrame(grid_search_data_frame, crs=satellite_image.crs, geometry="Geometry")

    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(pixel_layer_start, pixel_layer_count):
            for layer_coordinate in range(0, size_of_layer(layer_index)):
                grid_search_data_frame[get_layer_coordinate_label(band_index, layer_index, layer_coordinate)] = grid_search_data_frame.apply(lambda row : get_pixel_by_index(row, band_index, layer_index, layer_coordinate), axis=1)

    for band_index in range(0, len(satellite_image.bands)):
        for layer_index in range(aggregate_layer_start, aggregate_layer_count):
            grid_search_data_frame[get_layer_label(band_index, layer_index)] = grid_search_data_frame.apply(lambda row : get_aggregate_by_index(row, band_index, layer_index), axis=1)

    return grid_search_data_frame

def filter_white_pixels(grid_search_data_frame) -> pandas.DataFrame:
    df = grid_search_data_frame
    df = df.loc[(df["B0L0C0"] != 255) & (df["B1L0C0"] != 255) & (df["B2L0C0"] != 255)]
    return df

__all__ = ["create_features", "create_summary_data_frame", "create_grid_search_data_frame", "filter_white_pixels"]