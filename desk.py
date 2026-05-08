from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cylinder,
                   mat_wood, mat_fabric, mat_metal, mat_plastic, mat_paper,
                   set_material, mat_emissive, mat_reset_emissive)

# ═══════════════════════════════════════════════════════
#  MEJA BELAJAR — dinding BELAKANG (z=-3), tengah-kanan
# ═══════════════════════════════════════════════════════
def draw_desk():
    dx  =  1.20
    dz  = -2.30
    mw  =  1.85
    md  =  0.85
    mh  =  0.84

    mat_wood(0.68, 0.50, 0.27)
    draw_box(dx, mh, dz, mw, 0.055, md, 0.68, 0.50, 0.27)
    mat_wood(0.52, 0.36, 0.17)
    draw_box(dx, mh - 0.01, dz, mw + 0.03, 0.025, md + 0.03, 0.52, 0.36, 0.17)

    mat_wood(0.42, 0.28, 0.13)
    for ox, oz in [(-0.83,-0.36),(0.83,-0.36),(-0.83,0.36),(0.83,0.36)]:
        draw_box(dx+ox, 0.00, dz+oz, 0.07, mh, 0.07, 0.42, 0.28, 0.13)
    mat_wood(0.40, 0.26, 0.12)
    draw_box(dx, 0.28, dz - 0.36, mw - 0.20, 0.04, 0.04, 0.40, 0.26, 0.12)
    draw_box(dx, 0.28, dz + 0.36, mw - 0.20, 0.04, 0.04, 0.40, 0.26, 0.12)

    _draw_desk_pedestal(dx + 0.72, dz, mh)
    _draw_laptop(dx - 0.12, mh + 0.055, dz + 0.04)

    mat_paper(0.74, 0.28, 0.22)
    draw_box(dx - 0.72, mh + 0.055, dz - 0.14, 0.075, 0.30, 0.24, 0.74, 0.28, 0.22)
    mat_paper(0.28, 0.50, 0.64)
    draw_box(dx - 0.62, mh + 0.055, dz - 0.14, 0.075, 0.34, 0.24, 0.28, 0.50, 0.64)
    mat_paper(0.64, 0.52, 0.20)
    draw_box(dx - 0.52, mh + 0.055, dz - 0.14, 0.075, 0.26, 0.24, 0.64, 0.52, 0.20)
    mat_metal(0.55, 0.50, 0.44)
    draw_box(dx - 0.79, mh + 0.055, dz - 0.14, 0.025, 0.22, 0.22, 0.55, 0.50, 0.44)

    set_material(0.58, 0.44, 0.30, amb_scale=0.25,
                 spec=(0.28,0.24,0.18,1.0), shininess=32.0)
    draw_cylinder(dx - 0.74, mh + 0.055, dz + 0.26, 0.055, 0.16, slices=12)
    set_material(0.82, 0.70, 0.20, amb_scale=0.25,
                 spec=(0.15,0.14,0.10,1.0), shininess=20.0)
    draw_box(dx - 0.74, mh + 0.19, dz + 0.22, 0.015, 0.10, 0.015, 0.82, 0.70, 0.20)
    set_material(0.30, 0.55, 0.32, amb_scale=0.25,
                 spec=(0.15,0.14,0.10,1.0), shininess=20.0)
    draw_box(dx - 0.71, mh + 0.19, dz + 0.27, 0.015, 0.12, 0.015, 0.30, 0.55, 0.32)

    mat_fabric(0.22, 0.20, 0.18)
    draw_box(dx + 0.30, mh + 0.055, dz + 0.22, 0.34, 0.008, 0.26, 0.22, 0.20, 0.18)
    mat_plastic(0.28, 0.28, 0.30)
    draw_box(dx + 0.28, mh + 0.063, dz + 0.20, 0.10, 0.038, 0.15, 0.28, 0.28, 0.30)
    mat_metal(0.50, 0.50, 0.52)
    draw_box(dx + 0.28, mh + 0.100, dz + 0.19, 0.018, 0.018, 0.05, 0.50, 0.50, 0.52)

    set_material(0.92, 0.90, 0.86, amb_scale=0.28,
                 spec=(0.35,0.33,0.30,1.0), shininess=40.0)
    draw_cylinder(dx + 0.50, mh + 0.055, dz - 0.14, 0.052, 0.11, slices=14)
    set_material(0.18, 0.12, 0.08, amb_scale=0.20,
                 spec=(0.20,0.16,0.12,1.0), shininess=20.0)
    draw_box(dx + 0.50, mh + 0.155, dz - 0.14, 0.09, 0.008, 0.09, 0.18, 0.12, 0.08)
    set_material(0.90, 0.88, 0.84, amb_scale=0.28,
                 spec=(0.30,0.28,0.26,1.0), shininess=36.0)
    draw_box(dx + 0.57, mh + 0.10, dz - 0.14, 0.05, 0.05, 0.025, 0.90, 0.88, 0.84)


