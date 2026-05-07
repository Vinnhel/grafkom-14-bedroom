from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cylinder, draw_cone,
                   mat_wood, mat_fabric, mat_metal, set_material,
                   mat_emissive, mat_reset_emissive)

# ═══════════════════════════════════════════════════════
#  SOFA SINGLE — menghadap ke +X (menghadap kasur di sisi kiri)
#  Sandaran di sisi +X (jauh dari kasur), dudukan ke -X
#  Posisi: kanan-tengah ruangan
# ═══════════════════════════════════════════════════════
def draw_reading_sofa():
    # Sofa dirotasi: sandaran menghadap ke kanan (+X),
    # dudukan menghadap ke kiri (-X) → orang duduk melihat kasur
    sox  =  1.80   # center X (lebih ke kanan)
    soz  =  1.20   # center Z (tengah ruangan)

    C_FRAME  = (0.40, 0.28, 0.14)
    C_BASE   = (0.52, 0.44, 0.36)
    C_SEAT   = (0.68, 0.58, 0.46)
    C_SEAT_H = (0.76, 0.66, 0.54)
    C_BACK   = (0.64, 0.54, 0.42)
    C_BACK_H = (0.72, 0.62, 0.50)
    C_ARM    = (0.60, 0.50, 0.40)
    C_ARM_H  = (0.68, 0.58, 0.48)
    C_PIL    = (0.78, 0.64, 0.52)

    # Sandaran di sisi +X, dudukan menghadap -X
    # back_x = sox + 0.40 (sandaran di sisi kanan/+X)
    back_x = sox + 0.40

    # ── 4 Kaki kayu (silinder) ────────────────────────
    mat_wood(*C_FRAME)
    leg_r, leg_h = 0.040, 0.22
    for ox, oz in [(-0.38,-0.42),(0.38,-0.42),(-0.38,0.42),(0.38,0.42)]:
        draw_cylinder(sox+ox, 0, soz+oz, leg_r, leg_h, slices=12)

    # ── Rangka bawah ──────────────────────────────────
    mat_wood(*C_FRAME)
    draw_box(sox, 0.22, soz, 0.90, 0.06, 1.00, *C_FRAME)

    # ── Dudukan (seat cushion) ────────────────────────
    mat_fabric(*C_BASE)
    draw_box(sox, 0.28, soz, 0.84, 0.08, 0.94, *C_BASE)
    mat_fabric(*C_SEAT)
    draw_box(sox, 0.36, soz, 0.80, 0.12, 0.88, *C_SEAT)
    mat_fabric(*C_SEAT_H)
    draw_box(sox, 0.47, soz, 0.72, 0.04, 0.80, *C_SEAT_H)
    # Jahitan tengah
    mat_fabric(*C_BASE)
    draw_box(sox, 0.37, soz, 0.016, 0.14, 0.90, *C_BASE)
    draw_box(sox, 0.37, soz, 0.82, 0.14, 0.016, *C_BASE)

    # ── Sandaran punggung (di sisi +X) ───────────────
    mat_wood(*C_FRAME)
    draw_box(back_x + 0.04, 0.28, soz, 0.10, 0.76, 1.00, *C_FRAME)
    mat_fabric(*C_BACK)
    draw_box(back_x, 0.30, soz, 0.16, 0.72, 0.92, *C_BACK)
    mat_fabric(*C_BACK_H)
    draw_box(back_x - 0.02, 0.32, soz, 0.10, 0.64, 0.82, *C_BACK_H)
    # Jahitan vertikal sandaran
    mat_fabric(*C_BASE)
    draw_box(back_x - 0.01, 0.34, soz, 0.11, 0.66, 0.016, *C_BASE)
    # Rail atas sandaran
    mat_wood(*C_FRAME)
    draw_box(back_x + 0.04, 0.28 + 0.76 - 0.01, soz, 0.12, 0.06, 1.02, *C_FRAME)

    # ── Armrest depan (-Z) dan belakang (+Z) ─────────
    _draw_armrest_hz(sox, soz - 0.50, C_FRAME, C_ARM, C_ARM_H)
    _draw_armrest_hz(sox, soz + 0.50, C_FRAME, C_ARM, C_ARM_H)

    # ── Bantal aksesori ───────────────────────────────
    mat_fabric(*C_PIL)
    draw_box(back_x - 0.04, 0.52, soz - 0.26, 0.10, 0.30, 0.34, *C_PIL)
    set_material(0.70, 0.54, 0.44,
                 amb_scale=0.22, spec=(0.04,0.04,0.04,1.0), shininess=4.0)
    draw_box(back_x - 0.04, 0.52, soz + 0.24, 0.10, 0.26, 0.30,
             0.70, 0.54, 0.44)

    # ── Selimut di armrest depan ───────────────────────
    mat_fabric(0.66, 0.56, 0.44)
    draw_box(sox - 0.10, 0.76, soz - 0.52, 0.55, 0.10, 0.06, 0.66, 0.56, 0.44)
    draw_box(sox - 0.20, 0.72, soz - 0.44, 0.30, 0.08, 0.24, 0.66, 0.56, 0.44)


