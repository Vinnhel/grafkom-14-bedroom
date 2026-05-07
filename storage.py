from OpenGL.GL import *
from OpenGL.GLU import *
from utils import (draw_box, draw_cylinder,
                   mat_wood, mat_metal, mat_glass, mat_paper,
                   set_material, mat_emissive, mat_reset_emissive)

# ═══════════════════════════════════════════════════════
#  LEMARI  —  dinding KANAN (x≈+3), menghadap ke KIRI (-X)
#  Lemari 2 pintu geser dengan panel cermin & rel atas
# ═══════════════════════════════════════════════════════
def draw_wardrobe():
    wx  =  2.36   # center X  (punggung menempel dinding x=+3)
    wz  = -1.55   # center Z
    wW  =  0.56   # tebal lemari (arah X)
    wD  =  2.20   # panjang (arah Z)
    wH  =  2.50   # tinggi

    # ── Badan belakang / carcass ──────────────────────
    mat_wood(0.38, 0.26, 0.12)
    draw_box(wx, 0.00, wz, wW, wH, wD, 0.38, 0.26, 0.12)

    # ── Panel samping kiri & kanan (visible dari depan) ──
    mat_wood(0.44, 0.31, 0.15)
    draw_box(wx-0.01, 0.00, wz - wD/2 + 0.03, wW+0.02, wH+0.02, 0.05,
             0.44, 0.31, 0.15)
    draw_box(wx-0.01, 0.00, wz + wD/2 - 0.03, wW+0.02, wH+0.02, 0.05,
             0.44, 0.31, 0.15)

    # ── Mahkota atas ──────────────────────────────────
    mat_wood(0.50, 0.36, 0.18)
    draw_box(wx, wH, wz, wW+0.06, 0.10, wD+0.08, 0.50, 0.36, 0.18)
    # Profil mahkota (strip tipis lebih gelap)
    mat_wood(0.34, 0.22, 0.10)
    draw_box(wx-0.24, wH-0.01, wz, 0.04, 0.06, wD+0.06, 0.34, 0.22, 0.10)

    # ── Alas / plinth ─────────────────────────────────
    mat_wood(0.36, 0.24, 0.11)
    draw_box(wx, 0.00, wz, wW+0.04, 0.08, wD+0.06, 0.36, 0.24, 0.11)

    # ══ PINTU 2 panel — digambar di muka lemari (sisi -X) ═══
    # Pintu kiri  (z lebih positif)
    _draw_wardrobe_door(wx, wz + wD*0.25, wH)
    # Pintu kanan (z lebih negatif)
    _draw_wardrobe_door(wx, wz - wD*0.25, wH)

    # ── Rel atas (strip logam panjang) ────────────────
    mat_metal(0.55, 0.52, 0.48)
    draw_box(wx-0.24, wH-0.02, wz, 0.02, 0.04, wD-0.06, 0.55, 0.52, 0.48)


def _draw_wardrobe_door(wx, dz, wH):
    """Satu panel pintu lemari lengkap dengan bingkai, cermin, gagang."""
    fw = wH * 0.88        # tinggi pintu
    fd = 1.02             # lebar pintu (arah Z)
    px = wx - 0.24        # posisi X muka pintu

    # Frame pintu utama — kayu medium
    mat_wood(0.52, 0.37, 0.18)
    draw_box(px, 0.07, dz, 0.045, fw, fd, 0.52, 0.37, 0.18)

    # Bingkai atas pintu (rail)
    mat_wood(0.46, 0.32, 0.15)
    draw_box(px+0.002, fw-0.03, dz, 0.06, 0.07, fd+0.02, 0.46, 0.32, 0.15)

    # Bingkai bawah pintu (rail)
    mat_wood(0.46, 0.32, 0.15)
    draw_box(px+0.002, 0.08, dz, 0.06, 0.07, fd+0.02, 0.46, 0.32, 0.15)

    # Bingkai kiri & kanan pintu (stile)
    mat_wood(0.46, 0.32, 0.15)
    draw_box(px+0.002, fw*0.50+0.07, dz - fd/2 + 0.04, 0.06, fw-0.10, 0.06,
             0.46, 0.32, 0.15)
    draw_box(px+0.002, fw*0.50+0.07, dz + fd/2 - 0.04, 0.06, fw-0.10, 0.06,
             0.46, 0.32, 0.15)

    # Panel cermin utama (dalam bingkai) — kaca reflektif
    mat_glass(0.72, 0.78, 0.82)
    draw_box(px+0.018, fw*0.50+0.07, dz, 0.015, fw*0.78, fd-0.14,
             0.72, 0.78, 0.82)

    # Panel kayu bawah (di bawah cermin)
    mat_wood(0.54, 0.39, 0.19)
    draw_box(px+0.010, 0.19, dz, 0.03, 0.22, fd-0.14, 0.54, 0.39, 0.19)

    # Gagang — logam silinder horizontal
    mat_metal(0.72, 0.68, 0.62)
    # Batang gagang (silinder rebah → pakai draw_box tipis panjang)
    draw_box(px-0.04, fw*0.45, dz, 0.025, 0.025, 0.18, 0.72, 0.68, 0.62)
    # Ujung gagang kiri & kanan (tombol)
    draw_box(px-0.04, fw*0.45, dz-0.09, 0.035, 0.035, 0.025, 0.65, 0.62, 0.58)
    draw_box(px-0.04, fw*0.45, dz+0.09, 0.035, 0.035, 0.025, 0.65, 0.62, 0.58)


