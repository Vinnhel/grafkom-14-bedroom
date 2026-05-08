from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cylinder,
                   mat_wall, mat_wood, mat_glass, mat_fabric,
                   set_material, mat_metal)
import math, time

def draw_room():
    # ── Lantai ────────────────────────────────────────
    mat_wood(0.54, 0.38, 0.20)
    draw_box(0, 0, 0, 6.0, 0.04, 6.0, 0.54, 0.38, 0.20)
    mat_wood(0.40, 0.28, 0.13)
    draw_box( 0.00, 0.02, -2.98, 6.0, 0.12, 0.04, 0.40, 0.28, 0.13)
    draw_box(-2.98, 0.02,  0.00, 0.04, 0.12, 6.0, 0.40, 0.28, 0.13)
    draw_box( 2.98, 0.02,  0.00, 0.04, 0.12, 6.0, 0.40, 0.28, 0.13)

    # ── Dinding belakang ──────────────────────────────
    mat_wall(0.88, 0.84, 0.76)
    draw_box(0, 0, -3.00, 6.0, 4.0, 0.05, 0.88, 0.84, 0.76)

    # ── Dinding kiri ──────────────────────────────────
    mat_wall(0.85, 0.81, 0.73)
    draw_box(-3.00, 0, 0, 0.05, 4.0, 6.0, 0.85, 0.81, 0.73)

    # ── Dinding kanan ─────────────────────────────────
    mat_wall(0.85, 0.81, 0.73)
    draw_box(3.00, 0, 0, 0.05, 4.0, 6.0, 0.85, 0.81, 0.73)

    # ── Plafon ────────────────────────────────────────
    mat_wall(0.96, 0.94, 0.90)
    draw_box(0, 4.00, 0, 6.0, 0.05, 6.0, 0.96, 0.94, 0.90)
    mat_wall(0.90, 0.87, 0.82)
    draw_box( 0.00, 3.94, -2.98, 6.0, 0.10, 0.06, 0.90, 0.87, 0.82)
    draw_box(-2.98, 3.94,  0.00, 0.06, 0.10, 6.0, 0.90, 0.87, 0.82)
    draw_box( 2.98, 3.94,  0.00, 0.06, 0.10, 6.0, 0.90, 0.87, 0.82)

    # ── Wainscoting panel bawah ───────────────────────
    mat_wall(0.82, 0.78, 0.70)
    draw_box(0, 0.04, -2.97, 5.80, 1.10, 0.03, 0.82, 0.78, 0.70)
    mat_wood(0.55, 0.42, 0.24)
    draw_box(0, 1.14, -2.97, 5.82, 0.04, 0.04, 0.55, 0.42, 0.24)


