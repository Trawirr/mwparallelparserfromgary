from .conftest import ParserTestCase


class DoubleBracesTestCase(ParserTestCase):
    def test_basic(self):
        wikitext = '{{This will be deleted}}'
        self.assertParsed(wikitext, [])

    def test_embeded(self):
        wikitext = '{{This <ref>{{This is a test}}</ref>}}'
        self.assertParsed(wikitext, [])

    def test_with_ref_and_link_after(self):
        wikitext = 'to<ref>{{Cytuj stronę |url=http://www.mytopdozen.com/Best_Polish_Composers.html |tytuł=Lista polskich kompozytorów najczęściej wymienianych w internecie |język=en |data dostępu=3 grudnia 2008}}</ref>: [[Fryderyk Chopin]]'
        self.assertParsed(wikitext, ['to: Fryderyk Chopin'])
