from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cylinder,
                   mat_wall, mat_wood, mat_glass, mat_fabric,
                   set_material, mat_metal)
import math, time

# ═══════════════════════════════════════════════════════
#  HELPERS WARNA
# ═══════════════════════════════════════════════════════
def lerp(a, b, t): return a + (b - a) * t
def lerp3(c1, c2, t): return (lerp(c1[0],c2[0],t), lerp(c1[1],c2[1],t), lerp(c1[2],c2[2],t))
def smooth_step(a, b, x):
    t = max(0.0, min(1.0, (x - a) / (b - a)))
    return t * t * (3 - 2 * t)

def get_time_of_day():
    return (time.time() / 120.0 * 24.0) % 24.0

def get_sky_colors(hour):
    SKY = [
        ( 0.0, (0.02,0.04,0.14), (0.04,0.06,0.18)),
        ( 5.0, (0.02,0.04,0.14), (0.04,0.06,0.18)),
        ( 5.5, (0.18,0.08,0.14), (0.40,0.18,0.12)),
        ( 6.5, (0.60,0.30,0.18), (0.90,0.55,0.30)),
        ( 8.0, (0.35,0.62,0.92), (0.72,0.88,1.00)),
        (12.0, (0.22,0.52,0.90), (0.65,0.85,1.00)),
        (16.0, (0.30,0.58,0.88), (0.70,0.86,1.00)),
        (17.5, (0.52,0.32,0.18), (0.92,0.62,0.28)),
        (18.5, (0.28,0.12,0.20), (0.70,0.28,0.14)),
        (19.5, (0.06,0.06,0.16), (0.12,0.08,0.20)),
        (21.0, (0.02,0.04,0.14), (0.04,0.06,0.18)),
        (24.0, (0.02,0.04,0.14), (0.04,0.06,0.18)),
    ]
    top = SKY[-1][1]; bot = SKY[-1][2]
    for i in range(len(SKY)-1):
        h0, top0, bot0 = SKY[i]
        h1, top1, bot1 = SKY[i+1]
        if h0 <= hour <= h1:
            t = smooth_step(h0, h1, hour)
            top = lerp3(top0, top1, t)
            bot = lerp3(bot0, bot1, t)
            break

    if   hour < 6.0:  sun_col = (1.0, 0.50, 0.20)
    elif hour < 8.0:  sun_col = lerp3((1.0,0.50,0.20),(1.0,0.96,0.75), smooth_step(6.0,8.0,hour))
    elif hour < 16.0: sun_col = (1.0, 0.96, 0.75)
    elif hour < 18.5: sun_col = lerp3((1.0,0.96,0.75),(1.0,0.45,0.12), smooth_step(16.0,18.5,hour))
    else:             sun_col = (1.0, 0.40, 0.10)

    if   hour < 5.5:  sun_vis = 0.0
    elif hour < 6.5:  sun_vis = smooth_step(5.5, 6.5, hour)
    elif hour < 18.0: sun_vis = 1.0
    elif hour < 19.5: sun_vis = 1.0 - smooth_step(18.0, 19.5, hour)
    else:             sun_vis = 0.0

    if   hour < 5.0:  moon_vis = 1.0
    elif hour < 6.5:  moon_vis = 1.0 - smooth_step(5.0, 6.5, hour)
    elif hour < 19.0: moon_vis = 0.0
    elif hour < 20.5: moon_vis = smooth_step(19.0, 20.5, hour)
    else:             moon_vis = 1.0

    return top, bot, sun_col, sun_vis, moon_vis


