import os
import sys
sys.path.append('../')
import config
from slimit import minify

modulelist = ['core', 'editor','workbench']

def encode_module(input_path, output_path):
    for m in modulelist:
        listingfile(m, input_path, output_path)
        
def listingfile(m, input_path, output_path):
    content = ''
    for f in os.listdir(input_path+m):
        print 'm='+m+',f='+f
        filepath = input_path + m + '/' + f
        if os.path.isfile(filepath):
            fd = open(filepath, 'r')
            for line in fd:
                content += line
            fd.close()
            content += '\n'
    out =  minify(content, mangle=True)
    f = open(output_path+m+'.js', 'w')
    f.write('/* Copyright (C) 2012 Technical Rockstars Co.,Ltd. All Rights Reserved. */'+out)
    f.close()
    return out

if __name__ == '__main__':
    argvs = sys.argv
    argc = len(argvs)
    if argc == 1:
        encode_module(config.CLOOCA_ROOT+'/static/js/dev/', config.CLOOCA_ROOT+'/static/js/')
    if argc == 2:
        encode_module(config.CLOOCA_ROOT+'/static/js/dev/', config.CLOOCA_ROOT+'/static/js/')
