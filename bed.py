from OpenGL.GL import *
from OpenGL.GLU import *
from utils import draw_box, draw_cone

def draw_bed():
    """
    Kasur menempel dinding KIRI (x=-3), headboard ke dinding BELAKANG (z=-3).
    Kasur memanjang ke arah +Z (ke depan).
    Center X kasur = -1.65 (lebar ~2.5, jadi -3 .. -0.4)
    """
    bx = -1.65

    # ── Rangka/platform kayu ──────────────────────────
    draw_box(bx, 0.04, -0.05, 2.50, 0.24, 4.10, 0.44, 0.28, 0.13)

    # ── Headboard (detail panel berlapis) ────────────
    # Panel utama
    draw_box(bx, 0.04, -2.08, 2.50, 1.10, 0.14, 0.40, 0.24, 0.11)
    # Panel dekoratif tengah (lebih terang)
    draw_box(bx, 0.20, -2.07, 2.00, 0.80, 0.05, 0.52, 0.36, 0.18)
    # Topping headboard
    draw_box(bx, 1.14, -2.06, 2.52, 0.07, 0.17, 0.46, 0.30, 0.14)

    # ── Matras ────────────────────────────────────────
    draw_box(bx, 0.28, -0.05, 2.28, 0.30, 3.80, 0.82, 0.77, 0.71)
    # Piping/border matras (strip tipis lebih terang)
    draw_box(bx, 0.42, -0.05, 2.30, 0.04, 3.82, 0.88, 0.84, 0.78)

    # ── Selimut (dusty rose, berlapis) ───────────────
    # Lapisan utama selimut
    draw_box(bx, 0.58, 0.80, 2.28, 0.12, 2.30, 0.86, 0.70, 0.66)
    # Lipatan selimut di ujung atas
    draw_box(bx, 0.62, -0.60, 2.24, 0.20, 0.38, 0.90, 0.75, 0.70)

    # ── Bantal (2 bantal, berbeda ukuran) ────────────
    # Bantal kiri (besar)
    draw_box(bx - 0.52, 0.60, -1.58, 0.90, 0.22, 0.60, 0.96, 0.91, 0.87)
    # Highlight bantal kiri
    draw_box(bx - 0.52, 0.80, -1.60, 0.80, 0.04, 0.52, 0.99, 0.96, 0.93)
    # Bantal kanan (besar)
    draw_box(bx + 0.52, 0.60, -1.58, 0.90, 0.22, 0.60, 0.93, 0.86, 0.82)
    # Bantal kecil dekoratif (tengah)
    draw_box(bx, 0.62, -1.42, 0.50, 0.26, 0.42, 0.78, 0.60, 0.56)

    # ── Kaki rangka (4 kaki kecil) ───────────────────
    for ox, oz in [(-1.1, -1.9), (1.1, -1.9), (-1.1, 1.85), (1.1, 1.85)]:
        draw_box(bx+ox, 0, -0.05+oz, 0.10, 0.08, 0.10, 0.32, 0.20, 0.09)


def draw_nightstand():
    """
    Nakas di kanan kasur, dekat headboard (tengah antara kasur dan meja).
    """
    nx, nz = 0.25, -1.60

    # ── Badan nakas (2 laci) ──────────────────────────
    # Badan utama
    draw_box(nx, 0.04, nz, 0.58, 0.56, 0.58, 0.50, 0.36, 0.19)
    # Laci atas
    draw_box(nx, 0.32, nz-0.27, 0.50, 0.17, 0.03, 0.60, 0.45, 0.26)
    # Laci bawah
    draw_box(nx, 0.13, nz-0.27, 0.50, 0.17, 0.03, 0.60, 0.45, 0.26)
    # Gagang laci atas
    draw_box(nx, 0.40, nz-0.26, 0.08, 0.04, 0.03, 0.72, 0.60, 0.38)
    # Gagang laci bawah
    draw_box(nx, 0.21, nz-0.26, 0.08, 0.04, 0.03, 0.72, 0.60, 0.38)
    # Top surface (sedikit lebih terang)
    draw_box(nx, 0.59, nz, 0.60, 0.03, 0.60, 0.62, 0.47, 0.27)

    # ── Lampu tidur di atas nakas ─────────────────────
    # Alas lampu
    draw_box(nx, 0.62, nz, 0.18, 0.04, 0.18, 0.55, 0.42, 0.24)
    # Tiang (silinder tipis)
    draw_box(nx, 0.66, nz, 0.04, 0.38, 0.04, 0.50, 0.38, 0.21)
    # Simpul dekoratif tiang
    draw_box(nx, 0.84, nz, 0.07, 0.06, 0.07, 0.58, 0.44, 0.25)
    # Kap lampu (trapesium — cone)
    glColor3f(0.95, 0.88, 0.70)
    draw_cone(nx, 1.04, nz, 0.21, 0.08, 0.26, 14)
    # Tutup atas kap (lingkaran kecil)
    draw_box(nx, 1.29, nz, 0.16, 0.03, 0.16, 0.88, 0.80, 0.62)
    # Bohlam (titik cahaya kecil)
    glPushMatrix()
    glTranslatef(nx, 1.08, nz)
    glColor3f(1.0, 0.98, 0.80)
    q = gluNewQuadric()
    gluSphere(q, 0.05, 8, 8)
    gluDeleteQuadric(q)
    glPopMatrix()

    # ── Dekorasi atas nakas ───────────────────────────
    # Buku kecil rebahan
    draw_box(nx-0.14, 0.62, nz+0.18, 0.22, 0.04, 0.15, 0.38, 0.26, 0.18)
    # Cangkir kecil
    draw_box(nx+0.15, 0.62, nz-0.15, 0.09, 0.10, 0.09, 0.72, 0.54, 0.40)
