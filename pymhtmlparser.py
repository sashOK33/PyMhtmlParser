# -*- coding: utf-8 -*-
import codecs


class PyMhtml:
    def __init__(self, filename):
        self.filename = filename

        with codecs.open(self.filename, 'r', encoding='utf8') as f:
            lines = f.readlines()
        f.close()

        begin = 0
        end = 0

        for i in range(len(lines)):
            if '<!DOCTYPE html>' in lines[i] and not begin:
                begin = i
                print(i)
            if '</html>' in lines[i] and not end:
                end = i + 1
                print(i)
        self.html = lines[begin:end].copy()
        self.begin = lines[:begin].copy()
        self.end = lines[end:].copy()
        self.code = lines

    def split(self):
        i = 0
        size = len(self.html)
        res = []
        while i + 75 < size:
            if self.html[i + 74] == '=':
                res.append(self.html[i: i + 74] + '=\r\n')
                i += 74
            elif self.html[i + 73] == '=':
                res.append(self.html[i: i + 73] + '=\r\n')
                i += 73
            else:
                res.append(self.html[i: i + 75] + '=\r\n')
                i += 75
        res.append(self.html[i:])
        self.html = res
        return res

    def join(self):
        res = []
        for line in self.html:
            res.append(line.replace('=\r\n', ''))
        self.html = ''.join(res)
        self.code = self.begin + self.html + self.end

    def get_mhtml(self, out_filename):
        self.join()
        with codecs.open(out_filename, 'w', encoding='utf8') as f:
            for line in self.code:
                f.write(line)
        f.close()

    def delete_tag(self, tag_name):
        begin = self.html.find(tag_name)
        for i in range(begin, 0, -1):
            if self.html[i] == '<':
                begin = i
                break
        i = begin
        tag = ''
        while ord(self.html[i]) != 32:
            tag = tag + self.html[i]
            i += 1
        end_teg = '</' + tag[1:] + '>'
        count = 1
        for i in range(begin + 1, len(self.html)):
            new_teg = self.html[i: i + len(tag)]
            if new_teg == tag:
                count += 1
            new_end_teg = self.html[i: i + len(end_teg)]
            if new_end_teg == end_teg:
                count -= 1
            if count == 0:
                end = i + len(end_teg)
                self.html = self.html[: begin] + self.html[end:]
                return self.html[begin: end]
        return ValueError(f'Tag {tag} not found!')
