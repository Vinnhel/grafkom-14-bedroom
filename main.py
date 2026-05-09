import glfw
from OpenGL.GL import *
from OpenGL.GLU import *
import math, time

from room    import draw_room, draw_window, draw_sky_background, draw_sun_rays, draw_moon_rays, draw_dust_particles
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

cam_yaw        = CAM_YAW_DEFAULT
cam_pitch      = CAM_PITCH_DEFAULT
cam_dist       = CAM_DIST_DEFAULT
last_x, last_y = 0, 0
mouse_pressed  = False
lamp_on        = True
viewport_w     = 1000
viewport_h     = 720

# Simulasi waktu
TIME_SCALE      = 120.0   # detik real = 1 hari simulasi
sim_time_start  = time.time()
sim_paused      = False
sim_pause_accum = 0.0     # akumulasi waktu saat di-pause
sim_pause_start = 0.0

SPEED_LEVELS = [0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0]
speed_idx    = 1  # default 1x

def get_sim_hour():
    if sim_paused:
        elapsed = sim_pause_accum
    else:
        elapsed = sim_pause_accum + (time.time() - sim_time_start) * SPEED_LEVELS[speed_idx]
    return (elapsed / TIME_SCALE * 24.0) % 24.0

# ═══════════════════════════════════════════════════════
#  CALLBACK
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
    global speed_idx, sim_paused, sim_pause_accum, sim_time_start, sim_pause_start
    if action == glfw.PRESS:
        if key == glfw.KEY_L:
            lamp_on = not lamp_on
            print(f"  Lampu: {'ON' if lamp_on else 'OFF'}")

        elif key == glfw.KEY_R:
            cam_yaw   = CAM_YAW_DEFAULT
            cam_pitch = CAM_PITCH_DEFAULT
            cam_dist  = CAM_DIST_DEFAULT
            print("  Kamera reset.")

        elif key in (glfw.KEY_EQUAL, glfw.KEY_KP_ADD):       # tombol + / =
            if speed_idx < len(SPEED_LEVELS) - 1:
                # Simpan akumulasi sebelum ganti speed agar jam tidak lompat
                if not sim_paused:
                    sim_pause_accum += (time.time() - sim_time_start) * SPEED_LEVELS[speed_idx]
                    sim_time_start   = time.time()
                speed_idx += 1
                print(f"  Kecepatan waktu: {SPEED_LEVELS[speed_idx]}x")

        elif key in (glfw.KEY_MINUS, glfw.KEY_KP_SUBTRACT):  # tombol -
            if speed_idx > 0:
                if not sim_paused:
                    sim_pause_accum += (time.time() - sim_time_start) * SPEED_LEVELS[speed_idx]
                    sim_time_start   = time.time()
                speed_idx -= 1
                print(f"  Kecepatan waktu: {SPEED_LEVELS[speed_idx]}x")

        elif key == glfw.KEY_SPACE:                           # pause / resume
            if sim_paused:
                # Resume
                sim_time_start = time.time()
                sim_paused     = False
                print("  Simulasi dilanjutkan.")
            else:
                # Pause
                sim_pause_accum += (time.time() - sim_time_start) * SPEED_LEVELS[speed_idx]
                sim_paused       = True
                print("  Simulasi dijeda.")

        elif key in (glfw.KEY_Q, glfw.KEY_ESCAPE):
            glfw.set_window_should_close(window, True)

def framebuffer_size_callback(window, width, height):
    global viewport_w, viewport_h
    if height == 0: height = 1
    viewport_w, viewport_h = width, height
    glViewport(0, 0, width, height)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, width / height, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)

# ═══════════════════════════════════════════════════════
#  PENCAHAYAAN DINAMIS
# ═══════════════════════════════════════════════════════
def lerp(a, b, t): return a + (b - a) * t
def lerp3(c1, c2, t): return (lerp(c1[0],c2[0],t), lerp(c1[1],c2[1],t), lerp(c1[2],c2[2],t))
def smooth_step(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)

def get_sun_color_and_intensity(hour):
    if   hour < 5.5:  intensity = 0.0
    elif hour < 7.0:  intensity = smooth_step(5.5, 7.0, hour) * 0.55
    elif hour < 10.0: intensity = 0.55 + smooth_step(7.0, 10.0, hour) * 0.45
    elif hour < 14.0: intensity = 1.0
    elif hour < 17.0: intensity = 1.0 - smooth_step(14.0, 17.0, hour) * 0.2
    elif hour < 19.0: intensity = 0.8 - smooth_step(17.0, 19.0, hour) * 0.8
    else:             intensity = 0.0
    C_DAWN=(1.0,0.50,0.20); C_MORN=(1.0,0.88,0.55)
    C_NOON=(1.0,0.96,0.82); C_AFT=(1.0,0.80,0.42); C_DUSK=(1.0,0.45,0.15)
    if   hour < 6.0:  col = C_DAWN
    elif hour < 9.0:  col = lerp3(C_DAWN, C_MORN, smooth_step(6.0, 9.0, hour))
    elif hour < 12.0: col = lerp3(C_MORN, C_NOON, smooth_step(9.0, 12.0, hour))
    elif hour < 15.0: col = lerp3(C_NOON, C_AFT,  smooth_step(12.0, 15.0, hour))
    elif hour < 18.0: col = lerp3(C_AFT,  C_DUSK, smooth_step(15.0, 18.0, hour))
    else:             col = C_DUSK
    return col, intensity

