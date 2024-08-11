#!/usr/bin/python3
"""This module is for markdown to HTML conversion."""
import sys
import os
import re


def parse_markdown_line(line, in_unordered_list, in_ordered_list):
    """
    Parses a single line of markdown and converts it to HTML.
    Handles headings, unordered lists, and ordered lists.
    """
    heading_match = re.match(r'^(#{1,6}) (.+)$', line)
    unordered_list_item_match = re.match(r'^- (.+)$', line)
    ordered_list_item_match = re.match(r'^\* (.+)$', line)

    if heading_match:
        # Close any open lists before starting a new heading
        if in_unordered_list:
            in_unordered_list = False
            line = f"</ul>\n<h{len(heading_match.group(1))}>" \
                   f"{heading_match.group(2)}</h{len(heading_match.group(1))}>"
        elif in_ordered_list:
            in_ordered_list = False
            line = f"</ol>\n<h{len(heading_match.group(1))}>" \
                   f"{heading_match.group(2)}</h{len(heading_match.group(1))}>"
        else:
            line = f"<h{len(heading_match.group(1))}>" \
                   f"{heading_match.group(2)}</h{len(heading_match.group(1))}>"

        return line, in_unordered_list, in_ordered_list

    if unordered_list_item_match:
        # Handle unordered list items
        if not in_unordered_list:
            in_unordered_list = True
            line = f"<ul>\n<li>{unordered_list_item_match.group(1)}</li>"
        else:
            line = f"<li>{unordered_list_item_match.group(1)}</li>"

        if in_ordered_list:
            in_ordered_list = False
            line = f"</ol>\n{line}"

        return line, in_unordered_list, in_ordered_list

    if ordered_list_item_match:
        # Handle ordered list items
        if not in_ordered_list:
            in_ordered_list = True
            line = f"<ol>\n<li>{ordered_list_item_match.group(1)}</li>"
        else:
            line = f"<li>{ordered_list_item_match.group(1)}</li>"

        if in_unordered_list:
            in_unordered_list = False
            line = f"</ul>\n{line}"

        return line, in_unordered_list, in_ordered_list

    # Close any open lists if the line is not a list item
    if in_unordered_list:
        in_unordered_list = False
        return f"</ul>\n{line}", in_unordered_list, in_ordered_list

    if in_ordered_list:
        in_ordered_list = False
        return f"</ol>\n{line}", in_unordered_list, in_ordered_list

    return line, in_unordered_list, in_ordered_list


def main():
    """Main function for markdown to HTML conversion."""
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
    in_unordered_list = False
    in_ordered_list = False
    for line in markdown_lines:
        html_line, in_unordered_list, in_ordered_list = parse_markdown_line(
            line.strip(), in_unordered_list, in_ordered_list)
        html_lines.append(html_line)

    # Close any open lists at the end of the document
    if in_unordered_list:
        html_lines.append("</ul>")
    if in_ordered_list:
        html_lines.append("</ol>")

    with open(output_file, 'w') as out_file:
        out_file.write("\n".join(html_lines))

    sys.exit(0)


if __name__ == "__main__":
    main()
