"""
HBS Case Figure Generator

Generates publication-quality figures for HBS teaching cases.
"""

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import pandas as pd
import numpy as np
from datetime import datetime
from typing import List, Tuple, Optional
import os


def setup_style():
    """Set up professional figure style for HBS cases."""
    plt.style.use('seaborn-v0_8-whitegrid')
    plt.rcParams.update({
        'figure.figsize': (10, 6),
        'figure.dpi': 150,
        'font.family': 'sans-serif',
        'font.size': 11,
        'axes.labelsize': 12,
        'axes.titlesize': 14,
        'axes.titleweight': 'bold',
        'axes.labelweight': 'bold',
        'xtick.labelsize': 10,
        'ytick.labelsize': 10,
        'legend.fontsize': 10,
        'legend.frameon': True,
        'legend.framealpha': 0.9,
        'axes.spines.top': False,
        'axes.spines.right': False,
        'figure.facecolor': 'white',
        'axes.facecolor': 'white',
        'grid.color': '#E5E5E5',
        'grid.linewidth': 0.5,
    })


def save_figure(fig, filename: str, output_dir: str = '.', dpi: int = 300):
    """Save figure with professional formatting."""
    filepath = os.path.join(output_dir, filename)
    fig.savefig(filepath, dpi=dpi, bbox_inches='tight',
                facecolor='white', edgecolor='none')
    print(f"Saved: {filepath}")
    plt.close(fig)
    return filepath


def plot_time_series(
    dates: List,
    values: List,
    title: str,
    ylabel: str,
    filename: str,
    output_dir: str = '.',
    color: str = '#1f77b4',
    annotate_points: List[dict] = None,
    show_values: bool = False,
    date_format: str = '%b %Y'
) -> str:
    """
    Plot a time series with professional styling.

    Args:
        dates: List of dates (datetime or convertible)
        values: List of numeric values
        title: Figure title
        ylabel: Y-axis label
        filename: Output filename
        output_dir: Output directory
        color: Line color
        annotate_points: List of dicts with 'date', 'value', 'text' for annotations
        show_values: Whether to show values at each point
        date_format: Date format for x-axis

    Returns:
        Path to saved figure
    """
    setup_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    ax.plot(dates, values, color=color, linewidth=2, marker='o', markersize=5)

    if show_values:
        for d, v in zip(dates, values):
            ax.annotate(f'{v:,.0f}', (d, v), textcoords="offset points",
                       xytext=(0, 10), ha='center', fontsize=9)

    if annotate_points:
        for ann in annotate_points:
            ax.annotate(ann['text'], (ann['date'], ann['value']),
                       textcoords="offset points", xytext=ann.get('offset', (0, 15)),
                       ha='center', fontsize=9,
                       arrowprops=dict(arrowstyle='->', color='gray', lw=0.5))

    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.set_ylabel(ylabel)
    ax.set_xlabel('')

    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_format))
    fig.autofmt_xdate()

    ax.set_ylim(bottom=0)

    return save_figure(fig, filename, output_dir)


def plot_bar_chart(
    categories: List[str],
    values: List[float],
    title: str,
    ylabel: str,
    filename: str,
    output_dir: str = '.',
    colors: List[str] = None,
    horizontal: bool = False,
    show_values: bool = True,
    value_format: str = '{:,.0f}'
) -> str:
    """
    Plot a bar chart with professional styling.

    Args:
        categories: Category labels
        values: Numeric values
        title: Figure title
        ylabel: Y-axis label
        filename: Output filename
        output_dir: Output directory
        colors: List of colors for bars
        horizontal: Whether to use horizontal bars
        show_values: Whether to show values on bars
        value_format: Format string for values

    Returns:
        Path to saved figure
    """
    setup_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    if colors is None:
        colors = ['#1f77b4'] * len(categories)

    x = np.arange(len(categories))

    if horizontal:
        bars = ax.barh(x, values, color=colors)
        ax.set_yticks(x)
        ax.set_yticklabels(categories)
        ax.set_xlabel(ylabel)
        ax.invert_yaxis()

        if show_values:
            for bar, val in zip(bars, values):
                ax.text(bar.get_width() + 0.01 * max(values), bar.get_y() + bar.get_height()/2,
                       value_format.format(val), va='center', fontsize=10)
    else:
        bars = ax.bar(x, values, color=colors)
        ax.set_xticks(x)
        ax.set_xticklabels(categories, rotation=45, ha='right')
        ax.set_ylabel(ylabel)

        if show_values:
            for bar, val in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.01 * max(values),
                       value_format.format(val), ha='center', fontsize=10)

    ax.set_title(title, fontweight='bold', fontsize=14)

    return save_figure(fig, filename, output_dir)