def _draw_desk_pedestal(px, dz, mh):
    md_val = 0.78
    mat_wood(0.58, 0.42, 0.21)
    draw_box(px, 0.00, dz, 0.38, mh - 0.06, md_val, 0.58, 0.42, 0.21)
    mat_wood(0.64, 0.48, 0.25)
    draw_box(px, 0.00, dz - md_val/2 + 0.01, 0.34, mh - 0.06, 0.025,
             0.64, 0.48, 0.25)
    mat_wood(0.36, 0.24, 0.11)
    draw_box(px, mh*0.50, dz - md_val/2 + 0.008, 0.32, 0.025, 0.028,
             0.36, 0.24, 0.11)
    mat_wood(0.70, 0.52, 0.28)
    draw_box(px, mh*0.70, dz - md_val/2 + 0.012, 0.30, mh*0.36, 0.018,
             0.70, 0.52, 0.28)
    draw_box(px, mh*0.24, dz - md_val/2 + 0.012, 0.30, mh*0.44, 0.018,
             0.70, 0.52, 0.28)
    mat_metal(0.70, 0.58, 0.38)
    draw_box(px, mh*0.70, dz - md_val/2, 0.09, 0.04, 0.025, 0.70, 0.58, 0.38)
    draw_box(px, mh*0.24, dz - md_val/2, 0.09, 0.04, 0.025, 0.70, 0.58, 0.38)
    mat_wood(0.62, 0.46, 0.24)
    draw_box(px, mh - 0.06, dz, 0.40, 0.04, md_val + 0.02, 0.62, 0.46, 0.24)


def _draw_laptop(lx, ly, lz):
    # ── Base / keyboard ──────────────────────────────
    mat_plastic(0.20, 0.20, 0.24)
    draw_box(lx, ly, lz, 0.70, 0.022, 0.46, 0.20, 0.20, 0.24)
    # Keyboard area (recessed darker)
    set_material(0.14, 0.14, 0.18, amb_scale=0.18,
                 spec=(0.20,0.20,0.22,1.0), shininess=28.0)
    draw_box(lx, ly + 0.014, lz - 0.02, 0.62, 0.010, 0.36, 0.14, 0.14, 0.18)
    # Touchpad
    set_material(0.24, 0.24, 0.28, amb_scale=0.20,
                 spec=(0.35,0.35,0.38,1.0), shininess=40.0)
    draw_box(lx, ly + 0.018, lz + 0.10, 0.20, 0.008, 0.14, 0.24, 0.24, 0.28)

    # ── Layar — engsel di bagian BELAKANG base ────────
    # Hinge posisi: ujung belakang base (lz - 0.23), atas base (ly + 0.022)
    hinge_y = ly + 0.022
    hinge_z = lz - 0.23

    glPushMatrix()
    glTranslatef(lx, hinge_y, hinge_z)   # pindah ke hinge
    glRotatef(100, 1, 0, 0)              # buka layar ~100° ke depan (+Z), sedikit miring ke belakang
    # Sekarang gambar layar: bawah layar di hinge (y=0), layar tegak ke atas
    mat_plastic(0.18, 0.18, 0.22)
    draw_box(0, 0.215, 0, 0.70, 0.43, 0.018, 0.18, 0.18, 0.22)
    # Layar (screen panel)
    set_material(0.08, 0.12, 0.22, amb_scale=0.12,
                 spec=(0.60,0.62,0.68,1.0), shininess=72.0)
    draw_box(0, 0.215, 0.001, 0.62, 0.37, 0.008, 0.08, 0.12, 0.22)
    # Konten layar (biru/UI)
    set_material(0.20, 0.40, 0.80, amb_scale=0.20,
                 spec=(0.50,0.55,0.65,1.0), shininess=60.0)
    draw_box(0, 0.215, 0.002, 0.40, 0.20, 0.005, 0.20, 0.40, 0.80)
    # Logo
    mat_metal(0.65, 0.65, 0.68)
    draw_box(0, 0.215, -0.010, 0.10, 0.10, 0.004, 0.65, 0.65, 0.68)
    glPopMatrix()


