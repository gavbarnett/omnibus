import drawSvg as draw
import cElementTree as ElementTree
def main():
    print("drawing start")
    d = draw.Drawing(200, 100, origin='center')

    d.append(draw.Lines(-80, -45,70, -49, 95, 49, -90, 40, close=False, fill='#eeee00', stroke='black'))
    d.append(draw.Rectangle(0,0,40,50, fill='#1248ff'))
    d.append(draw.Circle(-40, -10, 30,fill='red', stroke_width=2, stroke='black'))

    # Display in iPython notebook
    d.rasterize()  # Display as PNG
    d.saveSvg('example.svg')

    d  # Display as SVG

if __name__ == "__main__":
    main()