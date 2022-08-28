# coding=utf-8
import os
import re
import sys


def style_to_fill(svg):
    style_pos = svg.find('<style type="text/css">')
    close_style_pos = svg.find('</style>')

    style = {}

    for s_class in svg[style_pos:close_style_pos].split('.'):
        if s_class.find('{') != -1:
            props = s_class.split('{')
            style[props[0]] = props[1].replace('}', '')

    for key in style.keys():
        attr = style[key].split(':')
        svg = svg.replace('class="' + key + '"', attr[0] + '="' + attr[1].replace(';', '') + '"')

    return svg


def format_svg(svg_file):
    svg = ""

    for line in svg_file.readlines():
        svg += line

    svg = svg.replace('<svg', '<symbol') \
        .replace('version="1.1" ', '') \
        .replace('xmlns:xlink="http://www.w3.org/1999/xlink" ', '') \
        .replace('</svg', '</symbol') \
        .replace('<?xml version="1.0" encoding="utf-8"?>', '') \
        .replace('x="0px" y="0px"', '')

    svg = re.sub(r'id="[^"]*" ', '', svg)
    svg = re.sub(r'id="[^"]*"', '', svg)
    svg = re.sub(r'xml:space="[^"]*" ', '', svg)
    svg = re.sub(r'xml:space="[^"]*"', '', svg)
    svg = re.sub(r'style="[^"]*" ', '', svg)
    svg = re.sub(r'style="[^"]*"', '', svg)

    svg = style_to_fill(svg)

    svg = re.sub(r'<!--(.*?)-->|\s\B', '', svg)
    svg = re.sub(r'<style type="[^"]*">[^"]*<\/style>', '', svg)
    return svg


def perform(path):
    svg_file = open(path, 'r')

    extension_pos = path.find('.svg')
    new_file_path = path[:extension_pos] + '-formatted' + path[extension_pos:]

    svg = format_svg(svg_file)

    new_file = open(new_file_path, 'w')
    new_file.write(svg)

    svg_file.close()
    new_file.close()


def main():
    arg = sys.argv[1]

    if arg == '-R':
        path = sys.argv[2]

        for filename in os.listdir(path):
            f = os.path.join(path, filename)

            if os.path.isfile(f) and f.split('.')[-1] == "svg" and f.find('-formatted') == -1:
                perform(f)
    else:
        path = arg

        if path.split('.')[-1] != "svg":
            return

        perform(path)


if __name__ == "__main__":
    main()
