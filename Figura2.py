# %% Il seguente script crea il grafico della IRF come definita da Joos et al (2013)


import numpy as np
import matplotlib.pyplot as plt


# Definisci la funzione
def IRF(t):
    return 21.73 + 22.4 * np.exp(-t / 394.4) + 28.24 * np.exp(-t / 36.54) + 27.63 * np.exp(-t / 4.304)

# Genera un intervallo di valori di tempo
t = np.linspace(0, 1000, 500)

# Calcola i valori corrispondenti di IRF
y = IRF(t)

# Normalizza i valori di y nell'intervallo [0, 1]
y_normalized = y / 100

# Creazione del grafico
plt.figure(figsize=(10, 6))
plt.plot(t, y_normalized, label='IRF', color='blue')
plt.xlabel('Tempo trascorso dall\'emissione (anni)')
plt.ylabel('Frazione che persiste nell\'atmosfera')
plt.xlim(0, 1000)
plt.ylim(0, 1.1)
plt.legend()
plt.title('IRF')
plt.grid(True)

# Salva il grafico nella directory specificata
directory_path = r'C:\thesis\python'
file_path = directory_path + r'\fig2.pdf'
plt.savefig(file_path, bbox_inches='tight')
# Mostra il grafico
plt.show()