# ═══════════════════════════════════════════════════════
#  SKY — digambar PERTAMA (sebelum dinding) via 2D overlay
# ═══════════════════════════════════════════════════════
def draw_sky_background(hour, viewport_w, viewport_h):
    """
    Menggambar langit sebagai quad 2D fullscreen di depan semua,
    lalu akan ditimpa dinding kecuali area jendela.
    HARUS dipanggil sebelum draw_room() dan draw_window_frame().
    
    Strategi: switch ke ortho 2D, gambar langit hanya di area piksel
    yang sesuai dengan bukaan jendela dalam screen-space.
    Untuk pendekatan lebih robust: gambar ke stencil buffer.
    """
    # Pendekatan stencil:
    # 1. Tulis 1 ke stencil di area jendela (proyeksi kamera saat ini)
    # 2. Gambar langit fullscreen hanya di area stencil == 1

    t = time.time()
    sky_top, sky_bot, sun_col, sun_vis, moon_vis = get_sky_colors(hour)

    # Dimensi jendela dalam world-space
    wx, wy = 0.30, 0.95
    ww, wh = 2.60, 2.30
    x_left  = wx - ww/2 - 0.02
    x_right = wx + ww/2 + 0.02
    y_bot   = wy + 0.04
    y_top   = wy + wh - 0.03
    z_win   = -2.95   # tepat di muka dinding (z=-3.00)

    # ── STENCIL PASS: tulis area jendela ke stencil ──
    glEnable(GL_STENCIL_TEST)
    glClear(GL_STENCIL_BUFFER_BIT)
    glStencilFunc(GL_ALWAYS, 1, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_REPLACE)
    glColorMask(GL_FALSE, GL_FALSE, GL_FALSE, GL_FALSE)
    glDepthMask(GL_FALSE)
    glDisable(GL_LIGHTING)

    # Gambar quad area jendela sebagai stencil mask
    glBegin(GL_QUADS)
    glVertex3f(x_left,  y_bot, z_win)
    glVertex3f(x_right, y_bot, z_win)
    glVertex3f(x_right, y_top, z_win)
    glVertex3f(x_left,  y_top, z_win)
    glEnd()

    # ── SKY PASS: gambar langit hanya di area stencil == 1 ──
    glColorMask(GL_TRUE, GL_TRUE, GL_TRUE, GL_TRUE)
    glStencilFunc(GL_EQUAL, 1, 0xFF)
    glStencilOp(GL_KEEP, GL_KEEP, GL_KEEP)

    # Switch ke ortho 2D untuk gambar sky fullscreen
    glMatrixMode(GL_PROJECTION)
    glPushMatrix()
    glLoadIdentity()
    glOrtho(0, viewport_w, 0, viewport_h, -1, 1)
    glMatrixMode(GL_MODELVIEW)
    glPushMatrix()
    glLoadIdentity()

    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)

    # Gambar sky gradient fullscreen
    W = float(viewport_w); H = float(viewport_h)
    glBegin(GL_QUADS)
    glColor3f(*sky_top)
    glVertex2f(0, H); glVertex2f(W, H)
    glColor3f(*sky_bot)
    glVertex2f(W, 0); glVertex2f(0, 0)
    glEnd()

    glMatrixMode(GL_PROJECTION)
    glPopMatrix()
    glMatrixMode(GL_MODELVIEW)
    glPopMatrix()

    # ── Gambar matahari / bulan / bintang di world-space ──
    # Masih pakai stencil == 1 (area jendela)
    glDepthMask(GL_FALSE)

    if sun_vis > 0.01:
        sun_t = smooth_step(5.5, 18.5, hour)
        sun_x = wx + ww * (sun_t - 0.5) * 0.80
        sun_y = wy + wh * (0.20 + math.sin(sun_t * math.pi) * 0.65)
        sun_r = 0.20
        sr, sg, sb = sun_col
        glColor3f(sr, sg, sb)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(sun_x, sun_y, z_win + 0.01)
        for i in range(33):
            a = math.radians(i * 11.25)
            glVertex3f(sun_x + math.cos(a)*sun_r, sun_y + math.sin(a)*sun_r, z_win + 0.01)
        glEnd()
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(sr, sg*0.85, sb*0.5, 0.28*sun_vis)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(sun_x, sun_y, z_win + 0.008)
        for i in range(33):
            a = math.radians(i * 11.25)
            glVertex3f(sun_x + math.cos(a)*sun_r*2.4, sun_y + math.sin(a)*sun_r*2.4, z_win + 0.008)
        glEnd()
        glColor4f(sr, sg*0.7, sb*0.3, 0.10*sun_vis)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(sun_x, sun_y, z_win + 0.006)
        for i in range(33):
            a = math.radians(i * 11.25)
            glVertex3f(sun_x + math.cos(a)*sun_r*4.5, sun_y + math.sin(a)*sun_r*4.5, z_win + 0.006)
        glEnd()
        glDisable(GL_BLEND)

    if moon_vis > 0.01:
        moon_x = wx + ww * 0.20
        moon_y = wy + wh * 0.72 + math.sin(t * 0.008) * 0.04
        moon_r = 0.14
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(0.92, 0.92, 0.82, moon_vis)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(moon_x, moon_y, z_win + 0.01)
        for i in range(33):
            a = math.radians(i * 11.25)
            glVertex3f(moon_x + math.cos(a)*moon_r, moon_y + math.sin(a)*moon_r, z_win + 0.01)
        glEnd()
        import random
        rng = random.Random(42)
        for _ in range(22):
            sx2 = rng.uniform(x_left+0.1, x_right-0.1)
            sy2 = rng.uniform(wy + wh*0.42, y_top - 0.04)
            sr2 = rng.uniform(0.011, 0.023)
            twinkle = 0.5 + 0.5*math.sin(t * rng.uniform(0.8,2.2) + rng.uniform(0,6))
            glColor4f(0.95, 0.95, 1.0, moon_vis * twinkle * 0.9)
            glBegin(GL_TRIANGLE_FAN)
            glVertex3f(sx2, sy2, z_win + 0.009)
            for i in range(7):
                a = math.radians(i * 60)
                glVertex3f(sx2 + math.cos(a)*sr2, sy2 + math.sin(a)*sr2, z_win + 0.009)
            glEnd()
        glDisable(GL_BLEND)

    # Awan (siang/sore)
    cloud_vis = 0.0
    if 7.0 < hour < 18.0:
        cloud_vis = min(smooth_step(7.0,9.0,hour), smooth_step(18.0,16.0,hour))
    if cloud_vis > 0.01:
        _draw_cloud(wx - 0.50, wy + wh*0.65, t, z_win, scale=1.0,  alpha=cloud_vis)
        _draw_cloud(wx + 0.60, wy + wh*0.52, t, z_win, scale=0.65, alpha=cloud_vis*0.8)
        if hour < 17.0:
            _draw_cloud(wx - 0.90, wy + wh*0.38, t, z_win, scale=0.48, alpha=cloud_vis*0.55)

    # Reset stencil & depth
    glDepthMask(GL_TRUE)
    glEnable(GL_DEPTH_TEST)
    glDisable(GL_STENCIL_TEST)
    glEnable(GL_LIGHTING)


