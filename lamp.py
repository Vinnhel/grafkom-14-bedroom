from OpenGL.GL import *
from OpenGL.GLU import *
from utils import draw_box, draw_cylinder

def draw_reading_sofa():
    """
    Sofa single untuk membaca — tengah bawah denah (di depan bookshelf).
    Menghadap ke arah -Z (ke jendela/meja).
    """
    sox  =  1.20   # center X (sejajar bookshelf)
    soz  =  1.72   # center Z

    # ── Kaki sofa (4 kaki kayu pendek) ───────────────
    for ox, oz in [(-0.40,-0.40),(0.40,-0.40),(-0.40,0.40),(0.40,0.40)]:
        draw_box(sox+ox, 0, soz+oz, 0.09, 0.20, 0.09, 0.38, 0.26, 0.12)

    # ── Dudukan sofa ──────────────────────────────────
    # Base dudukan
    draw_box(sox, 0.20, soz, 1.05, 0.10, 0.92, 0.56, 0.40, 0.26)
    # Busa dudukan (sedikit lebih terang)
    draw_box(sox, 0.30, soz, 1.00, 0.18, 0.86, 0.64, 0.48, 0.32)
    # Lipatan tengah dudukan
    draw_box(sox, 0.30, soz, 0.04, 0.19, 0.88, 0.52, 0.37, 0.23)

    # ── Sandaran belakang ─────────────────────────────
    # Frame sandaran
    draw_box(sox, 0.20, soz-0.40, 1.05, 0.72, 0.12, 0.54, 0.38, 0.24)
    # Busa sandaran
    draw_box(sox, 0.22, soz-0.36, 0.96, 0.62, 0.09, 0.62, 0.47, 0.32)
    # Lipatan tengah sandaran
    draw_box(sox, 0.22, soz-0.35, 0.04, 0.63, 0.10, 0.52, 0.38, 0.24)
    # Rail atas sandaran
    draw_box(sox, 0.88, soz-0.40, 1.07, 0.07, 0.14, 0.50, 0.36, 0.22)

    # ── Sandaran tangan kiri ──────────────────────────
    draw_box(sox-0.46, 0.20, soz-0.05, 0.12, 0.48, 0.84, 0.54, 0.38, 0.24)
    # Busa armrest kiri
    draw_box(sox-0.46, 0.62, soz-0.05, 0.14, 0.08, 0.80, 0.62, 0.47, 0.32)

    # ── Sandaran tangan kanan ─────────────────────────
    draw_box(sox+0.46, 0.20, soz-0.05, 0.12, 0.48, 0.84, 0.54, 0.38, 0.24)
    draw_box(sox+0.46, 0.62, soz-0.05, 0.14, 0.08, 0.80, 0.62, 0.47, 0.32)

    # ── Bantal sofa ───────────────────────────────────
    # Bantal sandaran kiri
    draw_box(sox-0.24, 0.38, soz-0.32, 0.44, 0.38, 0.10, 0.78, 0.64, 0.52)
    # Bantal sandaran kanan
    draw_box(sox+0.24, 0.38, soz-0.32, 0.44, 0.38, 0.10, 0.72, 0.58, 0.48)
    # Bantal duduk dekoratif
    draw_box(sox, 0.52, soz+0.15, 0.40, 0.16, 0.40, 0.80, 0.68, 0.55)

    # ── Selimut/throw blanket di sofa ─────────────────
    draw_box(sox-0.20, 0.50, soz+0.28, 0.55, 0.08, 0.52, 0.72, 0.60, 0.44)


def draw_ceiling_lamp(lamp_on):
    """
    Lampu gantung bulat di tengah plafon — gaya rice paper lamp (foto inspo 1).
    lamp_on: bool (True=nyala, False=mati)
    """
    lx, lz = 0.0, 0.5   # posisi X,Z lampu

    # ── Kabel/tali dari plafon ────────────────────────
    draw_box(lx, 3.58, lz, 0.035, 0.42, 0.035, 0.30, 0.28, 0.25)

    # ── Fitting/dudukan lampu ─────────────────────────
    draw_box(lx, 3.56, lz, 0.14, 0.05, 0.14, 0.35, 0.32, 0.28)

    # ── Bola lampu (rice paper globe) ────────────────
    glPushMatrix()
    glTranslatef(lx, 3.18, lz)

    if lamp_on:
        # Halo luar (blur glow effect — sphere besar transparan)
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
        # Bola utama (kuning hangat)
        glColor3f(1.0, 0.97, 0.80)
    else:
        glColor3f(0.80, 0.78, 0.74)

    q = gluNewQuadric()
    gluSphere(q, 0.38, 20, 20)
    gluDeleteQuadric(q)

    # ── Titik bohlam dalam (hanya saat nyala) ─────────
    if lamp_on:
        glDisable(GL_LIGHTING)
        glColor3f(1.0, 1.0, 0.85)
        q2 = gluNewQuadric()
        gluSphere(q2, 0.06, 8, 8)
        gluDeleteQuadric(q2)
        glEnable(GL_LIGHTING)

    glPopMatrix()
