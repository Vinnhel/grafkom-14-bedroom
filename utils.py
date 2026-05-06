from OpenGL.GL import *
from OpenGL.GLU import *

def draw_box(x, y, z, w, h, d, r, g, b):
    """
    Gambar balok (cuboid).
    (x,y,z) = titik tengah alas bawah
    w=lebar(X), h=tinggi(Y), d=dalam(Z)
    r,g,b = warna 0..1
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
    """Silinder tegak, alas bawah di (x,y,z)"""
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
    """Kerucut/trapesium silinder dari bawah ke atas"""
    glPushMatrix()
    glTranslatef(x, y, z)
    glRotatef(-90, 1, 0, 0)
    q = gluNewQuadric()
    gluCylinder(q, r_bottom, r_top, height, slices, 4)
    gluDisk(q, 0, r_bottom, slices, 1)
    gluDeleteQuadric(q)
    glPopMatrix()
