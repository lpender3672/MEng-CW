import numpy as np
import matplotlib.pyplot as plt

#declare some arrays to work with
#declare some arrays to work with
N  = 41
L  = 2.0 
dx = L/(N-1)
x  = np.linspace(0,L,N)
u    = np.zeros(N)
u_dt = np.zeros(N)

#set the convection speed
A = 1
timespan = 2
c =.5
alpha = 1/6
#set the time step based on the cfl number
dt = c/A*dx
print(dt)
Nstep = 10



def timestep(alpha):
  for i in range(1,N-1):
    u_dt[i] = u[i] - c *(u[i]-u[i-1]) + alpha * (u[i-1] - 2*u[i] + u[i+1])
  u[1:] = u_dt[1:]           
  return

u0      = np.zeros(N)
u0[0:10] = 1

def solve_convection(alpha):
  #set an intial condition
  u[:]    = u0[:]
  global ans
  ans = [u0.copy()]
  T = [0]  

  for k in range(0,Nstep):
      timestep(alpha)
      #the lines below simply store a copy of the solution 
      #after each time step so that it can be plotted and animated
      ans.append(u.copy())
      T.append(k*dt)
  
  return u, T

####################
#Create a simple plot of the results    
####################
plt.plot(x,u0, label = 'Initial condition')
u1,_ = solve_convection(0)
plt.plot(x,u1, label = r'$\alpha = 0$')
u2,_ = solve_convection(1/6)
plt.plot(x,u2, label = r'$\alpha = 1/6$')
plt.legend(['Initial condition', "Solution at t = {} s".format(timespan)])
plt.xlabel('x')
plt.ylabel('u');
plt.legend()
#plt.savefig('EP1_Q6b.png', dpi=300)
plt.show()

###########
#The code below creates an animation NOT EXAMINABLE!
###########
from matplotlib.animation import FuncAnimation
import matplotlib.animation as animation

fig,ax = plt.subplots()
ax.plot(x,u0)
ax.set_title('c = {}, A = {}'.format(c,A))
ax.set_xlabel('x')
ax.set_ylabel('u');
uline=ax.plot([],[])[0]
def anim(i):
    uline.set_data(x,ans[i])
    plt.legend(['Initial condition', "Solution at t = {:.2f} s".format(T[i])])
ani = FuncAnimation(fig, anim, frames=range(0,len(ans)),interval=200)    

plt.show()

