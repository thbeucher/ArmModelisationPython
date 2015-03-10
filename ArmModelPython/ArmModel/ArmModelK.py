from ArmModel.ParametresRobot import *
from ArmModel.ParametresArmModel import *
from ArmModel.ParametresHogan import *
from ArmModel.SavingData import *
from numpy import *
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib import animation


print("Bienvenue dans ce programme !")

robot = ParametresRobot()

hogan = ParametresHogan()

arm = ParametresArmModel(hogan.GammaMax)
q = arm.q0
dotq = arm.dotq0

save = SavingData()
coordEL, coordHA = save.calculCoord(q, robot)
save.SaveTrajectory(coordEL, coordHA)


#Boucle de fonctionnement
while(arm.t<=2):
    if 0<=arm.t and arm.t<= 0.15:
        arm.ub1 = 1
        arm.ut1 = 0
    
        arm.ub2 = 0.9
        arm.ut2 = 0.1
    
        arm.ub3 = 0.9
        arm.ut3 = 0.15
    
    
    elif 0.15<arm.t and arm.t<= 0.3:
        arm.ut1 = 0.5
        arm.ub1 = 0.15
    
        arm.ut2 = 0.4
        arm.ub2 = 0
    
        arm.ub3 = 1
        arm.ut3 = 0.15
    
    elif (0.3<arm.t and arm.t<= 0.45):
        arm.ut1 = 0.5
        arm.ub1 = 0.5
    
        arm.ut2 = 0.3
        arm.ub2 = 0.3
    
        arm.ub3 = 0.35
        arm.ut3 = 0.35
    
    elif 0.45<arm.t and arm.t<= 0.6:
        arm.ut1 = 0.5
        arm.ub1 = 0.75
    
        arm.ut2 = 0.5
        arm.ub2 = 1
    
        arm.ub3 = 0.5
        arm.ut3 = 0.55
    
    elif 0.6<arm.t and arm.t<=0.75:
        arm.ut1 = 1
        arm.ub1 = 0.1
    
        arm.ut2 = 1
        arm.ub2 = 0
    
        arm.ub3 = 1
        arm.ut3 = 0.5
    
    elif 0.75<arm.t and arm.t<=1:
        arm.ut1 = 0
        arm.ub1 = 0
    
        arm.ut2 = 0.2
        arm.ub2 = 0.5
    
        arm.ub3 = 0.5
        arm.ut3 = 0.2
    
    
    # Vecteur des activations musculaires
    U = mat([[arm.ub1],[arm.ut1],[arm.ub2],[arm.ut2],[arm.ub3],[arm.ut3]])
    
    # Calcul du couple Gamma pour une raideur non nulle
    Gamma_AM = (arm.At*arm.fmax-(arm.Kraid*diag([q[0,0], q[0,0], q[1,0], q[1,0], q[0,0], q[0,0]])))*U
    
    # Integration
    ddotq = arm.MDD( Gamma_AM,q,dotq,robot)
    dotq += ddotq*arm.dt
    q += dotq*arm.dt
    
    #Sauvegarde position pour visualition trajectoire
    coordEL, coordHA = save.calculCoord(q, robot)
    save.SaveTrajectory(coordEL, coordHA)
    #Sauvegarde des differents parametres
    save.saveParameters(q, dotq, ddotq, Gamma_AM, arm)
    
    arm.t += arm.dt
    arm.i += 1

save.createCoord()

fig = plt.figure()
upperArm, = plt.plot([],[]) 
foreArm, = plt.plot([],[])
plt.xlim(-0.7, 0.7)
plt.ylim(-0.7,0.7)

def init():
    upperArm.set_data([0],[0])
    foreArm.set_data([save.xEl[0]],[save.yEl[0]])
    return upperArm,foreArm,

def animate(i): 
    xe = (0, save.xEl[i])
    ye = (0, save.yEl[i])
    xh = (save.xEl[i], save.xHa[i])
    yh = (save.yEl[i], save.yHa[i])
    upperArm.set_data(xe, ye)
    foreArm.set_data(xh, yh)
    return upperArm,foreArm
 
ani = animation.FuncAnimation(fig, animate, init_func=init, frames=200, blit=True, interval=20, repeat=True)

plt.show(block=True)

