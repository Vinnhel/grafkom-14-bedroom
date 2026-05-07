import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math

# Import semua modul furniture
from room    import draw_room, draw_window, draw_sun_rays
from bed     import draw_bed, draw_nightstand
from desk    import draw_desk, draw_chair
from storage import draw_wardrobe, draw_bookshelf
from lamp    import draw_reading_sofa, draw_ceiling_lamp

# ═══════════════════════════════════════════════════════
#  STATE GLOBAL
# ═══════════════════════════════════════════════════════
CAM_YAW_DEFAULT   = 32.0
CAM_PITCH_DEFAULT = 20.0
CAM_DIST_DEFAULT  = 11.0

cam_yaw       = CAM_YAW_DEFAULT
cam_pitch     = CAM_PITCH_DEFAULT
cam_dist      = CAM_DIST_DEFAULT
last_x, last_y = 0, 0
mouse_pressed  = False
lamp_on        = True   # toggle dengan tombol L

# ═══════════════════════════════════════════════════════
#  CALLBACK INPUT
# ═══════════════════════════════════════════════════════
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
    cam_dist  = max(3.0, min(20.0, cam_dist))

def key_callback(window, key, scancode, action, mods):
    global lamp_on, cam_yaw, cam_pitch, cam_dist
    if action == glfw.PRESS:
        if key == glfw.KEY_L:
            lamp_on = not lamp_on
            print(f"  Lampu gantung: {'ON v' if lamp_on else 'OFF x'}")
        elif key == glfw.KEY_R:
            cam_yaw   = CAM_YAW_DEFAULT
            cam_pitch = CAM_PITCH_DEFAULT
            cam_dist  = CAM_DIST_DEFAULT
            print("  Kamera direset ke posisi default.")
        elif key in (glfw.KEY_Q, glfw.KEY_ESCAPE):
            glfw.set_window_should_close(window, True)
            print("  Program keluar.")

def framebuffer_size_callback(window, width, height):
    """Reshape callback — menyesuaikan viewport & proyeksi saat window diubah ukurannya."""
    if height == 0:
        height = 1
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# ═══════════════════════════════════════════════════════
#  PENCAHAYAAN
# ═══════════════════════════════════════════════════════
def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [0.06, 0.05, 0.04, 1.0])
    glShadeModel(GL_SMOOTH)

def apply_lighting():
    """
    Dipanggil SETIAP FRAME setelah gluLookAt().
    GL_LIGHT0 = sinar matahari dari jendela (selalu aktif)
    GL_LIGHT1 = lampu gantung (toggle L)
    GL_LIGHT2 = lampu meja nakas (selalu aktif, dim warm)
    """
    # ── LIGHT0 : Cahaya matahari dari jendela ─────────
    glEnable(GL_LIGHT0)
    glLightfv(GL_LIGHT0, GL_POSITION, [ 0.4, 2.8, -2.90, 1.0])
    glLightfv(GL_LIGHT0, GL_DIFFUSE,  [ 1.0, 0.90, 0.62, 1.0])
    glLightfv(GL_LIGHT0, GL_AMBIENT,  [ 0.04, 0.03, 0.02, 1.0])
    glLightfv(GL_LIGHT0, GL_SPECULAR, [ 0.5,  0.42, 0.28, 1.0])
    glLightf (GL_LIGHT0, GL_CONSTANT_ATTENUATION,   0.30)
    glLightf (GL_LIGHT0, GL_LINEAR_ATTENUATION,     0.07)
    glLightf (GL_LIGHT0, GL_QUADRATIC_ATTENUATION,  0.012)

    # ── LIGHT1 : Lampu gantung (toggle) ───────────────
    if lamp_on:
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, [ 0.0, 3.60, 0.5,  1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE,  [ 0.75, 0.65, 0.44, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT,  [ 0.03, 0.03, 0.02, 1.0])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [ 0.25, 0.20, 0.12, 1.0])
        glLightf (GL_LIGHT1, GL_CONSTANT_ATTENUATION,  0.35)
        glLightf (GL_LIGHT1, GL_LINEAR_ATTENUATION,    0.08)
        glLightf (GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.020)
    else:
        glDisable(GL_LIGHT1)

    # ── LIGHT2 : Lampu meja nakas ─────────────────────
    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_POSITION, [ 0.25, 1.12, -1.58, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE,  [ 0.58, 0.42, 0.20, 1.0])
    glLightfv(GL_LIGHT2, GL_AMBIENT,  [ 0.02, 0.01, 0.00, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [ 0.10, 0.08, 0.04, 1.0])
    glLightf (GL_LIGHT2, GL_CONSTANT_ATTENUATION,  0.45)
    glLightf (GL_LIGHT2, GL_LINEAR_ATTENUATION,    0.30)
    glLightf (GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.15)

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
def main():
    if not glfw.init():
        print("Gagal inisialisasi GLFW!")
        return

    window = glfw.create_window(
        1000, 720,
        "Kamar Tidur 3D  |  L=toggle lampu  |  R=reset kamera  |  Q/ESC=keluar",
        None, None
    )
    if not window:
        glfw.terminate()
        return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window,     mouse_button_callback)
    glfw.set_cursor_pos_callback(window,       cursor_pos_callback)
    glfw.set_scroll_callback(window,           scroll_callback)
    glfw.set_key_callback(window,              key_callback)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_NORMALIZE)
    glClearColor(0.07, 0.06, 0.05, 1.0)

    # Proyeksi perspektif awal
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1000/720, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

    setup_lighting()

    print("=" * 58)
    print("  Visualisasi 3D Interior Kamar Tidur -- OpenGL")
    print("  Universitas Siliwangi -- Grafika Komputer 2026")
    print("  L      : toggle lampu gantung on/off")
    print("  R      : reset kamera ke posisi default")
    print("  Drag   : putar kamera (klik kiri + geser)")
    print("  Scroll : zoom in / zoom out")
    print("  Q/ESC  : keluar")
    print("=" * 58)

    while not glfw.window_should_close(window):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # ── Posisi kamera (spherical coordinate) ──────
        ex = cam_dist * math.sin(math.radians(cam_yaw))   * math.cos(math.radians(cam_pitch))
        ey = cam_dist * math.sin(math.radians(cam_pitch))
        ez = cam_dist * math.cos(math.radians(cam_yaw))   * math.cos(math.radians(cam_pitch))
        gluLookAt(ex, ey, ez,   0.0, 1.6, 0.0,   0.0, 1.0, 0.0)

        # ── Terapkan lighting SETELAH gluLookAt ───────
        apply_lighting()

        # ── Gambar semua objek ─────────────────────────
        draw_room()
        draw_window()
        draw_bed()
        draw_nightstand()
        draw_desk()
        draw_chair()
        draw_wardrobe()
        draw_bookshelf()
        draw_reading_sofa()
        draw_ceiling_lamp(lamp_on)
        draw_sun_rays()   # transparan, digambar TERAKHIR

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    print("Program selesai.")

if __name__ == "__main__":
    main()
