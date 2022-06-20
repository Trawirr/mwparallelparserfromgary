from settings import *

class Tag:
    def __init__(self, type, start, line, length, attributes={}):
        self.type = type
        self.spans = [{
            'line': line,
            'start': start,
            'length': length
        }]
        if attributes:
            self.attributes = attributes

    def __str__(self) -> str:
        return str({attr:self.__getitem__(attr) for attr in [a for a in 
        dir(self) if not a.startswith('__') and not callable(getattr(self, a))]})

    def __getitem__(self, key):
        try:
            return getattr(self, key)
        except AttributeError:
            return None

    @classmethod
    def create_tag(cls, tag_type, start, line, content):
        attributes = {}
        if 'link' in tag_type:
            destination, content = Tag.disassembly_link_content(tag_type=tag_type, content=content)
            attributes['destination'] = destination

        if tag_type in META_TAGS:
            attributes['content'] = content
            content = ''
            if tag_type == 'template':
                start, line = 0, 0
        elif tag_type not in NONPARSABLE_TAG_NAMES:
            content = Tag.fix_content(content)

        tag = Tag(tag_type, start, line, len(content), attributes)
        return content, tag

    @staticmethod
    def fix_content(content):
        for rep in REPETITIONS_TO_REPLACE:
            while rep in content:
                content = content.replace(rep, REPETITIONS_TO_REPLACE[rep])
        return content.strip()

    @staticmethod
    def disassembly_template_content(content):
        pass

    @staticmethod
    def disassembly_link_content(tag_type, content):
        if tag_type == 'link':
            if '|' in content:
                content_split = content.split('|')
                destination, content = content_split[0], content_split[-1]
            else:
                destination = content
        elif tag_type == 'external link':
            content_split = content.split(' ')
            destination, content = content_split[0], " ".join(content_split[1:])
        return destination, content

    def print_attributes(self):
        for attr in [a for a in dir(self) if not a.startswith('__') and not callable(getattr(self, a))]:
            print(attr)

class Link(Tag):
    def __init__(self, type, start, line, content, link):
        super().__init__(type=type, start=start, line=line, content=content)
        self.attributes = {
            'destination': link
        }

class Template(Tag):
    def __init__(self, type, start, line, content):
        super().__init__(type=type, start=start, line=line, content=content)
        #self.template = template
