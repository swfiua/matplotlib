"""
Utility to help generate meta data for a weather dataset.
"""



from datetime import date
import karmapi.weather
from karmapi.weather import RawWeather

# defaults are good
raw = RawWeather()

meta = dict(
    base = "euro",
    fields = ['tmax', 'tmin', 'precipitation', 'evaporation', 'photo'],
    start_year = raw.start_day.year,
    start_month = raw.start_day.month,
    start_day = raw.start_day.day,

    end_year = raw.end_day.year,
    end_month = raw.end_day.month,
    end_day = raw.end_day.day,

    lats = raw.latitudes(),
    lons = raw.longitudes(),
)

# Stuff we can build
meta['builds'] = dict(
    day = dict(
        doc="extract data for a day from the raw data",
        path="time/<int:year>/<int:month>/<int:day>/<field>",
        karma="karmapi.weather.build_day",
        model = "karmapi.models.lat_lon_grid.LatLonGrid",
        source = "raw/{field}",
    ),
    time = dict(
        doc="extract data for a day from the raw data",
        path="time/<field>",
        karma="karmapi.weather.build_time",
        model = "karmapi.models.lat_lon_grid.LatLonGrid",
        source = "raw/{field}",
    ),
    lon = dict(
        doc="extract data from the day files for a specific latitude",
        path="space/<float:lat>/<field>",
        karma="karmapi.weather.build_latitude",
        model = "karmapi.models.lists.ListFloat",
    ),
    space = dict(
        doc="extract data from the day files for all lat/lons",
        path="space/<field>",
        karma="karmapi.weather.build_space",
        model = "karmapi.models.lists.ListFloat",
    ),
)


# Stuff we can get
meta['gets'] = dict(
    day = dict(
        doc="Data for a specific year/month/day",
        path="time/<int:year>/<int:month>/<int:day>/<field>",
        karma="karmapi.weather.get_array",
        model = "karmapi.models.lat_lon_grid.LatLonGrid",
        ),
    all_day = dict(
        doc="Data for a specific year/month/day",
        path="time/<int:year>/<int:month>/<int:day>/",
        karma="karmapi.weather.get_all_arrays",
        model = "karmapi.models.lat_lon_grid.LatLonGrid",
        ),
    latlon = dict(
        doc="Data for a specific lat/lon",
        path="space/<float:lat>/<float:lon>/<field>",
        karma="karmapi.weather.get_lat_lon",
        model = "karmapi.models.lists.ListFloat",
        ),
    all_latlon = dict(
        path="space/<float:lat>/<float:lon>",
        karma="karmapi.weather.get_all_for_lat_lon",
        model = "karmapi.models.lists.ListFloat",
        ),
)


if __name__ == '__main__':

    # write out meta data for dataset
    import json
    
    with open('meta.json', 'w') as out:
        out.write(json.dumps(meta, indent=True))
