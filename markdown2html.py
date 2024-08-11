#!/usr/bin/python3
"""task module for markdown to html conversion"""
import sys
import os
import re


def parse_markdown_line(line):
    """
    Parses single line of markdown and convert it to HTML if matches h pattern
    """
    heading_match = re.match(r'^(#{1,6}) (.+)$', line)

    if heading_match:
        heading_level = len(heading_match.group(1))
        heading_text = heading_match.group(2)
        return f"<h{heading_level}>{heading_text}</h{heading_level}>"
    return line


def main():
    """Check if the number of arguments is less than 2"""
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
    for line in markdown_lines:
        html_line = parse_markdown_line(line.strip())
        html_lines.append(html_line)

    with open(output_file, 'w') as out_file:
        out_file.write("\n".join(html_lines))

    sys.exit(0)


if __name__ == "__main__":
    main()
