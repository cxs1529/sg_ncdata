import folium
import pandas as pd



def create_map(sgid, df):
    # create map object
    current_lat = df.loc[0,"gps_lat_end"]
    current_lon = df.loc[0,"gps_lon_end"]
    m = folium.Map(location=[current_lat, current_lon], zoom_start=8)

    # current target
    tgt_lat = df.loc[0,"TGT_lat"]
    tgt_lon = df.loc[0,"TGT_lon"]
    tgt_name = df.loc[0,"TGT_name"]
    folium.CircleMarker(
        location=[tgt_lat, tgt_lon],  # Latitude and Longitude
        radius=5,                      # Radius in pixels
        color='black',                   # Outline color
        fill=True,                      # Fill the circle
        fill_color="black",              # Fill color
        fill_opacity=0.6,               # Fill opacity
        popup=f"TGT:{tgt_name}",           # Popup text on click
        tooltip=f"TGT:{tgt_name} | {tgt_lat},{tgt_lon}"     # Tooltip text on hover
    ).add_to(m)

    # loop through end-of-dive positions
    for i in range(0, len(df)):
        thisdive_lat = df.loc[i,"gps_lat_end"]
        thisdive_lon = df.loc[i,"gps_lon_end"]
        fcolor = "blue"

        if i == 0:
            fcolor = "red"

        # create circle marker for each target
        folium.CircleMarker(
            location=[thisdive_lat, thisdive_lon],  # Latitude and Longitude
            radius=5,                      # Radius in pixels
            color='black',                   # Outline color
            fill=True,                      # Fill the circle
            fill_color=fcolor,              # Fill color
            fill_opacity=0.6,               # Fill opacity
            popup=f"dive: {i}",           # Popup text on click
            tooltip=f"{thisdive_lat},{thisdive_lon}"     # Tooltip text on hover
        ).add_to(m)
        

        # offset based on target direction
        latOffset = 0.1
        lonOffset = 0.1
        # add target text as marker to map
        # folium.Marker(
        #     location=[pos["lat"] + latOffset , pos["lon"] + lonOffset],
        #     popup=None, #folium.Popup('<i>The center of map</i>')
        #     tooltip=None,
        #     icon=folium.DivIcon(html= f"""<b>{text}</b>""", class_name="mapText"),
        #     ).add_to(m)

    # save map as html
    map_name = f"sg{sgid}_map.html"
    m.save(f"static/maps/{map_name}")
    return map_name