from settings import *
from tag import *
import time

class Parser:
    def __init__(self):
        self.lines = []
        self.text = ''
        self.tags = []
        self.tags_meta = []

    # get tags by type
    def __getitem__(self, item):
        if item == 'lines':
            return self.reconstruct_text().split('\n')
        return list(filter(lambda x: x['type'] == item, self.tags))

    def find_templates(self):
        templates_found = []
        start = 0
        while start < len(self.lines)-1:
            template_found = False
            if self.lines[start].startswith('{{'):
                counter = 0
                end = start
                while end < len(self.lines)-1:
                    counter += self.lines[end].count('{{') - self.lines[end].count('}}')
                    end += 1
                    if self.lines[end].startswith('}}') and counter == 1:
                        template_found = True
                        break
                if template_found:
                    end += 1
                    templates_found.append(self.lines[start:end])
                    for i in range(start, end+1):
                        self.lines[i] = ''
                    start = end
                    continue

            start += 1

        for content in templates_found:
            self.__append_tags('template', '\n'.join(content))

    def __parse_line(self, text, line):
        if not text:
            return ''

        for opening in STARTERS:
            ending = STARTERS[opening]
            if text.startswith(opening) and text.endswith(STARTERS[opening]):
                if len(ending) > 0:
                    content = text[len(opening):-len(ending)]
                else:
                    content = text[len(opening):]
                if TAG_NAME[opening] not in NONPARSABLE_TAG_NAMES:
                    content = self.__parse_line_recursively(content, line)
                return self.__append_tags(TAG_NAME[opening], content, line)
        text = self.__parse_line_recursively(text, line)
        return self.__append_tags('', text, line)

    def __add_tag(self, text, opened_pos, closed_pos, opening, closing, line, start, continuation):
        tag_content = text[opened_pos:closed_pos]
        tag_content_parsed = tag_content
        if TAG_NAME[opening] not in NONPARSABLE_TAG_NAMES:
            tag_content_parsed = self.__parse_line_recursively(
                tag_content, line, start + opened_pos - len(opening))

        tag_content_replacement = self.__append_tags(
            TAG_NAME[opening], tag_content_parsed, line, start, continuation)

        text = text.replace(opening + tag_content + closing, tag_content_replacement)
        return text, opened_pos - len(opening) + len(tag_content_replacement)

    def __append_tags(self, tag_type, content, line=0, start=0, continuation=''):
        tag_content, tag = Tag.create_tag(tag_type, start, line, content, continuation)
        if tag_type in META_TAGS:
            self.tags_meta.append(tag)
        else:
            self.tags.append(tag)
        return tag_content

    def __parse_line_recursively(self, text, line=0, start=0):
        text = text.strip()
        i = 0
        opened_tags = []
        opened_pos = len(text)
        something_happened = False
        while i < len(text):
            # sprawdzanie, czy to może być domknięcie innego tagu
            if len(opened_tags) > 1:
                op = opened_tags[-1]
                closed_tag = TAG_ENDINGS[op]
                if text[i:i+len(closed_tag)] == closed_tag:
                    i += len(closed_tag)
                    something_happened = True
                    opened_tags.pop()
                    continue

            # sprawdzenie, czy to jest domknięcie aktualnego tagu
            if len(opened_tags) > 0:
                opening = opened_tags[0]
                closed_tag = TAG_ENDINGS[opening]
                if text[i:i + len(closed_tag)] == closed_tag:

                    continuation_end = i+len(closed_tag)
                    for j in range(i+len(closed_tag), len(text)):
                        if not text[j].isalpha():
                            continuation_end = j
                            break
                    continuation = text[i+len(closed_tag):continuation_end]

                    text, i = self.__add_tag(
                        text, opened_pos, i, opening, closed_tag, line, start + opened_pos - len(opening), continuation)
                    opened_pos = len(text)
                    opened_tags = []
                    something_happened = True
                    continue

            # sprawdzanie, czy znaleziono tag
            for op in TAG_ENDINGS:
                if len(opened_tags) > 0:
                    closed_tag = TAG_ENDINGS[opened_tags[0]]
                else:
                    closed_tag = None
                if text[i:].startswith(op) and op != closed_tag:
                    opened_tags.append(op)
                    i += len(op)
                    opened_pos = min(opened_pos, i)
                    something_happened = True
                    break
            if not something_happened:
                i += 1
            something_happened = False

        # dodawanie tagu, jeśli nie znaleziono zamknięcia tagu
        if len(opened_tags) > 0:
            opening = opened_tags[0]
            text, i = self.__add_tag(text, opened_pos, i, opening, '', line, start + opened_pos - len(opening), '')
        return text

    def parse_text(self, text):
        self.text = text
        self.lines = text.split('\n')
        self.tags = []
        self.tags_meta = []
        self.find_templates()
        i = 0
        while i < len(self.lines):
            self.lines[i] = self.__parse_line(self.lines[i], i)
            if self.lines[i] == '':
                self.lines.pop(i)
            else:
                i += 1
        i = 0
        while i < len(self.tags):
            if self.tags[i].type == '':
                self.tags.pop(i)
            else:
                i += 1
        return {'lines': self.lines, 'tags': self.get_tags(), 'meta_tags': self.tags_meta}

    def get_tags(self):
        return [str(tag) for tag in self.tags]

    def parse_file(self, filename, encoding="utf8"):
        self.tags = []
        with open(filename, 'r') as f:
            text = f.read()
        self.parse_text(text)

    def print_tags(self):
        print('Tags:')
        for i, tag in enumerate(self.tags):
            print(f"    {tag}")

    def print_tags_meta(self):
        print('Metadata:')
        for i, tag in enumerate(self.tags_meta):
            print(f"    {tag}")

    def print_lines(self):
        print('Lines:')
        for i, line in enumerate(self.lines):
            print(f"    {line}")

    def save(self):
        with open('result_tags.txt', 'w+', errors="ignore") as f:
            for i, tag in enumerate(self.tags):
                f.write(str(i) + ', ' + str(tag) + '\n')
        with open('result_text.txt', 'w+', errors="ignore") as f:
            f.write(self.text)

if __name__ == '__main__':
    parser = Parser()

    with open('tests/wikicode.txt', encoding="utf8") as f:
        wikicode = f.read()
    parser.parse_text(wikicode)
    parser.save()
    parser.print_tags_meta()
    parser.print_tags()
    parser.print_lines()