#Figures  
'''qsave1 = []
qsave2 = []
for elt in save.qsave:
    qsave1.append(elt[0])
    qsave2.append(elt[1])
plt.figure()
a = plt.plot(save.tsave,qsave1,color='red')
b = plt.plot(save.tsave,qsave2,color='blue')
plt.xlabel('t [s]')
plt.ylabel('q1 [rad], q2[rad]')
red_patch = mpatches.Patch(color='red', label='q1')
blue_patch = mpatches.Patch(color='blue', label='q2')
plt.legend([a, b])
plt.title('Variations de q1 et q2 en fonction du temps')
plt.grid(True)

dotqsave1 = []
dotqsave2 = []
for el in save.dotqsave:
    dotqsave1.append(el[0])
    dotqsave2.append(el[1])
plt.figure()
a = plt.plot(save.tsave,dotqsave1,'green')
b = plt.plot(save.tsave,dotqsave2,'blue')
plt.grid(True)
plt.xlabel('t [s]')
plt.ylabel('dq1 [rad/s], dq2 [rad/s]')
green_patch2 = mpatches.Patch(color='green', label='dq1')
blue_patch2 = mpatches.Patch(color='blue', label='dq2')
plt.legend(handles=[green_patch2,blue_patch2])
plt.title('Variations de dq1 et dq2 en fonction du temps')

ddotqsave1 = []
ddotqsave2 = []
for el in save.ddotqsave:
    ddotqsave1.append(el[0])
    ddotqsave2.append(el[1])
plt.figure()
a = plt.plot(save.tsave,ddotqsave1,'green')
b = plt.plot(save.tsave,ddotqsave2,'blue')
plt.xlabel('t [s]')
plt.ylabel('ddq1[rad.s^-2], ddq2[rad.s^-2]')
green_patch3 = mpatches.Patch(color='green', label='ddq1')
blue_patch3 = mpatches.Patch(color='blue', label='ddq2')
plt.legend(handles=[green_patch3,blue_patch3])
plt.title('Variations de ddq1 et ddq2 en fonction du temps')

Gammasave1 = []
Gammasave2 = []
for el in save.Gammasave:
    Gammasave1.append(el[0])
    Gammasave2.append(el[1])
plt.figure()
a = plt.plot(save.tsave,Gammasave1,'green')
b = plt.plot(save.tsave,Gammasave2,'blue')
plt.xlabel('t [s]')
plt.ylabel('Gamma [N.m]')
green_patch4 = mpatches.Patch(color='green', label='Gamma(1)')
blue_patch4 = mpatches.Patch(color='blue', label='gamma(2)')
plt.legend(handles=[green_patch4,blue_patch4])
plt.title('Variations de Gamma en fonction du temps')

plt.figure()
plt.subplot(3,1,1)
a = plt.plot(save.tsave,save.ub1save,'green')
b = plt.plot(save.tsave,save.ut1save,'blue')
plt.grid(True)
plt.xlabel('t')
plt.ylabel('ub1, ut1')
green_patch5 = mpatches.Patch(color='green', label='ub1')
blue_patch5 = mpatches.Patch(color='blue', label='ut1')
plt.legend(handles=[green_patch5,blue_patch5])
plt.title('Variations de ub1 et ut1 en fonction du temps')
plt.subplot(3,1,2)
c = plt.plot(save.tsave,save.ub2save,'green')
d = plt.plot(save.tsave,save.ut2save,'blue')
plt.grid(True)
plt.xlabel('t')
plt.ylabel('ub2, ut2')
green_patch6 = mpatches.Patch(color='green', label='ub2')
blue_patch6 = mpatches.Patch(color='blue', label='ut2')
plt.legend(handles=[green_patch6,blue_patch6])
plt.title('Variations de ub2 et ut2 en fonction du temps')
plt.subplot(3,1,3)
e = plt.plot(save.tsave,save.ub3save,'green')
f = plt.plot(save.tsave,save.ut3save,'blue')
plt.grid(True)
plt.xlabel('t')
plt.ylabel('ub3, ut3')
green_patch7 = mpatches.Patch(color='green', label='ub3')
blue_patch7 = mpatches.Patch(color='blue', label='ut3')
plt.legend(handles=[green_patch7,blue_patch7])
plt.title('Variations de ub3 et ut3 en fonction du temps')
plt.show(block=True)'''
