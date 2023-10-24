import pandas as pd
from bokeh.plotting import figure, show
from bokeh.io import output_notebook
from bokeh.palettes import Category20, cividis
from bokeh.models import (
    Legend,
    HoverTool,
    PrintfTickFormatter,
    ColumnDataSource,
    Range1d,
)
from IPython import get_ipython
from IPython.display import display, Markdown
from typing import Optional, List
from .data_retrieval import (
    get_data_from_imf,
    rename_from_abbr_to_full_name,
    get_all_metric_data,
)


def generate_graph(
    cfa_df: pd.DataFrame, non_cfa_df: pd.DataFrame, metric_name: str, unit: str
) -> figure:
    p = figure(
        title=f"{metric_name}",
        x_axis_label="Year",
        y_axis_label=unit,
        width=1000,
        height=400,
    )
    p.line(
        x="year",
        y="median",
        color="rosybrown",
        line_width=2,
        legend_label=f"Non-CFA Median {metric_name}",
        source=ColumnDataSource(non_cfa_df),
    )
    p.line(
        x="year",
        y="median",
        color="cornflowerblue",
        line_width=2,
        legend_label=f"CFA Median {metric_name}",
        source=ColumnDataSource(cfa_df),
    )
    for legend in p.legend:
        p.add_layout(legend, "right")
    # hover = HoverTool(tooltips=[("Year", "@x"), (metric_name, "@y")], formatters={"@x": "numeral", "@y": "numeral"})
    # p.add_tools(hover)
    # p.yaxis[0].formatter = PrintfTickFormatter(format="%d")
    p.legend.click_policy = "hide"
    p.xgrid.grid_line_color = None
    p.ygrid.grid_line_color = None
    p.xaxis.major_tick_line_color = None  # turn off x-axis major ticks
    p.xaxis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.yaxis.major_tick_line_color = None  # turn off y-axis major ticks
    p.yaxis.minor_tick_line_color = None  # turn off y-axis minor ticks
    return p


def chat_gpt_analyze_results(
    indicator: str,
    years: List[int],
    intervals_where_median_is_higher: str,
    description: str,
):
    get_ipython().run_cell_magic(
        "ai", "openai-chat:gpt-3.5-turbo -r", "reset the chat history"
    )  # reset the model
    return get_ipython().run_cell_magic(
        "ai",
        "openai-chat:gpt-3.5-turbo -f markdown",
        f"""
            Professional tone like a macro economist: For {indicator} {intervals_where_median_is_higher} had more intervals with a higher median? Is it economically better for {indicator} to be higher
            or lower? To help with answering this question and explaining the indicator in the later section What is {indicator} please consider the {description}
            I am providing you about the {indicator}.Based on your response to that draw a conclusion comparing african cfa franc zone countries and 
            african non cfa franc zone countries.
            
            Please format response in markdown like this:
            # Since the 1980s, {indicator} comparison between CFA African Franc Zone Countries and Non CFA African Franc Zone Countries
            ### What is {indicator}? 
            in this section explain what the indicator means
            ### Conclusion
            in this section make a simple conclusion comparing CFA African Franc Zone Countries and Non CFA African Franc Zone Countries.
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
