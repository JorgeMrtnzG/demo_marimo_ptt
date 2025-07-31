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
def _(TILES, folium, gpd, mo):
    url = f"{mo.notebook_location()}/public/adm2_risaralda.geojson"

    gdf = gpd.read_file(url)
    _centroid = gdf.dissolve().centroid.to_dict()[0]

    map = folium.Map(tiles=TILES, min_zoom=5, location=(_centroid.y, _centroid.x))
    folium.GeoJson(gdf, layer_name="boundaries").add_to(map)


    map

    return


@app.cell
def _():
    return


if __name__ == "__main__":
    app.run()
