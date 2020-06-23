import os
import sys
import json
import math
import consts
import matplotlib.pyplot as plt
import pylab
import numpy as np #библиотека 
from numpy.linalg import inv
from mpl_toolkits.mplot3d import Axes3D

class Vector3D:
    def __init__(self):
        self.vec = np.array([0, 0, 0], float)   

    def set_val(self, x, y, z):
        self.vec[0] = x
        self.vec[1] = y
        self.vec[2] = z

class Vector:
    def __init__(self):
        self.vec = [0, 0, 0, 0, 0, 0]   

    def set_val(self, x, y, z, vx, vy, vz, p, vp):
        self.vec[0] = x
        self.vec[1] = y
        self.vec[2] = z
        self.vec[3] = vx
        self.vec[4] = vy
        self.vec[5] = vz

#------------------Функции-------------------------
def save(name='', fmt='png'): #функция plot для сохранения png графиков
    pwd = os.getcwd()
    iPath = './pictures/{}'.format(fmt)
    if not os.path.exists(iPath):
        os.mkdir(iPath)
    os.chdir(iPath)
    plt.savefig('{}.{}'.format(name, fmt), fmt='png')
    os.chdir(pwd)

def Module3D(vec):
  return math.sqrt(vec[0]**2 + vec[1]**2 + vec[2]**2)

def F(r_j2000, t, a_sun, a_grav):
    res = Vector()
    res.vec[0] = r_j2000[3]
    res.vec[1] = r_j2000[4]
    res.vec[2] = r_j2000[5]
    res.vec[3] = -consts.Mukm / Module3D(r_j2000)**3 * r_j2000[0] + a_grav[0] + a_sun[0]
    res.vec[4] = -consts.Mukm / Module3D(r_j2000)**3 * r_j2000[1] + a_grav[1] + a_sun[1]
    res.vec[5] = -consts.Mukm / Module3D(r_j2000)**3 * r_j2000[2] + a_grav[2] + a_sun[2]
    return res.vec

def Fquart(quart, omegap):
    res = np.array([0, 0, 0, 0], float)
    res[0] = 0.5 * (omegap[0]*quart[0] - omegap[1]*quart[1] - omegap[2]*quart[2] - omegap[3]*quart[3])
    res[1] = 0.5 * (omegap[0]*quart[1] + omegap[1]*quart[0] + omegap[3]*quart[2] - omegap[2]*quart[3])
    res[2] = 0.5 * (omegap[0]*quart[2] + omegap[2]*quart[0] + omegap[1]*quart[3] - omegap[3]*quart[2])
    res[3] = 0.5 * (omegap[0]*quart[3] + omegap[3]*quart[0] + omegap[2]*quart[1] - omegap[2]*quart[3])  
    return res 

def Ksi1(quart_sop, Ro0_j2000):
    res = np.array([0, 0, 0, 0], float)
    res[0] = Ro0_j2000[0]*quart_sop[0] - Ro0_j2000[1]*quart_sop[1] - Ro0_j2000[2]*quart_sop[2] - Ro0_j2000[3]*quart_sop[3]
    res[1] = Ro0_j2000[0]*quart_sop[1] + Ro0_j2000[1]*quart_sop[0] + Ro0_j2000[3]*quart_sop[2] - Ro0_j2000[2]*quart_sop[3]
    res[2] = Ro0_j2000[0]*quart_sop[2] + Ro0_j2000[2]*quart_sop[0] + Ro0_j2000[1]*quart_sop[3] - Ro0_j2000[3]*quart_sop[1]
    res[3] = Ro0_j2000[0]*quart_sop[3] + Ro0_j2000[3]*quart_sop[0] + Ro0_j2000[2]*quart_sop[1] - Ro0_j2000[1]*quart_sop[2]
    return res

