import marimo

__generated_with = "0.14.15"
app = marimo.App(width="medium")


@app.cell
def _(mo):
    mo.md(r"""# Pereira tech talks demo""")
    return


@app.cell
def _():
    import marimo as mo
    import geopandas as gpd
    import folium

    TILES = "Cartodb dark_matter"
    return TILES, folium, gpd, mo


@app.cell
def _(gpd, mo):
    _location = mo.notebook_location().as_posix()

    _url = f"{_location}/public/adm2_risaralda.geojson"
    boundaries_gdf = gpd.read_file(_url)

    _url = f"{_location}/public/amenities.geojson"
    amenities_gdf = gpd.read_file(_url)
    return amenities_gdf, boundaries_gdf


@app.cell
def _(amenities_gdf, boundaries_gdf, mo):
    _amenities_options = amenities_gdf.amenity.unique().tolist()
    amenities_dropdown = mo.ui.dropdown(label="Amenity", options=_amenities_options, searchable=True)
    amenities_dropdown

    _bnd_options = boundaries_gdf.gaul2_name.unique().tolist()
    bnd_dropdown = mo.ui.dropdown(label="Municipality", options=_bnd_options, searchable=True)

    mo.hstack([bnd_dropdown, amenities_dropdown], justify="start")
    return amenities_dropdown, bnd_dropdown


@app.cell
def _(
    TILES,
    amenities_dropdown,
    amenities_gdf,
    bnd_dropdown,
    boundaries_gdf,
    folium,
    gpd,
):
    _filtered_bnd_gdf = boundaries_gdf if bnd_dropdown.value is None else boundaries_gdf.loc[boundaries_gdf.gaul2_name == bnd_dropdown.value]

    _filtered_gdf = gpd.overlay(amenities_gdf, _filtered_bnd_gdf, how="intersection")[["name", "amenity", "geometry"]]
    _filtered_gdf = _filtered_gdf if amenities_dropdown.value is None else _filtered_gdf.loc[_filtered_gdf.amenity == amenities_dropdown.value]

    _centroid = _filtered_bnd_gdf.dissolve().centroid.to_dict()[0]

    map = folium.Map(tiles=TILES, location=(_centroid.y, _centroid.x), min_zoom=11)

    _tooltip = folium.GeoJsonTooltip(fields=["name"])

    folium.GeoJson(_filtered_bnd_gdf).add_to(map)

    if _filtered_gdf.shape[0] > 0:
        folium.GeoJson(_filtered_gdf, layer_name="amenities", marker=folium.Circle(weigth=10, radius=50, stroke=False, fill=True, fill_opacity=0.6, opacity=1), tooltip=_tooltip).add_to(map)

    map

    return


if __name__ == "__main__":
    app.run()