def draw_window():
    """
    Jendela tanpa blinds.
    Di luar jendela ditampilkan: langit biru + awan + sinar matahari.
    Sinar matahari masuk melalui kaca secara dinamis (berubah seiring waktu).
    """
    wx, wy =  0.30, 0.95
    ww, wh =  2.60, 2.30

    t = time.time()

    # ══ LUAR JENDELA — langit & matahari ══════════════
    # Digambar dengan depth test dimatikan sementara agar
    # langit selalu terlihat di belakang kaca, tidak terblock dinding
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)   # bypass depth buffer sepenuhnya

    # Langit gradasi (biru cerah atas → putih kekuningan bawah)
    glBegin(GL_QUADS)
    glColor3f(0.42, 0.68, 0.92)   # biru cerah atas
    glVertex3f(wx - ww/2 - 0.02, wy + wh - 0.06, -2.98)
    glVertex3f(wx + ww/2 + 0.02, wy + wh - 0.06, -2.98)
    glColor3f(0.78, 0.90, 1.00)   # putih kebiruan bawah
    glVertex3f(wx + ww/2 + 0.02, wy + 0.07, -2.98)
    glVertex3f(wx - ww/2 - 0.02, wy + 0.07, -2.98)
    glEnd()

    # Matahari (disc putih kekuningan, posisi dinamis naik-turun pelan)
    sun_y = wy + wh * 0.72 + math.sin(t * 0.04) * 0.08
    sun_x = wx + ww * 0.30
    glColor3f(1.0, 0.97, 0.70)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(sun_x, sun_y, -2.975)
    for i in range(33):
        a = math.radians(i * 11.25)
        glVertex3f(sun_x + math.cos(a)*0.22, sun_y + math.sin(a)*0.22, -2.975)
    glEnd()
    # Corona matahari (soft glow)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glColor4f(1.0, 0.95, 0.60, 0.25)
    glBegin(GL_TRIANGLE_FAN)
    glVertex3f(sun_x, sun_y, -2.974)
    for i in range(33):
        a = math.radians(i * 11.25)
        glVertex3f(sun_x + math.cos(a)*0.44, sun_y + math.sin(a)*0.44, -2.974)
    glEnd()
    glDisable(GL_BLEND)

    # Awan 1
    _draw_cloud(wx - 0.55, wy + wh * 0.62, t)
    # Awan 2 (lebih kecil)
    _draw_cloud(wx + 0.60, wy + wh * 0.50, t, scale=0.65)

    glEnable(GL_DEPTH_TEST)    # aktifkan kembali depth test
    glEnable(GL_LIGHTING)

    # ══ BINGKAI JENDELA ════════════════════════════════
    mat_wood(0.90, 0.87, 0.82)
    draw_box(wx, wy, -2.96, ww + 0.22, wh + 0.24, 0.08, 0.90, 0.87, 0.82)

    # ══ KACA — semi-transparan, reflektif ══════════════
    # Gambar kaca SETELAH langit agar overlay langit terlihat
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)

    # Panel kiri
    glColor4f(0.78, 0.92, 1.00, 0.18)
    glBegin(GL_QUADS)
    glVertex3f(wx - ww*0.49, wy + 0.08,        -2.93)
    glVertex3f(wx - 0.04,    wy + 0.08,        -2.93)
    glVertex3f(wx - 0.04,    wy + wh - 0.06,   -2.93)
    glVertex3f(wx - ww*0.49, wy + wh - 0.06,   -2.93)
    glEnd()
    # Panel kanan
    glBegin(GL_QUADS)
    glVertex3f(wx + 0.04,    wy + 0.08,        -2.93)
    glVertex3f(wx + ww*0.49, wy + 0.08,        -2.93)
    glVertex3f(wx + ww*0.49, wy + wh - 0.06,   -2.93)
    glVertex3f(wx + 0.04,    wy + wh - 0.06,   -2.93)
    glEnd()

    # Kilap kaca (highlight putih di pojok kiri atas)
    glColor4f(1.0, 1.0, 1.0, 0.12)
    glBegin(GL_QUADS)
    glVertex3f(wx - ww*0.48, wy + wh*0.72,  -2.929)
    glVertex3f(wx - ww*0.20, wy + wh*0.72,  -2.929)
    glVertex3f(wx - ww*0.24, wy + wh - 0.08,-2.929)
    glVertex3f(wx - ww*0.48, wy + wh - 0.08,-2.929)
    glEnd()

    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)

    # ══ TIANG JENDELA ══════════════════════════════════
    mat_wood(0.88, 0.84, 0.78)
    draw_box(wx,           wy + 0.07, -2.92, 0.06, wh - 0.08, 0.03,
             0.88, 0.84, 0.78)
    draw_box(wx - ww*0.49, wy + 0.07, -2.92, 0.05, wh - 0.08, 0.03,
             0.88, 0.84, 0.78)
    draw_box(wx + ww*0.49, wy + 0.07, -2.92, 0.05, wh - 0.08, 0.03,
             0.88, 0.84, 0.78)

    # Rail horizontal tengah
    mat_wood(0.88, 0.84, 0.78)
    draw_box(wx, wy + wh * 0.52, -2.92, ww - 0.08, 0.05, 0.03,
             0.88, 0.84, 0.78)

    # ══ TIRAI kiri & kanan ════════════════════════════
    mat_fabric(0.96, 0.92, 0.86)
    draw_box(wx - ww*0.50 - 0.22, wy + 0.06, -2.90,
             0.30, wh + 0.26, 0.10, 0.96, 0.92, 0.86)
    mat_fabric(0.88, 0.84, 0.78)
    for fold in [-0.01, 0.02, 0.05]:
        draw_box(wx - ww*0.50 - 0.22, wy + 0.06, -2.90 + fold,
                 0.025, wh + 0.26, 0.10, 0.88, 0.84, 0.78)

    mat_fabric(0.96, 0.92, 0.86)
    draw_box(wx + ww*0.50 + 0.22, wy + 0.06, -2.90,
             0.30, wh + 0.26, 0.10, 0.96, 0.92, 0.86)
    mat_fabric(0.88, 0.84, 0.78)
    for fold in [-0.01, 0.02, 0.05]:
        draw_box(wx + ww*0.50 + 0.22, wy + 0.06, -2.90 + fold,
                 0.025, wh + 0.26, 0.10, 0.88, 0.84, 0.78)

    # Pelmet / rel tirai atas
    mat_wood(0.72, 0.58, 0.36)
    draw_box(wx, wy + wh + 0.14, -2.90, ww + 0.90, 0.12, 0.14,
             0.72, 0.58, 0.36)

    # Kusen bawah menonjol
    mat_wood(0.82, 0.76, 0.68)
    draw_box(wx, wy - 0.04, -2.86, ww + 0.46, 0.06, 0.22,
             0.82, 0.76, 0.68)


