from OpenGL.GL import *
from OpenGL.GLU import *
from utils import draw_box

def draw_room():
    """
    Layout koordinat:
      X: -3 (kiri/kasur) .. +3 (kanan/lemari)
      Y:  0 (lantai)     ..  4 (plafon)
      Z: -3 (belakang/jendela) .. +3 (depan/kamera)
    """
    # Lantai kayu hangat
    draw_box( 0, 0,  0,  6.0, 0.04, 6.0,  0.55, 0.39, 0.21)
    # Dinding belakang (krem)
    draw_box( 0, 0, -3,  6.0, 4.00, 0.05, 0.90, 0.86, 0.78)
    # Dinding kiri
    draw_box(-3, 0,  0,  0.05, 4.00, 6.0, 0.87, 0.83, 0.75)
    # Dinding kanan
    draw_box( 3, 0,  0,  0.05, 4.00, 6.0, 0.87, 0.83, 0.75)
    # Plafon
    draw_box( 0, 4,  0,  6.0, 0.05, 6.0, 0.94, 0.92, 0.87)


def draw_window():
    """
    Jendela di dinding belakang (z≈-3), posisi tengah.
    Bingkai, kaca, tirai, venetian blind.
    """
    wx, wy   =  0.3, 0.95   # center x, y bawah bingkai
    ww, wh   =  2.6, 2.3    # lebar, tinggi jendela

    # Bingkai luar (kayu putih)
    draw_box(wx, wy,        -2.97, ww+0.20, wh+0.20, 0.10, 0.88, 0.84, 0.78)
    # Kaca (biru cerah)
    draw_box(wx, wy+0.07,   -2.95, ww-0.10, wh-0.08, 0.04, 0.80, 0.92, 1.00)

    # Tiang vertikal tengah
    draw_box(wx, wy+0.07,   -2.92, 0.07, wh-0.08, 0.04, 0.90, 0.86, 0.80)
    # Tiang horizontal tengah
    draw_box(wx, wy+wh*0.52,-2.92, ww-0.10, 0.07,   0.04, 0.90, 0.86, 0.80)

    # Tirai kiri
    draw_box(wx - ww*0.5 - 0.24, wy+0.05, -2.90, 0.32, wh+0.22, 0.09, 0.97, 0.94, 0.88)
    # Tirai kanan
    draw_box(wx + ww*0.5 + 0.24, wy+0.05, -2.90, 0.32, wh+0.22, 0.09, 0.97, 0.94, 0.88)

    # Venetian blind — kisi horizontal
    for i in range(8):
        yy = wy + 0.12 + i * (wh / 8.5)
        draw_box(wx, yy, -2.92, ww-0.14, 0.035, 0.025, 0.78, 0.76, 0.70)

    # Kusen bawah (windowsill)
    draw_box(wx, wy-0.04, -2.88, ww+0.40, 0.06, 0.18, 0.84, 0.80, 0.72)


def draw_sun_rays():
    """
    Berkas cahaya matahari masuk dari jendela — quad transparan (blending).
    Digambar TERAKHIR setelah semua objek solid.
    """
    glDisable(GL_LIGHTING)
    glEnable(GL_BLEND)
    glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
    glDepthMask(GL_FALSE)

    # Setiap ray: (x_kiri_atas, x_kanan_atas, x_kiri_bawah, x_kanan_bawah, alpha)
    # Asal di z=-2.88 (jendela), ujung di z=+2.5 (lantai depan)
    rays = [
        (-1.10, -0.50,  -3.0,  -1.2,  0.08),
        (-0.50,  0.10,  -1.5,   0.5,  0.10),
        ( 0.10,  0.70,   0.0,   2.0,  0.10),
        ( 0.70,  1.30,   1.2,   3.0,  0.08),
        ( 1.10,  1.50,   2.0,   3.2,  0.06),
    ]

    for (xl, xr, xl2, xr2, alpha) in rays:
        glBegin(GL_QUADS)
        glColor4f(1.0, 0.91, 0.62, alpha)        # terang di jendela
        glVertex3f(xl,  2.85, -2.88)
        glVertex3f(xr,  2.85, -2.88)
        glColor4f(1.0, 0.88, 0.58, 0.0)          # fade transparan di lantai
        glVertex3f(xr2, 0.05,  2.5)
        glVertex3f(xl2, 0.05,  2.5)
        glEnd()

    glDepthMask(GL_TRUE)
    glDisable(GL_BLEND)
    glEnable(GL_LIGHTING)
