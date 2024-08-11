#!/usr/bin/python3
"""module to convert markdown to html."""
import sys
import os
import re


def parse_markdown_line(line, in_list):
    """
    Parses a single line of markdown and converts it to HTML.
    Handles headings and unordered lists.
    """
    heading_match = re.match(r'^(#{1,5}) (.+)$', line)
    list_item_match = re.match(r'^- (.+)$', line)

    if heading_match:
        heading_level = len(heading_match.group(1))
        heading_text = heading_match.group(2)
        return f"<h{heading_level}>{heading_text}</h{heading_level}>", in_list

    if list_item_match:
        list_item = list_item_match.group(1)
        if not in_list:
            return f"<ul>\n<li>{list_item}</li>", True
        return f"<li>{list_item}</li>", in_list

    if in_list:
        return f"</ul>\n{line}", False

    return line, in_list


def main():
    """main module for our functionalities"""
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
            )
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
        out_file.write("<html><body>\n")
        out_file.write("\n".join(html_lines))
        out_file.write("\n</body></html>")

    sys.exit(0)


if __name__ == "__main__":
    main()