# ═══════════════════════════════════════════════════════
#  KURSI BELAJAR — menghadap ke jendela (sandaran ke +Z, dudukan ke -Z)
#  Posisi di depan meja, bergeser sedikit ke depan agar tidak overlap meja
# ═══════════════════════════════════════════════════════
def draw_chair():
    cx  =  1.20
    cz  = -1.30   # di depan meja (meja di z=-2.30)

    C_WOOD    = (0.44, 0.30, 0.14)
    C_WOOD_D  = (0.36, 0.24, 0.11)
    C_SEAT    = (0.60, 0.48, 0.32)
    C_SEAT_H  = (0.70, 0.58, 0.42)
    C_BACK    = (0.58, 0.46, 0.30)
    C_BACK_H  = (0.68, 0.56, 0.40)

    # ── 4 Kaki silinder ───────────────────────────────
    mat_wood(*C_WOOD_D)
    for ox, oz in [(-0.29,-0.29),(0.29,-0.29),(-0.29,0.29),(0.29,0.29)]:
        draw_cylinder(cx+ox, 0.00, cz+oz, 0.028, 0.46, slices=12)

    mat_wood(*C_WOOD_D)
    draw_box(cx, 0.20, cz, 0.56, 0.03, 0.03, *C_WOOD_D)
    draw_box(cx, 0.20, cz, 0.03, 0.03, 0.56, *C_WOOD_D)

    # ── Dudukan ───────────────────────────────────────
    mat_wood(*C_WOOD)
    draw_box(cx, 0.46, cz, 0.72, 0.07, 0.72, *C_WOOD)
    mat_fabric(*C_SEAT)
    draw_box(cx, 0.53, cz, 0.66, 0.10, 0.66, *C_SEAT)
    mat_fabric(*C_SEAT_H)
    draw_box(cx, 0.62, cz, 0.58, 0.04, 0.58, *C_SEAT_H)
    mat_fabric(*C_WOOD_D)
    draw_box(cx, 0.54, cz, 0.016, 0.11, 0.68, *C_WOOD_D)
    draw_box(cx, 0.54, cz, 0.68, 0.11, 0.016, *C_WOOD_D)

    # ── Sandaran di sisi +Z (menghadap ke -Z = arah jendela) ──
    # Sandaran di belakang orang duduk (sisi +Z dari dudukan)
    back_z = cz + 0.33
    mat_wood(*C_WOOD)
    draw_box(cx - 0.28, 0.53, back_z, 0.06, 0.76, 0.06, *C_WOOD)
    draw_box(cx + 0.28, 0.53, back_z, 0.06, 0.76, 0.06, *C_WOOD)
    mat_fabric(*C_BACK)
    draw_box(cx, 0.55, back_z, 0.64, 0.68, 0.10, *C_BACK)
    mat_fabric(*C_BACK_H)
    draw_box(cx, 0.57, back_z, 0.54, 0.60, 0.07, *C_BACK_H)
    mat_fabric(*C_WOOD_D)
    draw_box(cx, 0.58, back_z, 0.016, 0.62, 0.08, *C_WOOD_D)
    mat_wood(*C_WOOD)
    draw_box(cx, 1.22, back_z, 0.72, 0.06, 0.08, *C_WOOD)
