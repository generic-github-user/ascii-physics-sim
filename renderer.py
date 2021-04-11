import curses
import numpy as np
import tkinter


class GlyphSet:
    def __init__(self, line_characters='_-\\|/', angles=[0, 0, 60, 90, 120], heights=[0, 0.5, 0.5, 0.5, 0.5]):
        self.symbols = list(zip(line_characters, angles, heights))


class Camera:
    def __init__(self, pos, zoom=1):
        self.zoom: Scalar = zoom
        self.pos: Vector = pos


class Renderer:
    """Class for renderer to convert object data into a final image"""
    def __init__(self, rtype, dims, camera, glyphs, objects):
        """Create a new renderer"""
        self.rtype: str = rtype
        """Renderer type; either `line`, `opengl`, or `canvas`"""
        self.dims: Vector = dims
        """The width and height of the scene"""
        self.camera: Camera = camera
        """A camera to store additional rendering properties"""

        self.glyphs: GlyphSet = glyphs
        """A list of (ASCII) characters that can be used for rendering the scene"""
        self.default_char: str = 'o'
        """Character used for rendering points when line data is not available"""
        self.empty: str = ' '
        """Character used to fill areas where no objects are present"""

        self.objects = objects
        """List of objects for the renderer to display"""
        self.console = curses.initscr()

        self.root = tkinter.Tk()
        self.canvas = tkinter.Canvas(self.root, bg="white", height=700, width=700)
    def fetch_line_glyph(self, angle, height):
        return min(self.glyphs.symbols, key=(lambda x: abs(angle - x[1]) + abs(height - x[2])))[0]
    def dot(self, m):
        if m > 0:
            return self.default_char
        else:
            return self.empty
    def at(self, x, y):
        # return list(filter(lambda o: round(o.x) == x and round(o.y) == y, self.objects))
        return list(filter(lambda o: np.array_equal(np.round_(o.pos()), np.array([x, y])), self.objects))
    def build_mask(self):
        """Create an array marking which cells contain a part of an object; which ones will be used in rendering"""
        pass
    def combine_output(self, g):
        # return ['\n'.join([''.join([h for h in g])])]
        # return ['\n'.join([''.join(h.tolist()) for h in g])]
        # print(g.astype('|S1'))
        # print(g.astype(str))
        return '\n'.join([''.join(h) for h in g])
    def form_output(self, angles):
        # TODO: use numpy char array
        # char_array = np.chararray(self.dims())
        # for x, y in np.ndindex(char_array.shape):
        #     # TODO: incorporate pos
        #     char_array[x, y] = self.fetch_line_glyph(angles[x, y], 0)

        char_array = []
        dims = self.dims()
        # for x in range(dims[0]):
        #     char_array.append([self.fetch_line_glyph(angles[x, y], 0) for y in range(dims[1])])
        for x in range(dims[0]):
            row = []
            for y in range(dims[1]):
                if angles[x, y] == 0:
                    row.append(' ')
                else:
                    row.append(self.fetch_line_glyph(angles[x, y], 0.5))
            char_array.append(row)

        return char_array
    def render_frame(self, callback, steps=300, current=0, show=True, delay=0):
        con = self.console
        if show:
            con.clear()

        dims = self.dims()
        frame_angles = np.zeros(dims)
        frame_pos = np.zeros(dims)
        rtype = self.rtype

        # TODO: separate ASCII rendering library
        # TODO: move into functions (? - not sure if this would slow program down by much)
        if rtype == 'point':
            output_text = '\n'.join([''.join([self.dot(len(self.at(x, y))) for x in range(0, self.dims.x)]) for y in range(0, self.dims.y)])
        elif rtype == 'line':
            for obj in self.objects:
                obj_geometry = obj.matter.geometry
                if type(obj_geometry) is Circle:
                    # print(True)
                    tangents = obj_geometry.get_tangents()
                    window = tangents.shape
                    xo = round(obj.pos()[0])
                    yo = round(obj.pos()[1])
                    # print(obj.pos())
                    # print(tangents)
                    # TODO: offset by half of window size
                    # TODO: fix
                    try:
                        frame_angles[xo:window[0]+xo, yo:window[1]+yo] += tangents
                    except:
                        pass

                    # should we make the angle list first?
                    output_text = self.form_output(frame_angles)
                    # print(output_text)
                    output_text = self.combine_output(output_text)
                    # print(output_text)

            if show:
                con.addstr(output_text)
                con.refresh()

        # TODO: debug mode
        # print(frame_angles)
        # TODO: add colors
        elif rtype == 'canvas':
            canvas_objs = []
            canv = self.canvas
            for obj in self.objects:
                # draw arcs
                # TODO: fix render settings handling
                center = np.round(obj.pos()) * 10
                # TODO: use this more
                cx, cy = center
                # TODO: use actual radius
                r = 20
                coord = cx-r, cy-r, cx+r, cy+r
                # print(coord)
                # TODO: use ellipse?
                # cv_obj = myCanvas.create_arc(coord, start=0, extent=360, outline='black')
                # cv_obj = myCanvas.create_arc(coord, start=0, extent=360, outline='black', style='arc', width=5, fill='green')
                # TODO: optimize
                if not obj.display:
                    cv_obj = canv.create_oval(coord)
                    obj.display = cv_obj
                    canvas_objs.append(cv_obj)
                if not obj.canvas:
                    obj.canvas = canv
                canv.move(obj.display, *obj.delta())
                # myCanvas.move(obj.display, 0.05, 0.05)
                # self.canvas.after(delay, self.move_ball)
        elif rtype == 'opengl':
            pass
        elif rtype == 'cairo':
            pass

        callback()
        if current < steps:
            self.root.after(33, lambda: self.render_frame(callback=callback, current=current+1, steps=300))


        # myCanvas.update()
        # myCanvas.Update()
        # TODO: use proper solution later - https://stackoverflow.com/a/21359051
        # myCanvas.update_idletasks()
        # time.sleep(delay)



        # TODO: optimization
        # TODO: per-shape and per-cell rendering
