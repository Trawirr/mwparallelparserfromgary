MULTILINE_TAGS = [

]

TEMPLATES = [

]

STARTERS = {
    "======": "======",
    "=====": "=====",
    "====": "====",
    "===": "===",
    "==": "==",
    "----": "",
    "###": '',
    "##": '',
    "#": '',
    "***": '',
    "**": '',
    "*": '',
    ";": '',
    ":": '',
    ":": '',
    " ": '',
}

TAG_ENDINGS = {
    "<!--": "-->",
    "{{": "}}",
    "'''": "'''",
    "''": "''",
    "[[": "]]",
    "[": "]",
    "<u>": '</u>',
    "<s>": '</s>',
    "<code>": '</code>',
    "<q>": '</q>',
    "<nowiki>": '</nowiki>',
    "<gallery": '</gallery>',
    "<ref>": '</ref>',
    "<ref ": '</ref>',
    "<ref": '/>',
    "<pre>": '</pre>',
    "<center>": "</center>",
    "<small>": "</small>",

}

TAG_NAME = {
    "<!--": "deleted",
    "{{": "template",
    "'''": 'bold',
    "''": 'italic',
    "[[": 'link',
    "[": "external link",
    "======": 'heading level 6',
    "=====": 'heading level 5',
    "====": 'heading level 4',
    "===": 'heading level 3',
    "==": 'heading level 2',
    "----": "horizontal rule",
    "###": 'numbered list level 3',
    "##": 'numbered list level 2',
    "#": 'numbered list level 1',
    "***": 'bullet list level 3',
    "**": 'bullet list level 2',
    "*": 'bullet list level 1',
    ";": 'definition 1',
    ":": 'definition 2',
    ":": 'indent',
    " ": 'preformatted',
    "<u>": 'underline',
    "<s>": 'deleted',
    "<code>": 'code',
    "<q>": 'quote',
    "<nowiki>": 'preformatted',
    "<gallery": 'gallery',
    "<ref>": 'ref',
    "<ref n": 'ref',
    "<ref ": 'ref',
    "<pre>": 'preformatted',
    "<center>": "center",
    "<small>": "small",

}

META_TAGS = [
    'ref',
    'template'
]

SUBSTRINGS_TO_DELETE = [
    'Category:',
    '\n',

]

NONPARSABLE_TAG_NAMES = [
    'template',
    'link',
    'preformatted',
    'gallery',
    'ref',
    'short ref',

]

REPETITIONS_TO_REPLACE = {
    '  ': ' '
}

MAX_LEN_TAG = 10

