import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import seaborn as sns

suffix = ''
root_results_dir = Path(__file__).parent / ('results' + suffix)



# LOAD DATA ------------

def make_chart(results_dir, filename):
    all_data = {}
    rps_data = {}

    for directory in results_dir.iterdir():
        if directory.is_dir():
            # Get the alphabetically last CSV file
            csv_files = sorted(directory.glob('*.csv'))
            if csv_files:
                last_csv = csv_files[-1]

                # Read the 'response-time' column
                df = pd.read_csv(last_csv)
                #if 'response-time' in df.columns:
                all_data[directory.name] = df['response-time']

                last_row = df.iloc[-1]
                total_time = last_row['offset'] + last_row['response-time']  # Total time for requests
                total_requests = len(df)  # Number of packets (rows in CSV)
                
                # Calculate requests per second (RPS)
                rps = total_requests / total_time
                rps_data[directory.name] = rps

    rps_data = dict(sorted(rps_data.items(), key=lambda x: x[1]))
    all_data = dict(sorted(all_data.items(), key=lambda x: x[1].median()))


    # BOXPLOT ------------------

    if False:
      # Create a boxplot for all directories
      plt.figure(figsize=(10, 6))
      plt.boxplot(all_data.values(), tick_labels=all_data.keys(), showfliers=False)
      plt.xticks(rotation=45)
      #plt.title('Response Time')
      plt.ylabel('Response Time')
      plt.tight_layout()
      plt.savefig('boxplot.png')


    # BARCHART -------------------

    if False:
      # Create the bar chart for Requests Per Second (RPS)
      plt.figure(figsize=(10, 6))
      plt.bar(rps_data.keys(), rps_data.values())
      plt.xticks(rotation=45)
      plt.title('Requests Per Second by Directory')
      plt.ylabel('Requests Per Second')
      plt.tight_layout()
      plt.savefig('rps_barchart.png')



    # COMBINED ---------------

    NODE_COLOR = '#5fb252'
    BUN_COLOR = '#f472b6'

    fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(7, 7), sharex=True)
    shared_order = list(rps_data.keys())
    colors = [(NODE_COLOR if 'node' in k else BUN_COLOR) for k in shared_order]

    ax1.yaxis.grid(True, linestyle='dotted', linewidth=0.8, color=(0.5,0.5,0.5))  # Customize line style and color
    boxplot = sns.boxplot(data={k: all_data[k] for k in shared_order}, ax=ax1, showfliers=False)
    ax1.set_ylabel('Response Time (s)')
    #ax1.set_title('Response Time Boxplot by Directory (Outliers Hidden)')
    ax1.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)  # Hide x-axis labels here

    for patch, color in zip(boxplot.patches, colors):
        patch.set_facecolor(color)


    # Plot the bar chart for Requests Per Second (RPS) using Seaborn on the second subplot
    ax2.yaxis.grid(True, linestyle='dotted', linewidth=0.8, color=(0.5,0.5,0.5), zorder=0)  # Customize line style and color
    barplot = sns.barplot(x=shared_order, y=[rps_data[k] for k in shared_order], ax=ax2, zorder=2)
    ax2.set_ylabel('Requests Per Second')
    #ax2.set_title('Requests Per Second by Directory')
    #ax2.set_xlabel('Directory')
    ax2.set_ylim(0, max(rps_data.values()) * 1.1)

    def format_height(h):
        thousands = h / 1000
        if thousands >= 100:
            return f'{thousands:.0f}k'
        else:
            return f'{thousands:.1f}k'

    for patch, color in zip(barplot.patches, colors):
        patch.set_facecolor(color)
        height = patch.get_height()
        ax2.text(patch.get_x() + patch.get_width() / 2, height+100, format_height(height), ha='center', va='bottom')


    # Legend
    node_legend = mpatches.Patch(color=NODE_COLOR, label='Node')
    bun_legend = mpatches.Patch(color=BUN_COLOR, label='Bun')
    ax1.legend(handles=[node_legend, bun_legend], loc='upper right')

    # Save or show the combined chart
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig(filename)



for directory in root_results_dir.iterdir():
    print('making chart for', directory)
    if directory.is_dir():
        make_chart(directory, f'charts/combined_{directory.name}{suffix}.svg')
