import drawSvg as draw
import xml.etree.cElementTree as ElementTree
from bs4 import BeautifulSoup
import lxml
import os
import csv
import pprint

def main():
    StopPoints = [] #[{StopPointRef: $, CommonName: $, x: f, y:, f}]
    stoplist = []
    #list all bus stops used in Aberdenshire by using the id "SVRAB..."
    print("gathering bus stops")
    directory = "E:/gav_b/Documents/GitHub/omnibus/travelinedata/S/"
    for filename in os.listdir(directory):
        if filename.startswith("SVRAB"): 
            routefile = os.path.join(directory, filename)
            print("file:", filename)
            stoplist += liststops(routefile)
            continue
        else:
            continue
    #remove duplicates
    stoplist = list(set(stoplist))
    print ("Number of stops:", len(stoplist))
    
    #list all bus stops as json for fats lookup
    csvfile = csv.DictReader(open("E:/gav_b/Documents/GitHub/omnibus/data.gov/GTFS/Stops.csv"))
    fastcsv = {}
    for each in csvfile:
        info = {
            "lat":float(each["stop_lat"]),
            "lon":float(each["stop_lon"]),
            "stop name":each["stop_name"],
            "ref":each["ï»¿stop_id"]
            }
        fastcsv[each["ï»¿stop_id"]] = info

    #with each bus stop reference listed find its lat, lon and name    
    for stopnum in range(0, len(stoplist)):
        info = stopinfo(stoplist[stopnum], fastcsv)
        stoplist[stopnum] = {
            "StopRef": info["ref"], 
            "lat": info["lat"],
            "lon": info["lon"],
            "stop name": info["stop name"]
        }
    #pp = pprint.PrettyPrinter()
    #pp.pprint(stoplist)
    
    #normalise lat/lon

    #find mean values and subract. this should move points to near 0
    mean = {"lat":0, "lon":0}
    for each in stoplist:
        mean["lat"] = mean["lat"] + each["lat"]/len(stoplist)
        mean["lon"] = mean["lon"] + each["lon"]/len(stoplist)
    for each in stoplist:
        each["lat"] = (each["lat"]-mean["lat"])*100
        each["lon"] = (each["lon"]-mean["lon"])*100

    print("drawing start...")
    d = draw.Drawing(1000, 500, origin='center')
    d.draw(draw.Rectangle(-500,-250,1000,500, fill='#ddd'))
    lat = 57.09
    lon = -2.27
    for each in stoplist:
        d.append(draw.Circle(each["lon"], each["lat"],2,fill='red'))

    #d.append(draw.Lines(-80, -45,70, -49, 95, 49, -90, 40, close=False, fill = 'none', stroke='black'))
    d.rasterize()  # Display as PNG
    d.saveSvg('map.svg')
    print("drawing complete")
    d  # Display as SVG

def liststops(routefile):
    stoplist = []
    markup = open(routefile)
    tree = BeautifulSoup(markup, features="lxml")
    annotatedstoppointref = tree.find_all('annotatedstoppointref')
    for stop in annotatedstoppointref:
        stoplist.append(stop.find('stoppointref').text)
    #print(stoplist)    
    return(stoplist)

def stopinfo(stopref, fastcsv):
    try:
        info = {
            "lat":fastcsv[stopref]["lat"],
            "lon":fastcsv[stopref]["lon"],
            "stop name":fastcsv[stopref]["stop name"],
            "ref":fastcsv[stopref]["ref"]
            }
    except:
        info = {
                "lat":0,
                "lon":0,
                "stop name":"unknown",
                "ref":stopref
                }
    return(info)


if __name__ == "__main__":
    main()