def _draw_cloud(cx, cy, t, z_val, scale=1.0, alpha=1.0):
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    drift = math.sin(t * 0.025 + cx) * 0.06
    blobs = [(0.00,0.00,0.20),(0.22,0.04,0.16),(-0.20,0.02,0.15),(0.10,0.12,0.13),(-0.10,0.10,0.11)]
    for (bx, by, br) in blobs:
        glColor4f(0.98, 0.98, 1.00, 0.72 * alpha)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(cx + (bx+drift)*scale, cy + by*scale, z_val+0.005)
        for i in range(25):
            a = math.radians(i * 15)
            glVertex3f(cx + (bx+drift+math.cos(a)*br)*scale,
                       cy + (by+math.sin(a)*br)*scale, z_val+0.005)
        glEnd()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)


# ═══════════════════════════════════════════════════════
#  RUANGAN
# ═══════════════════════════════════════════════════════
def draw_room():
    mat_wood(0.54, 0.38, 0.20)
    draw_box(0, 0, 0, 6.0, 0.04, 6.0, 0.54, 0.38, 0.20)
    mat_wood(0.40, 0.28, 0.13)
    draw_box( 0.00, 0.02, -2.98, 6.0, 0.12, 0.04, 0.40, 0.28, 0.13)
    draw_box(-2.98, 0.02,  0.00, 0.04, 0.12, 6.0, 0.40, 0.28, 0.13)
    draw_box( 2.98, 0.02,  0.00, 0.04, 0.12, 6.0, 0.40, 0.28, 0.13)
    mat_wall(0.88, 0.84, 0.76)
    draw_box(0, 0, -3.00, 6.0, 4.0, 0.05, 0.88, 0.84, 0.76)
    mat_wall(0.85, 0.81, 0.73)
    draw_box(-3.00, 0, 0, 0.05, 4.0, 6.0, 0.85, 0.81, 0.73)
    mat_wall(0.85, 0.81, 0.73)
    draw_box(3.00, 0, 0, 0.05, 4.0, 6.0, 0.85, 0.81, 0.73)
    mat_wall(0.96, 0.94, 0.90)
    draw_box(0, 4.00, 0, 6.0, 0.05, 6.0, 0.96, 0.94, 0.90)
    mat_wall(0.90, 0.87, 0.82)
    draw_box( 0.00, 3.94, -2.98, 6.0, 0.10, 0.06, 0.90, 0.87, 0.82)
    draw_box(-2.98, 3.94,  0.00, 0.06, 0.10, 6.0, 0.90, 0.87, 0.82)
    draw_box( 2.98, 3.94,  0.00, 0.06, 0.10, 6.0, 0.90, 0.87, 0.82)
    mat_wall(0.82, 0.78, 0.70)
    draw_box(0, 0.04, -2.97, 5.80, 1.10, 0.03, 0.82, 0.78, 0.70)
    mat_wood(0.55, 0.42, 0.24)
    draw_box(0, 1.14, -2.97, 5.82, 0.04, 0.04, 0.55, 0.42, 0.24)