def plot_stacked_bar(
    categories: List[str],
    series: List[dict],
    title: str,
    ylabel: str,
    filename: str,
    output_dir: str = '.',
    show_legend: bool = True
) -> str:
    """
    Plot a stacked bar chart.

    Args:
        categories: Category labels
        series: List of dicts with 'name', 'values', 'color'
        title: Figure title
        ylabel: Y-axis label
        filename: Output filename
        output_dir: Output directory
        show_legend: Whether to show legend

    Returns:
        Path to saved figure
    """
    setup_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(categories))
    bottom = np.zeros(len(categories))

    for s in series:
        ax.bar(x, s['values'], bottom=bottom, label=s['name'],
               color=s.get('color', '#1f77b4'))
        bottom += np.array(s['values'])

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold', fontsize=14)

    if show_legend:
        ax.legend(loc='upper right', frameon=True)

    return save_figure(fig, filename, output_dir)


def plot_pie_chart(
    labels: List[str],
    values: List[float],
    title: str,
    filename: str,
    output_dir: str = '.',
    colors: List[str] = None,
    show_percentages: bool = True
) -> str:
    """
    Plot a pie chart.

    Args:
        labels: Slice labels
        values: Slice values
        title: Figure title
        filename: Output filename
        output_dir: Output directory
        colors: List of colors
        show_percentages: Whether to show percentages

    Returns:
        Path to saved figure
    """
    setup_style()

    fig, ax = plt.subplots(figsize=(8, 8))

    if colors is None:
        colors = plt.cm.Set2.colors[:len(labels)]

    wedges, texts, autotexts = ax.pie(
        values, labels=labels, colors=colors,
        autopct='%1.1f%%' if show_percentages else None,
        startangle=90, pctdistance=0.75
    )

    if show_percentages:
        for autotext in autotexts:
            autotext.set_fontsize(10)
            autotext.set_fontweight('bold')

    ax.set_title(title, fontweight='bold', fontsize=14)

    return save_figure(fig, filename, output_dir)


def plot_dual_axis(
    dates: List,
    values1: List[float],
    values2: List[float],
    title: str,
    ylabel1: str,
    ylabel2: str,
    filename: str,
    output_dir: str = '.',
    label1: str = 'Series 1',
    label2: str = 'Series 2',
    color1: str = '#1f77b4',
    color2: str = '#d62728'
) -> str:
    """
    Plot a dual-axis time series chart.

    Args:
        dates: List of dates
        values1: Values for left axis
        values2: Values for right axis
        title: Figure title
        ylabel1: Left y-axis label
        ylabel2: Right y-axis label
        filename: Output filename
        output_dir: Output directory
        label1: Label for left series
        label2: Label for right series
        color1: Color for left series
        color2: Color for right series

    Returns:
        Path to saved figure
    """
    setup_style()

    fig, ax1 = plt.subplots(figsize=(10, 6))

    ax1.plot(dates, values1, color=color1, linewidth=2, marker='o', markersize=5, label=label1)
    ax1.set_ylabel(ylabel1, color=color1)
    ax1.tick_params(axis='y', labelcolor=color1)
    ax1.set_xlabel('')

    ax2 = ax1.twinx()
    ax2.plot(dates, values2, color=color2, linewidth=2, marker='s', markersize=5, label=label2)
    ax2.set_ylabel(ylabel2, color=color2)
    ax2.tick_params(axis='y', labelcolor=color2)

    ax1.xaxis.set_major_formatter(mdates.DateFormatter('%b %Y'))
    fig.autofmt_xdate()

    ax1.set_title(title, fontweight='bold', fontsize=14)

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    return save_figure(fig, filename, output_dir)


