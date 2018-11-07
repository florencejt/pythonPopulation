# importing modules that will be used during the script
import random
import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
# population simulation of some animal with assumed variables
# using the logistic function for population growth
T = 0
Vowels = ["A", "E", "I", "O", "U"]
InputName = input("Name your species: ")
# Inputting maximum population numbers and starting numbers

# controlling what the user can input to avoid errors
while True:
        try:
            InputK = int(input("Choose a maximum number for your species "
                               "population between 2000 and 5000: "))
            if int(InputK) < 2000 or int(InputK) > 5000:
                raise ValueError
            break
        except ValueError:
            print("That is not allowed. Please choose an integer between 2000 and 5000.")

while True:
        try:
            InputN = int(input("Choose a staring number for your species "
                               "population between 50 and 150: "))
            if int(InputN) < 50 or int(InputN) > 150:
                raise ValueError
            break

        except ValueError:
            print("That is not allowed. Please choose an integer between 50 and 150.")


# defining a class for the species we are simulating

class Species:
    def __init__(self, Name, CarryingCapacity, Rmax, Population):
        self.Name = Name
        self.K = CarryingCapacity
        self.Rmax = Rmax
        self.N = Population

    def StatPrint(self):  # to give the user a report of how their species is doing
        if T == 0:
            print("Your species, " + self.Name +
                  ", will start at " + str(T) + " years with " + str(self.N) + " animals.")
        else:
            print("The species,", self.Name + ", at", T, "years has a population of",
                  int(FinalN[0]))


class Events:
    def __init__(self, Description, Effect):
        self.Description = Description
        self.Effect = Effect


ListOfEvents = []

Earthquake = Events("Earthquake", 0.3)
ListOfEvents.append(Earthquake)
PreyBoost = Events("Prey Boost", 1.6)
ListOfEvents.append(PreyBoost)
PredatorBoost = Events("Predator Boost", 0.5)
ListOfEvents.append(PredatorBoost)
Disease = Events("Disease", 0.4)
ListOfEvents.append(Disease)
Poaching = Events("Poaching", 0.7)
ListOfEvents.append(Poaching)
Drought = Events("Drought", 0.6)
ListOfEvents.append(Drought)
ConservationAttempt = Events("Conservation Attempt", 1.3)
ListOfEvents.append(ConservationAttempt)

Animal = Species(InputName, int(InputK), 0.1, int(InputN))

# Rmax chosen for graph to look most like example logistic function graphs

Species.StatPrint(Animal)

# subplot of species growth while affected by events
plt.subplot(2, 1, 1)
plt.xlabel("Time (Years)")
plt.ylabel("Population")
plt.title("Logistic Function over 100 Years with Catastrophic Events")

if T == 0:
    def dN_dT(N, T):  # defining the logistic function differential equation
        Rmax = Animal.Rmax
        K = Animal.K
        return Rmax * ((K - N) / K) * N

    InitN = Animal.N  # initial condition
    RangeT = np.linspace(T, T + 10)
    RangeN = odeint(dN_dT, InitN, RangeT)
    plt.plot(RangeT, RangeN, 'b--')
    FinalN = odeint(dN_dT, InitN, RangeT)[-1]  # final value of N in this T period
    T = T + 10
    Species.StatPrint(Animal)


while T > 0 and T <= 90:
    Event1 = ListOfEvents[random.randrange(len(ListOfEvents))]  # randomising catastrophic events

    def dN_dT(N, T):  # defining function again with Event effect included
        Rmax = Animal.Rmax
        K = Animal.K
        return Event1.Effect * Rmax * ((K - N) / K) * N
    RangeT = np.linspace(T, T + 10)  # linear space of gap 10
    InitN = FinalN  # defining initial condition as the value where the previous T period ends
    RangeN = odeint(dN_dT, InitN, RangeT)
    plt.plot(RangeT, RangeN, "b--")
    FinalN = odeint(dN_dT, FinalN, RangeT)[-1]
    if T <= 50:  # arranging annotations for best presentation
        plt.annotate(Event1.Description, xy=(T, InitN), xytext=(T - 10, InitN + 350),
                     arrowprops=dict(arrowstyle="->"),
                     size='small')
    else:
        plt.annotate(Event1.Description, xy=(T, InitN), xytext=(T + 5, InitN - 400),
                     arrowprops=dict(arrowstyle="->"), size='small')
    if Event1.Description[0] in Vowels:  # correcting grammar in report
        print("there has been an occurrence of an", Event1.Description, "at", T, "years")
    else:
        print("there has been an occurrence of a", Event1.Description, "at", T, "years")
    T = T + 10
    Species.StatPrint(Animal)


# plotting the logistic function without catastrophic events

plt.subplot(2, 1, 2)
plt.xlabel("Time (Years)")
plt.ylabel("Population")
plt.title("Logistic Function over 100 Years without Catastrophic Events")

T = 0  # resetting years for second plot
InitN = Animal.N
FinalN = Animal.N  # resetting final value of N
while T <= 90:
    def dN_dT(N, T):
        Rmax = Animal.Rmax
        K = Animal.K
        return Rmax * ((K - N) / K) * N
    RangeT = np.linspace(T, T + 10)
    InitN = FinalN
    RangeN = odeint(dN_dT, InitN, RangeT)
    plt.plot(RangeT, RangeN, "g--")
    FinalN = odeint(dN_dT, FinalN, RangeT)[-1]
    T = T + 10

# labelling with equation
plt.annotate(r'$\frac{R_{max}(K-N)N}{K}$', xy=(0, Animal.K/2), fontsize=15)
plt.show()