def _draw_cloud(cx, cy, t, scale=1.0):
    """Awan sederhana dari beberapa disc putih semi-transparan."""
    glDisable(GL_LIGHTING)
    glDisable(GL_DEPTH_TEST)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    drift = math.sin(t * 0.025 + cx) * 0.05   # gerak pelan
    blobs = [
        (0.00,  0.00, 0.20),
        (0.22,  0.04, 0.16),
        (-0.20, 0.02, 0.15),
        (0.10,  0.12, 0.13),
        (-0.10, 0.10, 0.11),
    ]
    for (bx, by, br) in blobs:
        glColor4f(0.98, 0.98, 1.00, 0.72)
        glBegin(GL_TRIANGLE_FAN)
        glVertex3f(cx + (bx + drift) * scale, cy + by * scale, -2.983)
        for i in range(25):
            a = math.radians(i * 15)
            glVertex3f(cx + (bx + drift + math.cos(a)*br) * scale,
                       cy + (by + math.sin(a)*br) * scale, -2.983)
        glEnd()
    glDisable(GL_BLEND)
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)


def draw_sun_rays():
    """
    Berkas cahaya matahari dinamis dari jendela.
    Intensitas dan posisi berubah sedikit seiring waktu (t).
    Digambar TERAKHIR setelah semua objek solid.
    """
    t = time.time()
    # Intensitas bergetar sedikit (simulasi flicker matahari)
    intensity = 0.08 + math.sin(t * 0.5) * 0.012

    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)

    # Setiap ray: (x_kiri_atas, x_kanan_atas, x_kiri_bawah, x_kanan_bawah, alpha_factor)
    rays = [
        (-1.15, -0.40, -1.40, -0.30, 0.90),
        (-0.38,  0.20, -0.60,  0.60, 1.00),
        ( 0.22,  0.70,  0.20,  1.40, 1.00),
        ( 0.72,  1.20,  1.00,  2.20, 0.90),
        ( 1.22,  1.60,  1.80,  2.80, 0.70),
    ]

    for (xl, xr, xl2, xr2, af) in rays:
        alpha = intensity * af
        glBegin(GL_QUADS)
        glColor4f(1.0, 0.93, 0.64, alpha)
        glVertex3f(xl,  2.90, -2.88)
        glVertex3f(xr,  2.90, -2.88)
        glColor4f(1.0, 0.90, 0.58, 0.0)
        glVertex3f(xr2, 0.04,  2.8)
        glVertex3f(xl2, 0.04,  2.8)
        glEnd()

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
