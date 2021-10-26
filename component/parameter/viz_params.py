from .color_gradient import red_to_green

# vizualisation parameters of the final_layer
final_viz = {
    "min": 0,
    "max": 5,
    "palette": red_to_green,
}

# matplotlib viz_param but in GEE
# https://code.earthengine.google.com/?scriptPath=users%2Fgena%2Fpackages%3palettes
plt_viz = {
    "inferno": {
        "min": 0,
        "max": 10,
        "palette": [
            "#000004",
            "#320A5A",
            "#781B6C",
            "#BB3654",
            "#EC6824",
            "#FBB41A",
            "#FCFFA4",
        ],
    },
    "magma": {
        "min": 0,
        "max": 10,
        "palette": [
            "#000004",
            "#2C105C",
            "#711F81",
            "#B63679",
            "#EE605E",
            "#FDAE78",
            "#FCFDBF",
        ],
    },
    "plasma": {
        "min": 0,
        "max": 10,
        "palette": [
            "#0D0887",
            "#5B02A3",
            "#9A179B",
            "#CB4678",
            "#EB7852",
            "#FBB32F",
            "#F0F921",
        ],
    },
    "viridis": {
        "min": 0,
        "max": 10,
        "palette": [
            "#440154",
            "#433982",
            "#30678D",
            "#218F8B",
            "#36B677",
            "#8ED542",
            "#FDE725",
        ],
    },
}

# the vizaulization paramters for aoi
aoi_style = {  # default styling of the layer
    "stroke": True,
    "color": "black",
    "weight": 2,
    "opacity": 1,
    "fill": True,
    "fillColor": "black",
    "fillOpacity": 0.4,
}
