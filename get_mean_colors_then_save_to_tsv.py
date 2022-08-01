import csv

from util import get_formatted_datetime, find_all_files, get_mean_colors

def main():
    a_list = []

    ignore_string = './templates/'
    textures = './templates/images/svg/textures'

    ignore_dirs = ['colormap', 'effect', 'entity', 'environment', 'font', 'gui', 'item', 'map', 'misc', 'mob_effect', 'models', 'painting', 'particle']

    for file in find_all_files(textures):
        r, g, b, h, s, v = get_mean_colors(file)
        file = file[len(ignore_string):]
        if file[-4:] == '.svg':
            another_list = ['/{}/'.format(ignore_dir) in file for ignore_dir in ignore_dirs]
            if True not in another_list:
                a_list.append([file, r, g, b, h, s, v])

    output_file = 'output-{}.csv'.format(get_formatted_datetime())
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(a_list)

if __name__ == '__main__':
    main()