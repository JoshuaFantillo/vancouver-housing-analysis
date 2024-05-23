from flask import Flask, render_template, jsonify, request, redirect, url_for, send_from_directory
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import io
from io import BytesIO
import base64
from matplotlib.colors import LinearSegmentedColormap
import os

app = Flask(__name__)

df = pd.read_csv('scripts/data/Interactive_Tool_ML_Model.csv')
df.replace(0, np.nan, inplace=True)
# Pre-calculate the global min and max for both types across all years
land_value_columns = [f'CURRENT_LAND_VALUE_{year}' for year in range(2006, 2034)]
improvement_value_columns = [f'CURRENT_IMPROVEMENT_VALUE_{year}' for year in range(2006, 2034)]
count_columns = [f'CURRENT_IMPROVEMENT_VALUE_{year}' for year in range(2006, 2024)]
global_land_min = np.log2(df[land_value_columns].quantile(0.02).min().min())
global_land_max = np.log2(df[land_value_columns].quantile(0.95).max().max())

global_improvement_min = np.log2(df[improvement_value_columns].quantile(0.02).min().min())
global_improvement_max = np.log2(df[improvement_value_columns].quantile(0.95).max().max())

global_land_min_value = df[land_value_columns].quantile(0.02).min().min()
global_land_max_value = df[land_value_columns].quantile(0.70).max().max()
global_improvement_max_value = df[improvement_value_columns].quantile(0.70).max().max()
global_improvement_min_value = df[improvement_value_columns].quantile(0.02).min().min()


def save_legend(min_val, max_val, file_name):
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, 'static/pictures')
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, f'{file_name}.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')

    # Define the colormap
    cmap = LinearSegmentedColormap.from_list('custom_cmap', ['#0D47A1', '#2196F3', '#F9A825', '#B71C1C'], N=100)

    # Create a figure
    fig = plt.figure(figsize=(1, 6))
    cbar_ax = fig.add_axes([0.1, 0.05, 0.15, 0.9])
    title_ax = fig.add_axes([0.1, 0.95, 0.8, 0.05])  
    title_ax.set_axis_off()  

    title_ax.set_title("In $ Log Base 2", fontsize=10, loc='center')

    # Create a colorbar in the figure
    cb = mpl.colorbar.ColorbarBase(cbar_ax, cmap=cmap, norm=plt.Normalize(vmin=min_val, vmax=max_val), orientation='vertical')

    cb.ax.ticklabel_format(style='plain')

    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

    print(f'Saved legend to {file_path}') 

save_legend(global_land_min, global_land_max, 'land_value_legend')
save_legend(global_improvement_min, global_improvement_max, 'improvement_value_legend')

@app.route('/')
def main_menu():
    return render_template('main_menu.html')

@app.route('/interactive_map')
def interactive_map():
    return render_template('metrovancouver.html')

@app.route('/graphs')
def graphs_menu():
    return render_template('graphs.html')

def sum_and_average_columns(df, column_prefix):
    years = range(2006, 2025)
    averages = {}
    for year in years:
        column_name = f"{column_prefix}{year}"
        if column_name in df.columns:
            if(column_name == ['NEW_CONSTRUCTION_']):
                averages[year] = df.iloc[0]
            else:
                averages[year] = df[column_name].mean()
    return pd.DataFrame(list(averages.items()), columns=['Year', 'Average'])

def calculate_percent_change(df):
    df['PercentChange'] = df['Average'].pct_change() * 100
    return df

