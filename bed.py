from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cone, draw_cylinder,
                   mat_wood, mat_fabric, mat_metal,
                   set_material, mat_emissive, mat_reset_emissive)

# ═══════════════════════════════════════════════════════
#  KASUR DOUBLE — menempel dinding KIRI (x=-3)
#  Headboard ke dinding BELAKANG (z=-3)
# ═══════════════════════════════════════════════════════
def draw_bed():
    bx = -1.65   # center X (lebar kasur ~2.4, dari x=-2.85 ke x=-0.45)

    # ── Platform / rangka kayu ────────────────────────
    mat_wood(0.36, 0.24, 0.11)
    draw_box(bx, 0.00, -0.10, 2.55, 0.26, 4.15, 0.36, 0.24, 0.11)
    # Profil tepi platform (strip lebih terang)
    mat_wood(0.46, 0.32, 0.16)
    draw_box(bx, 0.24,  1.90, 2.56, 0.04, 0.06, 0.46, 0.32, 0.16)  # tepi depan
    draw_box(bx, 0.24, -0.10, 0.04, 0.04, 4.16, 0.46, 0.32, 0.16)  # tepi kiri tengah

    # ── Headboard berlapis 3 panel ────────────────────
    # Panel dasar
    mat_wood(0.32, 0.20, 0.09)
    draw_box(bx, 0.00, -2.10, 2.56, 1.20, 0.18, 0.32, 0.20, 0.09)
    # Panel busa tengah (tufted fabric headboard)
    mat_fabric(0.52, 0.42, 0.36)
    draw_box(bx, 0.10, -2.06, 2.10, 0.96, 0.08, 0.52, 0.42, 0.36)
    # Highlight busa (bagian tengah lebih terang)
    mat_fabric(0.62, 0.52, 0.44)
    draw_box(bx, 0.14, -2.05, 1.80, 0.80, 0.05, 0.62, 0.52, 0.44)
    # Grid tufted (jahitan vertikal + horizontal)
    mat_fabric(0.40, 0.30, 0.24)
    for ox in [-0.55, 0.00, 0.55]:
        draw_box(bx+ox, 0.14, -2.05, 0.025, 0.82, 0.06, 0.40, 0.30, 0.24)
    for oy_frac in [0.28, 0.56]:
        draw_box(bx, 0.14 + 0.80*oy_frac, -2.05, 1.82, 0.025, 0.06,
                 0.40, 0.30, 0.24)
    # Rail atas headboard (kayu gelap)
    mat_wood(0.38, 0.24, 0.10)
    draw_box(bx, 1.18, -2.08, 2.58, 0.08, 0.20, 0.38, 0.24, 0.10)

    # ── Footboard (papan kaki kasur) ─────────────────
    mat_wood(0.36, 0.24, 0.11)
    draw_box(bx, 0.00, 2.02, 2.56, 0.50, 0.14, 0.36, 0.24, 0.11)
    mat_wood(0.44, 0.30, 0.14)
    draw_box(bx, 0.00, 2.02, 2.58, 0.07, 0.17, 0.44, 0.30, 0.14)  # cap atas

    # ── Matras ────────────────────────────────────────
    mat_fabric(0.88, 0.84, 0.80)
    draw_box(bx, 0.26, -0.08, 2.30, 0.28, 3.88, 0.88, 0.84, 0.80)
    # Border / piping matras
    mat_fabric(0.78, 0.72, 0.68)
    draw_box(bx, 0.26, -0.08, 2.32, 0.30, 0.04, 0.78, 0.72, 0.68)  # tepi belakang
    draw_box(bx, 0.26, -0.08, 0.04, 0.30, 3.90, 0.78, 0.72, 0.68)  # tepi kiri
    draw_box(bx, 0.40, -0.08, 2.32, 0.04, 3.90, 0.78, 0.72, 0.68)  # tepi atas

    # ── Selimut (duvet) — dusty blue ─────────────────
    # Bagian selimut utama (menutupi 2/3 kasur dari bawah)
    mat_fabric(0.60, 0.68, 0.76)
    draw_box(bx, 0.56, 0.70, 2.28, 0.16, 2.56, 0.60, 0.68, 0.76)
    # Lipatan atas selimut (fold-back)
    mat_fabric(0.66, 0.74, 0.82)
    draw_box(bx, 0.64, -0.52, 2.20, 0.24, 0.40, 0.66, 0.74, 0.82)
    # Jahitan grid selimut
    mat_fabric(0.52, 0.60, 0.68)
    for ox in [-0.70, 0.00, 0.70]:
        draw_box(bx+ox, 0.57, 0.70, 0.020, 0.17, 2.58, 0.52, 0.60, 0.68)
    for oz_off in [-0.80, 0.00, 0.80]:
        draw_box(bx, 0.57, 0.70 + oz_off, 2.28, 0.17, 0.020, 0.52, 0.60, 0.68)

    # ── Bantal (2 besar + 1 dekoratif) ───────────────
    # Bantal kiri
    mat_fabric(0.94, 0.90, 0.86)
    draw_box(bx - 0.54, 0.58, -1.56, 0.96, 0.24, 0.64, 0.94, 0.90, 0.86)
    # Highlight bantal kiri
    mat_fabric(0.98, 0.96, 0.93)
    draw_box(bx - 0.54, 0.78, -1.58, 0.82, 0.05, 0.54, 0.98, 0.96, 0.93)
    # Jahitan bantal kiri
    mat_fabric(0.80, 0.76, 0.72)
    draw_box(bx - 0.54, 0.60, -1.56, 0.020, 0.24, 0.66, 0.80, 0.76, 0.72)

    # Bantal kanan
    mat_fabric(0.92, 0.88, 0.84)
    draw_box(bx + 0.54, 0.58, -1.56, 0.96, 0.24, 0.64, 0.92, 0.88, 0.84)
    mat_fabric(0.96, 0.94, 0.90)
    draw_box(bx + 0.54, 0.78, -1.58, 0.82, 0.05, 0.54, 0.96, 0.94, 0.90)
    mat_fabric(0.78, 0.74, 0.70)
    draw_box(bx + 0.54, 0.60, -1.56, 0.020, 0.24, 0.66, 0.78, 0.74, 0.70)

    # Bantal dekoratif kecil (tengah, dusty rose)
    mat_fabric(0.80, 0.62, 0.58)
    draw_box(bx, 0.62, -1.44, 0.52, 0.28, 0.44, 0.80, 0.62, 0.58)
    mat_fabric(0.88, 0.70, 0.66)
    draw_box(bx, 0.80, -1.46, 0.42, 0.06, 0.36, 0.88, 0.70, 0.66)

    # ── Kaki rangka (4 sudut) ─────────────────────────
    mat_wood(0.28, 0.18, 0.08)
    for ox, oz in [(-1.15,-2.00),(1.15,-2.00),(-1.15,1.92),(1.15,1.92)]:
        draw_box(bx+ox, 0.00, -0.10+oz, 0.12, 0.06, 0.12, 0.28, 0.18, 0.08)