def Ksi(Ksi1, quart):
    res = np.array([0, 0, 0, 0], float)
    Ksi1[0] = 0
    res[0] = quart[0]*Ksi1[0] - quart[1]*Ksi1[1] - quart[2]*Ksi1[2] - quart[3]*Ksi1[3]
    res[1] = quart[0]*Ksi1[1] + quart[1]*Ksi1[0] + quart[3]*Ksi1[2] - quart[2]*Ksi1[3]
    res[2] = quart[0]*Ksi1[2] + quart[2]*Ksi1[0] + quart[1]*Ksi1[3] - quart[3]*Ksi1[1]
    res[3] = quart[0]*Ksi1[3] + quart[3]*Ksi1[0] + quart[2]*Ksi1[1] - quart[1]*Ksi1[2]
    return res

def VxV(a, b):
    res = np.array([0, 0, 0], float)
    res[0] = a[1]*b[2] - a[2]*b[1]
    res[1] = a[2]*b[0] - a[0]*b[2]
    res[2] = a[0]*b[1] - a[1]*b[0]
    return res

def JK(Jmatr, Ksi):
    c = np.array([0, 0, 0], float)
    c[0] = Jmatr[0][0] * Ksi[1] + Jmatr[0][1] * Ksi[2] + Jmatr[0][2] * Ksi[2]
    c[1] = Jmatr[1][0] * Ksi[1] + Jmatr[1][1] * Ksi[2] + Jmatr[1][2] * Ksi[2]
    c[2] = Jmatr[2][0] * Ksi[1] + Jmatr[2][1] * Ksi[2] + Jmatr[2][2] * Ksi[2]
    return c

def KJ(Ksi, JK):
    res = np.array([0, 0, 0], float)
    res[0] = Ksi[1]*JK[2] - Ksi[2]*JK[1]
    res[1] = Ksi[2]*JK[0] - Ksi[0]*JK[2]
    res[2] = Ksi[0]*JK[1] - Ksi[1]*JK[1]
    return res

def sign(r):
    if r > 0:
        return 1
    elif r == 0:
        return 0
    else:
        return -1

def FOMEGA(OMEGA, sigma, Idm):
    res = np.array([0, 0, 0], float)
    res = -pow(Idm, -1) * sigma
    return res

def Fomegap(omegap, sigma, Msumm, OMEGA, Jmatr_1, Idm, Jmatr):
    res = np.array([0, 0, 0], float)
    res = np.dot(Jmatr_1, (Msumm - (VxV(omegap, (np.dot(Jmatr, omegap) + np.dot(Idm, OMEGA)))) + sigma))
    return res

#===============================Рассчетная часть===========================
    #Начальные параметры

var_l = json.loads(sys.argv[1]) # JSON values from API
# vx = 0.593397
# vy = 5.793711
# vz = 4.948645
# x = 4226.800251 
# y = 3085.944251
# z = -4321.376266
vx = float(var_l['vx'])
vy = float(var_l['vy'])
vz = float(var_l['vz'])
x = float(var_l['x']) 
y = float(var_l['y'])
z = float(var_l['z'])
#-----------
quart = np.array([0.632866, -0.1826981, 0.3653963, -0.657713], float) #p,x,y,z
omegap = np.array([0.0, 0.00005, 0.000006, -0.00005], float) #p,x,y,z
#Тензор инерции
Jx = 0.1
Jy = 0.3
Jz = 0.5
#-------------
OmegaMAX = 628
LMAX = 0.008
Idm = 1.6e-4
Kp = 0.005
Kd = 0.3
O = 0
OMEGA = np.array([0, 0, 0], float) #x, y, z
# t = 0.0 #начальное время
# dt = 0.1 #шаг
# tend = 2000 #время интегрирования
t = float(var_l['tstart'])
dt = float(var_l['dt'])
tend = float(var_l['tend'])

Jmatr = np.array([[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]], float)
Jmatr = np.array([[0, 0, 0],
                [0, 0, 0],
                [0, 0, 0]], float)

f = open("result.txt", "w")

r_j2000 = np.array([x, y, z], float)
r_j2000_f = Vector()
r_j2000_f.vec = np.array([x, y, z, vx, vy, vz], float)
k1 = k2 = k3 = k4 = Vector()

Jmatr[0][0] = Jx
Jmatr[1][1] = Jy
Jmatr[2][2] = Jz

Jmatr_1 = inv(Jmatr) #Обратная к Jmatr

