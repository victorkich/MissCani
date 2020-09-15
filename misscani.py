import time


Missionarios = 3
Canibais = 3
n_Barco = 2
OP = []

for i in range(n_Barco+1):
    for j in range(n_Barco+1):
        if i+j != 0 and i+j <= n_Barco and not (j > i > 0):
            OP.append([i, j])

print("Possíveis barcos:", OP)

NODES = []
T_NODES = []


class Margem:
    def __init__(self, M, C):
        self.M = M
        self.C = C
    
    def compara_Margens(margem_A,margem_B):
        if margem_A.M == margem_B.M and margem_A.C == margem_B.C:
            return True
        else:
            return False
    
    def __str__(self):
        return str(self.M) + " missionários e " + str(self.C) + " canibais"


class Barco:
    def __init__(self, M, C):
        self.M = M
        self.C = C
    
    def atravessa(self, margem_A, margem_B):
        margem_A.M = margem_A.M - self.M
        margem_A.C = margem_A.C - self.C
        margem_B.M = margem_B.M + self.M
        margem_B.C = margem_B.C + self.C


class Estado:
    def __init__(self, margem_E, margem_D, rodada):
        self.margem_E = margem_E
        self.margem_D = margem_D
        self.rodada = rodada

        self.valido = self.teste_Estado()
        self.is_Objetivo = self.teste_Objetivo()
        self.P = []
        self.OPRS = []

    def teste_Estado(self):
        if (self.margem_E.C > self.margem_E.M > 0) or (self.margem_D.C > self.margem_D.M > 0):
            return False
        elif (self.margem_E.C < 0) or (self.margem_E.M < 0) or (self.margem_D.C < 0) or (self.margem_D.M < 0):
            return False
        else:
            return True
    
    def teste_Objetivo(self):
        if self.margem_E.C == Canibais and self.margem_E.M == Missionarios:
            return True
        else:
            return False
        
    def set_Possibs(self):
        for op in OP:
            barco = Barco(op[0], op[1])
            
            margem_D = Margem(self.margem_D.M, self.margem_D.C)
            margem_E = Margem(self.margem_E.M, self.margem_E.C)
                        
            if self.rodada % 2 == 0:
                barco.atravessa(margem_D, margem_E)
                
            else:
                barco.atravessa(margem_E, margem_D)
            
            new = Estado(margem_E, margem_D, self.rodada+1)
            
            if new.valido:
                for j in self.OPRS:
                    new.OPRS.append(j)
                new.OPRS.append(op)
                self.P.append(new)

    def compara_Estados(estado_A, estado_B):
        if Margem.compara_Margens(estado_A.margem_D, estado_B.margem_D) and Margem.compara_Margens(estado_A.margem_E, estado_B.margem_E):
            return True
        else:
            return False

    def __str__(self):
        return "Operadores:" + str(self.OPRS) + "\nMargem Esquerda: " + str(self.margem_E) + "\nMargem Direita: " + str(self.margem_D) + "\nRodada: " + str(self.rodada)


def main():
    estado_Inicial = Estado(Margem(0, 0), Margem(Missionarios, Canibais), 0)
    NODES.append(estado_Inicial)
    
    rod_Ant = 0
    cont = 0
    loop = True
    while loop:
        if len(NODES) > 0:
            if NODES[0].is_Objetivo:
                print("Objetivo encontrado!")
                print(NODES[0])
                print("Na tentativa:", cont)
                loop = False
                                
            else:
                NODES[0].set_Possibs()
                for p in NODES[0].P:
                    f = 0
                    for n in T_NODES:
                        if Estado.compara_Estados(NODES[0], n) and NODES[0].rodada % 2 == n.rodada % 2 and NODES[0].rodada > n.rodada:
                            f = 1
                    if f == 0:    
                        NODES.append(p)
                    
            if NODES[0].rodada > rod_Ant:
                rod_Ant = NODES[0].rodada
                print(time.strftime("\n[%H:%M:%S]"))
                print(NODES[0].rodada)
                print("Testadas:", cont, "possibilidades")
                print(len(NODES)-len(NODES[0].P), "possibilidades a serem testadas\n")
            
            T_NODES.append(NODES[0])
            NODES.remove(NODES[0])
            cont = cont + 1
        else:
            print("Todas as possibilidades foram testadas\nSolução não existe")
            loop = False
    NODES.clear()


if __name__ == "__main__":
    main()
    print("\nMissionários:", Missionarios)
    print("Canibais:", Canibais)
    print("Max no barco:", n_Barco)
    print("Possíveis barcos:", OP)
