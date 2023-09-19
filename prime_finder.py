import multiprocessing
import argparse
import csv
import math

def e_primo(n):
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True

def encontrar_primos(inicio, fim):
    primos = []
    for num in range(inicio, fim + 1):
        if e_primo(num):
            primos.append(num)
    return primos

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Encontre números primos em uma faixa específica.")
    parser.add_argument("--workers", type=int, default=multiprocessing.cpu_count(), help="Número de workers (padrão: número de CPUs)")
    parser.add_argument("--start", type=int, default=1, help="Início da faixa de números primos")
    parser.add_argument("--end", type=int, default=100, help="Fim da faixa de números primos")
    args = parser.parse_args()

    with multiprocessing.Pool(processes=args.workers) as pool:
        tamanho_do_grupo = math.ceil((args.end - args.start + 1) / args.workers)
        intervalos = [(i, min(i + tamanho_do_grupo - 1, args.end)) for i in range(args.start, args.end + 1, tamanho_do_grupo)]
        resultados = pool.starmap(encontrar_primos, intervalos)

    with open("numeros_primos.csv", mode="w", newline="") as arquivo:
        escritor = csv.writer(arquivo)
        escritor.writerow(["Início do Intervalo", "Fim do Intervalo", "Números Primos"])
        for i, resultado in enumerate(resultados):
            escritor.writerow([intervalos[i][0], intervalos[i][1], resultado])
