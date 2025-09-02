import random
import matplotlib.pyplot as plt

def local_search(solution, neighborhood_fn, evaluate):
    best = solution
    for neighbor in neighborhood_fn(solution):
        if evaluate(neighbor) > evaluate(best):
            best = neighbor
    return best

def VND(initial, neighborhoods, evaluate, max_iter=100):
    sol = initial
    history = [evaluate(sol)]
    k, it = 0, 0
    while k < len(neighborhoods) and it < max_iter:
        it += 1
        temp = local_search(sol, neighborhoods[k], evaluate)
        val_temp, val_sol = evaluate(temp), history[-1]
        if val_temp > val_sol:
            sol = temp
            history.append(val_temp)
            k = 0
        else:
            history.append(val_sol)
            k += 1
    return sol, history

def shaking(solution):
    sol = solution.copy()
    i, j = sorted(random.sample(range(len(sol)), 2))
    sol[i:j+1] = reversed(sol[i:j+1])
    return sol

def BasicVNS(initial, neighborhood_fn, evaluate, max_iter=100):
    sol = initial
    history = [evaluate(sol)]
    it = 0
    while it < max_iter:
        it += 1
        perturbed = shaking(sol)
        improved = local_search(perturbed, neighborhood_fn, evaluate)
        val_improved = evaluate(improved)
        val_sol = history[-1]
        if val_improved > val_sol:
            sol = improved
            history.append(val_improved)
        else:
            history.append(val_sol)
    return sol, history

# — Ejemplo de problema con datos diseñados para destacar diferencias —
n = 30
initial = [random.randint(0, 1) for _ in range(n)]
evaluate = lambda sol: sum(sol)

def neigh_flip_one(sol):
    for i in range(len(sol)):
        neighbor = sol.copy()
        neighbor[i] = 1 - neighbor[i]
        yield neighbor

# Ejecutamos ambos algoritmos
best_vnd, hist_vnd = VND(initial, [neigh_flip_one], evaluate, max_iter=200)
best_vns, hist_vns = BasicVNS(initial, neigh_flip_one, evaluate, max_iter=200)

# Graficar
plt.figure(figsize=(10, 6))
plt.plot(hist_vnd, label='Búsqueda Descendente (VND)')
plt.plot(hist_vns, label='Basic VNS', linestyle='--')
plt.xlabel("Iteraciones")
plt.ylabel("Valor de la función objetivo")
plt.title("Comparación: VND vs Basic VNS")
plt.legend()
plt.grid(True)
plt.show()

print("Solución inicial:", evaluate(initial))
print("Mejor VND:", evaluate(best_vnd), "| Mejor VNS:", evaluate(best_vns))


