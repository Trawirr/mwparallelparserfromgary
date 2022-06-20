import time
from .. import parserfromgary as GaryParser

TAG_ENDINGS = {
    "'''": "'''",
    "[[": "]]",
    "''": "''",
    "==": "==",
    "*": '\n',
    ";": '\n',
    ":": '\n',
    "<u>": '</u>',
    "<s>": '</s>',
    "<code>": '</code>',
    "<q>": '</q>',
    "<nowiki>": '</nowiki>',

}

TAG_NAME = {
    "''": 'italic',
    "'''": 'bold',
    "[[": 'link',
    "==": 'heading',
    "*": 'list element',
    ";": 'definition 1',
    ":": 'definition 2',
    "<u>": 'underline',
    "<s>": 'deleted',
    "<code>": 'code',
    "<q>": 'quote',

}

class Parser:
    def __init__(self):
        self.tags = []
        self.text = ''

    def __getitem__(self, item):
        return list(filter(lambda x: x['type'] == item, self.tags))

    def __parse(self, text):
        self.text = text
        opened_tag = None
        opened_pos = None
        for line in [l + '\n' for l in text.split('\n')]:
            #print(f'{row_num}. {line}')
            i = 0
            while i < len(line):
                if opened_tag:
                    # drugi warunek, aby zapobiec pomyłce jak w przykładzie:
                    # '''''bold and italic''''' = ''' ''bold and italic'' ''' !
                    if line[i:].startswith(TAG_ENDINGS[opened_tag]) and line[
                            min(i + len(opened_tag), len(line) - 1)] not in opened_tag:
                        # print('TAG:', line[opened_pos:i])
                        self.add_tag(line[opened_pos:i], TAG_NAME[opened_tag], (opened_pos, i))
                        i += len(TAG_ENDINGS[opened_tag])
                        opened_tag = None
                        continue
                else:
                    for op in TAG_ENDINGS:
                        if opened_tag is not None:
                            break
                        if line[i:].startswith(op):
                            #print(len(self.tags)+1, op)
                            opened_tag = op
                            opened_pos = i + len(op)
                            i += len(op)
                            break
                i += 1

    def parse_text(self, text):
        self.tags = []
        self.__parse(text)
        for tag in self.tags:
            #print('tag loop')
            self.__parse(tag['content'])

    def parse_file(self, filename):
        self.tags = []
        with open(filename, 'r') as f:
            text = f.read()
        self.parse_text(text)

    def add_tag(self, content, tag_type, pos):
        tag = {
            'type': tag_type,
            'start': pos[0],
            'length': pos[1]-pos[0],
            'content': content
        }
        self.tags.append(tag)

    def print_tags(self):
        print(self.tags)
        for i, tag in enumerate(self.tags):
            print(f'\n{i}.{tag}')


if __name__ == '__main__':
    with open('wikicode.txt', 'r', encoding="utf8") as file:
        wikicode = file.read()

    parser = Parser()
    start = time.time()

    parser.parse_text(wikicode)
    tags1 = parser.tags

    gary_parser = GaryParser()
    gary_parser.parse_text(wikicode)
    tags2 = gary_parser.tags

    print(f'tags lengths: {len(tags1)}, {len(tags2)}')

    tags_intersection = list(filter(lambda x: x not in tags1, tags2))
    for i, tag in enumerate(tags_intersection):
        print(f'{i}. {tag}')
        # if tag not in tags1:
        #     print(tag)