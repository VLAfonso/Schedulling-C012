# FCFS - First-Come First-Served
def FCFS(processos):
    ordemProcessos = []
    tempoDeEspera = []
    tempoInicial = []
    tempoFinal = []
    tempoAtual = 0

    # Ordenar os processos com base no tempo de chegada
    ordenado = sorted(processos, key=lambda x: x['tempoChegada'])

    for p in ordenado:
        if p['tempoChegada'] > tempoAtual:
            tempoAtual = p['tempoChegada']

        tempoRestante = p['prazoFinal'] - tempoAtual

        if tempoRestante >= p['picoCPU']:
            # Estudo completo
            porcentagemEstudada = 100
            print(f"{p['processo']} - Estudo completo. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            ordemProcessos.append(p['processo'])
            tempoDeEspera.append(tempoAtual - p['tempoChegada'])
            tempoInicial.append(tempoAtual)
            tempoAtual += p['picoCPU']
            tempoFinal.append(tempoAtual)
        elif tempoRestante > 0:
            # Estudo parcial
            tempoEstudado = tempoRestante
            porcentagemEstudada = (tempoEstudado / p['picoCPU']) * 100
            print(f"{p['processo']} - Estudo interrompido. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            ordemProcessos.append(p['processo'])
            tempoDeEspera.append(tempoAtual - p['tempoChegada'])
            tempoInicial.append(tempoAtual)
            tempoAtual += tempoEstudado
            tempoFinal.append(tempoAtual)
        else:
            # Nenhum tempo de estudo válido
            porcentagemEstudada = 0
            print(f"{p['processo']} - Estudo não realizado. {porcentagemEstudada:.2f}% do necessário foi estudado.")

    return ordemProcessos, tempoDeEspera, tempoInicial, tempoFinal

# SJF - Shortest Job Firts
def SJF(processos):
    ordemProcessos = []
    tempoDeEspera = []
    tempoInicial = []
    tempoFinal = []
    tempoAtual = 0

    while True:
        #Verificar se acabaram os processos
        if len(processos)==0:
            break

        # Verificar se os processos já chegaram
        chegaram = [p for p in processos if p['tempoChegada'] <= tempoAtual]
        #Se nenhum chegou, passar o tempo
        if len(chegaram)==0:
            tempoAtual += 1
        else:
            #Selecionar próximo processo e removê-lo dos processos restantes
            processoAtual = min(chegaram, key=lambda x: x['picoCPU'])
            processos.remove(processoAtual)

            tempoRestante = processoAtual['prazoFinal'] - tempoAtual

        if tempoRestante >= processoAtual['picoCPU']:
            porcentagemEstudada = 100
            print(f"{processoAtual['processo']} - Estudo completo. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            tempoInicial.append(tempoAtual)
            tempoAtual += processoAtual['picoCPU']
            tempoFinal.append(tempoAtual)
        elif tempoRestante > 0:
            tempoEstudado = tempoRestante
            porcentagemEstudada = (tempoEstudado / processoAtual['picoCPU']) * 100
            print(f"{processoAtual['processo']} - Estudo parcial. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            tempoInicial.append(tempoAtual)
            tempoAtual += tempoEstudado
            tempoFinal.append(tempoAtual)
        else:
            porcentagemEstudada = 0
            print(f"{processoAtual['processo']} - Estudo não realizado. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            tempoInicial.append(None)
            tempoFinal.append(None)

        ordemProcessos.append(processoAtual['processo'])
        tempoDeEspera.append(max(0, tempoAtual - processoAtual['tempoChegada']))

    return ordemProcessos, tempoDeEspera, tempoInicial, tempoFinal

# PS - Priority Scheduling
def PS(processos):
    ordemProcessos = []
    tempoDeEspera = []
    tempoInicial = []
    tempoFinal = []
    tempoAtual = 0

    processos_restantes = processos.copy()

    while processos_restantes:
        prontos = [p for p in processos_restantes if p['tempoChegada'] <= tempoAtual]
        if not prontos:
            tempoAtual += 1
            continue

        processoAtual = min(prontos, key=lambda x: x['prioridade'])
        processos_restantes.remove(processoAtual)

        tempoRestante = processoAtual['prazoFinal'] - tempoAtual

        if tempoRestante >= processoAtual['picoCPU']:
            porcentagemEstudada = 100
            print(f"{processoAtual['processo']} - Estudo completo. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            tempoInicial.append(tempoAtual)
            tempoAtual += processoAtual['picoCPU']
            tempoFinal.append(tempoAtual)
        elif tempoRestante > 0:
            tempoEstudado = tempoRestante
            porcentagemEstudada = (tempoEstudado / processoAtual['picoCPU']) * 100
            print(f"{processoAtual['processo']} - Estudo parcial. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            tempoInicial.append(tempoAtual)
            tempoAtual += tempoEstudado
            tempoFinal.append(tempoAtual)
        else:
            porcentagemEstudada = 0
            print(f"{processoAtual['processo']} - Estudo não realizado. {porcentagemEstudada:.2f}% do necessário foi estudado.")
            tempoInicial.append(None)
            tempoFinal.append(None)

        ordemProcessos.append(processoAtual['processo'])
        tempoDeEspera.append(max(0, tempoAtual - processoAtual['tempoChegada']))

    return ordemProcessos, tempoDeEspera, tempoInicial, tempoFinal

# RR - Round Robin Scheduling
def RR(processos, quantum):
    ordemProcessos = []
    filaDeExecucao = []
    temposIniciais = {}
    temposFinais = {}
    tempoDeEspera = {p['processo']: 0 for p in processos}
    tempoAtual = 0
    fila = sorted(processos, key=lambda x: x['tempoChegada'])
    temposRestantes = {p['processo']: p['picoCPU'] for p in processos}
    processosFinalizados = set()

    while fila or filaDeExecucao:
        while fila and fila[0]['tempoChegada'] <= tempoAtual:
            filaDeExecucao.append(fila.pop(0))

        if not filaDeExecucao:
            tempoAtual += 1
            continue

        processoAtual = filaDeExecucao.pop(0)
        nome = processoAtual['processo']

        if nome not in temposIniciais:
            temposIniciais[nome] = tempoAtual

        tempoRestante = processoAtual['prazoFinal'] - tempoAtual
        tempoExecutado = min(quantum, temposRestantes[nome], max(0, tempoRestante))

        temposRestantes[nome] -= tempoExecutado
        tempoAtual += tempoExecutado

        if temposRestantes[nome] == 0 or tempoRestante <= 0:
            if nome not in processosFinalizados:
                totalEstudado = processoAtual['picoCPU'] - temposRestantes[nome]
                porcentagemEstudada = (totalEstudado / processoAtual['picoCPU']) * 100
                if porcentagemEstudada == 100:
                    print(f"{nome} - Estudo completo. {porcentagemEstudada:.2f}% do necessário foi estudado.")
                elif porcentagemEstudada > 0:
                    print(f"{nome} - Estudo parcial. {porcentagemEstudada:.2f}% do necessário foi estudado.")
                else:
                    print(f"{nome} - Estudo não realizado. {porcentagemEstudada:.2f}% do necessário foi estudado.")

                temposFinais[nome] = tempoAtual
                processosFinalizados.add(nome)
        else:
            filaDeExecucao.append(processoAtual)

        ordemProcessos.append(nome)

    tempoInicial = [temposIniciais.get(p['processo'], None) for p in processos]
    tempoFinal = [temposFinais.get(p['processo'], None) for p in processos]
    tempoDeEspera = [max(0, temposIniciais[p['processo']] - p['tempoChegada']) if p['processo'] in temposIniciais else 0 for p in processos]

    return ordemProcessos, tempoDeEspera, tempoInicial, tempoFinal

prova1 = {'processo': 'Sistemas Operacionais', 'tempoChegada': 0, 'picoCPU': 5, 'prioridade': 1, 'prazoFinal': 6} #picoCPU = quantos dias são necessários de estudo para cobrir toda a matéria
prova2 = {'processo': 'Análise de dados', 'tempoChegada': 0, 'picoCPU': 2, 'prioridade': 4, 'prazoFinal': 6}
prova3 = {'processo': 'Inteligência Computacional', 'tempoChegada': 0, 'picoCPU': 3, 'prioridade': 3, 'prazoFinal': 5}
prova4 = {'processo': 'Redes', 'tempoChegada': 0, 'picoCPU': 7, 'prioridade': 2, 'prazoFinal': 10}

print("Resultados dos Estudos:")
print("FCFS:")
fcfs = FCFS([prova1, prova2, prova3, prova4])
print("-"*15)
print("SJF:")
sjf =SJF([prova1, prova2, prova3, prova4])
print("-"*15)
print("PS:")
ps = PS([prova1, prova2, prova3, prova4])
print("-"*15)
print("RR:")
rr = RR([prova1, prova2, prova3, prova4], 2) #estabelecendo um quantum de dois dias
print("-"*15)

print("Informações dos Escalonamentos:")
print("FCFS:")
for i in range(len(fcfs[0])):
    print(f"Matéria: {fcfs[0][i]} - Tempo de espera: {fcfs[1][i]} - Tempo inicial: {fcfs[2][i]} - Tempo final: {fcfs[3][i]}")
print("-"*15)
print("SJF:")
for i in range(len(sjf[0])):
    print(f"Matéria: {sjf[0][i]} - Tempo de espera: {sjf[1][i]} - Tempo inicial: {sjf[2][i]} - Tempo final: {sjf[3][i]}")
print("-"*15)
print("PS:")
for i in range(len(ps[0])):
    if ps[2][i] != None:
        print(f"Matéria: {ps[0][i]} - Tempo de espera: {ps[1][i]} - Tempo inicial: {ps[2][i]} - Tempo final: {ps[3][i]}")
print("-"*15)
print("RR:")
for i in range(len(rr[1])):
    print(f"Matéria: {rr[0][i]} - Tempo de espera: {rr[1][i]} - Tempo inicial: {rr[2][i]} - Tempo final: {rr[3][i]}")
print("-"*15)