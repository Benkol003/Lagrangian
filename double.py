########
# Double pendulum simulation.
#Takes two second order ODE's and use euler method of integration for both derivatives. (Inaccurate, should use RK4 instead.)
# #######

import pygame
from sympy import *
import math

init_printing()


def rk4(func,y_n, h):
    k1 = func(y_n)
    k2 = func(y_n + (h * k1/2 ))
    k3 = func(y_n + (h * k2/2 ))
    k4 = func(y_n + h*k3 )

    delta_y = (h / 6)*(k1 + 2*k2 + 2*k3 + k4) #
    
    return delta_y

t, g, l1, l2, m1, m2, theta1, theta2, theta1_d, theta2_d, theta1_dd, theta2_dd = symbols("t g l₁ l₂ m₁ m₂ θ₁ θ₂ θ₁' θ₂' θ₁'' θ₂'' ")

alpha1 = (m1+m2) * (l1**2)
beta1 = m2*l1*l2*cos(theta1-theta2)
gamma1 = -m2*l1*l2*theta1_d*theta2_d*sin(theta1-theta2) - (m1+m2)*l1*g*sin(theta1)

alpha2 = m2*l1*l2*cos(theta1-theta2)
beta2 = m2*l2**2
gamma2 = m2*l1*l2*theta1_d*theta2_d*sin(theta1-theta2) - l2*m2*g*sin(theta2)

theta1_dd = ( beta2*gamma1 - beta1*gamma2 ) / ( alpha1*beta2-alpha2*beta1 )

theta2_dd = ( alpha1*gamma2 - alpha2*gamma1 ) / ( alpha1*beta2 - alpha2*beta1 )


### INITIAL VALUES

g_v = 9.81

m1_v = 1
m2_v = 2

l1_v = 1.5

l2_v = 2.5


theta1_t0 = 60 / 180 * math.pi
theta2_t0 = 45 / 180 * math.pi

theta1_d_t0 = 0
theta2_d_t0 = 0

theta1_dd = theta1_dd.subs({m1: m1_v, m2: m2_v, l1: l1_v, l2: l2_v, g: g_v})
theta2_dd = theta2_dd.subs({m1: m1_v, m2: m2_v, l1: l1_v, l2: l2_v, g: g_v})

FPS = 500
#rendering

pivot = (500,200)

pygame.init()
screen = pygame.display.set_mode((1280,720))
clock=pygame.time.Clock()
running=True

t = 0

#perform simple euler integration atm
def timestep(dt):
       global theta1_t0, theta2_t0, theta1_d_t0, theta2_d_t0
       theta1_dd_t0 = theta1_dd.evalf(subs={theta1: theta1_t0, theta2: theta2_t0, theta1_d: theta1_d_t0, theta2_d: theta2_d_t0})
       theta2_dd_t0 = theta2_dd.evalf(subs={theta1: theta1_t0, theta2: theta2_t0, theta1_d: theta1_d_t0, theta2_d: theta2_d_t0})

       theta1_d_t0 = theta1_d_t0 + theta1_dd_t0 * dt
       theta2_d_t0 = theta2_d_t0 + theta2_dd_t0 * dt

       theta1_t0 = theta1_t0 + theta1_d_t0 * dt
       theta2_t0 = theta2_t0 + theta2_d_t0 * dt

####### TODO cleanup paste

while running:
        dt = clock.tick(FPS) / 1000

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        #numeric iteration
        t+=dt
        timestep(dt)

        if theta1_t0 > 2*math.pi:
            theta1_t0 = theta1_t0-(2*math.pi)

        if theta2_t0 > 2*math.pi:
            theta2_t0 = theta2_t0-(2*math.pi)

        #calculate screen coordinates
        p1_x = pivot[0]+((l1_v*100)*math.sin(theta1_t0))
        p1_y = pivot[1]+((l1_v*100)*math.cos(theta1_t0))

        p2_x = p1_x+((l2_v*100)*math.sin(theta2_t0))
        p2_y = p1_y+((l2_v*100)*math.cos(theta2_t0))

        #pivot
        pygame.draw.circle(screen,"red",pivot,16)

        #line 1
        pygame.draw.line(screen,"white",pivot,(p1_x,p1_y),8)

        #pendulum
        pygame.draw.circle(screen,"blue",(p1_x,p1_y),16)

        #line 2
        pygame.draw.line(screen,"white",(p1_x,p1_y),(p2_x,p2_y),8)

        #pendulum
        pygame.draw.circle(screen,"blue",(p2_x,p2_y),16)

        pygame.display.flip()