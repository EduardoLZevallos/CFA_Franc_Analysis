import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_notebook, curdoc
from bokeh.palettes import HighContrast
from bokeh.models import (
    Legend,
    HoverTool,
    PrintfTickFormatter,
    ColumnDataSource,
    Range1d,
    Title,
    BasicTickFormatter,
    Range1d,
)
from IPython import get_ipython
from IPython.display import display, Markdown
from typing import Optional, List, Dict
from .data_retrieval import (
    get_data_from_imf,
    rename_from_abbr_to_full_name,
    get_all_metric_data,
)


def generate_graph(merged_df_dict: Dict, metric_name: str, unit: str) -> figure:
    curdoc().theme = "light_minimal"
    no_log_scale_metrics = [
        ("Real GDP Growth Rate", "Annual % change"),
        ("Inflation Rate, Average Consumer Prices", "Annual % change"),
        ("Inflation Rate, End Of Period Consumer Prices", "Annual % change"),
        ("Private Inflows Excluding Direct Investment (% Of GDP)", "Percent"),
        ("Private Outflows Excluding Direct Investment (% Of GDP)", "Percent"),
        ("Real Non-oil GDP Growth", "Annual % change"),
    ]
    if (metric_name, unit) in no_log_scale_metrics:
        p = figure(
            x_axis_label="Year",
            y_axis_label=f"{unit}",
            width=800,
            height=400,
            toolbar_location=None,
        )
    else:
        p = figure(
            x_axis_label="Year",
            y_axis_label=f"{unit}",
            width=800,
            height=400,
            toolbar_location=None,
            y_axis_type="log",
        )
        p.line(
            x="Year",
            y="abs_noncfa_median",
            color="#D55E00",
            line_width=3,
            source=ColumnDataSource(merged_df_dict),
            line_alpha=0.3,
        )
        p.line(
            x="Year",
            y="abs_cfa_median",
            color="#0072B2",
            line_width=3,
            source=ColumnDataSource(merged_df_dict),
            line_alpha=0.3,
        )

    p.line(
        x="Year",
        y="noncfa_median",
        color="#D55E00",
        line_width=3,
        legend_label="Non-CFA",
        source=ColumnDataSource(merged_df_dict),
        line_alpha=0.7,
    )
    p.line(
        x="Year",
        y="cfa_median",
        color="#0072B2",
        line_width=3,
        legend_label="CFA",
        source=ColumnDataSource(merged_df_dict),
        line_alpha=0.7,
    )

    for legend in p.legend:
        p.add_layout(legend, "right")

    hover = HoverTool(
        tooltips=[
            ("Year", "@Year"),
            (f"Median {metric_name} (Non-CFA)", "@noncfa_median{0.00}"),
            (f"Median {metric_name} (CFA)", "@cfa_median{0.00}"),
        ]
    )
    p.add_tools(hover)

    p.add_layout(
        Title(
            text="CFA African Countries vs. Non-CFA Middle Africa/West Africa Countries \n\n",
            text_font_size="12pt",
            text_align="center",
            align="center",
            text_font_style="normal",
        ),
        "above",
    )
    p.add_layout(
        Title(
            text=f"Median {metric_name}",
            text_font_size="18pt",
            text_align="center",
            align="center",
        ),
        "above",
    )
    p.title.offset = 200
    p.title.align = "center"

    # p.xgrid.grid_line_color = "#DDDDDD"
    # p.ygrid.grid_line_color = "#DDDDDD"

    p.axis.minor_tick_line_color = None  # turn off x-axis minor ticks
    # p.axis.major_tick_line_alpha =  0.1
    p.axis.major_tick_line_color = "#AAAAAA"
    p.axis.major_tick_line_dash = "dashed"

    p.axis.axis_label_text_font_size = "12pt"
    p.axis.axis_label_text_font_style = "bold"
    p.axis.major_label_text_font_size = "12px"
    p.axis.axis_label_standoff = 20
    p.xaxis.major_label_orientation = 1.0
    p.yaxis[0].formatter = BasicTickFormatter(use_scientific=False)
    # p.yaxis[0].formatter = PrintfTickFormatter(format="%2f")

    p.legend.border_line_color = None
    p.legend.border_line_alpha = 0
    # p.legend.click_policy = "hide" dont want legend to be clickable 

    p.min_border = 100
    return p


def chat_gpt_analyze_results(
    indicator: str,
    years: List[int],
    intervals_where_median_is_higher: str,
    description: str,
    unit: str,
):
    get_ipython().run_cell_magic(
        "ai", "openai-chat:gpt-3.5-turbo -r", "reset the chat history"
    )  # reset the model
    return get_ipython().run_cell_magic(
        "ai",
        "openai-chat:gpt-3.5-turbo -f markdown",
        f"""
        In a professional tone like a keynesian economist: 
        The response has to be formatted into two sections, and only two sections.  Those two sections are, 
        
        The first section: markdown heading 3  "What is {indicator}?"
        In this section explain what the {indicator} means.  For more context this {indicator} is measured in unit {unit} and can be described as {description}. Is it better for economic development for {indicator} to be higher or lower? What does it suggest about economic development for {indicator} to be high or low?
         
        The second section: markdown heading 3 "Conclusion":
        With regards to if it is better for economic developement for {indicator} to be higher or lower, for {indicator} {intervals_where_median_is_higher} had more yearly intervals with a higher median from {years[0]} to {years[-1]}. Please draw a simple conclusion about economic development comparing african cfa franc zone countries and african non cfa franc zone countries.
        """,
    )


# def graph_inflation_of_countries(list_of_countries:list):
#     abbr = [countries[x] for x in list_of_countries] # countries is from imf
#     inflation_rates = rename_from_abbr_to_full_name(get_all_inflation_rate(abbr))
#     p = figure(title="Inflation Over Time in Non-CFA Franc Zone",
#            x_axis_label="Year",
#            y_axis_label="Inflation Rate"
#         )
#     # Define the colors for each country
#     if len(inflation_rates) > 20:
#         colors = cividis(len(inflation_rates))
#     else:
#         colors = Category20[len(inflation_rates)]
#     # Add a line for each country
#     for i, (country, values) in enumerate(inflation_rates.items()):
#         x = list(values.keys())
#         y = list(values.values())
#         p.line(x=x, y=y, color=colors[i], alpha = 0.5)

#     # median is the median inflation rate of cfa countries
#     p.line(x=list(medians.keys()), y = list(medians.values()), color = 'cornflowerblue', line_width = 4,  line_dash = "dashed")
#     hover = HoverTool(tooltips=[("Country", "$name"), ("Year", "@x"), ("Inflation", "@y")], formatters={"@name": "printf", "@x": "numeral", "@y": "numeral"})
#     p.add_tools(hover)

#     legend = Legend(items=[(country, [line]) for country, line in zip(inflation_rates.keys(), p.renderers)], location="top_right")
#     p.add_layout(legend)

#     # Disable scientific notation for y-axis ticks
#     p.yaxis[0].formatter = PrintfTickFormatter(format="%d")
#     p.legend.title = "Countries"
#     p.legend.background_fill_alpha = 0
#     p.legend.border_line_alpha = 0
#     p.legend.click_policy="hide"

#     p.xgrid.grid_line_color = None
#     p.ygrid.grid_line_color = None
#     p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
#     p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
#     p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
#     p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
#     # Show the plot
#     return p
