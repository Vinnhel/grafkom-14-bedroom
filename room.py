from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cylinder,
                   mat_wall, mat_wood, mat_glass, mat_fabric,
                   set_material, mat_metal)

def draw_room():
    """
    Koordinat:
      X: -3 (kiri/kasur) .. +3 (kanan/lemari)
      Y:  0 (lantai)     ..  4 (plafon)
      Z: -3 (belakang)   .. +3 (depan/kamera)
    """
    # ── Lantai — papan kayu hangat ────────────────────
    mat_wood(0.54, 0.38, 0.20)
    draw_box(0, 0, 0, 6.0, 0.04, 6.0, 0.54, 0.38, 0.20)
    # Moulding lantai (baseboard) — 4 sisi
    mat_wood(0.40, 0.28, 0.13)
    draw_box( 0.00, 0.02, -2.98, 6.0, 0.12, 0.04, 0.40, 0.28, 0.13)  # belakang
    draw_box(-2.98, 0.02,  0.00, 0.04, 0.12, 6.0, 0.40, 0.28, 0.13)  # kiri
    draw_box( 2.98, 0.02,  0.00, 0.04, 0.12, 6.0, 0.40, 0.28, 0.13)  # kanan

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
    # Cornice/crown moulding atas-bawah
    mat_wall(0.90, 0.87, 0.82)
    draw_box( 0.00, 3.94, -2.98, 6.0, 0.10, 0.06, 0.90, 0.87, 0.82)
    draw_box(-2.98, 3.94,  0.00, 0.06, 0.10, 6.0, 0.90, 0.87, 0.82)
    draw_box( 2.98, 3.94,  0.00, 0.06, 0.10, 6.0, 0.90, 0.87, 0.82)

    # ── Panel dinding dekoratif (wainscoting) ─────────
    # Dinding belakang: panel horizontal di 1/3 bawah
    mat_wall(0.82, 0.78, 0.70)
    draw_box(0, 0.04, -2.97, 5.80, 1.10, 0.03, 0.82, 0.78, 0.70)
    # Rail pemisah panel
    mat_wood(0.55, 0.42, 0.24)
    draw_box(0, 1.14, -2.97, 5.82, 0.04, 0.04, 0.55, 0.42, 0.24)


