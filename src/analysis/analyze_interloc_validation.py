import csv
import matplotlib.pyplot as plt
import numpy as np


def analyze_validation(filename):
    with open(filename) as file:
        reader = csv.DictReader(file)
        data = list(reader)

        valid_angle_data = list(filter(lambda d: (float(d['Azimuth']) < 9999), data))

        calculated_angles = np.array([float(v['Azimuth']) for v in valid_angle_data])
        expected_angles = np.array([float(v['angle']) for v in valid_angle_data])

        unique_angles = np.unique(expected_angles)
        mean_calculated_angles = np.zeros(unique_angles.shape)
        std_calculated_angles = np.zeros(unique_angles.shape)

        for i in range(len(mean_calculated_angles)):
            data_points = list(filter(lambda d: (float(d['angle']) == unique_angles[i]), valid_angle_data))
            mean_calculated_angles[i] = np.mean([float(v['Azimuth']) for v in data_points])
            std_calculated_angles[i] = np.std([float(v['Azimuth']) for v in data_points])

        plt.figure()
        plt.title("Sortie du HiveBoard")
        plt.xlabel("Angle réel (°)")
        plt.ylabel("Angle mesuré (°)")
        plt.plot(expected_angles, calculated_angles, '.')
        plt.plot(unique_angles, mean_calculated_angles, '-')

        plt.figure()
        plt.title("Précision de l'angle mesuré")
        plt.xlabel("Angle Réel (°)")
        plt.ylabel("Erreur absolue (°)")
        plt.plot(unique_angles, np.abs(unique_angles - mean_calculated_angles), '.')

        plt.figure()
        plt.title("Écart-type de l'angle calculé")
        plt.xlabel("Angle Réel (°)")
        plt.ylabel("Écart-type (°)")
        plt.plot(unique_angles, std_calculated_angles, '.')

        plt.show()


analyze_validation("../data/validation_hb6.csv")