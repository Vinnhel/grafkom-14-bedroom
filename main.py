import glfw
from OpenGL.GL import *
from OpenGL.GLU import *

# ── Kamera ──────────────────────────────────────────
cam_yaw   = 30.0   # rotasi horizontal
cam_pitch = 20.0   # rotasi vertikal
cam_dist  = 8.0    # jarak zoom
last_x, last_y = 0, 0
mouse_pressed  = False

def mouse_button_callback(window, button, action, mods):
    global mouse_pressed, last_x, last_y
    if button == glfw.MOUSE_BUTTON_LEFT:
        mouse_pressed = (action == glfw.PRESS)
        last_x, last_y = glfw.get_cursor_pos(window)

def cursor_pos_callback(window, xpos, ypos):
    global cam_yaw, cam_pitch, last_x, last_y
    if mouse_pressed:
        cam_yaw   += (xpos - last_x) * 0.3
        cam_pitch -= (ypos - last_y) * 0.3
        cam_pitch  = max(-89, min(89, cam_pitch))
    last_x, last_y = xpos, ypos

def scroll_callback(window, xoff, yoff):
    global cam_dist
    cam_dist -= yoff * 0.5
    cam_dist  = max(2.0, min(20.0, cam_dist))

# ── Gambar Ruangan ───────────────────────────────────
def draw_room():
    glBegin(GL_QUADS)

    # Lantai (abu-abu terang)
    glColor3f(0.6, 0.6, 0.6)
    glVertex3f(-3, 0,  3)
    glVertex3f( 3, 0,  3)
    glVertex3f( 3, 0, -3)
    glVertex3f(-3, 0, -3)

    # Plafon (putih)
    glColor3f(0.9, 0.9, 0.9)
    glVertex3f(-3, 4,  3)
    glVertex3f( 3, 4,  3)
    glVertex3f( 3, 4, -3)
    glVertex3f(-3, 4, -3)

    # Dinding belakang (biru muda)
    glColor3f(0.7, 0.8, 0.9)
    glVertex3f(-3, 0, -3)
    glVertex3f( 3, 0, -3)
    glVertex3f( 3, 4, -3)
    glVertex3f(-3, 4, -3)

    # Dinding kiri (biru muda)
    glColor3f(0.65, 0.75, 0.85)
    glVertex3f(-3, 0, -3)
    glVertex3f(-3, 0,  3)
    glVertex3f(-3, 4,  3)
    glVertex3f(-3, 4, -3)

    # Dinding kanan (biru muda)
    glColor3f(0.65, 0.75, 0.85)
    glVertex3f(3, 0,  3)
    glVertex3f(3, 0, -3)
    glVertex3f(3, 4, -3)
    glVertex3f(3, 4,  3)

    glEnd()

# ── Setup Proyeksi ───────────────────────────────────
def setup_projection(width, height):
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# ── Main ─────────────────────────────────────────────
def main():
    if not glfw.init():
        return

    window = glfw.create_window(800, 600, "Visualisasi 3D Kamar Tidur", None, None)
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window, mouse_button_callback)
    glfw.set_cursor_pos_callback(window,   cursor_pos_callback)
    glfw.set_scroll_callback(window,       scroll_callback)

    glEnable(GL_DEPTH_TEST)
    glClearColor(0.1, 0.1, 0.1, 1.0)
    setup_projection(800, 600)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Posisi kamera
        import math
        ex = cam_dist * math.sin(math.radians(cam_yaw)) * math.cos(math.radians(cam_pitch))
        ey = cam_dist * math.sin(math.radians(cam_pitch))
        ez = cam_dist * math.cos(math.radians(cam_yaw)) * math.cos(math.radians(cam_pitch))
        gluLookAt(ex, ey, ez,  0, 1.5, 0,  0, 1, 0)

        draw_room()

        glfw.swap_buffers(window)
        glfw.poll_events()

        if glfw.get_key(window, glfw.KEY_ESCAPE) == glfw.PRESS:
            break

    glfw.terminate()

if __name__ == "__main__":
    main()