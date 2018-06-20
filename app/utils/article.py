from html.parser import HTMLParser


class MyHTMLParser(HTMLParser):
    def __init__(self):
        self.pre_count = 0
        self.table_count = 0
        self.data = []
        return super(MyHTMLParser, self).__init__()
    
    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.pre_count += 1
        elif tag == 'table':
            self.table_count += 1
        print('starttag', tag, attrs)
    
    def handle_endtag(self, tag):
        if tag == 'pre':
            self.pre_count -= 1
        elif tag == 'table':
            self.table_count -= 1
        print('endtag', tag)
    
    def handle_data(self, data):
        if not self.pre_count and not self.table_count:
            self.data.append(data)
        print('data', data)
    
    def __clean_data(self):
        valid_data = []
        for item in self.data:
            n_item = item.replace('\n', '').strip()

            if n_item:
                valid_data.append(n_item)
        self.data = valid_data
    
    def get_abscontent(self, html_):
        self.feed(html_)
        self.__clean_data()
        ab_data = '<strong>' + self.data.pop(0) + '</strong>'
        while len(ab_data) < 120 and self.data:
            ab_data = ' '.join([ab_data, self.data.pop(0)])
        return ab_data + ' ...'