#============================Массивы точек для графиков================
r_j2000_x = np.array([], float)
r_j2000_y = np.array([], float)
r_j2000_z = np.array([], float)
OmegA_x = np.array([], float)
OmegA_y = np.array([], float)
OmegA_z = np.array([], float)
omegap_x = np.array([], float)
omegap_y = np.array([], float)
omegap_z = np.array([], float)


t_going = np.array([]) # массив времени
#=================================================================

while t <= tend:

    # расчет ускорения за счет влияния несферичности гравполя
    JD = 2458773.4446875
    _t = (JD - consts.JD0) / consts.JDD
    _f = 86400 * JD % 1.0
    alpha = consts.DS2R * ((consts.A + (consts.B + (consts.C + consts.D * _t)*_t)*_t) + _f)
    M_Grin = np.array([[np.cos((alpha)) , np.sin((alpha)), 0],
                        [-np.sin((alpha)), np.cos((alpha)), 0],
                        [0, 0, 1]], float)
    r_Grin = np.dot(r_j2000, M_Grin) * 1000

    M_GrinT = M_Grin.transpose()

    # aj2 = Vector()
    aj2 = np.array([0, 0, 0], float)
    
    aj2[0] = -1.5 * consts.J2 * (consts.Mum / Module3D(r_Grin)**2) * (consts.Re / Module3D(r_Grin))**2 * ((1 - 5 * (r_Grin[2] / Module3D(r_Grin))**2) * (r_Grin[0] / Module3D(r_Grin)))
    aj2[1] = -1.5 * consts.J2 * (consts.Mum / Module3D(r_Grin)**2) * (consts.Re / Module3D(r_Grin))**2 * ((1 - 5 * (r_Grin[2] / Module3D(r_Grin))**2) * (r_Grin[1] / Module3D(r_Grin)))
    aj2[2] = -1.5 * consts.J2 * (consts.Mum / Module3D(r_Grin)**2) * (consts.Re / Module3D(r_Grin))**2 * ((3 - 5 * (r_Grin[2] / Module3D(r_Grin))**2) * (r_Grin[2] / Module3D(r_Grin)))
    
    a_grav = Vector()
    a_grav.vec = np.dot(aj2, M_GrinT) * 1000

    # Ускорение засчет граввлияния Солнца
    Modif_JD = (JD - 2451545) / 36525
    MidAnom = 357.5226 + 35999.049 * Modif_JD
    lambda0 = consts.Om_om + MidAnom + (6892 / 60 / 60)*np.sin(np.radians(MidAnom)) + (72 / 60 / 60)*np.sin(np.radians(2 * MidAnom))
    Mod_r0 = (149.619 - 2.499*np.cos(np.radians(MidAnom)) - 0.021*np.cos(np.radians(2 * MidAnom)))*pow(10, 6)

    r_sun = Vector3D()

    r_sun.vec[0] = Mod_r0*np.cos(np.radians(lambda0))
    r_sun.vec[1] = Mod_r0*np.sin(np.radians(lambda0))*np.cos(np.radians(consts.Ekl))
    r_sun.vec[2] = Mod_r0*np.sin(np.radians(lambda0))*np.sin(np.radians(consts.Ekl))

    a_sun = Vector3D()
    a_sun.vec = consts.Mu_sun * ((r_Grin - r_j2000) / Module3D(r_sun.vec - r_j2000)**3 - r_sun.vec / Module3D(r_sun.vec)**3)
    
    #rj2000
    k1 = np.dot(F(r_j2000_f.vec, t, a_sun.vec, a_grav.vec), dt)
    k2 = np.dot(F(r_j2000_f.vec + 0.5 * k1, t + 0.5 * dt, a_sun.vec, a_grav.vec), dt)
    k3 = np.dot(F(r_j2000_f.vec + 0.5 * k2, t + 0.5 * dt, a_sun.vec, a_grav.vec), dt)
    k4 = np.dot(F(r_j2000_f.vec + k3, t + dt, a_sun.vec, a_grav.vec), dt)
    r_j2000_f.vec = r_j2000_f.vec + np.dot(6, np.add.reduce([k1, np.dot(2, k2), np.dot(2, k3), k4]))**(-1)
    r_j2000 = np.array([r_j2000_f.vec[0], r_j2000_f.vec[1], r_j2000_f.vec[2]]) #связь между полным и 3комп веторами

    #Кватернион
    omegap[0] = 0
    k1 = Fquart(quart, omegap) * dt
    k2 = Fquart(quart + 0.5 * k1, omegap) * dt
    k3 = Fquart(quart + 0.5 * k2, omegap) * dt
    k4 = Fquart(quart + k3, omegap) * dt
    quart = quart + 1.0 / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)

    
    quart3d = np.array([quart[1],quart[2],quart[3]]) #орт без угла поворота
    omegap3d = np.array([omegap[1],omegap[2],omegap[3]])
    sigma = (-Kp * sign(quart[0])  * quart3d -  Kd * omegap3d) #вектор управления


    #первая нелинейность
    if abs(sigma[0]) >= LMAX:
        sigma[0] = LMAX * sign(sigma[0])

    if abs(sigma[1]) >= LMAX: 
        sigma[1] = sign(sigma[1]) * LMAX
    
    if (abs(sigma[2]) >= LMAX): 
        sigma[2] = sign(sigma[2]) * LMAX

    #вторая нелинейность
    if abs(OMEGA[0]) >= OmegaMAX:
        sigma[0] = sigma[0] * O
    
    if abs(OMEGA[1]) >= OmegaMAX: 
        sigma[1] = sigma[1] * O
    
    if abs(OMEGA[2]) >= OmegaMAX: 
        sigma[2] = sigma[2] * O
    
    # вектор угловых скоростей вращения ДМ
    k1 = FOMEGA(OMEGA,sigma, Idm) * dt
    k2 = FOMEGA(OMEGA + 0.5 * k1, sigma,  Idm) * dt
    k3 = FOMEGA(OMEGA + 0.5 * k2, sigma,  Idm) * dt
    k4 = FOMEGA(OMEGA + k3,sigma, Idm) * dt
    OMEGA = OMEGA + 1.0 / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)


    # гравитационный момент
    R = (math.sqrt(pow(r_j2000[0], 2) + pow(r_j2000[1], 2) + pow(r_j2000[2], 2))) # расстояние от центра масс Земли до центра масс КА (м)
    Ro_j2000 = r_j2000 / R   # нормированный вектор из центра Земли в центр масс КА
    Ro0_j2000 = np.array([0, Ro_j2000[0], Ro_j2000[1], Ro_j2000[2]], float) #pxyz
    quart_sop = np.array([quart[0], -quart[1], -quart[2], -quart[3]], float) #сопряженный кватернион

    Ksi1_vec = Ksi1(quart_sop, Ro0_j2000) #умножение сопряженного кватерниона на нормированный вектор из центра Земли в центр масс КА
    Ksi_vec = Ksi(Ksi1_vec, quart) #умножение Ksi1  на текущий кватернион получаем проекцию вектора Ksi

    MR = 3 * consts.Mukm / (2 * (pow(R, 3)))
    JK_val = JK(Jmatr, Ksi_vec) #произведение тензора инерции на проекцию вектора Ksi 
    KJ_val = KJ(Ksi_vec, JK_val) # произведение проекции вектора Ksi на JK 
    Msumm = MR * KJ_val #гравитационный момент

    k1 = Fomegap(omegap3d, sigma, Msumm, OMEGA, Jmatr_1, Idm, Jmatr) * dt
    k2 = Fomegap(omegap3d + 0.5 * k1, sigma, Msumm, OMEGA, Jmatr_1, Idm, Jmatr) * dt
    k3 = Fomegap(omegap3d + 0.5 * k2, sigma, Msumm, OMEGA, Jmatr_1, Idm, Jmatr) * dt
    k4 = Fomegap(omegap3d + k3, sigma, Msumm, OMEGA, Jmatr_1, Idm, Jmatr) * dt
    omegap3d = omegap3d + 1.0 / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    omegap = np.array([omegap[0], omegap3d[0], omegap3d[1], omegap3d[2]])
    
    # print('=======================', t, '======================')
    # print('r_j2000 = ', r_j2000_f.vec)
    # print('quart = ', quart)
    # # print('sigma = ', sigma)
    # print('Omega = ', OMEGA)
    # print('omegap = ', omegap)
    
    #================plot point=========================
    # plt.scatter(r_j2000[0], t, color='r')
    r_j2000_x = np.append(r_j2000_x, [r_j2000_f.vec[0]]) # радиус-вектор КА
    r_j2000_y = np.append(r_j2000_y, [r_j2000_f.vec[1]])
    r_j2000_z = np.append(r_j2000_z, [r_j2000_f.vec[2]])

    OmegA_x = np.append(OmegA_x, [OMEGA[0]]) # вектор угловых скоростей вращения ДМ
    OmegA_y = np.append(OmegA_y, [OMEGA[1]])
    OmegA_z = np.append(OmegA_z, [OMEGA[2]])

    omegap_x = np.append(omegap_x, [omegap[1]]) # вектор угловой скорости вращения КА
    omegap_y = np.append(omegap_y, [omegap[2]])
    omegap_z = np.append(omegap_z, [omegap[3]])


    
    t_going = np.append(t_going, t)
    #===================================================
    f.write(str(t))
    f.write(' ')
    f.write(str(r_j2000))
    f.write(' ')
    f.write(str(quart)) 
    f.write(' ')
    f.write(str(sigma))
    f.write(' ')
    f.write(str(OMEGA))
    f.write(' ')
    f.write(str(omegap))
    f.write('\n')
    # print('{:.2f}'.format(r_j2000_f.vec[0]))
    t = t + dt    
    