def draw_window():
    """
    Jendela besar di dinding belakang — double panel dengan venetian blind.
    """
    wx, wy =  0.30, 0.95
    ww, wh =  2.60, 2.30

    # ── Bingkai luar (architrave) — kayu putih ────────
    mat_wood(0.90, 0.87, 0.82)
    draw_box(wx, wy, -2.96, ww + 0.22, wh + 0.24, 0.08, 0.90, 0.87, 0.82)

    # ── Panel kaca (2 panel kiri & kanan) ─────────────
    mat_glass(0.76, 0.90, 1.00)
    draw_box(wx - ww*0.26, wy + 0.08, -2.94, ww*0.46, wh - 0.10, 0.025,
             0.76, 0.90, 1.00)
    draw_box(wx + ww*0.26, wy + 0.08, -2.94, ww*0.46, wh - 0.10, 0.025,
             0.76, 0.90, 1.00)

    # ── Tiang vertikal tengah + 2 tiang luar ──────────
    mat_wood(0.88, 0.84, 0.78)
    draw_box(wx,             wy + 0.07, -2.92, 0.06, wh - 0.08, 0.03,
             0.88, 0.84, 0.78)  # tengah
    draw_box(wx - ww*0.49,   wy + 0.07, -2.92, 0.05, wh - 0.08, 0.03,
             0.88, 0.84, 0.78)  # kiri
    draw_box(wx + ww*0.49,   wy + 0.07, -2.92, 0.05, wh - 0.08, 0.03,
             0.88, 0.84, 0.78)  # kanan

    # ── Rail horizontal tengah ────────────────────────
    mat_wood(0.88, 0.84, 0.78)
    draw_box(wx, wy + wh*0.52, -2.92, ww - 0.08, 0.05, 0.03,
             0.88, 0.84, 0.78)

    # ── Venetian blind (12 slat horizontal) ──────────
    set_material(0.82, 0.80, 0.76,
                 amb_scale=0.25, spec=(0.18,0.18,0.16,1.0), shininess=22.0)
    for i in range(12):
        yy = wy + 0.14 + i * (wh * 0.072)
        draw_box(wx, yy, -2.90, ww - 0.16, 0.028, 0.020,
                 0.82, 0.80, 0.76)

    # Tali venetian blind (2 tali vertikal tipis)
    set_material(0.68, 0.66, 0.62,
                 amb_scale=0.22, spec=(0.05,0.05,0.05,1.0), shininess=4.0)
    draw_box(wx - ww*0.20, wy + wh*0.50, -2.91, 0.012, wh - 0.10, 0.012,
             0.68, 0.66, 0.62)
    draw_box(wx + ww*0.20, wy + wh*0.50, -2.91, 0.012, wh - 0.10, 0.012,
             0.68, 0.66, 0.62)

    # ── Tirai kiri & kanan ────────────────────────────
    mat_fabric(0.96, 0.92, 0.86)
    # Tirai kiri
    draw_box(wx - ww*0.50 - 0.22, wy + 0.06, -2.90,
             0.30, wh + 0.26, 0.10, 0.96, 0.92, 0.86)
    # Lipatan tirai kiri (3 strip simulasi kerutan)
    mat_fabric(0.88, 0.84, 0.78)
    for dz_fold in [-0.01, 0.02, 0.05]:
        draw_box(wx - ww*0.50 - 0.22, wy + 0.06, -2.90 + dz_fold,
                 0.025, wh + 0.26, 0.10, 0.88, 0.84, 0.78)
    # Tirai kanan
    mat_fabric(0.96, 0.92, 0.86)
    draw_box(wx + ww*0.50 + 0.22, wy + 0.06, -2.90,
             0.30, wh + 0.26, 0.10, 0.96, 0.92, 0.86)
    mat_fabric(0.88, 0.84, 0.78)
    for dz_fold in [-0.01, 0.02, 0.05]:
        draw_box(wx + ww*0.50 + 0.22, wy + 0.06, -2.90 + dz_fold,
                 0.025, wh + 0.26, 0.10, 0.88, 0.84, 0.78)

    # Pelmet/valance (rel tirai atas) — kayu
    mat_wood(0.72, 0.58, 0.36)
    draw_box(wx, wy + wh + 0.14, -2.90, ww + 0.90, 0.12, 0.14,
             0.72, 0.58, 0.36)

    # Kusen bawah (windowsill) menonjol
    mat_wood(0.82, 0.76, 0.68)
    draw_box(wx, wy - 0.04, -2.86, ww + 0.46, 0.06, 0.22,
             0.82, 0.76, 0.68)


def draw_sun_rays():
    """Berkas cahaya matahari — digambar TERAKHIR (transparan)."""
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)

    rays = [
        (-1.10, -0.50,  -3.0, -1.20, 0.08),
        (-0.50,  0.10,  -1.5,  0.50, 0.10),
        ( 0.10,  0.70,   0.0,  2.00, 0.10),
        ( 0.70,  1.30,   1.2,  3.00, 0.08),
        ( 1.10,  1.50,   2.0,  3.20, 0.06),
    ]
    for (xl, xr, xl2, xr2, alpha) in rays:
        glBegin(GL_QUADS)
        glColor4f(1.0, 0.91, 0.62, alpha)
        glVertex3f(xl,  2.85, -2.88)
        glVertex3f(xr,  2.85, -2.88)
        glColor4f(1.0, 0.88, 0.58, 0.0)
        glVertex3f(xr2, 0.05,  2.5)
        glVertex3f(xl2, 0.05,  2.5)
        glEnd()

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
