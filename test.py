
from flask import Flask, render_template, request, jsonify
import networkx as nx
import random
import math
from colorama import Fore, Back, Style, init
from flask_frozen import Freezer

app = Flask(__name__)

freezer = Freezer(app)

init()  # Para Colorama

Semilla = random.seed(37)  # Para reproducir ejemplos

############################################################################
# Funciones para hacer la digráfica mas estética y ejemplificar la generación de texto
############################################################################

def calculate_positions(G, QN, UnoAbs, DosAbs):
    positions = {}
    num_nodes = len(G.nodes)
    for i, node in enumerate(G.nodes):
        if node in QN:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (3 * math.cos(theta), 3 * math.sin(theta))
        elif node in UnoAbs:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (2 * math.cos(theta), 2 * math.sin(theta))
        elif node in DosAbs:
            theta = (num_nodes / (2 * math.pi)) + (i / (2 * math.pi))
            positions[node] = (math.cos(theta), math.sin(theta))
    return positions

def Color(texto):
    color = ''
    if texto in QN:
        color = 'qn'
    elif texto in UnoAbs:
        color = 'uno'
    elif texto in DosAbs:
        color = 'dos'
    return color

############################################################################
# Creación de la digráfica de co-ocurrencia
############################################################################

def SepararTexto(texto):
    palabra = []
    x = ''

    for letra in texto:
        if letra == " ":
            x += letra
        else:
            if x and x[-1] == " ":
                palabra.append(x)
                x = ""
            x += letra

    if x:
        palabra.append(x)

    palabra[-1] += ' '

    return palabra

def DiGraCo(A):
    Aa = [SepararTexto(A[i]) for i in range(len(A))]

    G = nx.DiGraph()

    for i in range(len(A)):
        for j in range(len(Aa[i]) - 1):
            G.add_edge(Aa[i][j], Aa[i][j + 1])

    return G

A = [
    "Un gato ve un gato.", 
    "Vi un gato. Es naranja.",
    "Es raro ver el color naranja. Excepto en un gato."
]  # Esto es básicamente la base de datos.

G = DiGraCo(A)

############################################################################
# Funciones para calcular quasi-núcleo
############################################################################

nodes = list(G.nodes())

def ConjIndMax(DiGra):
    con = set()
    nodos = list(DiGra.nodes())

    while nodos:
        node = nodos.pop()
        con.add(node)
        nodos = [
            n for n in nodos if not (n in DiGra[node] or node in DiGra[n])
        ]

    return con

def PropDosAbs(G, S):
    for nodo in set(G.nodes) - S:
        if all(
                nx.shortest_path_length(G, nodo, s) > 2 for s in S
                if nx.has_path(G, nodo, s)):
            return False
    return True

def QuasiNucleo(G):
    S = ConjIndMax(G)
    while not PropDosAbs(G, S):
        S = ConjIndMax(G)
    return S

############################################################################
# Calcular un quasi-nucleo de la sub-digrafica
############################################################################

NodosEliminar = []

def SubDiGra(G):
    Nodos = list(reversed(nodes))

    H = G.copy()

    for n in range(0, len(nodes) - 5):
        v = Nodos[n]
        Pred_v = G.predecessors(v)

        H_nodes = list(H.nodes())

        if v in H_nodes:
            NodosEliminar.append(v)
            H.remove_node(v)
            H.remove_nodes_from(Pred_v)

    return H

H = SubDiGra(G)

QN = set()

if not len(H) == 0:
    if nx.is_weakly_connected(H):
        QN = QuasiNucleo(H)
    else:
        for C in nx.weakly_connected_components(H):
            QN.update(QuasiNucleo(H.subgraph(list(C))))

############################################################################
# Completar el quasi-núcleo
############################################################################

Invertir_NodosEliminar = list(reversed(NodosEliminar))

for n in range(0, len(NodosEliminar)):

    QN_copy = QN.copy()

    if any(
            G.has_edge(Invertir_NodosEliminar[n], s)
            or G.has_edge(s, Invertir_NodosEliminar[n]) for s in QN_copy):
        continue
    else:
        QN.add(Invertir_NodosEliminar[n])

UnoAbs = set(v for v in set(G.nodes - QN) if any(
    nx.shortest_path_length(G, v, s) == 1 for s in QN if nx.has_path(G, v, s)))

DosAbs = set(v for v in set(G.nodes - QN - UnoAbs) if any(
    nx.shortest_path_length(G, v, s) == 2 for s in QN if nx.has_path(G, v, s)))

def SigNodo(Nodo1, QNucleo, DiGra):
    if Nodo1 in QNucleo:
        Vecinos = [
            vecino for vecino in DiGra[Nodo1]
            if vecino not in QNucleo and set(Nodo1)
        ]
        if Vecinos:
            return random.choice(Vecinos)
    elif Nodo1 in UnoAbs:
        Vecinos = [vecino for vecino in DiGra[Nodo1] if vecino in QNucleo]
        if Vecinos:
            return random.choice(Vecinos)
    elif Nodo1 in DosAbs:
        Vecinos = [vecino for vecino in DiGra[Nodo1] if vecino in UnoAbs]
        if Vecinos:
            return random.choice(Vecinos)
    return None

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate_text():
    texto_input = request.json.get('text', '')
    
    if not texto_input:
        return jsonify({'response': 'Por favor ingresa un texto.'})
    
    B = [texto_input]
    Bb = SepararTexto(B[0])
    UltNodo = Bb[-1]
    
    Continuator = [{'text': B[0] + ' ', 'color': 'input'}]
    
    for _ in range(50):
        next_node = SigNodo(UltNodo, QN, G)
        if next_node is None:
            break
        elif "." == next_node or "?" in next_node or "!" in next_node:
            Continuator.append({'text': next_node, 'color': Color(next_node)})
            UltNodo = next_node
            break
        
        Continuator.append({'text': next_node, 'color': Color(next_node)})
        UltNodo = next_node
    
    if len(Continuator) <= 1:
        return jsonify({'response': [{'text': 'Perdón no se como responder.', 'color': 'error'}]})
    else:
        return jsonify({'response': Continuator})

if __name__ == '__main__':
    freezer.freeze()  # Generates HTML files in a "build" folder

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