# ═══════════════════════════════════════════════════════
#  FRAME/KACA JENDELA — dipanggil SETELAH draw_room
# ═══════════════════════════════════════════════════════
def draw_window(hour=12.0):
    """Menggambar hanya frame, kaca, tirai jendela. Sky sudah digambar di draw_sky_background."""
    wx, wy = 0.30, 0.95
    ww, wh = 2.60, 2.30

    # ══ BINGKAI JENDELA ════════════════════════════════
    mat_wood(0.90, 0.87, 0.82)
    draw_box(wx, wy, -2.96, ww + 0.22, wh + 0.24, 0.08, 0.90, 0.87, 0.82)

    # ══ KACA — semi-transparan ══════════════════════════
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    if hour < 6 or hour > 20:
        tint = (0.15, 0.20, 0.40, 0.20)
    elif hour < 9:
        tint = (0.85, 0.65, 0.50, 0.12)
    elif hour < 16:
        tint = (0.78, 0.92, 1.00, 0.12)
    elif hour < 19:
        tint = (0.90, 0.70, 0.40, 0.14)
    else:
        tint = (0.15, 0.20, 0.40, 0.20)

    glColor4f(*tint)
    glBegin(GL_QUADS)
    glVertex3f(wx - ww*0.49, wy + 0.08,      -2.93)
    glVertex3f(wx - 0.04,    wy + 0.08,      -2.93)
    glVertex3f(wx - 0.04,    wy + wh - 0.06, -2.93)
    glVertex3f(wx - ww*0.49, wy + wh - 0.06, -2.93)
    glEnd()
    glBegin(GL_QUADS)
    glVertex3f(wx + 0.04,    wy + 0.08,      -2.93)
    glVertex3f(wx + ww*0.49, wy + 0.08,      -2.93)
    glVertex3f(wx + ww*0.49, wy + wh - 0.06, -2.93)
    glVertex3f(wx + 0.04,    wy + wh - 0.06, -2.93)
    glEnd()
    glColor4f(1.0, 1.0, 1.0, 0.09)
    glBegin(GL_QUADS)
    glVertex3f(wx - ww*0.48, wy + wh*0.72,   -2.929)
    glVertex3f(wx - ww*0.20, wy + wh*0.72,   -2.929)
    glVertex3f(wx - ww*0.24, wy + wh - 0.08, -2.929)
    glVertex3f(wx - ww*0.48, wy + wh - 0.08, -2.929)
    glEnd()
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

    # ══ TIANG JENDELA ══════════════════════════════════
    mat_wood(0.88, 0.84, 0.78)
    draw_box(wx,           wy + 0.07, -2.92, 0.06, wh - 0.08, 0.03, 0.88, 0.84, 0.78)
    draw_box(wx - ww*0.49, wy + 0.07, -2.92, 0.05, wh - 0.08, 0.03, 0.88, 0.84, 0.78)
    draw_box(wx + ww*0.49, wy + 0.07, -2.92, 0.05, wh - 0.08, 0.03, 0.88, 0.84, 0.78)
    draw_box(wx, wy + wh * 0.52, -2.92, ww - 0.08, 0.05, 0.03, 0.88, 0.84, 0.78)

    # ══ TIRAI ══════════════════════════════════════════
    mat_fabric(0.96, 0.92, 0.86)
    draw_box(wx - ww*0.50 - 0.22, wy + 0.06, -2.90, 0.30, wh + 0.26, 0.10, 0.96, 0.92, 0.86)
    mat_fabric(0.88, 0.84, 0.78)
    for fold in [-0.01, 0.02, 0.05]:
        draw_box(wx - ww*0.50 - 0.22, wy + 0.06, -2.90+fold, 0.025, wh+0.26, 0.10, 0.88, 0.84, 0.78)
    mat_fabric(0.96, 0.92, 0.86)
    draw_box(wx + ww*0.50 + 0.22, wy + 0.06, -2.90, 0.30, wh + 0.26, 0.10, 0.96, 0.92, 0.86)
    mat_fabric(0.88, 0.84, 0.78)
    for fold in [-0.01, 0.02, 0.05]:
        draw_box(wx + ww*0.50 + 0.22, wy + 0.06, -2.90+fold, 0.025, wh+0.26, 0.10, 0.88, 0.84, 0.78)
    mat_wood(0.72, 0.58, 0.36)
    draw_box(wx, wy + wh + 0.14, -2.90, ww + 0.90, 0.12, 0.14, 0.72, 0.58, 0.36)
    mat_wood(0.82, 0.76, 0.68)
    draw_box(wx, wy - 0.04, -2.86, ww + 0.46, 0.06, 0.22, 0.82, 0.76, 0.68)


