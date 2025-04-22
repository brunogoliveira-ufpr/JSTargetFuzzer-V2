import pandas as pd

def generate_latex_chart_content(plot_data, config):
    latex_content = r"""
    \documentclass{article}
    \usepackage{graphicx}
    \usepackage{booktabs}
    \usepackage{pgfplots}
    \pgfplotsset{compat=1.17}
    \begin{document}

    \begin{tikzpicture}
    \begin{axis}[
        x tick label style={/pgf/number format/1000 sep=},
        enlargelimits=0.15,
        legend style={at={(0.5,1.1)}, anchor=south,legend columns=-1}, % Legend above the chart
        ybar,
        bar width=12pt,
        width=1.2\textwidth,
        height=0.7\textheight,
        xlabel={%s},
        ylabel={%s},
        symbolic x coords={%s},
        xtick=data,
        ymajorgrids=true,
        grid style=dashed,
        x tick label style={rotate=45, anchor=east, font=\small},
        ymin=0,
    ]
    """ % (
        config.get('xlabel', 'Category'),
        config.get('ylabel', 'Average Count'),
        ', '.join([f"{{{cat}}}" for cat in plot_data['categories']])
    )

    latex_content += r"""
    \addplot[
        ybar,
        fill=blue,
        draw=blue,
        mark=none,
    ] coordinates {"""
    
    for cat, mean1 in zip(plot_data['categories'], plot_data['means_1']):
        try:
            value = float(mean1)
        except ValueError:
            value = 0.0
        latex_content += f"({cat}, {value:.2f}) "
    
    latex_content += r"""};

    \addplot[
        ybar,
        fill=red,
        draw=red,
        mark=none,
    ] coordinates {"""
    
    for cat, mean500 in zip(plot_data['categories'], plot_data['means_500']):
        try:
            value = float(mean500)
        except ValueError:
            value = 0.0
        latex_content += f"({cat}, {value:.2f}) "
    
    latex_content += r"""};
    
    \legend{%s, %s}
    \end{axis}
    \end{tikzpicture}

    \end{document}
    """ % (
        config.get('legend_label1', "Fuzzilli's Programs"),
        config.get('legend_label2', "JSTargetFuzzer's Programs")
    )
    
    return latex_content

def save_latex_chart_file(plot_data, config, file_path="chart_only_report.tex"):
    latex_content = generate_latex_chart_content(plot_data, config)
    with open(file_path, "w") as f:
        f.write(latex_content)
