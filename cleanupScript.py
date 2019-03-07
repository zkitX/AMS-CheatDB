#!/usr/bin/env python3

"""cleanupScript.py: Data cleansing to make cheat files compatible with atmosphère."""

__author__ = 'TehPsychedelic'

import os
import re

baseFolder = 'atmosphere/titles'
fileExt = '.txt'
backupExt = '.bak'
maxSize =  64
patternCredits = re.compile(r'\[From (.*) by (.*) for (.*)\]$')
patternCheatNamea = re.compile(r'\[(.*)\]$')
patternCheatNameb = re.compile(r'([ ]*)\[(.*)\]([ ]*)$')
patternCheat1a = re.compile(r'([a-zA-Z0-9]{8})+([ ]{1}[a-zA-Z0-9]{8})*$') # Does not check max 3 (eg. 4 blocks is ok).
patternCheat1b = re.compile(r'(\s)*(\s*[a-zA-Z0-9]{8}\s*)+(\s+[a-zA-Z0-9]{8}\s*)*(\s)*$') # Does not check max 3 (eg. 4 blocks is ok). This version takes care of multiple spaces and/or trailing tabs.
patternCheat2 = re.compile(r'\[HEAP\+[a-zA-Z0-9]+\] ;\([a-zA-Z0-9]+\)$')
patternEmptyLinea = re.compile(r'$')
patternEmptyLineb = re.compile(r'[ ]+$')

def processLine(line):
    if patternCredits.match(line):
        return '[Credits ' + patternCredits.match(line).group(2) + ']\n' # Does not check if author length is 50ish characters or so.
    elif patternCheatNamea.match(line) and len(line) > maxSize:
        return line[:maxSize] # Does not check if last character is newline in which case needs to cut before closing ] then append ']\n'. Does not check if it cuts midway and needs to append ']\n'. Does not check if it's actually a cheat name (next line = cheat code).
    elif patternCheatNamea.match(line) and len(line) <= maxSize:
        return line
    elif patternCheatNameb.match(line) and len(line) > maxSize:
        return line.strip()[:maxSize] + '\n' # Does not check if last character is newline in which case needs to cut before closing ] then append ']\n'. Does not check if it cuts midway and needs to append ']\n'. Does not check if it's actually a cheat name (next line = cheat code).
    elif patternCheatNameb.match(line) and len(line) <= maxSize:
        return line.strip() + '\n'
    elif patternCheat1a.match(line):
        return line
    elif patternCheat1b.match(line):
        return re.sub('\s+', ' ', line).strip() + '\n'
    elif patternCheat2.match(line):
        return line
    elif patternEmptyLinea.match(line):
        return line # Respect empty line
    elif patternEmptyLineb.match(line):
        return '\n' # Respect empty line
    else:
        return ''

def processFile(fileName):
    print('Processing: ' + fileName)

    modifiedFlag = False
    oldFile = open(fileName,'r')
    newFile = open(fileName + backupExt, 'w')

    for line in oldFile:
        newLine = processLine(line)
        if newLine != line:
            modifiedFlag = True
        newFile.write(newLine)

    oldFile.close()
    newFile.close()

    if modifiedFlag:
        print('\tModified!')
        os.remove(fileName)
        os.rename(fileName + backupExt, fileName)
    else:
        os.remove(fileName + backupExt)

def main():
    for root, dirs, files in os.walk(baseFolder):
        for file in files:
            if file.endswith(fileExt):
                 processFile(os.path.join(root, file))

if __name__ == "__main__": main()
