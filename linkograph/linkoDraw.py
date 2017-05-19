#!/usr/bin/env python3

import argparse  # For argument parsing.
import math
from linkograph import linkoCreate
from linkograph import stats


# Post script uses points which are 1/72 an inch.
# So mutliplication by __convertToInch converts
# to and inch.
__convertToInch=72

def linkoDrawEPS(linkograph, fileEPS, scale=1):
    """ Draws an EPS version of a linkograph. """

    # Controls the scale.
    #scale=0.1

    # Controls the size of the dots used.
    dotRadius=0.05*__convertToInch*scale

    # Controls the line segement steps.
    step=0.2*__convertToInch*scale

    # Controls the horizontal spacing for labels.
    labelStep=0.25*__convertToInch*scale

    # Controls the distance from the dots to the labels.
    labelDist=0.2*__convertToInch*scale

    # Controls the baseline offset for the labels.
    labelBase = -0.05*__convertToInch*scale

    # The x coordinate of the last label's dot.
    xStart=4*__convertToInch*scale

    xBox = xStart

    # The y coordinate of the last label's dot.
    yStart=1*__convertToInch*scale

    yBox = yStart

    # Font type.
    fontString='Times-Roman'

    # Font size.
    fontSize=15*scale

    with open(fileEPS, 'w') as fe:

        # Print the PS header.
        fe.write('%!PS-Adobe-3.0\n')

        # Find the longest links.
        linkwidth = max(stats.linkDifference(linkograph))

        # Longest Labels.
        labelwidth = max({len(' '.join(e[0])) for e in linkograph})
        
        #totalWidth = linkwidth*step + labelwidth*fontSize
        totalWidth = (linkwidth*step + labelwidth*10*scale
                      + labelDist*2)

        height = 2*len(linkograph)*step

        xBox = xBox - linkwidth*step - labelwidth*scale
        yBox = yBox - step

        fe.write('%%BoundingBox: ' + str(xBox) + ' ' + str(yBox)
                 + ' ' + str(xBox + totalWidth)
                 + ' ' + str(yBox + height) + '\n')

        fe.write('%%Title:\n')
        fe.write('%%CreationDate:\n')
        fe.write('%%Pages: 1\n')
        fe.write('%%DocumentFonts: Times-Roman\n')
        fe.write('%%EndComments\n\n')

        # Set the line width
        fe.write(str(1*scale) + ' setlinewidth\n')


        # Print the font header
        fontDeclaration(fontString, fontSize, fe)

        # Print dot declaration.
        dotDeclaration(dotRadius, fe)

        # Move to the starting location
        #fe.write(str(xStart) + ' ' + str(yStart) + ' moveto\n')

        depth = len(linkograph)-1

        for line in linkograph[::-1]:
            # Print the back links.
            printLinks(line[1], step, depth, xStart, yStart, fe)
            depth -= 1

            # Move to the start of the labels.
            fe.write(str(xStart + labelDist) + ' '
                     + str(yStart + labelBase)
                     + ' moveto\n')

            # Print the labels.
            printLabel(line[0], labelStep, fe)

            # Move the start position up one step
            # and reset position.
            yStart += 2*step


        # xStartAbs = xStartAbs - linkwidth*step - labelwidth
        # yStartAbs = yStartAbs - step

        # Draw bounding rectangle
        # fe.write('newpath\n')
        # fe.write(str(xStartAbs) + ' ' + str(yStartAbs) + ' moveto\n')
        # fe.write('0 ' + str(len(linkograph)*2*step) + ' rlineto\n')
        # fe.write(str(totalWidth)  + ' 0' + ' rlineto\n')
        # fe.write('0 ' + str(-1* len(linkograph)*2*step)
        #          + ' rlineto\n')
        # fe.write(str(-1*totalWidth) + ' 0' + ' rlineto\n')
        # fe.write('closepath\n')
        # fe.write('stroke\n')

        fe.write('%%EOF')

def dotDeclaration(size, fh):
    """ Defines the declare dots function. """
    fh.write(('/dot\n'
              '{newpath '
              + str(int(size)) +
              ' 0 360 arc 0 setgray fill stroke} def \n'))