# ═══════════════════════════════════════════════════════
#  NAKAS — di kanan kasur, dekat headboard
# ═══════════════════════════════════════════════════════
def draw_nightstand():
    nx, nz = 0.25, -1.60

    # ── Badan nakas ───────────────────────────────────
    mat_wood(0.44, 0.32, 0.16)
    draw_box(nx, 0.00, nz, 0.60, 0.60, 0.60, 0.44, 0.32, 0.16)

    # Panel depan (muka nakas, sedikit lebih terang)
    mat_wood(0.54, 0.40, 0.20)
    draw_box(nx, 0.00, nz - 0.28, 0.56, 0.60, 0.04, 0.54, 0.40, 0.20)

    # Garis pemisah laci
    mat_wood(0.36, 0.24, 0.11)
    draw_box(nx, 0.30, nz - 0.28, 0.54, 0.02, 0.04, 0.36, 0.24, 0.11)

    # Muka laci atas
    mat_wood(0.58, 0.43, 0.22)
    draw_box(nx, 0.44, nz - 0.285, 0.50, 0.26, 0.025, 0.58, 0.43, 0.22)
    # Muka laci bawah
    draw_box(nx, 0.14, nz - 0.285, 0.50, 0.26, 0.025, 0.58, 0.43, 0.22)

    # Gagang laci atas — logam kecil
    mat_metal(0.74, 0.62, 0.40)
    draw_box(nx, 0.44, nz - 0.30, 0.10, 0.04, 0.025, 0.74, 0.62, 0.40)
    # Gagang laci bawah
    draw_box(nx, 0.14, nz - 0.30, 0.10, 0.04, 0.025, 0.74, 0.62, 0.40)

    # Top surface (permukaan atas lebih terang)
    mat_wood(0.60, 0.46, 0.24)
    draw_box(nx, 0.60, nz, 0.62, 0.03, 0.62, 0.60, 0.46, 0.24)

    # ── Lampu meja di atas nakas ──────────────────────
    # Alas / base lampu
    mat_wood(0.50, 0.38, 0.20)
    draw_box(nx, 0.63, nz, 0.20, 0.04, 0.20, 0.50, 0.38, 0.20)
    # Tiang silinder
    draw_cylinder(nx, 0.67, nz, 0.025, 0.36, slices=10)
    # Simpul dekoratif tengah tiang
    mat_wood(0.56, 0.42, 0.22)
    draw_box(nx, 0.84, nz, 0.07, 0.07, 0.07, 0.56, 0.42, 0.22)
    # Kap lampu (trapesium via draw_cone)
    mat_fabric(0.96, 0.88, 0.70)
    draw_cone(nx, 1.04, nz, 0.22, 0.09, 0.28, 16)
    # Tutup atas kap
    mat_fabric(0.86, 0.78, 0.60)
    draw_box(nx, 1.31, nz, 0.18, 0.03, 0.18, 0.86, 0.78, 0.60)
    # Bohlam emissive
    mat_emissive(1.0, 0.98, 0.82)
    glPushMatrix()
    glTranslatef(nx, 1.09, nz)
    q = gluNewQuadric()
    gluSphere(q, 0.05, 8, 8)
    gluDeleteQuadric(q)
    glPopMatrix()
    mat_reset_emissive()

    # ── Dekorasi atas nakas ───────────────────────────
    # Buku rebahan (2 buku stack)
    mat_fabric(0.36, 0.26, 0.18)
    draw_box(nx - 0.16, 0.63, nz + 0.18, 0.24, 0.04, 0.16, 0.36, 0.26, 0.18)
    mat_fabric(0.48, 0.36, 0.24)
    draw_box(nx - 0.14, 0.67, nz + 0.18, 0.20, 0.04, 0.14, 0.48, 0.36, 0.24)
    # Cangkir keramik
    set_material(0.70, 0.52, 0.38,
                 amb_scale=0.25, spec=(0.32,0.28,0.22,1.0), shininess=36.0)
    draw_box(nx + 0.16, 0.63, nz - 0.16, 0.09, 0.11, 0.09, 0.70, 0.52, 0.38)
    # Pegangan cangkir
    set_material(0.60, 0.44, 0.30,
                 amb_scale=0.25, spec=(0.28,0.24,0.18,1.0), shininess=30.0)
    draw_box(nx + 0.22, 0.68, nz - 0.16, 0.06, 0.05, 0.03, 0.60, 0.44, 0.30)