def plot_comparison_bars(
    categories: List[str],
    series: List[dict],
    title: str,
    ylabel: str,
    filename: str,
    output_dir: str = '.',
    bar_width: float = 0.35
) -> str:
    """
    Plot grouped comparison bar chart.

    Args:
        categories: Category labels
        series: List of dicts with 'name', 'values', 'color'
        title: Figure title
        ylabel: Y-axis label
        filename: Output filename
        output_dir: Output directory
        bar_width: Width of bars

    Returns:
        Path to saved figure
    """
    setup_style()

    fig, ax = plt.subplots(figsize=(10, 6))

    x = np.arange(len(categories))

    for i, s in enumerate(series):
        offset = (i - len(series)/2 + 0.5) * bar_width
        ax.bar(x + offset, s['values'], bar_width,
               label=s['name'], color=s.get('color', plt.cm.Set2.colors[i]))

    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right')
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight='bold', fontsize=14)
    ax.legend(loc='upper right', frameon=True)

    return save_figure(fig, filename, output_dir)


# Example usage for SVB case
if __name__ == '__main__':
    import os

    output_dir = 'c:/Users/weikaili/Dropbox/My Documents/HBS Cases/SVB Collapse/figures'
    os.makedirs(output_dir, exist_ok=True)

    # Figure 1: SVB Deposit Growth
    years = [2018, 2019, 2020, 2021, 2022]
    deposits = [45.1, 61.8, 115.9, 189.2, 173.1]

    dates = [datetime(y, 12, 31) for y in years]
    plot_time_series(
        dates, deposits,
        title='SVB Total Deposits (2018-2022)',
        ylabel='Deposits ($ Billions)',
        filename='exhibit_deposits.png',
        output_dir=output_dir,
        show_values=True
    )

    # Figure 2: Investment Portfolio Composition
    plot_bar_chart(
        categories=['Held-to-Maturity', 'Available-for-Sale'],
        values=[91.3, 28.5],
        title='SVB Investment Portfolio Composition (Dec 2022)',
        ylabel='Amount ($ Billions)',
        filename='exhibit_portfolio.png',
        output_dir=output_dir,
        colors=['#1f77b4', '#ff7f0e'],
        show_values=True
    )

    # Figure 3: Uninsured vs Insured Deposits
    plot_pie_chart(
        labels=['Uninsured (>$250K)', 'Insured (<$250K)'],
        values=[94, 6],
        title='SVB Deposit Insurance Status (Dec 2022)',
        filename='exhibit_uninsured.png',
        output_dir=output_dir,
        colors=['#d62728', '#2ca02c']
    )

    # Figure 4: Federal Funds Rate
    dates_rate = [
        datetime(2020, 3, 1), datetime(2022, 3, 1), datetime(2022, 5, 1),
        datetime(2022, 6, 1), datetime(2022, 7, 1), datetime(2022, 9, 1),
        datetime(2022, 11, 1), datetime(2022, 12, 1), datetime(2023, 2, 1)
    ]
    rates = [0.25, 0.50, 1.00, 1.75, 2.50, 3.25, 4.00, 4.50, 4.75]

    plot_time_series(
        dates_rate, rates,
        title='Federal Funds Rate (2020-2023)',
        ylabel='Rate (%)',
        filename='exhibit_fed_rates.png',
        output_dir=output_dir,
        color='#d62728',
        date_format='%b %y'
    )

    # Figure 5: SVB vs Peer Banks - Investment as % of Assets
    plot_comparison_bars(
        categories=['SVB', 'CA Banks Avg', 'US Banks Avg'],
        series=[
            {'name': 'Investment Securities', 'values': [57, 20, 13], 'color': '#1f77b4'},
        ],
        title='Investment Securities as % of Total Assets (2022)',
        ylabel='Percentage (%)',
        filename='exhibit_peer_comparison.png',
        output_dir=output_dir
    )

    # Figure 6: Unrealized Losses
    plot_stacked_bar(
        categories=['Dec 2021', 'Dec 2022'],
        series=[
            {'name': 'HTM Unrealized Loss', 'values': [1.3, 15.1], 'color': '#d62728'},
            {'name': 'AFS Unrealized Loss', 'values': [0.3, 2.5], 'color': '#ff7f0e'},
        ],
        title='SVB Unrealized Losses on Investment Portfolio',
        ylabel='Unrealized Loss ($ Billions)',
        filename='exhibit_unrealized_losses.png',
        output_dir=output_dir
    )

    print(f"\nAll figures saved to: {output_dir}")
