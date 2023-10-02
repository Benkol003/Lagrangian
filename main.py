'''
from the lagrangian we have a second-order ODE. To numerically solve:

Convert to a system of coupled first-order ODE's by introducing a new variable for the first derivative and apply runge-kutta to both.

'''


from sympy import *
from math import *
import matplotlib.pyplot as plt
import pygame

init_printing(use_unicode=True)

t, x, y, ang_v, = symbols('t x y ω')
#ang_v -> angular velocity

print(ang_v)


def rk4(func,y_n, h):
    k1 = func(y_n)
    k2 = func(y_n + (h * k1/2 ))
    k3 = func(y_n + (h * k2/2 ))
    k4 = func(y_n + h*k3 )

    delta_y = (h / 6)*(k1 + 2*k2 + 2*k3 + k4) #
    
    return delta_y

#wierd, if FPS increases then verlet has a different calculation
def verlet(x_0, x_1, dt, func): 
    x_2  = (2*x_1) - x_0 + func(x_1)*(dt**2)
    return x_2

#because we are using coupled equations, the computed change is applied to a different variable than the one used for the function arguement

g = -981 # gravity

l = 256.0 # length of pendulum arm

#theta : radians

theta_0 = pi/2
u_0 = 0

def pend_1(theta): # returns u_dot
    return g / l * sin(theta)

def pend_2(u):
    return u #aka theta_dot

def pend_2order(theta):
        return g / l * sin(theta)


u_n = u_0
FPS = 1000

theta_m = theta_0
theta_n =theta_m + (1/FPS)*u_0 + (1/2)*pend_2order(theta_0)*((1/FPS)**2)

t=0

mode = "rk4"

'''
h = 0.001
u_arr = []
theta_arr = []
t_arr = []

while t<=10:

    u_n = u_n + rk4(pend_1,theta_n, h)

    theta_n = theta_n + rk4(pend_2, u_n, h)

    u_arr.append(u_n)
    theta_arr.append(theta_n)

    t_arr.append(t)
    t+=h

    if theta_n > 2*pi:
        theta_n = theta_n-(2*pi)

plt.plot( t_arr, theta_arr)
plt.show()
'''


#-----------

pivot = (500,200)

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock=pygame.time.Clock()
running=True

while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        #numeric iteration
        t+=dt

        if mode=="rk4":
            theta_n = theta_n + rk4(pend_2, u_n, dt)
            u_n = u_n + rk4(pend_1,theta_n, dt)

        elif mode=="verlet": 
            theta_o = verlet(theta_m,theta_n,dt,pend_2order)
            theta_m = theta_n
            theta_n = theta_o

        else:
             raise ValueError("Numeric integration method '"+mode+"' not recognised.")
        

        if theta_n > 2*pi:
            theta_n = theta_n-(2*pi)

        #calculate screen coordinates
        p1_x = pivot[0]+(l*sin(theta_n))
        p1_y = pivot[1]+(l*cos(theta_n))

        #pivot
        pygame.draw.circle(screen,"red",pivot,16)

        #line
        pygame.draw.line(screen,"white",pivot,(p1_x,p1_y),8)

        #pendulum
        pygame.draw.circle(screen,"blue",(p1_x,p1_y),16)

        pygame.display.flip()

        fps_cur = 1/dt

        if fps_cur < FPS*0.9 or fps_cur > FPS*1.1:
             print(fps_cur)