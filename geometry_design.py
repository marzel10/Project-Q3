import numpy as np
import matplotlib.pyplot as plt

class geometry_design:

    def __init__(self, D,w,col,H,mat,setting,xs=0,zs=0,n=0):
        self.diameter=D
        self.x_spacing=xs
        self.z_spacing=zs
        self.width=w
        self.columns_number=col
        self.height=H
        self.material=mat
        self.setting=setting # a word indicating which setting of geometry is used (grid or rectangular)
        self.n=n #n is number of fasteners in one column (optional)


    def c(self): #defining minimum distance coefficient for different materials (mat)
        if self.material=="metal": #defining safety factor
            c=3
        else:
            c=5 #for the composite
        return c


    def number_of_fastners(self): # number of fasteners in one column

        if self.z_spacing<geometry_design.c(self)*self.diameter:
            self.z_spacing=geometry_design.c(self)*self.diameter
            print(f"INVALID GEOMETRY SPACING, resulting (minimal) spacing is {self.z_spacing}")

        c=geometry_design.c(self)
        if self.z_spacing==0:
            n=np.floor((self.width-3*self.diameter)/c/self.diameter)+1 #maximal number of fastners
        else:
            n=np.floor((self.width-3*self.diameter)/self.z_spacing)+1
        return n




    def cg_position(self):
        X,Z=geometry_design.position_matrix(self)

        x_cg=0
        z_cg=0
        area=0
        for i in range(len(Z)):
            x_cg += np.pi*self.diameter**2/4*X[i]
            z_cg += np.pi*self.diameter**2/4*Z[i]
            area += np.pi*self.diameter**2/4 #calculate the total area
        x_cg=np.round(x_cg/area,-4)
        z_cg=np.round(z_cg/area,-4)

        return x_cg,z_cg #return position of the center of gravity

    def position_matrix_rectangular(self):#return two arrays with X and Z coordinates of all fasteners (in case of the rectangular setting)

        #Checking if the z and x spacing between the fasteners is big enough
        if self.z_spacing<geometry_design.c(self)*self.diameter:
            zs=geometry_design.c(self)*self.diameter
            self.n=0
        else:
            zs=self.z_spacing

        if self.x_spacing<geometry_design.c(self)*self.diameter:
            xs=geometry_design.c(self)*self.diameter
            self.n=0
        else:
            xs=self.x_spacing

        #calculation of maximal number of fasteners in one column if number of fasteners was not specified by hand
        if self.n==0:
            self.n=geometry_design.number_of_fastners(self)

        n=int(self.n)

        l=(n-1)*zs #lenght of the fasteners column
        z1=np.arange(-l/2,l/2+zs,zs) #fasteners will be placed symetrically from 0 axis with step equal to zs (+zs included to include the end)
        xn=np.arange(-(self.height/2-1.5*self.diameter),-(self.height/2-1.5*self.diameter)+(self.columns_number/2-1)*xs+xs,xs) #distribution of fasteners columns on the negative axis
        xp=np.arange((self.height/2-1.5*self.diameter)-(self.columns_number/2-1)*xs,(self.height/2-1.5*self.diameter)+xs,xs) #distribution of fasteners columns on the positive axis
        x1=np.concatenate((xp,xn),axis=0)


        Z=[]
        X=[]
        for i in range(len(x1)): #for every column of fasteners
            for j in range(len(z1)): #for every row of fasteners
                Z.append(z1[j])
                X.append(x1[i])


        return X,Z

    def position_matrix_grid(self): #return two arrays with X and Z coordinates of all fasteners (in case of the grid setting)

        #Checking if the z and x spacing between the fasteners is big enough

        if self.z_spacing<geometry_design.c(self)*self.diameter:
            zs=geometry_design.c(self)*self.diameter
            self.n=0
        else:
            zs=self.z_spacing

        if self.x_spacing<geometry_design.c(self)*self.diameter:
            xs=geometry_design.c(self)*self.diameter
            self.n=0
        else:
            xs=self.x_spacing

        #calculation of maximal number of fasteners in one column
        if self.n==0:
            self.n=geometry_design.number_of_fastners(self)

        n=int(self.n)

        l1=(n-1)*zs #lenght of the fasteners line
        l2 = (n - 2) * zs  # lenght of the fasteners line (shorter)
        z1=np.arange(-l1/2,l1/2+zs,zs) #fasteners will be placed symetrically from 0 axis, +zs included to include the end
        z2 = np.arange(-l2 / 2, l2/ 2 + zs, zs)

        #the same code as for the rectangular configuration
        xn=np.arange(-(self.height/2-1.5*self.diameter),-(self.height/2-1.5*self.diameter)+(self.columns_number/2-1)*xs+xs,xs)
        xp=np.arange((self.height/2-1.5*self.diameter)-(self.columns_number/2-1)*xs,(self.height/2-1.5*self.diameter)+xs,xs)

        print(xn,xp)
        Z=[]
        X=[]

        # the same code as for the rectangular configuration, slightly changed to place longer columns on the other edges of the plate
        for i in range(len(xp)):
            if i%2==0:
                for j in range(len(z2)):
                    Z.append(z2[j])
                    X.append(xp[i])
            else:
                for j in range(len(z1)):
                    Z.append(z1[j])
                    X.append(xp[i])

        for i in range(len(xn)):
            if i%2==0:
                for j in range(len(z1)):
                    Z.append(z1[j])
                    X.append(xn[i])
            else:
                for j in range(len(z2)):
                    Z.append(z2[j])
                    X.append(xn[i])

        return X,Z

    def position_matrix(self): #return two arrays with X and Z coordinates of all fasteners (any setting)
        if self.setting=="grid":
            X,Z=geometry_design.position_matrix_grid(self)
        elif self.setting=="rectangular":
            X,Z=geometry_design.position_matrix_rectangular(self)
            print("Iamhere")
        else:
            X=0;Z=0;
            print("Wrong setting selection, chose grid or rectangular")
        return X,Z

    def display_geometry(self): #function that displays geometry
        X,Z=geometry_design.position_matrix(self)

        plt.scatter(X, Z)
        plt.xlabel("x"); plt.ylabel("z")
        plt.axvline(x=self.height/2, ymin=-self.width/2, ymax=self.width/2, linewidth=2, linestyle="--", color='red')
        plt.axvline(x=-self.height / 2, ymin=-self.width / 2, ymax=self.width / 2, linewidth=2, linestyle="--", color='red')
        plt.axhline(y=-self.width / 2, xmin=-self.height / 2, xmax=self.height / 2, linewidth=2, linestyle="--", color='red')
        plt.axhline(y=self.width / 2, xmin=-self.height / 2, xmax=self.height / 2, linewidth=2, linestyle="--",color='red')
        plt.axvline(x=self.height / 2-1.5*self.diameter, linewidth=2, linestyle="--", color='green')
        plt.axvline(x=-self.height / 2 + 1.5 * self.diameter, linewidth=2, linestyle="--", color='green')
        plt.axhline(y=-self.width/ 2 + 1.5 * self.diameter, linewidth=2, linestyle="--", color='green')
        plt.axhline(y=self.width / 2 - 1.5 * self.diameter, linewidth=2, linestyle="--", color='green')
        plt.show()



configuration1=geometry_design(7,50,2,100,"metal","rectangular",0,0,0)

print(configuration1.position_matrix())
configuration1.display_geometry()

