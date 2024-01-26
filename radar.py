"""radar.py

Author: James Buntwal (BuntwalJ@aol.co.uk)

Description: 

Generates a radar (or spider) chart visualizing an individual's skill levels.

The graph is then exported as a png.

"""

# Imports
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import math


# Set Skill levels
skills_dict = {
    "Python" : 8,
    "SQL" : 8,
    "R" : 5,
    "Statistics" : 5,
    "MS Office" : 7,
    "Leadership" : 4,
    "Proactivity" : 8,
    "Autonomy" : 8,
    "Problem Solving" : 7,
    "Strategic Thinking" : 6,
    "Predictive Modelling" : 7,
    "Time Management" : 4,
    "Team Working" : 9,
    "Communication" : 6
}

# Set boundaries for each proficiency level
boundaries_dict = {
    'Basic' : 4,
    'Full' : 7.5,
    'Advanced' : 10
}


# Create a dataframe with the skill levels for plotting
skills_df = (
    pd.DataFrame({  'Skills': skills_dict.keys(),
                    'MyLevel' : skills_dict.values()})
    .sort_values("MyLevel")
)

# add the proficiency levels
for key, value in boundaries_dict.items():
    skills_df[key] = value

# add the first row to the end of the dataset
# this is to close of the circles in the plot
skills_df = (
    pd.concat([skills_df, skills_df.iloc[[0]]])
    .reset_index(drop = True)
)

# Plot options for proficiency levels
proficiency_trace_options = {
    "fill"      : 'tonext',
    "opacity"   : 0.5,
    "line"      : { "width" : 1}
}

# plot options for my skill levels
MyLevel_trace_options = {
    "fill"      : None,
    "opacity"   : 1,
    "line"      : {"width" : 4}
}

# Create plotly figure
fig = go.Figure(
    layout = go.Layout(
        legend_title_text = 'Working Proficiency',
        autosize = False,
        width = 1024,
        height = 720,
        margin = {  "l" : 50,
                    "r" : 50,
                    "b" : 50,
                    "t" : 50,
                    "pad" : 4}
        )
    )

# For each trace, make the plot
for trace_name in list(boundaries_dict)+["MyLevel"]:

    # Select appropriate options
    options = (proficiency_trace_options
               if trace_name != "MyLevel"
               else MyLevel_trace_options
               )

    # Define the plot trace
    trace = go.Scatterpolar(
        r       = skills_df[trace_name],
        theta   = skills_df.Skills,
        name    = trace_name,
        mode    = "lines",
        **options
        )
    
    # Add trace to the plot
    fig.add_trace(trace)

# Remove hover over and save as png
(   fig
    .update_traces(
        hoverinfo       = 'skip',
        hovertemplate   = None
        )
    .write_image("radar_chart.png")
    )
