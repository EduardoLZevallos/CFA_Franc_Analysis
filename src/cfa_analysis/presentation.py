"""Creates the graphs for imf metrics and generates chatgpt prompt and call"""

from IPython.display import display, Markdown
from bokeh.plotting import figure, show
from bokeh.io import curdoc
from bokeh.models import HoverTool, ColumnDataSource, Title, BasicTickFormatter, Label
from .data_classes import Indicator


def generate_graph(
    merged_df_dict: dict, metric_name: str, unit: str
) -> figure:  # pragma: no cover
    """Creates median graph for imf metrics"""
    curdoc().theme = "light_minimal"
    no_log_scale_metrics = [
        ("Real GDP Growth Rate", "Annual % change"),
        ("Inflation Rate, Average Consumer Prices", "Annual % change"),
        ("Inflation Rate, End Of Period Consumer Prices", "Annual % change"),
        ("Private Inflows Excluding Direct Investment (% Of GDP)", "Percent"),
        ("Private Outflows Excluding Direct Investment (% Of GDP)", "Percent"),
        ("Real Non-oil GDP Growth", "Annual % change"),
        ("Current Account Balance", "Billions of U.S. dollars"),
        ("Primary Net Lending/Borrowing", "% of GDP"),
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
    p.add_layout(
        Title(
            text="Negative values on log scale graphs are represented as transparent lines",
            text_font_size="8pt",
            text_align="left",
            align="left",
        ),
        "below",
    )
    p.title.offset = 200
    p.title.align = "center"

    p.axis.minor_tick_line_color = None  # turn off x-axis minor ticks
    p.axis.major_tick_line_color = "#AAAAAA"
    p.axis.major_tick_line_dash = "dashed"

    p.axis.axis_label_text_font_size = "12pt"
    p.axis.axis_label_text_font_style = "bold"
    p.axis.major_label_text_font_size = "12px"
    p.axis.axis_label_standoff = 20
    p.xaxis.major_label_orientation = 1.0
    p.yaxis[0].formatter = BasicTickFormatter(use_scientific=False)

    p.legend.border_line_color = None
    p.legend.border_line_alpha = 0
    p.min_border = 100
    return p

def display_indicator_report(p: figure, definition: Markdown, conclusion: Markdown):
    display(
        Markdown(
            f"""## {indicator.label} comparison between African CFA Zone Countries to Non-CFA Middle Africa and Western Africa Countries"""
        )
    )
    show(p)
    display(Markdown(f"### Definition of {indicator.label}"))
    display(definition)
    display(Markdown(f"### Comparing Median Intervals for indicator {indicator.label}"))
    display(conclusion)

