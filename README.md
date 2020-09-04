# Country
`/country/{country_id:\d+}` - Get country by id

`/countries` - Get all countries [GET PARAMS: *q* - partial match by name or code, *limit* - limit of rows (max. 200)]

# Region
`/region/{region_id:\d+}` - Get region by id

`/regions/country-{country_id:\d+}` - Get all regions by country id [GET PARAMS: *q* - partial match by name, *limit* - limit of rows (max. 200)]

# Area
`/area/{area_id:\d+}` - Get area by id

`/areas/region-{region_id:\d+}` - Get all areas by region id [GET PARAMS: *q* - partial match by name, *limit* - limit of rows (max. 200)]

# Locality
`/locality/{locality_id:\d+}` - Get locality by id

`/localities/area-{area_id:\d+}` - Get all localities by area id [GET PARAMS: *q* - partial match by name, *limit* - limit of rows (max. 200)]

# District
`/district/{district_id:\d+}` - Get district by id

`/districts/locality-{locality_id:\d+}` - Get all districts by locality id [GET PARAMS: *q* - partial match by name, *limit* - limit of rows (max. 200)]

# Street
`/street/{street_id:\d+}` - Get street by id

`/streets/locality-{locality_id:\d+}` - Get all streets by locality id [GET PARAMS: *q* - partial match by name, *limit* - limit of rows (max. 200)]

`/streets/district-{district_id:\d+}` - Get all streets by district id [GET PARAMS: *q* - partial match by name, *limit* - limit of rows (max. 200)]

# House
`/house/{house_id:\d+}` - Get house by id

`/house/{house_id:\d+}/full` - Get full address row by house id

`/houses/street-{street_id:\d+}` - Get all houses by street id [GET PARAMS: *q* - partial match by name, *limit* - limit of rows (max. 200)]