def fontDeclaration(fontString, fontSize, fh):
    """ Defines the font for the labels. """
    # fh.write(('/MainFont\n'
    #           ' /' + fontString + ' findfont '
    #           + str(fontSize) + ' scalefont def\n'))
    # fh.write('MainFont setfont\n')
    fh.write('/' + fontString + ' findfont ' + str(fontSize)
             + ' scalefont setfont\n')

def printLinks(links, step, depth, xStart, yStart, fh):
    """ Prints the links. """
    #fh.write('newpath\ndot\n')

    currentDepth = depth

    #xEnd, yEnd = xStart, yStart

    maxdiff = 0

    fh.write(str(xStart) + ' ' + str(yStart) + ' dot\n')

    for l in links:
        difference = abs(currentDepth - l)

        if difference > maxdiff:
            maxdiff = difference

        fh.write(str(xStart - difference*step) + ' ' +
                 str(yStart + difference*step) + ' dot\n')
        fh.write('newpath\n' +
                 str(xStart - difference*step) + ' ' +
                 str(yStart + difference*step) + ' moveto\n' +
                 str(xStart) + ' ' +
                 str(yStart + 2*difference*step) + ' lineto\n' +
                 'stroke\n')

        # fh.write('newpath\n'
        #          + str(int(xStart)) + ' ' + str(int(yStart))
        #          + ' moveto\n'
        #          + '60 rotate\n')

        

        # Create line segements until l is reached.
        # while currentDepth != l:
        #     #yStart += step
        #     # fh.write(str(int(xStart)) + ' ' + str(int(yStart))
        #     #               + ' lineto\n')
            
        #     currentDepth -= step/abs(step)

        #fh.write('stroke\n')

        #fh.write(str(int(xStart)) + ' ' + str(int(yStart)) + ' dot\n')
        #fh.write('-60 rotate\n')

    fh.write('newpath\n' + 
             str(xStart) + ' ' + str(yStart) + ' moveto\n' + 
             str(xStart - maxdiff*step) + ' ' +
             str(yStart + maxdiff*step) + ' lineto\n' +
             str(xStart) + ' ' +
             str(yStart + 2*maxdiff*step) + ' lineto\n' +
             'stroke\n')
    

    
def printLabel(labels, labelStep, fh):
    """ Defines the printing of the label. """
    # for labelEntry in labels:
    #     fh.write('(' + labelEntry + ') show '
    #              + str(labelStep) + ' 0 rmoveto\n')

    labelsCombined = ' '.join(labels)

    fh.write('(' + labelsCombined + ') show '
                 + str(labelStep) + ' 0 rmoveto\n')


def moveToPoint(x, y, fh):
    """ Write the statement that moves to point (x,y). """
    fh.write(str(x) + ' ' + str(y) + ' moveto\n')

######################################################################
#----------------------- Command Line Programs -----------------------

def cli_linkoDrawEPS():
    """Draws the linkograph in eps format."""

    info = 'Draws the linkograph in eps format.'

    parser = argparse.ArgumentParser(description=info)
    parser.add_argument('linkograph', metavar='LINKOGRAPH.json',
                        nargs=1,
                        help='The linkograph to draw.')

    parser.add_argument('out', metavar='OUTPUT_FILE',
                        nargs=1,
                        help='The output file.')

    parser.add_argument('-s', '--scale', metavar='SCALE',
                        type=float,
                        help='Scales the graph.')

    args = parser.parse_args()

    # Read in the linkograph.
    linko = linkoCreate.readLinkoJson(args.linkograph[0])

    if args.scale is None:
        args.scale = 1

    linkoDrawEPS(linko, args.out[0], args.scale)



######################################################################

if __name__ == '__main__':

    linko = [
        (['F', 'F', 'D'],  [], [1,3,4]),
        (['Be'], [0], []),
        (['Bs'], [], []),
        (['S'],  [0], []),
        (['D'],  [0], [])
        ]

    linkoDrawEPS(linko, 'thefile.eps')


    print('done')
