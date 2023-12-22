import os
import argparse
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

PAD_CHAR = '!'
COLOR_RED = [1, 0, 0]
COLOR_BLUE = [0, 0, 1]
COLOR_GREEN = [0, 1, 0]

def read_binary_file(filename):
    with open(filename, 'rb') as file:
        data = np.fromfile(file, dtype=np.uint8)
    return data

def binary_to_heatmap(binary_str, pad_char):
    n_bits = len(binary_str)
    n_rows = int(np.sqrt(n_bits))
    n_cols = int(np.ceil(n_bits / n_rows))
    binary_str += pad_char * (n_rows * n_cols - n_bits)
    binary_arr = np.array(list(binary_str)).reshape(n_rows, n_cols)
    
    heatmap = np.zeros((n_rows, n_cols, 3))
    heatmap[binary_arr == '1'] = COLOR_RED
    heatmap[binary_arr == '0'] = COLOR_BLUE
    heatmap[binary_arr == pad_char] = COLOR_GREEN

    return heatmap

def plot_heatmap(heatmap, title, target_path):
    plt.imshow(heatmap)
    
    # Add title and legend
    legend_elements = [
        Line2D([0], [0], marker='o', color='w', markerfacecolor='red', markersize=10, label='1'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', markersize=10, label='0'),
        Line2D([0], [0], marker='o', color='w', markerfacecolor='green', markersize=10, label='Pad')
    ]

    plt.legend(handles=legend_elements)
    plt.title(title)
    target_filename = os.path.splitext(os.path.basename(target_path))[0] + '_heatmap.png'
    plt.savefig(target_path, bbox_inches="tight", pad_inches=0)

def generate_heatmap(filename, target_path):
    data = read_binary_file(filename)
    binary_str = ''.join('{:08b}'.format(byte) for byte in data)
    
    title = 'Allocated clusters'
    heatmap_data = binary_to_heatmap(binary_str, PAD_CHAR)
    
    plot_heatmap(heatmap_data, title, target_path)

def main():
    parser = argparse.ArgumentParser(description='Generate a heatmap from a binary file.')
    parser.add_argument('filename', help='Name of the binary file')
    parser.add_argument('target', help='Target folder for images')

    args = parser.parse_args()
    generate_heatmap(args.filename, args.target)

if __name__ == '__main__':
    main()
