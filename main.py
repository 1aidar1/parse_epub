#! /usr/bin/env python
# -*- coding: utf-8 -*-
# -*- codecs: utf-8 -*-
from bs4 import BeautifulSoup

import ebooklib
import codecs
import os
import json
import re

from ebooklib import epub


def cutWholeHtml(pathToFile,outFile):
    with open(pathToFile, 'r', encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        with open(outFile, 'w', encoding='utf-8') as writer:
            first = True
            i = 1
            for p in soup.find_all('section'):
                # if first:
                #     first = False
                writer.write(str(p))
                print(str(i),str(p))
                i = i + 1


def epub2thtml(epub_path):
    book = epub.read_epub(epub_path)
    chapters = []
    for item in book.get_items():
        if item.get_type() == ebooklib.ITEM_DOCUMENT:
            chapters.append(item.get_content())
    return chapters


# Press the green button in the gutter to run the script.

def htmlToFile(book,out):
    chapters = epub2thtml(book)
    with codecs.open(out,'w', "utf-8") as f:
        i = 0
        for chapter in chapters:
            c = chapter.decode("utf-8")
            f.write(c)

def parseHtmlChaps():
    directory = 'chapters'
    i = 1
    for filename in os.listdir(directory):
        if filename.endswith(".xhtml"):
            print(directory + '/' + filename)
            with open('./'+directory + '/' + filename, 'r',encoding='utf-8') as f:
                contents = f.read()
                soup = BeautifulSoup(contents, 'lxml')
                with open('./' + 'generated' + '/' + filename.replace(".xhtml","..html"), 'w', encoding='utf-8') as writer:
                    first = True
                    for p in soup.find_all('section'):
                        if first:
                            writer.write("<head><link rel='stylesheet' href='style.css' type='text/css'/></head>")
                            first = False
                        writer.write(str(p))
        i  = i + 1
            # print(directory + '/' + filename)

def chapters():
    out = []
    with open('./chapters/toc.xhtml', 'r', encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        i = 1

        for p in soup.find_all('a'):

            parent = 0
            if p['href'] == 'title-page.xhtml#title-page':
                p['href'] = 'title-page.html'
            else:
                anchor = re.split("tocForcedId", p['href'], 1)[1]
                p['href'] = re.split("-",p['href'],1)[1]
                p['href'] = re.split("\\.",p['href'],1)[0]
                parent = int(p['href'])
                p['href'] = "chapter"+str(parent) + ".html"

            if parent == i:
                parent = 0

            obj = {
                "BookId": 2,
                "ChapterAnchor": anchor,
                "Name": p.text,
                "ParentId": parent,
                "Prev": i - 1,
                "Next": i + 1,
                "Content": "books/2/" + p['href']

            }
            out.append(obj)

            print(str(i) + " " +str(p) + str(p.parent))
            i = i + 1

    with open("./chapters.json", "w", encoding="utf-8") as js:
        (json.dump(out, fp=js, indent=4, ensure_ascii=False))

def parseChapterContents(input):
    i = 0
    with open(input,'r',encoding="utf-8") as source:
        chapter = []
        for line in source:
            line = (line.rstrip())
            if line == "<header>":
                with open("generated/chapter"+str(i)+".html",'w',encoding='utf-8') as writer:
                    for v in chapter:
                        print(v)
                        writer.write(v+"\n")
                chapter = []
                chapter.append(line)
                i = i + 1
            else:
                chapter.append(line)
        with open("generated/chapter" + str(i) + ".html", 'w', encoding='utf-8') as writer:
            for v in chapter:
                print(v)
                writer.write(v + "\n")


def getChapters(input):
    i = 1
    arr = []
    with open(input, 'r', encoding='utf-8') as f:
        contents = f.read()
        soup = BeautifulSoup(contents, 'lxml')
        list = soup.find_all(["h1", "h2", "h3","h4"])
        last_h1 = 0
        last_h2 = 0

        for heading in list:
            parent = None

            if heading.name == "h1":
                parent = None
                print(parent)
                last_h1 = i


            if heading.name == "h2":
                last_h2 = i
                parent = last_h1
            if heading.name == "h3":
                parent = last_h2

            if i > 1:
                prev = i - 1
            else:
                prev = None

            obj = {
                "BookId": 2,
                "Chapter": i,
                "Name": heading.text,
                "ParentId": parent,
                "Prev": prev,
                "Next": i + 1,
                "Content": "books/2/chapter"+str(i)+".html"
            }
            arr.append(obj)

            print(i, heading.name,parent)
            i = i + 1
    with open("./chapters.json", "w", encoding="utf-8") as js:
        (json.dump(arr, fp=js, indent=4, ensure_ascii=False))


if __name__ == '__main__':
    chapters()
    book = "book.epub"
    htmlToFile(book,'test.html')
    cutWholeHtml('test.html','cut.html')
    parseChapterContents('cut.html')
    getChapters('./cut.html')

    # parseHtmlChaps()


