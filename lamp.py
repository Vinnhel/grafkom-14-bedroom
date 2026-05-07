from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cylinder, draw_cone,
                   mat_wood, mat_fabric, mat_metal, set_material,
                   mat_emissive, mat_reset_emissive)

# ═══════════════════════════════════════════════════════
#  SOFA SINGLE — menghadap ke -Z (ke jendela/meja)
#  Desain sofa club chair: kaki kayu, cushion terpisah,
#  armrest tebal, sandaran tegak
# ═══════════════════════════════════════════════════════
def draw_reading_sofa():
    sox  =  1.20   # center X
    soz  =  1.72   # center Z

    # Warna sofa — kain abu hangat
    C_FRAME  = (0.40, 0.28, 0.14)   # kayu rangka
    C_BASE   = (0.52, 0.44, 0.36)   # kain dudukan (gelap)
    C_SEAT   = (0.68, 0.58, 0.46)   # busa dudukan
    C_SEAT_H = (0.76, 0.66, 0.54)   # highlight dudukan
    C_BACK   = (0.64, 0.54, 0.42)   # sandaran
    C_BACK_H = (0.72, 0.62, 0.50)   # highlight sandaran
    C_ARM    = (0.60, 0.50, 0.40)   # armrest
    C_ARM_H  = (0.68, 0.58, 0.48)   # highlight armrest
    C_PIL    = (0.78, 0.64, 0.52)   # bantal aksesori

    # ── 4 Kaki kayu (silinder, tinggi pendek) ────────
    mat_wood(*C_FRAME)
    leg_r, leg_h = 0.040, 0.22
    for ox, oz in [(-0.42,-0.38),(0.42,-0.38),(-0.42,0.40),(0.42,0.40)]:
        draw_cylinder(sox+ox, 0, soz+oz, leg_r, leg_h, slices=12)

    # ── Rangka bawah (platform kayu tipis) ───────────
    mat_wood(*C_FRAME)
    draw_box(sox, 0.22, soz, 1.00, 0.06, 0.90, *C_FRAME)

    # ── Dudukan (seat cushion) — berlapis 3 ──────────
    # Layer 1: base kain
    mat_fabric(*C_BASE)
    draw_box(sox, 0.28, soz, 0.96, 0.08, 0.86, *C_BASE)
    # Layer 2: busa utama
    mat_fabric(*C_SEAT)
    draw_box(sox, 0.36, soz, 0.90, 0.12, 0.80, *C_SEAT)
    # Layer 3: highlight atas (cushion sedikit cembung)
    mat_fabric(*C_SEAT_H)
    draw_box(sox, 0.47, soz, 0.82, 0.04, 0.70, *C_SEAT_H)
    # Jahitan tengah dudukan (garis gelap tipis)
    mat_fabric(*C_BASE)
    draw_box(sox, 0.37, soz, 0.018, 0.14, 0.82, *C_BASE)  # jahit kiri-kanan
    draw_box(sox, 0.37, soz, 0.92, 0.14, 0.018, *C_BASE)  # jahit depan-belakang

    # ── Sandaran punggung (back cushion) — tebal & tegak ──
    back_z = soz - 0.40   # posisi sandaran (belakang dudukan)
    # Rangka sandaran
    mat_wood(*C_FRAME)
    draw_box(sox, 0.28, back_z - 0.04, 1.00, 0.76, 0.10, *C_FRAME)
    # Busa sandaran utama
    mat_fabric(*C_BACK)
    draw_box(sox, 0.30, back_z, 0.88, 0.72, 0.16, *C_BACK)
    # Highlight busa sandaran
    mat_fabric(*C_BACK_H)
    draw_box(sox, 0.32, back_z + 0.02, 0.78, 0.64, 0.10, *C_BACK_H)
    # Jahitan vertikal sandaran
    mat_fabric(*C_BASE)
    draw_box(sox, 0.34, back_z + 0.01, 0.018, 0.66, 0.12, *C_BASE)
    # Rail atas sandaran (kayu)
    mat_wood(*C_FRAME)
    draw_box(sox, 0.28 + 0.76 - 0.01, back_z - 0.04, 1.02, 0.06, 0.12, *C_FRAME)

    # ── Armrest KIRI ──────────────────────────────────
    _draw_armrest(sox - 0.48, soz, C_FRAME, C_ARM, C_ARM_H)
    # ── Armrest KANAN ─────────────────────────────────
    _draw_armrest(sox + 0.48, soz, C_FRAME, C_ARM, C_ARM_H)

    # ── Bantal aksesori (throw pillow) di sudut sofa ──
    # Bantal 1 — duduk di pojok kiri sandaran
    mat_fabric(*C_PIL)
    draw_box(sox - 0.26, 0.52, soz - 0.28, 0.34, 0.30, 0.08, *C_PIL)
    # Bantal 2 — lebih kecil, miring sedikit (simulasi dgn offset)
    set_material(0.70, 0.54, 0.44,
                 amb_scale=0.22, spec=(0.04,0.04,0.04,1.0), shininess=4.0)
    draw_box(sox + 0.24, 0.52, soz - 0.26, 0.30, 0.26, 0.08,
             0.70, 0.54, 0.44)

    # ── Selimut throw di atas armrest kanan ───────────
    mat_fabric(0.66, 0.56, 0.44)
    draw_box(sox + 0.50, 0.76, soz + 0.12, 0.06, 0.18, 0.52, 0.66, 0.56, 0.44)
    draw_box(sox + 0.42, 0.72, soz + 0.30, 0.28, 0.10, 0.28, 0.66, 0.56, 0.44)


