#!/usr/bin/env python
#coding=utf-8
import os
import markdown2
import settings

def processmkd(md_path, html_path):
    theHead = ''
    thehtml = markdown2.markdown_path(md_path)
    filename = os.path.split(md_path)[1]
    _filename = os.path.splitext(filename)[0]
    theTitle = unicode(_filename,"utf-8")
    fileHandle = open(os.path.join(html_path, _filename+'.html' ), "w")
    theHead = '<!DOCTYPE html>'
    theHead += '<html><head><meta charset="utf-8"/><title>' + theTitle + '</title><link href="demo.css" type="text/css" rel="stylesheet"/></head><body>'
    theHead += thehtml
    theHead += '</body></html>\n'
    theHTML =  theHead.encode('utf-8')
    fileHandle.write(theHTML)
    fileHandle.close()

if __name__=='__main__':
    md_source_path = os.path.join(settings.PROJECT_DIR + '/static/html/md')
    html_path = os.path.join(settings.PROJECT_DIR + '/static/html')
    for md_file in os.listdir(md_source_path):
        md_path = os.path.join(md_source_path, md_file)
        dir, ext =  os.path.splitext(md_path)
        if ext == '.md':
            processmkd(md_path, html_path)
            print "convert %s "%md_path 