def get_ambient_room_color(hour):
    C_NIGHT=(0.03,0.04,0.10); C_DAWN=(0.10,0.07,0.05); C_MORN=(0.11,0.09,0.06)
    C_NOON=(0.09,0.08,0.06);  C_AFT=(0.13,0.08,0.04);  C_DUSK=(0.14,0.06,0.03)
    C_EVNG=(0.05,0.04,0.09)
    if   hour < 5.5:  return C_NIGHT
    elif hour < 7.0:  return lerp3(C_NIGHT, C_DAWN, smooth_step(5.5,7.0,hour))
    elif hour < 10.0: return lerp3(C_DAWN,  C_MORN, smooth_step(7.0,10.0,hour))
    elif hour < 13.0: return lerp3(C_MORN,  C_NOON, smooth_step(10.0,13.0,hour))
    elif hour < 16.0: return lerp3(C_NOON,  C_AFT,  smooth_step(13.0,16.0,hour))
    elif hour < 18.0: return lerp3(C_AFT,   C_DUSK, smooth_step(16.0,18.0,hour))
    elif hour < 20.0: return lerp3(C_DUSK,  C_EVNG, smooth_step(18.0,20.0,hour))
    else:             return lerp3(C_EVNG,  C_NIGHT, min(smooth_step(20.0,22.0,hour),1.0))

def setup_lighting():
    glEnable(GL_LIGHTING)
    glEnable(GL_COLOR_MATERIAL)
    glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)
    glShadeModel(GL_SMOOTH)

def apply_lighting(hour):
    sun_col, sun_int = get_sun_color_and_intensity(hour)
    amb_col          = get_ambient_room_color(hour)
    glLightModelfv(GL_LIGHT_MODEL_AMBIENT, [amb_col[0], amb_col[1], amb_col[2], 1.0])
    if sun_int > 0.001:
        glEnable(GL_LIGHT0)
        sr, sg, sb = sun_col
        glLightfv(GL_LIGHT0, GL_POSITION, [0.4, 2.8, -2.90, 1.0])
        glLightfv(GL_LIGHT0, GL_DIFFUSE,  [sr*sun_int, sg*sun_int, sb*sun_int, 1.0])
        glLightfv(GL_LIGHT0, GL_AMBIENT,  [sr*0.04*sun_int, sg*0.03*sun_int, sb*0.02*sun_int, 1.0])
        glLightfv(GL_LIGHT0, GL_SPECULAR, [sr*0.4*sun_int, sg*0.35*sun_int, sb*0.25*sun_int, 1.0])
        glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION,  0.30)
        glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION,    0.07)
        glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.012)
    else:
        glDisable(GL_LIGHT0)
    if lamp_on:
        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, [0.0, 3.60, 0.5, 1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE,  [0.75, 0.65, 0.44, 1.0])
        glLightfv(GL_LIGHT1, GL_AMBIENT,  [0.03, 0.03, 0.02, 1.0])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [0.25, 0.20, 0.12, 1.0])
        glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION,  0.35)
        glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION,    0.08)
        glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.020)
    else:
        glDisable(GL_LIGHT1)
    glEnable(GL_LIGHT2)
    glLightfv(GL_LIGHT2, GL_POSITION, [0.25, 1.12, -1.58, 1.0])
    glLightfv(GL_LIGHT2, GL_DIFFUSE,  [0.58, 0.42, 0.20, 1.0])
    glLightfv(GL_LIGHT2, GL_AMBIENT,  [0.02, 0.01, 0.00, 1.0])
    glLightfv(GL_LIGHT2, GL_SPECULAR, [0.10, 0.08, 0.04, 1.0])
    glLightf(GL_LIGHT2, GL_CONSTANT_ATTENUATION,  0.45)
    glLightf(GL_LIGHT2, GL_LINEAR_ATTENUATION,    0.30)
    glLightf(GL_LIGHT2, GL_QUADRATIC_ATTENUATION, 0.15)

