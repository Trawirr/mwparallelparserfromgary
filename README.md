# mwparallelparserfromgary

This is a Python package for MediaWiki_wikicode parallel parsing.

# Basic usage
```python
parser = Parser()

# Parsing text
wikicode = '...'
wikicode_parsed = parser.parse_text(wikicode)

# Parsing text file with wikicode
wikicode_parsed = parser.parse_file('wikicode.txt')
```

''wikicode_parsed['lines']'' contains list of raw text lines.

``wikicode_parsed['tags']`` contains list of tags.

``wikicode_parsed['meta_tags']`` contains list of meta tags such as templates, references etc.

# Printing results
```
parser = Parser()
parser.parse_text(wikicode)

parser.print_tags_meta()
parser.print_tags()
parser.print_lines()
```