f.close()

print('END')
sys.stdout.flush()
# #===========================PLOTTING==========================
# pylab.figure (1)
# pylab.plot(r_j2000_x, t_going, label = "x")
# plt.title('Изменение X радиус-вектора КА по времени')
# plt.xlabel('X, км')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='r_j2000_x', fmt='png')

# pylab.figure (2)
# pylab.plot (r_j2000_y, t_going, label = "y")
# plt.title('Изменение Y радиус-вектора КА по времени')
# plt.xlabel('Y, км')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='r_j2000_y', fmt='png')

# pylab.figure (3)
# pylab.plot(r_j2000_z, t_going, label = "z")
# plt.title('Изменение Z радиус-вектора КА по времени')
# plt.xlabel('Z, км')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='r_j2000_z', fmt='png')

# pylab.figure (4) # угловая скорость КА
# pylab.plot(omegap_x, t_going, label = "omx")
# plt.title('Угловая скорость КА по оси X')
# plt.xlabel('Om, рад/с')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='omegap_x', fmt='png')

# pylab.figure (5)
# pylab.plot(omegap_y, t_going, label = "omy")
# plt.title('Угловая скорость КА по оси Y')
# plt.xlabel('Om, рад/с')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='omegap_z', fmt='png')

# pylab.figure (6)
# pylab.plot(omegap_z, t_going, label = "omz")
# plt.title('Угловая скорость КА по оси X')
# plt.xlabel('Om, рад/с')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='omegap_z', fmt='png')

# pylab.figure (7) # угловая скорость ДМ
# pylab.plot(OmegA_x, t_going, label = "Omx")
# plt.title('Угловая скорость ДМ по оси X')
# plt.xlabel('Om, рад/с')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='OmegA_x', fmt='png')

# pylab.figure (8)
# pylab.plot(OmegA_y, t_going, label = "Omy")
# plt.title('Угловая скорость ДМ по оси Y')
# plt.xlabel('Om, рад/с')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='OmegA_y', fmt='png')

# pylab.figure (9)
# pylab.plot(OmegA_z, t_going, label = "Omz")
# plt.title('Угловая скорость ДМ по оси X')
# plt.xlabel('Om, рад/с')
# plt.ylabel('Время, с')
# pylab.grid(True)
# save(name='OmegA_z', fmt='png')

# fig = plt.figure()
# ax = fig.add_subplot(111, projection='3d')
# ax.plot(r_j2000_x, r_j2000_y, r_j2000_z, label='parametric curve')

# # print('%2.2'.format(x))

# pylab.show()

