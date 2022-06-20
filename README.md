# mwparallelparserfromgary

This is a Python package for MediaWiki_wikicode parallel parsing

# Usage
```python
parser = Parser()

# Parsing text
wikicode = '...'
wikicode_parsed = parser.parse_text(wikicode)

# Parsing text file with wikicode
wikicode_parsed = parser.parse_file('wikicode.txt')
```

