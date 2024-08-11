#!/usr/bin/env python3
"""Task 1 on rendering a README html file."""
import sys
import os


def main():
    """Check if the number of arguments is less than 2"""
    if len(sys.argv) < 3:
        print(
            "Usage: ./markdown2html.py README.md README.html",
            file=sys.stderr
            )
        sys.exit(1)

    # Get the input and output filenames
    markdown_file = sys.argv[1]
    output_file = sys.argv[2]

    # Check if the Markdown file exists
    if not os.path.isfile(markdown_file):
        print(f"Missing {markdown_file}", file=sys.stderr)
        sys.exit(1)

    # after all checks pass, proceed to the dummy conversion
    with open(markdown_file, 'r') as mad_file:
        markdown_content = mad_file.read()
        html_content = f"<html><body>{markdown_content}</body></html>"

    # Write the HTML content to the output file
    with open(output_file, 'w') as out_file:
        out_file.write(html_content)

    # Exit successfully
    sys.exit(0)


if __name__ == "__main__":
    main()
