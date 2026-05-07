from OpenGL.GL import *
from OpenGL.GLU import *

# ═══════════════════════════════════════════════════════
#  HELPER MATERIAL — Phong Shading via glMaterialfv()
# ═══════════════════════════════════════════════════════
def set_material(r, g, b,
                 amb_scale=0.30,
                 spec=(0.15, 0.15, 0.15, 1.0),
                 shininess=16.0):
    """
    Terapkan properti material Phong untuk objek berikutnya.
      r, g, b    : warna diffuse (0..1)
      amb_scale  : faktor skala ambient relatif terhadap diffuse
      spec       : tuple RGBA specular
      shininess  : koefisien kilap (0..128)
    glColorMaterial(GL_AMBIENT_AND_DIFFUSE) sudah aktif dari setup_lighting(),
    sehingga glColor3f() juga mengatur diffuse & ambient sekaligus.
    Kita tetap set glMaterialfv() secara eksplisit agar specular & shininess
    berbeda per jenis material.
    """
    ambient  = [r * amb_scale, g * amb_scale, b * amb_scale, 1.0]
    diffuse  = [r, g, b, 1.0]
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT,   ambient)
    glMaterialfv(GL_FRONT_AND_BACK, GL_DIFFUSE,   diffuse)
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR,  list(spec))
    glMaterialf (GL_FRONT_AND_BACK, GL_SHININESS, shininess)
    glColor3f(r, g, b)


# ── Preset material berdasarkan jenis permukaan ───────
def mat_wood(r, g, b):
    """Kayu: specular rendah, sedikit kilap."""
    set_material(r, g, b,
                 amb_scale=0.25,
                 spec=(0.10, 0.08, 0.05, 1.0),
                 shininess=12.0)

def mat_fabric(r, g, b):
    """Kain/busa: hampir tidak ada specular."""
    set_material(r, g, b,
                 amb_scale=0.20,
                 spec=(0.04, 0.04, 0.04, 1.0),
                 shininess=4.0)

def mat_glass(r, g, b):
    """Kaca/cermin: specular tinggi, sangat mengkilap."""
    set_material(r, g, b,
                 amb_scale=0.15,
                 spec=(0.80, 0.85, 0.90, 1.0),
                 shininess=96.0)

def mat_metal(r, g, b):
    """Logam/gagang: specular sedang-tinggi."""
    set_material(r, g, b,
                 amb_scale=0.20,
                 spec=(0.50, 0.48, 0.44, 1.0),
                 shininess=48.0)

def mat_wall(r, g, b):
    """Dinding/plafon: cat matte, hampir tidak ada specular."""
    set_material(r, g, b,
                 amb_scale=0.35,
                 spec=(0.03, 0.03, 0.03, 1.0),
                 shininess=4.0)

def mat_plastic(r, g, b):
    """Plastik: specular sedang."""
    set_material(r, g, b,
                 amb_scale=0.25,
                 spec=(0.25, 0.25, 0.25, 1.0),
                 shininess=32.0)

def mat_paper(r, g, b):
    """Kertas/buku: matte."""
    set_material(r, g, b,
                 amb_scale=0.30,
                 spec=(0.05, 0.05, 0.05, 1.0),
                 shininess=6.0)

def mat_emissive(r, g, b):
    """Bohlam/sumber cahaya: emissive terang."""
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [r, g, b, 1.0])
    glColor3f(r, g, b)

def mat_reset_emissive():
    """Reset emissive ke nol setelah menggambar bohlam."""
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])


# ═══════════════════════════════════════════════════════
#  PRIMITIF GEOMETRI
# ═══════════════════════════════════════════════════════
def draw_box(x, y, z, w, h, d, r, g, b):
    """
    Gambar balok (cuboid) dengan warna & normal.
    (x,y,z) = titik tengah alas bawah
    w=lebar(X), h=tinggi(Y), d=dalam(Z)
    r,g,b  = warna 0..1  (material diterapkan oleh pemanggil jika perlu;
             fungsi ini hanya set glColor3f untuk kompatibilitas backward)
    """
    glPushMatrix()
    glTranslatef(x, y + h * 0.5, z)
    glScalef(w, h, d)
    glColor3f(r, g, b)
    glBegin(GL_QUADS)
    # Atas
    glNormal3f( 0, 1, 0)
    glVertex3f(-0.5, 0.5,-0.5); glVertex3f( 0.5, 0.5,-0.5)
    glVertex3f( 0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5)
    # Bawah
    glNormal3f( 0,-1, 0)
    glVertex3f(-0.5,-0.5, 0.5); glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5,-0.5)
    # Depan (+Z)
    glNormal3f( 0, 0, 1)
    glVertex3f(-0.5,-0.5, 0.5); glVertex3f( 0.5,-0.5, 0.5)
    glVertex3f( 0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5, 0.5)
    # Belakang (-Z)
    glNormal3f( 0, 0,-1)
    glVertex3f( 0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5,-0.5)
    glVertex3f(-0.5, 0.5,-0.5); glVertex3f( 0.5, 0.5,-0.5)
    # Kiri (-X)
    glNormal3f(-1, 0, 0)
    glVertex3f(-0.5,-0.5,-0.5); glVertex3f(-0.5,-0.5, 0.5)
    glVertex3f(-0.5, 0.5, 0.5); glVertex3f(-0.5, 0.5,-0.5)
    # Kanan (+X)
    glNormal3f( 1, 0, 0)
    glVertex3f( 0.5,-0.5, 0.5); glVertex3f( 0.5,-0.5,-0.5)
    glVertex3f( 0.5, 0.5,-0.5); glVertex3f( 0.5, 0.5, 0.5)
    glEnd()
    glPopMatrix()


def draw_cylinder(x, y, z, radius, height, slices=12):
    """Silinder tegak, alas bawah di (x,y,z)."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    q = gluNewQuadric()
    gluCylinder(q, radius, radius, height, slices, 4)
    gluDisk(q, 0, radius, slices, 1)           # tutup bawah
    glTranslatef(0, 0, height)
    gluDisk(q, 0, radius, slices, 1)           # tutup atas
    gluDeleteQuadric(q)
    glPopMatrix()


def draw_cone(x, y, z, r_bottom, r_top, height, slices=12):
    """Kerucut/trapesium silinder dari bawah ke atas."""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    q = gluNewQuadric()
    gluCylinder(q, r_bottom, r_top, height, slices, 4)
    gluDisk(q, 0, r_bottom, slices, 1)
    gluDeleteQuadric(q)
    glPopMatrix()