# ═══════════════════════════════════════════════════════
#  BOOKSHELF  —  dinding KANAN (x≈+3), menghadap ke KIRI (-X)
#  Rak 4 tingkat dengan buku berdiri rapat, dekorasi atas
# ═══════════════════════════════════════════════════════
def draw_bookshelf():
    sx  =  2.35    # center X
    sz  =  0.90    # center Z
    sW  =  0.46    # tebal rak (arah X)
    sD  =  1.96    # lebar rak (arah Z)
    sH  =  1.88    # tinggi total

    # ── Dinding samping kiri & kanan rak ──────────────
    mat_wood(0.46, 0.33, 0.16)
    draw_box(sx, 0.00, sz - sD/2 + 0.025, sW, sH, 0.05, 0.46, 0.33, 0.16)
    draw_box(sx, 0.00, sz + sD/2 - 0.025, sW, sH, 0.05, 0.46, 0.33, 0.16)

    # ── Panel belakang rak ────────────────────────────
    mat_wood(0.54, 0.40, 0.20)
    draw_box(sx + sW*0.40, 0.02, sz, 0.04, sH-0.04, sD-0.06, 0.54, 0.40, 0.20)

    # ── Alas & atap rak ───────────────────────────────
    mat_wood(0.46, 0.33, 0.16)
    draw_box(sx, 0.00, sz, sW, 0.05, sD, 0.46, 0.33, 0.16)          # lantai rak
    draw_box(sx, sH-0.02, sz, sW, 0.05, sD, 0.46, 0.33, 0.16)       # atap rak

    # ── 3 sekat horizontal (membentuk 4 kompartemen) ──
    shelf_y = [0.46, 0.92, 1.38]
    mat_wood(0.50, 0.37, 0.18)
    for yy in shelf_y:
        draw_box(sx, yy, sz, sW-0.02, 0.04, sD-0.06, 0.50, 0.37, 0.18)

    # ── Kompartemen 1 (y 0.05 → 0.46): buku berdiri ──
    _draw_shelf_books(sx, sz, sD, base_y=0.05, shelf_h=0.38,
        books=[
            (0.08, 0.72, 0.28, 0.22),   # tebal, r, g, b
            (0.07, 0.28, 0.48, 0.68),
            (0.09, 0.36, 0.60, 0.34),
            (0.06, 0.80, 0.65, 0.22),
            (0.08, 0.55, 0.30, 0.60),
            (0.07, 0.65, 0.42, 0.22),
            (0.10, 0.30, 0.55, 0.48),
            (0.06, 0.70, 0.26, 0.26),
            (0.08, 0.42, 0.58, 0.32),
        ])

    # ── Kompartemen 2 (y 0.50 → 0.92): buku berdiri ──
    _draw_shelf_books(sx, sz, sD, base_y=0.51, shelf_h=0.36,
        books=[
            (0.09, 0.32, 0.52, 0.50),
            (0.07, 0.72, 0.35, 0.42),
            (0.08, 0.45, 0.56, 0.28),
            (0.06, 0.62, 0.44, 0.20),
            (0.09, 0.26, 0.38, 0.62),
            (0.07, 0.75, 0.55, 0.25),
            (0.08, 0.38, 0.28, 0.56),
        ])

    # ── Kompartemen 3 (y 0.96 → 1.38): buku + dekorasi ──
    _draw_shelf_books(sx, sz, sD, base_y=0.97, shelf_h=0.36,
        books=[
            (0.08, 0.28, 0.56, 0.45),
            (0.07, 0.68, 0.28, 0.28),
            (0.09, 0.48, 0.68, 0.30),
            (0.06, 0.72, 0.50, 0.22),
            (0.08, 0.30, 0.42, 0.60),
        ])
    # Figurine kecil di sisi kompartemen 3
    set_material(0.65, 0.55, 0.38,
                 amb_scale=0.25, spec=(0.30,0.28,0.22,1.0), shininess=28.0)
    draw_box(sx+0.02, 0.99, sz + sD/2 - 0.16, 0.08, 0.28, 0.12, 0.65, 0.55, 0.38)

    # ── Kompartemen 4 (y 1.42 → 1.88): buku + deco ───
    _draw_shelf_books(sx, sz, sD, base_y=1.43, shelf_h=0.38,
        books=[
            (0.08, 0.60, 0.36, 0.22),
            (0.07, 0.26, 0.50, 0.64),
            (0.09, 0.56, 0.28, 0.45),
            (0.07, 0.42, 0.62, 0.28),
        ])

    # ── Dekorasi ATAS rak ─────────────────────────────
    # Pot tanaman — terakota + tanaman hijau
    set_material(0.62, 0.38, 0.22,
                 amb_scale=0.25, spec=(0.18,0.14,0.10,1.0), shininess=18.0)
    draw_box(sx+0.02, sH+0.01, sz + 0.60, 0.16, 0.20, 0.16, 0.62, 0.38, 0.22)
    # Tanah dalam pot
    set_material(0.28, 0.20, 0.12,
                 amb_scale=0.20, spec=(0.02,0.02,0.02,1.0), shininess=2.0)
    draw_box(sx+0.02, sH+0.19, sz + 0.60, 0.13, 0.03, 0.13, 0.28, 0.20, 0.12)
    # Daun tanaman (3 gumpalan)
    set_material(0.28, 0.54, 0.22,
                 amb_scale=0.20, spec=(0.04,0.07,0.03,1.0), shininess=6.0)
    draw_box(sx+0.02, sH+0.26, sz + 0.60, 0.18, 0.14, 0.18, 0.28, 0.54, 0.22)
    draw_box(sx+0.02, sH+0.34, sz + 0.56, 0.12, 0.10, 0.12, 0.24, 0.50, 0.20)
    draw_box(sx+0.02, sH+0.34, sz + 0.65, 0.10, 0.08, 0.10, 0.30, 0.58, 0.24)

    # Bingkai foto — kayu tipis + kaca
    mat_wood(0.40, 0.30, 0.18)
    draw_box(sx+0.02, sH+0.02, sz + 0.22, 0.06, 0.32, 0.24, 0.40, 0.30, 0.18)
    mat_glass(0.66, 0.74, 0.80)
    draw_box(sx+0.04, sH+0.03, sz + 0.22, 0.02, 0.24, 0.17, 0.66, 0.74, 0.80)

    # Lilin putih + api emissive
    set_material(0.92, 0.90, 0.85,
                 amb_scale=0.30, spec=(0.12,0.12,0.10,1.0), shininess=8.0)
    draw_box(sx+0.02, sH+0.02, sz - 0.30, 0.08, 0.18, 0.08, 0.92, 0.90, 0.85)
    mat_emissive(1.00, 0.80, 0.28)
    draw_box(sx+0.02, sH+0.20, sz - 0.30, 0.015, 0.07, 0.015, 1.0, 0.80, 0.28)
    mat_reset_emissive()

    # Buku rebahan (stack 2) di atas rak
    mat_paper(0.68, 0.44, 0.20)
    draw_box(sx+0.02, sH+0.02, sz - 0.62, 0.28, 0.04, 0.20, 0.68, 0.44, 0.20)
    mat_paper(0.36, 0.52, 0.42)
    draw_box(sx+0.02, sH+0.06, sz - 0.62, 0.25, 0.04, 0.18, 0.36, 0.52, 0.42)