# Creates land value vs construction
def land_value_vs_construction(df):
    land_value_avg = sum_and_average_columns(df, 'CURRENT_LAND_VALUE_')
    construction_first_value = sum_and_average_columns(df, 'NEW_CONSTRUCTION_')

    correlation = land_value_avg['Average'].corr(construction_first_value['Average'])

    fig, ax1 = plt.subplots(figsize=(15, 7))
    years = land_value_avg['Year']
    ax1.set_xticks(years[::2]) 
    ax1.set_xticklabels(years[::2].astype(str), rotation=45)
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Price In $', color=color)
    ax1.plot(land_value_avg['Year'], land_value_avg['Average'], label='Price In $', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:blue'
    ax2.set_ylabel('Amount Of New Construction Permits', color=color)
    ax2.plot(construction_first_value['Year'], construction_first_value['Average'], label='Amount Of New Construction Permits', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Land Value and Construction VS Year')
    plt.figtext(0.1, 0.7, f'Correlation: {correlation:.2f}', fontsize=12, color='purple')

    fig.tight_layout()  
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
    file_name = 'land_value_vs_construction'
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, 'static/pictures')
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, f'{file_name}.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Creates improvement value vs construction
def improvement_value_vs_construction(df):
    improvement_value_avg = sum_and_average_columns(df, 'CURRENT_IMPROVEMENT_VALUE_')
    construction_first_value = sum_and_average_columns(df, 'NEW_CONSTRUCTION_')

    correlation = improvement_value_avg['Average'].corr(construction_first_value['Average'])

    fig, ax1 = plt.subplots(figsize=(15, 7))
    years = improvement_value_avg['Year']
    ax1.set_xticks(years[::2])  
    ax1.set_xticklabels(years[::2].astype(str), rotation=45)
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Price In $', color=color)
    ax1.plot(improvement_value_avg['Year'], improvement_value_avg['Average'], label='Price In $', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:blue'
    ax2.set_ylabel('Amount Of New Construction Permits', color=color)
    ax2.plot(construction_first_value['Year'], construction_first_value['Average'], label='Amount Of New Construction Permits', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Improvement Value and Construction VS Year')
    plt.figtext(0.1, 0.7, f'Correlation: {correlation:.2f}', fontsize=12, color='purple')

    fig.tight_layout()  
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
    file_name = 'improvement_value_vs_construction'
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, 'static/pictures')
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, f'{file_name}.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Creates land value vs construction percentage
def land_value_vs_construction_percent_change(df):
    land_value_avg = sum_and_average_columns(df, 'CURRENT_LAND_VALUE_')
    construction_first_value = sum_and_average_columns(df, 'NEW_CONSTRUCTION_')

    land_value_percent_change = calculate_percent_change(land_value_avg)
    construction_percent_change = calculate_percent_change(construction_first_value)

    correlation = land_value_percent_change['PercentChange'].corr(construction_percent_change['PercentChange'])

    fig, ax1 = plt.subplots(figsize=(15, 7))
    years = land_value_avg['Year']
    ax1.set_xticks(years[::2])  
    ax1.set_xticklabels(years[::2].astype(str), rotation=45)
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('% Change In Price', color=color)
    ax1.plot(land_value_percent_change['Year'], land_value_percent_change['PercentChange'], label='% Change In Price', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:blue'
    ax2.set_ylabel('% Change Of New Construction Permits', color=color)
    ax2.plot(construction_percent_change['Year'], construction_percent_change['PercentChange'], label='% Change Of New Construction Permits', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('% Change Of Land Value and Construction VS Year')
    plt.figtext(0.1, 0.7, f'Correlation: {correlation:.2f}', fontsize=12, color='purple')

    fig.tight_layout()  
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
    file_name = 'land_value_vs_construction_percent_change'
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, 'static/pictures')
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, f'{file_name}.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Creates improvment value vs construction percentage
def improvement_value_vs_construction_percent_change(df):
    improvement_value_avg = sum_and_average_columns(df, 'CURRENT_IMPROVEMENT_VALUE_')
    construction_first_value = sum_and_average_columns(df, 'NEW_CONSTRUCTION_')

    improvement_value_percent_change = calculate_percent_change(improvement_value_avg)
    construction_percent_change = calculate_percent_change(construction_first_value)

    correlation = improvement_value_percent_change['PercentChange'].corr(construction_percent_change['PercentChange'])

    fig, ax1 = plt.subplots(figsize=(15, 7))
    years = improvement_value_avg['Year']
    ax1.set_xticks(years[::2])  
    ax1.set_xticklabels(years[::2].astype(str), rotation=45)
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('% Change In Price', color=color)
    ax1.plot(improvement_value_percent_change['Year'], improvement_value_percent_change['PercentChange'], label='% Change In Price', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:blue'
    ax2.set_ylabel('% Change Of New Construction Permits', color=color)
    ax2.plot(construction_percent_change['Year'], construction_percent_change['PercentChange'], label='% Change Of New Construction Permits', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('% Change Of Improvement Value and Construction VS Year')
    plt.figtext(0.1, 0.7, f'Correlation: {correlation:.2f}', fontsize=12, color='purple')

    fig.tight_layout()  
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
    file_name = 'improvement_value_vs_construction_percent_change'
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, 'static/pictures')
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, f'{file_name}.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Creates land value vs improvment value
def plot_land_vs_improvement(df):
    land_value_avg = sum_and_average_columns(df, 'CURRENT_LAND_VALUE_')
    improvement_value_avg = sum_and_average_columns(df, 'CURRENT_IMPROVEMENT_VALUE_')

    fig, ax1 = plt.subplots(figsize=(15, 7))
    
    correlation = land_value_avg['Average'].corr(improvement_value_avg['Average'])
    years = land_value_avg['Year']
    ax1.set_xticks(years[::2]) 
    ax1.set_xticklabels(years[::2].astype(str), rotation=45)
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Land Price', color=color)
    ax1.plot(land_value_avg['Year'], land_value_avg['Average'], label='Land Price', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:blue'
    ax2.set_ylabel('Improvement Price', color=color)
    ax2.plot(improvement_value_avg['Year'], improvement_value_avg['Average'], label='Improvement Price', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Land Price VS Improvement Price')
    plt.figtext(0.1, 0.7, f'Correlation: {correlation:.2f}', fontsize=12, color='purple')

    fig.tight_layout()  
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
    file_name = 'plot_land_value_vs_improvement'
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, 'static/pictures')
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, f'{file_name}.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Creates land value vs improvment value percentage
def plot_land_vs_improvement_percent_change(df):
    land_value_avg = sum_and_average_columns(df, 'CURRENT_LAND_VALUE_')
    improvement_value_avg = sum_and_average_columns(df, 'CURRENT_IMPROVEMENT_VALUE_')

    land_value_percent_change  = calculate_percent_change(land_value_avg)
    improvement_value_percent_change = calculate_percent_change(improvement_value_avg)

    fig, ax1 = plt.subplots(figsize=(15, 7))
    
    correlation = land_value_percent_change['PercentChange'].corr(improvement_value_percent_change['PercentChange'])
    years = land_value_avg['Year']
    ax1.set_xticks(years[::2]) 
    ax1.set_xticklabels(years[::2].astype(str), rotation=45)
    color = 'tab:red'
    ax1.set_xlabel('Year')
    ax1.set_ylabel('Land Value % Change', color=color)
    ax1.plot(land_value_percent_change ['Year'], land_value_percent_change ['PercentChange'], label='Land Value % Change', color=color, marker='o')
    ax1.tick_params(axis='y', labelcolor=color)

    ax2 = ax1.twinx() 
    color = 'tab:blue'
    ax2.set_ylabel('Improvement Value % Change', color=color)
    ax2.plot(improvement_value_percent_change['Year'], improvement_value_percent_change['PercentChange'], label='Improvement Value % Change', color=color, marker='x')
    ax2.tick_params(axis='y', labelcolor=color)

    plt.title('Land Value % Change VS Improvement Value % Change')
    plt.figtext(0.1, 0.7, f'Correlation: {correlation:.2f}', fontsize=12, color='purple')

    fig.tight_layout()  
    fig.legend(loc="upper left", bbox_to_anchor=(0.1,0.9))
    file_name = 'plot_land_vs_improvement_percent_change'
    current_dir = os.path.dirname(__file__)
    static_dir = os.path.join(current_dir, 'static/pictures')
    os.makedirs(static_dir, exist_ok=True)
    file_path = os.path.join(static_dir, f'{file_name}.png')
    plt.savefig(file_path, dpi=300, bbox_inches='tight')
    plt.close(fig)

# Calls all functions   
land_value_vs_construction(df)
improvement_value_vs_construction(df)
improvement_value_vs_construction_percent_change(df)
land_value_vs_construction_percent_change(df)
plot_land_vs_improvement(df)
plot_land_vs_improvement_percent_change(df)

# Calls the points to be called on the interactive map
@app.route('/data/coordinates')
def data_coordinates():
    year = request.args.get('year', default='2024', type=str)
    data_type = request.args.get('type', default='land', type=str)
    print(f"Received request for year: {year}, type: {data_type}")
    column_prefix = 'CURRENT_LAND_VALUE_' if data_type == 'land' else 'CURRENT_IMPROVEMENT_VALUE_'
    column_name = f'{column_prefix}{year}'

    coords_df = df[['LATITUDE', 'LONGITUDE', column_name]].dropna()
    coords_df = coords_df[coords_df[column_name] != 0]
    coords_df['log'] = np.log2(coords_df[column_name])
    # Chooses min and max for land value
    if(data_type=='land'):
        value_min = global_land_min
        value_max = global_land_max
        price_min = global_land_min_value
        price_max = global_land_max_value
    else:
        value_min = global_improvement_min
        value_max = global_improvement_max
        price_min = global_improvement_min_value
        price_max = global_improvement_max_value
    
    coords_df['log'] = (coords_df['log']-value_min)/(value_max-value_min)
    range_value = value_max - value_min
   
    coords_df['intensity'] = coords_df['log'].apply(lambda x: (x - value_min) / range_value)
    
    coords_data = coords_df[['LATITUDE', 'LONGITUDE', 'log', ]].to_dict(orient='records')

    response = {
        'coords': coords_data,
        'valueMin': price_min,
        'valueMax': price_max
    }

    return jsonify(response)

# Creates legend
@app.route('/legend/<legend_type>')
def serve_legend_image(legend_type):
    filename = f"{legend_type}_legend.png"
    return send_from_directory('static/pictures/', filename)



if __name__ == '__main__':
    app.run()