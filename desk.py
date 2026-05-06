from OpenGL.GL import *
from OpenGL.GLU import *
from utils import draw_box

def draw_desk():
    """
    Meja belajar menempel dinding BELAKANG (z=-3), posisi tengah-kanan.
    Sisi panjang meja sejajar dinding belakang (lebar X > dalam Z).
    Kursi di depannya menghadap jendela (+Z ke -Z).
    """
    dx  =  1.20   # center X meja
    dz  = -2.30   # center Z meja (dekat dinding belakang)
    mw  =  1.85   # lebar meja (arah X)
    md  =  0.85   # dalam meja (arah Z)
    mh  =  0.84   # tinggi kaki

    # ── Permukaan meja (kayu terang) ─────────────────
    draw_box(dx, mh,       dz, mw,      0.06, md,      0.70, 0.51, 0.28)
    # Edge/bibir meja (strip tipis lebih gelap)
    draw_box(dx, mh-0.01,  dz, mw+0.03, 0.03, md+0.03, 0.55, 0.38, 0.18)

    # ── Kaki meja (4 kaki, kayu lebih gelap) ─────────
    offsets = [(-0.82, -0.35), (0.82, -0.35), (-0.82, 0.35), (0.82, 0.35)]
    for ox, oz in offsets:
        draw_box(dx+ox, 0, dz+oz, 0.07, mh, 0.07, 0.48, 0.33, 0.16)

    # ── Laci samping kanan ────────────────────────────
    draw_box(dx+0.76, 0.10, dz, 0.40, mh-0.10, md-0.10, 0.62, 0.45, 0.23)
    # Laci 1 (atas)
    draw_box(dx+0.74, 0.62, dz-0.37, 0.35, 0.19, 0.02, 0.72, 0.54, 0.30)
    draw_box(dx+0.74, 0.62, dz-0.36, 0.08, 0.05, 0.02, 0.68, 0.56, 0.36) # gagang
    # Laci 2 (bawah)
    draw_box(dx+0.74, 0.40, dz-0.37, 0.35, 0.19, 0.02, 0.72, 0.54, 0.30)
    draw_box(dx+0.74, 0.40, dz-0.36, 0.08, 0.05, 0.02, 0.68, 0.56, 0.36)

    # ── Laptop ────────────────────────────────────────
    # Base laptop
    draw_box(dx-0.10, mh+0.06, dz+0.05, 0.68, 0.025, 0.44, 0.22, 0.22, 0.26)
    # Layar laptop (terbuka ~110°)
    glPushMatrix()
    glTranslatef(dx-0.10, mh+0.06, dz-0.17)
    glRotatef(-115, 1, 0, 0)   # sudut buka layar
    glTranslatef(0, 0.20, 0)
    from utils import draw_box as db
    db(0, 0, 0, 0.68, 0.40, 0.025, 0.20, 0.20, 0.24)
    # Layar display (abu gelap)
    db(0, 0.01, 0, 0.60, 0.34, 0.010, 0.12, 0.14, 0.20)
    glPopMatrix()

    # ── Buku & aksesoris meja ─────────────────────────
    # Buku tegak kiri
    draw_box(dx-0.72, mh+0.06, dz-0.15, 0.08, 0.28, 0.26, 0.72, 0.28, 0.22)
    draw_box(dx-0.62, mh+0.06, dz-0.15, 0.08, 0.32, 0.26, 0.28, 0.50, 0.62)
    draw_box(dx-0.52, mh+0.06, dz-0.15, 0.08, 0.24, 0.26, 0.62, 0.52, 0.20)
    # Tempat pensil
    draw_box(dx-0.75, mh+0.06, dz+0.25, 0.10, 0.16, 0.10, 0.60, 0.46, 0.30)
    # Mouse
    draw_box(dx+0.32, mh+0.06, dz+0.25, 0.10, 0.04, 0.15, 0.30, 0.30, 0.32)
    # Mousepad
    draw_box(dx+0.28, mh+0.06, dz+0.22, 0.32, 0.010, 0.28, 0.25, 0.22, 0.20)


def draw_chair():
    """
    Kursi di depan meja belajar, menghadap ke jendela (sandaran ke arah +Z).
    """
    cx  =  1.20   # center X sama dengan meja
    cz  = -1.22   # lebih ke depan dari meja

    # ── Dudukan kursi ─────────────────────────────────
    draw_box(cx, 0.46, cz, 0.70, 0.08, 0.70, 0.55, 0.39, 0.19)
    # Bantal dudukan
    draw_box(cx, 0.54, cz, 0.62, 0.08, 0.62, 0.65, 0.52, 0.35)

    # ── Sandaran punggung ─────────────────────────────
    # Frame sandaran
    draw_box(cx, 0.54, cz-0.31, 0.70, 0.68, 0.07, 0.50, 0.35, 0.16)
    # Bantal sandaran
    draw_box(cx, 0.56, cz-0.29, 0.60, 0.58, 0.06, 0.62, 0.50, 0.32)
    # Rail atas sandaran
    draw_box(cx, 1.20, cz-0.31, 0.72, 0.06, 0.09, 0.46, 0.32, 0.14)

    # ── Kaki kursi (4 kaki + palang penyangga) ────────
    for ox, oz in [(-0.29, -0.29), (0.29, -0.29), (-0.29, 0.29), (0.29, 0.29)]:
        draw_box(cx+ox, 0, cz+oz, 0.055, 0.46, 0.055, 0.42, 0.29, 0.13)
    # Palang tengah (H-bar)
    draw_box(cx, 0.18, cz, 0.58, 0.04, 0.04, 0.40, 0.28, 0.12)  # kiri-kanan
    draw_box(cx, 0.18, cz, 0.04, 0.04, 0.58, 0.40, 0.28, 0.12)  # depan-belakang
