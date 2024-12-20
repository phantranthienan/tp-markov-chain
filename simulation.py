import ciw
import numpy as np
from statistics import stdev 
import math
from scipy.stats import t

# Définir les paramètres du modèle
I = 0.001  # Temps d'initialisation
Y = 0.0001  # Temps de traitement statique
#R = 10000
#S = 1500
C = 707  # Bande passante réseau client (en Kbps)
B = 16  # Taille du tampon (en Ko)
F = 42.2  # Taille moyenne des fichiers (en Ko)
warmup = 10  # Temps de réchauffement
maxsimtime = 40  # Durée de la simulation principale
cooldown = 10  # Temps de refroidissement
precision = 0.8  # Niveau de précision pour l'intervalle de confiance

# Fonction pour créer le réseau de files d'attente
def simulation(a,ser,s,r):
    """
    Crée un réseau de files d'attente CIW avec les paramètres donnés.
    """
    A = a
    S = s
    R = r
    nb_serveur_SR = ser
    transition_matrix = [
        [0, 1, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 0, 1],
        [0, 1-B/F, 0, 0]
    ]
    
    # Convertir en float pour éviter les erreurs
    transition_matrix = [[float(value) for value in row] for row in transition_matrix]
    
    N = ciw.create_network(
        arrival_distributions=[ciw.dists.Exponential(rate=A),  # SI
                               ciw.dists.Deterministic(float('inf')),  # SR
                               ciw.dists.Deterministic(float('inf')),  # SS
                               ciw.dists.Deterministic(float('inf'))],  # SC
        service_distributions=[ciw.dists.Deterministic(value=I),  # SI
                               ciw.dists.Exponential(rate=1/(Y+B/R)),  # SR
                               ciw.dists.Deterministic(value=B/S),  # SS
                               ciw.dists.Deterministic(value=B/C)],  # SC
        routing=transition_matrix,
        number_of_servers=[1, nb_serveur_SR, 1, 1]

    )
    return N

# Fonction pour calculer les statistiques de temps de séjour
def stats(a, ser, s, r):
    """
    Effectue 10 simulations pour le réseau donné et retourne les statistiques :
    - Moyenne des bornes inférieures
    - Moyenne des temps de séjour
    - Moyenne des bornes supérieures
    """
    # Créer le réseau de files d'attente
    N = simulation(a, ser, s, r)
    print(f"Simulation pour A = {a}")

    all_mean_response_times = []  # Moyennes des temps de séjour
    all_lower_bounds = []  # Bornes inférieures des intervalles
    all_upper_bounds = []  # Bornes supérieures des intervalles

    # Exécuter plusieurs essais pour réduire la variance
    for trial in range(10):
        ciw.seed(trial)
        Q = ciw.Simulation(N)
        Q.simulate_until_max_time(maxsimtime + warmup + cooldown)
        records = Q.get_all_records()

        # Temps de séjour pour chaque requête
        response_times = [
            rec2.service_end_date - rec1.arrival_date
            for rec1 in records for rec2 in records
            if rec1.node == 1 and rec2.destination == -1
            and rec1.id_number == rec2.id_number
            and warmup < rec1.arrival_date < (warmup + maxsimtime)
        ]

        # Calcul des moyennes et intervalles de confiance
        if response_times:
            mean_response_time = np.mean(response_times)
            all_mean_response_times.append(mean_response_time)

            sample_mean = mean_response_time
            t_value = t.ppf(precision, len(response_times) - 1)
            confidence_half_width = (stdev(response_times) * t_value) / math.sqrt(len(response_times))
            lower_bound = sample_mean - confidence_half_width
            upper_bound = sample_mean + confidence_half_width

            all_lower_bounds.append(lower_bound)
            all_upper_bounds.append(upper_bound)

    # Moyennes globales pour les simulations
    overall_mean_response_time = np.mean(all_mean_response_times)
    overall_lower_bound = np.mean(all_lower_bounds)
    overall_upper_bound = np.mean(all_upper_bounds)

    return [overall_lower_bound, overall_mean_response_time, overall_upper_bound]


# results=stats(15,1,1500,10000)
# print("***** Résultat sur 10 simulations avec A=15 *****")
# print("Temps moyen de séjour : ",results[1])

# results=stats(30,1,1500,10000)
# print("***** Résultat sur 10 simulations avec A=30 *****")
# print("Temps moyen de séjour : ",results[1])


# Fonction pour exécuter les simulations et sauvegarder les résultats
def execute_and_save(valeurs_A, ser, s, r, filename):
    """
    Exécute les simulations pour une configuration donnée et enregistre les résultats.
    """
    results = [stats(a, ser, s, r) for a in valeurs_A]
    print(f"Résultats pour {filename}: {results}")
    with open(filename, "w") as f:
        f.write(f"{results}\n")

# Plage des taux d'arrivée
valeurs_A = np.arange(10, 41)

# Exécuter les simulations pour chaque configuration
execute_and_save(valeurs_A, ser=1, s=1500, r=10000, filename="init.txt")  # Configuration initiale
# execute_and_save(valeurs_A, ser=2, s=1500, r=10000, filename="double_serveurs.txt")  # Doubler le nombre de serveurs
# execute_and_save(valeurs_A, ser=1, s=3000, r=10000, filename="double_bande.txt")  # Doubler la bande passante (S)
# execute_and_save(valeurs_A, ser=1, s=1500, r=20000, filename="double_vitesse.txt")  # Doubler la vitesse dynamique (R)
