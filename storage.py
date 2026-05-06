from OpenGL.GL import *
from OpenGL.GLU import *
from utils import draw_box

# ═══════════════════════════════════════════════════════
#  LEMARI  — dinding KANAN (x≈+3), sisi panjang sejajar dinding (arah Z)
#  Posisi: bagian atas denah (z negatif)
#  Punggung lemari menempel x=+3, menghadap ke kiri (-X)
# ═══════════════════════════════════════════════════════
def draw_wardrobe():
    wx   =  2.35   # center X (dekat dinding kanan x=+3)
    wz   = -1.55   # center Z
    wW   =  0.58   # tebal lemari (arah X) — tipis karena menyamping
    wD   =  2.20   # panjang lemari (arah Z) — panjang sejajar dinding
    wH   =  2.50   # tinggi lemari

    # ── Badan utama ───────────────────────────────────
    draw_box(wx, 0.04, wz, wW, wH, wD, 0.46, 0.33, 0.17)

    # ── Mahkota atas ──────────────────────────────────
    draw_box(wx, wH+0.04, wz, wW+0.06, 0.09, wD+0.06, 0.52, 0.38, 0.20)

    # ── Alas bawah ────────────────────────────────────
    draw_box(wx, 0.04, wz, wW+0.04, 0.06, wD+0.04, 0.50, 0.36, 0.18)

    # ── 2 pintu (terbagi secara Z) ────────────────────
    # Pintu depan kiri (z lebih positif)
    draw_box(wx-0.01, 0.08, wz+0.52, wW-0.08, wH-0.08, 1.00, 0.56, 0.42, 0.23)
    # Pintu depan kanan (z lebih negatif)
    draw_box(wx-0.01, 0.08, wz-0.52, wW-0.08, wH-0.08, 1.00, 0.56, 0.42, 0.23)

    # ── Garis belah pintu (strip tengah vertikal) ─────
    draw_box(wx-0.01, 0.08, wz, 0.05, wH-0.06, 0.05, 0.44, 0.31, 0.15)

    # ── Gagang pintu ──────────────────────────────────
    # Gagang kiri
    draw_box(wx-0.25, 1.20, wz+0.15, 0.04, 0.22, 0.04, 0.70, 0.60, 0.38)
    # Gagang kanan
    draw_box(wx-0.25, 1.20, wz-0.15, 0.04, 0.22, 0.04, 0.70, 0.60, 0.38)

    # ── Panel dekoratif cermin/deco di tiap pintu ─────
    draw_box(wx-0.02, 0.55, wz+0.52, 0.03, wH*0.55, 0.75, 0.62, 0.50, 0.30)
    draw_box(wx-0.02, 0.55, wz-0.52, 0.03, wH*0.55, 0.75, 0.62, 0.50, 0.30)


# ═══════════════════════════════════════════════════════
#  BOOKSHELF  — dinding KANAN (x≈+3), di bawah lemari (z lebih positif)
#  Punggung menempel dinding kanan, menghadap ke kiri (-X)
# ═══════════════════════════════════════════════════════
def draw_bookshelf():
    sx   =  2.35   # center X
    sz   =  0.90   # center Z
    sW   =  0.50   # tebal (arah X)
    sD   =  2.00   # panjang (arah Z) — panjang sejajar dinding
    sH   =  1.90   # tinggi

    # ── Badan rak ─────────────────────────────────────
    draw_box(sx, 0.04, sz, sW, sH, sD, 0.50, 0.37, 0.19)

    # ── Panel dinding belakang (dalam rak, lebih terang) ──
    draw_box(sx+0.20, 0.04, sz, 0.03, sH-0.06, sD-0.06, 0.58, 0.45, 0.25)

    # ── Rak (3 sekat horizontal) ──────────────────────
    for yy in [0.60, 1.10, 1.55]:
        draw_box(sx, yy, sz, sW-0.06, 0.05, sD-0.06, 0.60, 0.46, 0.24)

    # ── BUKU BARIS 1 (paling bawah, z=0..sz+0.9) ─────
    books1 = [
        (0.72, 0.28, 0.22),  # merah
        (0.28, 0.48, 0.65),  # biru
        (0.36, 0.58, 0.34),  # hijau
        (0.78, 0.65, 0.22),  # kuning
        (0.55, 0.32, 0.58),  # ungu
        (0.65, 0.42, 0.22),  # coklat
    ]
    for i, (r,g,b) in enumerate(books1):
        bz = sz - 0.82 + i * 0.27
        bh = 0.42 + (i % 3) * 0.06
        draw_box(sx+0.02, 0.08, bz, 0.34, bh, 0.22, r, g, b)

    # ── BUKU BARIS 2 ──────────────────────────────────
    books2 = [
        (0.32, 0.52, 0.48),
        (0.72, 0.35, 0.42),
        (0.45, 0.55, 0.28),
        (0.60, 0.44, 0.20),
        (0.28, 0.38, 0.60),
    ]
    for i, (r,g,b) in enumerate(books2):
        bz = sz - 0.72 + i * 0.30
        bh = 0.38 + (i % 2) * 0.08
        draw_box(sx+0.02, 0.64, bz, 0.34, bh, 0.22, r, g, b)

    # ── BUKU BARIS 3 ──────────────────────────────────
    books3 = [
        (0.75, 0.55, 0.22),
        (0.35, 0.28, 0.55),
        (0.28, 0.55, 0.45),
        (0.68, 0.28, 0.28),
    ]
    for i, (r,g,b) in enumerate(books3):
        bz = sz - 0.52 + i * 0.32
        bh = 0.30 + (i % 2) * 0.10
        draw_box(sx+0.02, 1.14, bz, 0.34, bh, 0.22, r, g, b)

    # ── Dekorasi atas rak ─────────────────────────────
    # Pot tanaman kecil
    draw_box(sx+0.02, 1.94, sz+0.72, 0.14, 0.18, 0.14, 0.52, 0.36, 0.24)
    draw_box(sx+0.02, 2.12, sz+0.72, 0.10, 0.14, 0.10, 0.28, 0.52, 0.24)
    # Bingkai foto kecil
    draw_box(sx+0.02, 1.94, sz+0.35, 0.06, 0.28, 0.22, 0.42, 0.32, 0.20)
    draw_box(sx+0.04, 1.96, sz+0.35, 0.02, 0.22, 0.16, 0.65, 0.72, 0.78)
    # Lilin kecil
    draw_box(sx+0.02, 1.94, sz-0.20, 0.07, 0.16, 0.07, 0.92, 0.88, 0.82)
    draw_box(sx+0.02, 2.10, sz-0.20, 0.02, 0.06, 0.02, 0.95, 0.80, 0.30)  # api