def _draw_shelf_books(sx, sz, sD, base_y, shelf_h, books):
    """
    Gambar deretan buku berdiri tegak dalam satu kompartemen rak.
    Buku ditumpuk dari Z positif ke Z negatif (kiri ke kanan dari depan).
    Setiap buku: (tebal_z, r, g, b)
    """
    # Mulai dari sisi kiri (z tinggi) masuk ke kanan (z rendah)
    cur_z = sz + sD/2 - 0.06   # mulai dari tepi kiri rak
    bh = shelf_h * 0.92         # tinggi buku ≈ 92% tinggi kompartemen
    bw = 0.28                   # lebar buku (arah X, masuk ke dalam rak)

    for (bt, r, g, b) in books:
        if cur_z - bt < sz - sD/2 + 0.06:
            break   # jangan sampai keluar rak
        bz = cur_z - bt / 2.0
        mat_paper(r, g, b)
        draw_box(sx + 0.08, base_y, bz, bw, bh, bt, r, g, b)
        # Punggung buku (sisi yang terlihat dari depan, lebih gelap sedikit)
        set_material(r*0.80, g*0.80, b*0.80,
                     amb_scale=0.25,
                     spec=(0.06,0.06,0.06,1.0),
                     shininess=6.0)
        draw_box(sx - 0.01, base_y, bz, 0.015, bh*0.96, bt*0.96,
                 r*0.80, g*0.80, b*0.80)
        cur_z -= bt + 0.008   # jarak antar buku