# ═══════════════════════════════════════════════════════
#  HUD — tampilkan jam + speed di pojok kiri bawah
# ═══════════════════════════════════════════════════════
def draw_hud(hour, vw, vh):
    """Tampilkan overlay teks jam simulasi menggunakan OpenGL rasterpos."""
    h = int(hour)
    m = int((hour - h) * 60)
    label = f"  {h:02d}:{m:02d}  |  Speed: {SPEED_LEVELS[speed_idx]}x"
    if sim_paused:
        label += "  [PAUSE]"

    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glMatrixMode(GL_PROJECTION)
    glPushMatrix(); glLoadIdentity()
    glOrtho(0, vw, 0, vh, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix(); glLoadIdentity()

    # Background strip
    glColor4f(0, 0, 0, 0.45)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glBegin(GL_QUADS)
    glVertex2f(0, 0); glVertex2f(vw, 0)
    glVertex2f(vw, 22); glVertex2f(0, 22)
    glEnd()
    glDisable(GL_BLEND)

    # Teks (gunakan glutBitmapCharacter jika tersedia, atau skip)
    try:
        from OpenGL.GLUT import glutBitmapCharacter, GLUT_BITMAP_8_BY_13, glutInit
        import sys
        glutInit(sys.argv)
        glColor3f(1.0, 0.90, 0.55)
        glRasterPos2f(8, 6)
        for c in label:
            glutBitmapCharacter(GLUT_BITMAP_8_BY_13, ord(c))
    except Exception:
        pass  # GLUT tidak wajib

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)

# ═══════════════════════════════════════════════════════
#  MAIN
# ═══════════════════════════════════════════════════════
def main():
    global viewport_w, viewport_h

    if not glfw.init():
        print("Gagal inisialisasi GLFW!"); return

    # Request stencil buffer (8 bit)
    glfw.window_hint(glfw.STENCIL_BITS, 8)

    window = glfw.create_window(
        1000, 720,
        "Kamar Tidur 3D  |  L=lampu  +/-=speed  SPACE=pause  R=reset  Q=keluar",
        None, None)
    if not window:
        glfw.terminate(); return

    glfw.make_context_current(window)
    glfw.set_mouse_button_callback(window,     mouse_button_callback)
    glfw.set_cursor_pos_callback(window,       cursor_pos_callback)
    glfw.set_scroll_callback(window,           scroll_callback)
    glfw.set_key_callback(window,              key_callback)
    glfw.set_framebuffer_size_callback(window, framebuffer_size_callback)

    glEnable(GL_DEPTH_TEST)
    glEnable(GL_STENCIL_TEST)
    glEnable(GL_NORMALIZE)
    glClearColor(0.04, 0.03, 0.04, 1.0)

    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    gluPerspective(45.0, 1000/720, 0.1, 100.0)
    glMatrixMode(GL_MODELVIEW)
    setup_lighting()

    print("=" * 62)
    print("  Kamar Tidur 3D — Simulasi Waktu Dinamis")
    print("  L          : toggle lampu gantung on/off")
    print("  +  / =     : percepat simulasi waktu")
    print("  -          : perlambat simulasi waktu")
    print("  SPACE      : pause / resume simulasi")
    print("  R          : reset kamera")
    print("  Drag mouse : putar kamera")
    print("  Scroll     : zoom in / out")
    print("  Q / ESC    : keluar")
    print("  Speed: 0.5x 1x 2x 4x 8x 16x 32x")
    print("=" * 62)

    while not glfw.window_should_close(window):
        hour = get_sim_hour()

        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT | GL_STENCIL_BUFFER_BIT)
        glLoadIdentity()

        # Kamera spherical
        ex = cam_dist * math.sin(math.radians(cam_yaw))   * math.cos(math.radians(cam_pitch))
        ey = cam_dist * math.sin(math.radians(cam_pitch))
        ez = cam_dist * math.cos(math.radians(cam_yaw))   * math.cos(math.radians(cam_pitch))
        gluLookAt(ex, ey, ez,  0.0, 1.6, 0.0,  0.0, 1.0, 0.0)

        apply_lighting(hour)

        # ── URUTAN RENDER ──────────────────────────────
        # 1. Sky (stencil pass) — sebelum dinding
        draw_sky_background(hour, viewport_w, viewport_h)

        # 2. Ruangan + furnitur
        draw_room()
        draw_bed()
        draw_nightstand()
        draw_desk()
        draw_chair()
        draw_wardrobe()
        draw_bookshelf()
        draw_reading_sofa()
        draw_ceiling_lamp(lamp_on)

        # 3. Frame/kaca jendela + tirai (setelah dinding)
        draw_window(hour)

        # 4. Efek sinar matahari (transparan, paling akhir)
        draw_sun_rays(hour)

        # 4b. Efek cahaya bulan + partikel debu (aktif saat malam + lampu mati)
        draw_moon_rays(hour, lamp_on)
        draw_dust_particles(hour, lamp_on)

        # 5. HUD overlay
        draw_hud(hour, viewport_w, viewport_h)

        glfw.swap_buffers(window)
        glfw.poll_events()

    glfw.terminate()
    print("Program selesai.")

if __name__ == "__main__":
    main()
