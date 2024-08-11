#!/usr/bin/python3
"""this module file is for markdown to html conversion"""
import sys
import os
import re


def parse_markdown_line(line, in_list):
    """
    Parses a single line of markdown and converts it to HTML.
    Handles headings and unordered lists.
    """
    heading_match = re.match(r'^(#{1,6}) (.+)$', line)
    list_item_match = re.match(r'^- (.+)$', line)

    if heading_match:
        if in_list:
            in_list = False
            return (f"</ul>\n<h{len(heading_match.group(1))}>"
                    f"{
                        heading_match.group(2)
                        }</h{len(heading_match.group(1))}>",
                    in_list)

        return (f"<h{len(heading_match.group(1))}>"
                f"{heading_match.group(2)}</h{len(heading_match.group(1))}>",
                in_list)

    if list_item_match:
        if not in_list:
            in_list = True
            return f"<ul>\n<li>{list_item_match.group(1)}</li>", in_list

        return f"<li>{list_item_match.group(1)}</li>", in_list

    if in_list:
        in_list = False
        return f"</ul>\n{line}", in_list

    return line, in_list


def main():
    """main function for markdown to html conversion"""
    if len(sys.argv) < 3:
        print("Usage: ./markdown2html.py README.md README.html",
              file=sys.stderr)
        sys.exit(1)

    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    with open(markdown_file, 'r') as md_file:
        markdown_lines = md_file.readlines()

    html_lines = []
    in_list = False
    for line in markdown_lines:
        html_line, in_list = parse_markdown_line(line.strip(), in_list)
        html_lines.append(html_line)

    if in_list:
        html_lines.append("</ul>")

    with open(output_file, 'w') as out_file:
        out_file.write("\n".join(html_lines))

    sys.exit(0)


if __name__ == "__main__":
    main()
