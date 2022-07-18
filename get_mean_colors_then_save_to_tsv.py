import csv

from util import get_formatted_datetime, find_all_files, get_mean_colors

def main():
    a_list = []

    ignore = './templates/'

    for file in find_all_files('./templates/images/textures'):
        r, g, b, h, s, v = get_mean_colors(file)
        file = file[len(ignore):]
        print('.png' in file, file)
        if file[-4:] == '.png':
            a_list.append([file, r, g, b, h, s, v])

    output_file = 'output-{}.csv'.format(get_formatted_datetime())
    with open(output_file, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(a_list)

if __name__ == '__main__':
    main()