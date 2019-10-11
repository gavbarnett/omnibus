import drawSvg as draw
import xml.etree.cElementTree as ElementTree
from bs4 import BeautifulSoup
import lxml

def main():
    StopPoints = [] #[{StopPointRef: $, CommonName: $, x: f, y:, f}]

    print("routing data")
    #busroute('SVRABAN001.xml')
    busroute2('SVRABAN001.xml')
    print("drawing start")
    d = draw.Drawing(1000, 500, origin='center')
    d.draw(draw.Rectangle(-500,-250,1000,500, fill='#ddd'))

    d.append(draw.Lines(-80, -45,70, -49, 95, 49, -90, 40, close=False, fill = 'none', stroke='black'))
    # Display in iPython notebook
    d.rasterize()  # Display as PNG
    d.saveSvg('map.svg')

    d  # Display as SVG

def busroute2(routefile):
    markup = open(routefile)
    tree = BeautifulSoup(markup, features="lxml")
    routesections = tree.body.transxchange.routesections
    #print(routesections.prettify())
    routes = {}
    for routesection in routesections:
        routes["a"] = []
        for routelink in routesection:
            print(routelink)
            for each in routelink:
                print(each)
            #routes["a"].append(link.to.stoppointref)
    print(routes)

def busroute(routefile):
    tree = ElementTree.parse(routefile)
    root = tree.getroot()
    for child in root:
        print(child.tag)
    print('---')
    for RouteSection in root.iter('{http://www.transxchange.org.uk/}RouteSection'):
        print('s', RouteSection.tag, RouteSection.attrib)
        for RouteLink in RouteSection.iter('{http://www.transxchange.org.uk/}RouteLink'):
            print('l', RouteLink.tag, RouteLink.attrib)    
            for From in RouteLink.iter('{http://www.transxchange.org.uk/}From'):
                print('f', From.tag, From.attrib)
                for each in From:
                    print('each', each.tag, each.attrib)
                    for ea in each:
                        print('ea', ea.tag, ea.attrib)
                #for StopPointRef in From.iter('{http://www.transxchange.org.uk/}StopPointRef'):
            #        print('from:', StopPointRef.tag, StopPointRef.attrib)
        print('---')

if __name__ == "__main__":
    main()