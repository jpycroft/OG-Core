import numpy as np
import os
import matplotlib.pyplot as plt
from ogusa.constants import VAR_LABELS
cur_path = os.path.split(os.path.abspath(__file__))[0]
style_file = os.path.join(cur_path, 'OGUSAplots.mplstyle')
plt.style.use(style_file)


def plot_aggregates(base_tpi, base_params, reform_tpi=None,
                    reform_params=None, var_list=['Y', 'C', 'K', 'L'],
                    plot_type='pct_diff', num_years_to_plot=50,
                    start_year=2019, vertical_line_years=None,
                    plot_title=None, path=None):
    '''
    Create a plot of macro aggregates.

    Args:
        base_tpi (dictionary): TPI output from baseline run
        base_params (OG-USA Specifications class): baseline parameters object
        reform_tpi (dictionary): TPI output from reform run
        reform_params (OG-USA Specifications class): reform parameters object
        p (OG-USA Specifications class): parameters object
        var_list (list): names of variable to plot
        plot_type (string): type of plot, can be:
            'pct_diff': plots percentage difference between baselien
                and reform ((reform-base)/base)
            'diff': plots difference between baseline and reform (reform-base)
            'levels': plot variables in model units
            'cbo': plots variables in levels relative to CBO baseline
                projection (only available for macro variables in CBO
                long-term forecasts)
        num_years_to_plot (integer): number of years to include in plot
        start_year (integer): year to start plot
        vertical_line_years (list): list of integers for years want
            vertical lines at
        plot_title (string): title for plot
        path (string): path to save figure to

    Returns:
        fig (Matplotlib plot object): plot of immigration rates
    '''
    assert (isinstance(start_year, int))
    # Make sure both runs cover same time period
    if reform_tpi is not None:
        assert (base_params.start_year == reform_params.start_year)
    year_vec = np.arange(base_params.start_year, base_params.start_year
                         + num_years_to_plot)
    start_index = start_year - base_params.start_year
    # Check that reform included if doing pct_diff or diff plot
    if plot_type == 'pct_diff' or plot_type == 'diff':
        assert (reform_tpi is not None)
    fig1, ax1 = plt.subplots()
    for i, v in enumerate(var_list):
        if plot_type == 'pct_diff':
            plot_var = (reform_tpi[v] - base_tpi[v]) / base_tpi[v]
            ylabel = r'Pct. change'
            plt.plot(year_vec,
                     plot_var[start_index: start_index +
                              num_years_to_plot], label=VAR_LABELS[v])
        elif plot_type == 'diff':
            plot_var = reform_tpi[v] - base_tpi[v]
            ylabel = r'Difference (Model Units)'
            plt.plot(year_vec,
                     plot_var[start_index: start_index +
                              num_years_to_plot], label=VAR_LABELS[v])
        elif plot_type == 'levels':
            plt.plot(year_vec,
                     base_tpi[v][start_index: start_index +
                                 num_years_to_plot],
                     label='Baseline ' + VAR_LABELS[v])
            plt.plot(year_vec,
                     reform_tpi[v][start_index: start_index +
                                   num_years_to_plot],
                     label='Reform ' + VAR_LABELS[v])
            ylabel = r'Model Units'
        elif plot_type == 'cbo':
            plot_var = reform_tpi[v] - base_tpi[v]
            ylabel = r'Billions of \$'
        else:
            print('Please enter a valid plot type')
            assert(False)
    # vertical markers at certain years
    if vertical_line_years is not None:
        for yr in vertical_line_years:
            plt.axvline(x=yr, linewidth=0.5, linestyle='--', color='k')
    plt.xlabel(r'Year $t$')
    plt.ylabel(ylabel)
    if plot_title is not None:
        plt.title(plot_title, fontsize=15)
    vals = ax1.get_yticks()
    if plot_type == 'pct_diff':
        ax1.set_yticklabels(['{:,.0%}'.format(x) for x in vals])
    plt.xlim((base_params.start_year - 1, base_params.start_year +
              num_years_to_plot))
    plt.legend(loc=9, bbox_to_anchor=(0.5, -0.1), ncol=2)
    if path is not None:
        fig_path1 = os.path.join(path)
        plt.savefig(fig_path1, bbox_inches="tight")
    else:
        return fig1
    plt.close()
