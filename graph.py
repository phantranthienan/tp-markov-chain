import numpy as np
import matplotlib.pyplot as plt
import ast  # To safely evaluate the content of files as Python objects

# Load data from files
def load_data(filename):
    """
    Load data from a file and parse it as a Python object.
    """
    with open(filename, 'r') as file:
        data = file.read()
    return ast.literal_eval(data)

# Load the results from the corresponding files
init = load_data("init.txt")
double_R = load_data("double_vitesse.txt")
double_S = load_data("double_bande.txt")
double_serveurs = load_data("double_serveurs.txt")

# Define the range of arrival rates (A)
valeurs_A = np.arange(10, 41)

# Graph for initial configuration (Part 2, Task 2)
def graphp2t2():
    """
    Plot the mean response times and confidence intervals for the initial configuration.
    """
    lower = [row[0] for row in init]
    mean = [row[1] for row in init]
    upper = [row[2] for row in init]

    plt.plot(valeurs_A, lower, label="Borne inférieure")
    plt.plot(valeurs_A, mean, label="Temps moyen de séjour", marker="o")
    plt.plot(valeurs_A, upper, label="Borne supérieure")
    plt.title("Temps moyen de séjour en fonction des valeurs de A (Initial Configuration)")
    plt.xlabel("Taux d'arrivée (A)")
    plt.ylabel("Temps moyen de séjour")
    plt.legend()
    plt.grid(True)
    plt.show()

# Graph for doubling the number of servers (Part 3, Task 1)
def graphp3t1():
    """
    Plot the mean response times and confidence intervals for doubling the number of servers.
    """
    lower = [row[0] for row in double_serveurs]
    mean = [row[1] for row in double_serveurs]
    upper = [row[2] for row in double_serveurs]

    plt.plot(valeurs_A, lower, label="Borne inférieure")
    plt.plot(valeurs_A, mean, label="Temps moyen de séjour", marker="o")
    plt.plot(valeurs_A, upper, label="Borne supérieure")
    plt.title("Temps moyen de séjour en fonction des valeurs de A (Double Serveurs)")
    plt.xlabel("Taux d'arrivée (A)")
    plt.ylabel("Temps moyen de séjour")
    plt.legend()
    plt.grid(True)
    plt.show()

# Graph for differences compared to initial configuration (Part 3, Task 2)
def graphp3t2():
    """
    Plot the differences in mean response times between initial configuration and each enhancement.
    """
    init_mean = [row[1] for row in init]
    mean_R = [row[1] for row in double_R]
    mean_S = [row[1] for row in double_S]
    mean_serveurs = [row[1] for row in double_serveurs]

    diff_R = [init - r for init, r in zip(init_mean, mean_R)]
    diff_S = [init - s for init, s in zip(init_mean, mean_S)]
    diff_serveurs = [init - srv for init, srv in zip(init_mean, mean_serveurs)]

    plt.plot(valeurs_A, diff_R, label="Différence avec Double Vitesse (R)", marker="o")
    plt.plot(valeurs_A, diff_S, label="Différence avec Double Bande Passante (S)", marker="s")
    plt.plot(valeurs_A, diff_serveurs, label="Différence avec Double Serveurs", marker="^")
    plt.title("Différences par rapport à la configuration initiale")
    plt.xlabel("Taux d'arrivée (A)")
    plt.ylabel("Différence de temps moyen de séjour")
    plt.legend()
    plt.grid(True)
    plt.show()

# Graph for differences among enhanced configurations (Part 3, Task 3)
def graphp3t3():
    """
    Plot the differences in mean response times between the enhanced configurations.
    """
    mean_R = [row[1] for row in double_R]
    mean_S = [row[1] for row in double_S]
    mean_serveurs = [row[1] for row in double_serveurs]

    diff_R_S = [r - s for r, s in zip(mean_R, mean_S)]
    diff_S_serveurs = [s - srv for s, srv in zip(mean_S, mean_serveurs)]
    diff_serveurs_R = [srv - r for srv, r in zip(mean_serveurs, mean_R)]

    plt.plot(valeurs_A, diff_R_S, label="Double Vitesse vs Bande Passante", marker="o")
    plt.plot(valeurs_A, diff_S_serveurs, label="Double Bande Passante vs Serveurs", marker="s")
    plt.plot(valeurs_A, diff_serveurs_R, label="Double Serveurs vs Vitesse", marker="^")
    plt.title("Comparaison entre les configurations améliorées")
    plt.xlabel("Taux d'arrivée (A)")
    plt.ylabel("Différence de temps moyen de séjour")
    plt.legend()
    plt.grid(True)
    plt.show()

# Call the graph functions
graphp2t2()
graphp3t1()
graphp3t2()
graphp3t3()