def _draw_armrest_hz(sox, az, C_FRAME, C_ARM, C_ARM_H):
    """Armrest horizontal (sejajar Z), membentang di sisi depan/belakang sofa."""
    mat_wood(*C_FRAME)
    draw_box(sox, 0.28, az, 0.88, 0.52, 0.14, *C_FRAME)
    mat_fabric(*C_ARM)
    draw_box(sox, 0.30, az, 0.86, 0.46, 0.16, *C_ARM)
    mat_fabric(*C_ARM_H)
    draw_box(sox, 0.76, az, 0.84, 0.06, 0.18, *C_ARM_H)
    # Lekukan sisi luar
    mat_fabric(*C_FRAME)
    draw_box(sox, 0.30, az + (0.08 if az > 0 else -0.08), 0.87, 0.46, 0.03, *C_FRAME)


# ═══════════════════════════════════════════════════════
#  LAMPU GANTUNG — bohlam selalu terlihat
# ═══════════════════════════════════════════════════════
def draw_ceiling_lamp(lamp_on):
    lx, lz = 0.0, 0.5

    # ── Kabel dari plafon ─────────────────────────────
    mat_metal(0.30, 0.28, 0.25)
    draw_box(lx, 3.58, lz, 0.035, 0.42, 0.035, 0.30, 0.28, 0.25)

    # ── Fitting/dudukan ───────────────────────────────
    mat_metal(0.40, 0.36, 0.30)
    draw_box(lx, 3.56, lz, 0.16, 0.06, 0.16, 0.40, 0.36, 0.30)
    mat_metal(0.35, 0.32, 0.28)
    draw_box(lx, 3.50, lz, 0.20, 0.025, 0.20, 0.35, 0.32, 0.28)

    glPushMatrix()
    glTranslatef(lx, 3.18, lz)

    # ── Halo cahaya saat lampuOn (digambar SEBELUM sphere) ──
    if lamp_on:
        glDisable(GL_LIGHTING)
        glEnable(GL_BLEND)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glColor4f(1.0, 0.94, 0.70, 0.07)
        qh = gluNewQuadric()
        gluSphere(qh, 0.68, 16, 16)
        gluDeleteQuadric(qh)
        glColor4f(1.0, 0.95, 0.72, 0.12)
        qh2 = gluNewQuadric()
        gluSphere(qh2, 0.52, 16, 16)
        gluDeleteQuadric(qh2)
        glDisable(GL_BLEND)
        glEnable(GL_LIGHTING)

    # ── Globe bola lampu — SELALU digambar ───────────
    # Bedanya: saat ON → emissive/terang, saat OFF → kain putih redup
    if lamp_on:
        # Matikan lighting sementara agar warna emissive tidak terpengaruh
        # shading gelap dari lighting engine
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 0.97, 0.82)
        q = gluNewQuadric()
        gluSphere(q, 0.38, 20, 20)
        gluDeleteQuadric(q)
        # Titik bohlam inti (lebih putih)
        glColor3f(1.0, 1.0, 0.95)
        q2 = gluNewQuadric()
        gluSphere(q2, 0.08, 12, 12)
        gluDeleteQuadric(q2)
        glEnable(GL_LIGHTING)
    else:
        # Lampu mati: globe terlihat sebagai objek kain biasa
        mat_reset_emissive()
        set_material(0.80, 0.78, 0.74,
                     amb_scale=0.35,
                     spec=(0.08, 0.08, 0.07, 1.0),
                     shininess=8.0)
        q = gluNewQuadric()
        gluSphere(q, 0.38, 20, 20)
        gluDeleteQuadric(q)

    mat_reset_emissive()
    glPopMatrix()
