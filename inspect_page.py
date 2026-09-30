import sys

import pymupdf

file_name = sys.argv[1]
page_number = int(sys.argv[2])
sort = "--sort" in sys.argv

doc = pymupdf.open(file_name)
page = doc[page_number - 1]

print(f"=== {file_name} | page {page_number} | sort={sort} ===")
print(page.get_text(sort=sort))