# -*- coding: utf-8 -*-
"""
Created on Thu Nov  7 12:40:31 2024

@author: Charlie
"""
import os
import shutil
import trimesh

file = open("2Body.obj")
folderPath = 'TEMPFILES'
tfile = None
tfileNum = 0
vertCount = 0
vertOffset = 0

bodies = []
vlines = []
vtlines = []
vnlines = []
flines = []


if os.path.exists(folderPath):
    if os.path.isdir(folderPath):  # Check if it's a directory
        shutil.rmtree(folderPath)  # Remove the directory and its contents

os.makedirs(folderPath, exist_ok=True)

for line in file:
    if line.startswith('mtllib'):
        mtlLine = line
        mtlfile = line.strip('mtllib ').strip('\n')
        shutil.copy(mtlfile, folderPath)
    
    if line.startswith('v '):
        vertCount += 1
        vlines.append(line)

    if line.startswith('vt '):
        vtlines.append(line)

    if line.startswith('vn '):
        vnlines.append(line)

    if line.startswith('f '):
        flines.append(line)

    if line.startswith('usemtl '):
        flines.append(line)
        
    if line.startswith('g'):
        bodyLine = line
        bodyName = line.strip('g ').strip()
        
        if tfile != None:
            tfile.close()
            bodies.append([vlines, vtlines, vnlines, flines])
            vlines = []
            vtlines = []
            vnlines = []
            flines = []
            
        tFileName = "tBody" + str(tfileNum) + '.obj'
        tfileNum += 1
        tfile = open(folderPath + '/' + tFileName, 'w')
        print(bodyName)
        
        tfile.write("# Body Name == " + bodyName + '\n')
        tfile.write(mtlLine)
        vertOffset = vertCount
        
        
    if tfile != None:
                
        if line.startswith('f'):
            data = line.strip().strip('f ').split(' ')
            line = 'f '

            d = data[0].split('/')
            line += str(int(d[0]) - vertOffset) + '/'
            line += str(int(d[1]) - vertOffset) + '/'
            line += str(int(d[2]) - vertOffset) + ' '
            
            d = data[1].split('/')
            line += str(int(d[0]) - vertOffset) + '/'
            line += str(int(d[1]) - vertOffset) + '/'
            line += str(int(d[2]) - vertOffset) + ' '
            
            d = data[2].split('/')
            line += str(int(d[0]) - vertOffset) + '/'
            line += str(int(d[1]) - vertOffset) + '/'
            line += str(int(d[2]) - vertOffset) + '\n'
            
        tfile.write(line)

if tfile != None:
    tfile.close()

bodies.append([vlines, vtlines, vnlines, flines])




print(len(bodies))


tfile = open('TEMPFILES/combined0.obj', 'w')
tfile.write(mtlLine)
tfile.write('g PCB\n')

vertCount = 0;

for b in bodies[:5]:
    for l in b[0]:
        tfile.write(l)
        vertCount += 1;
    for l in b[1]:
        tfile.write(l)
    for l in b[2]:
        tfile.write(l)
    for l in b[3]:
        tfile.write(l)
tfile.close()

tfile = open('TEMPFILES/combined1.obj', 'w')
tfile.write(mtlLine)
tfile.write('g Case\n')
vertOffset = vertCount
for b in bodies[5:6]:
    for l in b[0]:
        tfile.write(l)
        vertCount += 1;
    for l in b[1]:
        tfile.write(l)
    for l in b[2]:
        tfile.write(l)
    for l in b[3]:
        if l.startswith('f '):
            data = l.strip().strip('f ').split(' ')
            l = 'f '

            d = data[0].split('/')
            l += str(int(d[0]) - vertOffset) + '/'
            l += str(int(d[1]) - vertOffset) + '/'
            l += str(int(d[2]) - vertOffset) + ' '

            d = data[1].split('/')
            l += str(int(d[0]) - vertOffset) + '/'
            l += str(int(d[1]) - vertOffset) + '/'
            l += str(int(d[2]) - vertOffset) + ' '

            d = data[2].split('/')
            l += str(int(d[0]) - vertOffset) + '/'
            l += str(int(d[1]) - vertOffset) + '/'
            l += str(int(d[2]) - vertOffset) + '\n'

        tfile.write(l)
tfile.close()

tfile = open('TEMPFILES/combined2.obj', 'w')
tfile.write(mtlLine)
tfile.write('g LID\n')
vertOffset = vertCount
for b in bodies[6:7]:
    for l in b[0]:
        tfile.write(l)
        vertCount += 1;
    for l in b[1]:
        tfile.write(l)
    for l in b[2]:
        tfile.write(l)
    for l in b[3]:
        if l.startswith('f '):
            data = l.strip().strip('f ').split(' ')
            l = 'f '

            d = data[0].split('/')
            l += str(int(d[0]) - vertOffset) + '/'
            l += str(int(d[1]) - vertOffset) + '/'
            l += str(int(d[2]) - vertOffset) + ' '

            d = data[1].split('/')
            l += str(int(d[0]) - vertOffset) + '/'
            l += str(int(d[1]) - vertOffset) + '/'
            l += str(int(d[2]) - vertOffset) + ' '

            d = data[2].split('/')
            l += str(int(d[0]) - vertOffset) + '/'
            l += str(int(d[1]) - vertOffset) + '/'
            l += str(int(d[2]) - vertOffset) + '\n'

        tfile.write(l)
tfile.close()




tfile = open('TEMPFILES/FINAL.obj', 'w')
tfile.write(mtlLine)
tfile.write('g PCB\n')

for b in bodies[:5]:
    for l in b[0]:
        tfile.write(l)
    for l in b[1]:
        tfile.write(l)
    for l in b[2]:
        tfile.write(l)
    for l in b[3]:
        tfile.write(l)

tfile.write('\ng Case\n')
for b in bodies[5:6]:
    for l in b[0]:
        tfile.write(l)
    for l in b[1]:
        tfile.write(l)
    for l in b[2]:
        tfile.write(l)
    for l in b[3]:
        tfile.write(l)

tfile.write('\ng LID\n')
for b in bodies[6:7]:
    for l in b[0]:
        tfile.write(l)
    for l in b[1]:
        tfile.write(l)
    for l in b[2]:
        tfile.write(l)
    for l in b[3]:
        tfile.write(l)





files = os.listdir('C:/Users/Charlie/Desktop/OBJ_Quest3/TEMPFILES')
for file in files:
    if file.startswith('tBod'):
        print('viewing : ' + file)
        mesh = trimesh.load('C:/Users/Charlie/Desktop/OBJ_Quest3/TEMPFILES/' + file)
        mesh.show()