def _draw_armrest(ax, soz, C_FRAME, C_ARM, C_ARM_H):
    """
    Satu armrest sofa club chair — arah Z sejajar dudukan.
    ax = center X armrest,  soz = center Z sofa
    """
    # Rangka kayu armrest (box persegi panjang)
    mat_wood(*C_FRAME)
    draw_box(ax, 0.28, soz - 0.05, 0.14, 0.52, 0.84, *C_FRAME)

    # Busa armrest (sedikit lebih lebar dari rangka)
    mat_fabric(*C_ARM)
    draw_box(ax, 0.30, soz - 0.04, 0.16, 0.46, 0.80, *C_ARM)

    # Top pad armrest (bantalan atas, lebih terang)
    mat_fabric(*C_ARM_H)
    draw_box(ax, 0.76, soz - 0.02, 0.18, 0.06, 0.76, *C_ARM_H)

    # Lekukan samping armrest (strip tipis lebih gelap)
    mat_fabric(*C_FRAME)
    draw_box(ax, 0.30, soz - 0.42, 0.17, 0.46, 0.03, *C_FRAME)


# ═══════════════════════════════════════════════════════
#  LAMPU GANTUNG — rice paper globe di tengah plafon
# ═══════════════════════════════════════════════════════
def draw_ceiling_lamp(lamp_on):
    lx, lz = 0.0, 0.5

    # ── Kabel dari plafon ─────────────────────────────
    mat_metal(0.30, 0.28, 0.25)
    draw_box(lx, 3.58, lz, 0.035, 0.42, 0.035, 0.30, 0.28, 0.25)

    # ── Fitting/dudukan ───────────────────────────────
    mat_metal(0.40, 0.36, 0.30)
    draw_box(lx, 3.56, lz, 0.16, 0.06, 0.16, 0.40, 0.36, 0.30)
    # Cincin fitting bawah
    mat_metal(0.35, 0.32, 0.28)
    draw_box(lx, 3.50, lz, 0.20, 0.025, 0.20, 0.35, 0.32, 0.28)

    # ── Bola lampu (rice paper globe) ────────────────
    glPushMatrix()
    glTranslatef(lx, 3.18, lz)

    if lamp_on:
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 0.94, 0.70, 0.08)
        q_halo = gluNewQuadric()
        gluSphere(q_halo, 0.62, 16, 16)
        gluDeleteQuadric(q_halo)
        glColor4f(1.0, 0.95, 0.72, 0.14)
        q_halo2 = gluNewQuadric()
        gluSphere(q_halo2, 0.50, 16, 16)
        gluDeleteQuadric(q_halo2)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

        set_material(1.0, 0.97, 0.80,
                     amb_scale=0.50,
                     spec=(0.30, 0.28, 0.22, 1.0),
                     shininess=20.0)
        glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.60, 0.55, 0.35, 1.0])
    else:
        mat_reset_emissive()
        set_material(0.80, 0.78, 0.74,
                     amb_scale=0.30,
                     spec=(0.08, 0.08, 0.07, 1.0),
                     shininess=8.0)

    q = gluNewQuadric()
    gluSphere(q, 0.38, 20, 20)
    gluDeleteQuadric(q)

    if lamp_on:
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 0.85)
        q2 = gluNewQuadric()
        gluSphere(q2, 0.06, 8, 8)
        gluDeleteQuadric(q2)
        glEnable(GL_LIGHTING)

    mat_reset_emissive()
    glPopMatrix()