# ═══════════════════════════════════════════════════════
#  SINAR MATAHARI (sun rays) — digambar TERAKHIR
# ═══════════════════════════════════════════════════════
def draw_sun_rays(hour=12.0):
    if   hour < 6.0:  ray_int = 0.0
    elif hour < 8.0:  ray_int = smooth_step(6.0, 8.0, hour) * 0.06
    elif hour < 11.0: ray_int = 0.06 + smooth_step(8.0, 11.0, hour) * 0.04
    elif hour < 15.0: ray_int = 0.10
    elif hour < 17.5: ray_int = 0.10 - smooth_step(15.0, 17.5, hour) * 0.04
    elif hour < 19.0: ray_int = 0.06 - smooth_step(17.5, 19.0, hour) * 0.06
    else:             ray_int = 0.0
    if ray_int < 0.001: return

    if hour < 9.0:    rc = (1.0, 0.72, 0.38)
    elif hour < 15.0: rc = (1.0, 0.93, 0.64)
    else:             rc = (1.0, 0.78, 0.42)

    t = time.time()
    flicker = ray_int + math.sin(t * 0.5) * ray_int * 0.12

    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)

    rays = [
        (-1.15,-0.40,-1.40,-0.30, 0.90),
        (-0.38, 0.20,-0.60, 0.60, 1.00),
        ( 0.22, 0.70, 0.20, 1.40, 1.00),
        ( 0.72, 1.20, 1.00, 2.20, 0.90),
        ( 1.22, 1.60, 1.80, 2.80, 0.70),
    ]
    for (xl, xr, xl2, xr2, af) in rays:
        alpha = flicker * af
        glBegin(GL_QUADS)
        glColor4f(rc[0], rc[1], rc[2], alpha)
        glVertex3f(xl,  2.90, -2.88)
        glVertex3f(xr,  2.90, -2.88)
        glColor4f(rc[0], rc[1], rc[2], 0.0)
        glVertex3f(xr2, 0.04,  2.8)
        glVertex3f(xl2, 0.04,  2.8)
        glEnd()

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
