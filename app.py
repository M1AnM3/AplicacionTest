
from flask import Flask, render_template, request, jsonify
import networkx as nx
import random
from colorama import Fore, Back, Style, init

app = Flask(__name__)

init()  # Para Colorama

############################################################################
# Funciones para hacer la digráfica mas estética y ejemplificar la generación de texto
############################################################################

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
    "Es raro ver el color naranja. Excepto en un gato.",
    "Un conjunto es una colección bien definida de objetos distintos.",
    "Dos conjuntos son iguales si tienen exactamente los mismos elementos.",
    "El conjunto vacío no contiene ningún elemento.",
    "La unión de dos conjuntos contiene todos los elementos que pertenecen a al menos uno de ellos.",
    "La intersección de dos conjuntos contiene solo los elementos que están en ambos.",
    "La diferencia de conjuntos A y B contiene los elementos que están en A pero no en B.",
    "Un conjunto A es subconjunto de B si todo elemento de A también está en B.",
    "La relación de pertenencia se denota por el símbolo ∈.",
    "El conjunto de las partes de A, denotado 𝒫(A), contiene todos los subconjuntos de A.",
    "El producto cartesiano de A y B es el conjunto de todos los pares ordenados (a, b) con a ∈ A y b ∈ B.",
    "Un conjunto puede ser finito, infinito numerable o no numerable.",
    "El conjunto de los números naturales es un conjunto infinito numerable.",
    "El conjunto de los números reales no es numerable.",
    "Georg Cantor fue el pionero de la teoría de conjuntos.",
    "Dos conjuntos tienen la misma cardinalidad si existe una biyección entre ellos.",
    "La cardinalidad del conjunto de los números naturales es ℵ₀ (aleph-cero).",
    "La paradoja de Russell revela problemas en la teoría ingenua de conjuntos.",
    "La teoría axiomática de conjuntos, como ZFC, evita paradojas mediante restricciones.",
    "Un conjunto puede contener otros conjuntos como elementos.",
    "La notación por comprensión define un conjunto especificando una propiedad.",
    "La unión disjunta de dos conjuntos considera a sus elementos como distintos incluso si son iguales.",
    "El principio del conjunto extensional dice que los conjuntos están determinados por sus elementos.",
    "El conjunto universal no existe en ZFC para evitar contradicciones.",
    "El axioma de elección permite seleccionar un elemento de cada conjunto en una colección arbitraria.",
    "El lema de Zorn es equivalente al axioma de elección.",
    "La función característica de un subconjunto A de X es una función de X en {0,1}.",
    "Un conjunto finito tiene una cantidad exacta de elementos que puede contarse.",
    "El conjunto de las funciones de A en B es denotado B^A.",
    "La intersección arbitraria de conjuntos puede ser vacía.",
    "La teoría de conjuntos es el lenguaje fundacional de las matemáticas.",
    "Las relaciones binarias se definen como subconjuntos del producto cartesiano.",
    "Una relación de equivalencia es reflexiva, simétrica y transitiva.",
    "Una partición de un conjunto está asociada a una relación de equivalencia.",
    "Un conjunto parcialmente ordenado tiene una relación de orden parcial.",
    "Las clases propias son colecciones que no pueden ser conjuntos en ZFC.",
    "Un conjunto inductivo contiene al 0 y es cerrado bajo sucesión.",
    "El axioma del infinito garantiza la existencia de un conjunto infinito.",
    "Las operaciones con conjuntos siguen leyes como la distributiva, conmutativa y asociativa.",
    "El diagrama de Venn representa gráficamente relaciones entre conjuntos.",
    "Los ordinales extienden el concepto de posición más allá de lo finito.",
    "Una topología sobre un conjunto X es una colección de subconjuntos abiertos que contiene a X y al vacío y es cerrada bajo uniones arbitrarias e intersecciones finitas.",
    "Un conjunto abierto depende de la topología elegida.",
    "Un espacio topológico es un par (X, τ), donde τ es una topología sobre X.",
    "La topología discreta es aquella donde todos los subconjuntos son abiertos.",
    "La topología trivial solo contiene a X y al conjunto vacío.",
    "Un conjunto cerrado es aquel cuyo complemento es abierto.",
    "Un espacio es conexo si no puede dividirse en dos abiertos disjuntos no vacíos.",
    "Un espacio es compacto si toda cubierta abierta tiene un subcubrimiento finito.",
    "En ℝ, los intervalos abiertos son conjuntos abiertos.",
    "El cierre de un conjunto es el menor cerrado que lo contiene.",
    "El interior de un conjunto es el mayor abierto contenido en él.",
    "La frontera de un conjunto es el conjunto de puntos adherentes que no están en su interior.",
    "Un punto de acumulación de A es uno tal que toda vecindad suya intersecta A en algún punto distinto.",
    "Una base de topología es una colección de abiertos que generan todos los demás.",
    "El espacio ℝⁿ con la topología euclidiana es uno de los ejemplos fundamentales.",
    "La continuidad se define en términos de la preimagen de abiertos.",
    "Un homeomorfismo es una función continua, biyectiva, con inversa continua.",
    "Dos espacios son topológicamente equivalentes si existe un homeomorfismo entre ellos.",
    "La topología del orden es generada por intervalos abiertos de la forma (a, b).",
    "La métrica induce una topología en un espacio métrico.",
    "Un espacio es Hausdorff si todo par de puntos distintos tiene vecindades disjuntas.",
    "La topología cociente resulta de identificar puntos según una relación de equivalencia.",
    "La topología producto de dos espacios topológicos se construye con bases formadas por productos de abiertos.",
    "El teorema de Tychonoff dice que el producto arbitrario de espacios compactos es compacto.",
    "Un espacio de Alexandrov tiene cerraduras finitas bajo intersección.",
    "La convergencia de sucesiones puede variar según la topología del espacio.",
    "El conjunto de funciones continuas entre dos espacios forma un objeto de estudio en topología funcional.",
    "La separación de conjuntos mediante funciones continuas caracteriza ciertas propiedades del espacio.",
    "El lema de Urysohn caracteriza los espacios normales.",
    "La propiedad de Lindelöf indica que toda cubierta abierta tiene un subcubrimiento numerable.",
    "La topología fina es la más grande que hace continua a una familia dada de funciones.",
    "Los espacios conexos por caminos generalizan la idea de “camino entre puntos”.",
    "Un retracto es un subconjunto con una función de retracción continua.",
    "La topología es fundamental en el estudio de variedades y geometría diferencial.",
    "El teorema de Brouwer establece que toda función continua de un disco cerrado en sí mismo tiene un punto fijo.",
    "Una categoría consiste en objetos y morfismos entre ellos, con composición asociativa y morfismos identidad.",
    "Los conjuntos y funciones forman una categoría llamada Set.",
    "En la categoría Top, los objetos son espacios topológicos y los morfismos son funciones continuas.",
    "Un morfismo que tiene inverso es un isomorfismo.",
    "Un funtor es una función entre categorías que preserva estructuras.",
    "Los funtores covariantes preservan la dirección de los morfismos.",
    "Los funtores contravariantes invierten la dirección de los morfismos.",
    "Una transformación natural es una manera de comparar dos funtores entre las mismas categorías.",
    "Dos categorías son equivalentes si hay funtor y transformación natural que lo demuestran.",
    "El producto categórico generaliza el producto cartesiano de conjuntos.",
    "Un objeto inicial tiene un único morfismo hacia cualquier otro objeto.",
    "Un objeto final recibe un único morfismo desde cualquier objeto.",
    "Un límite en una categoría generaliza conceptos como productos e intersecciones.",
    "Un colímite generaliza uniones y sumas directas.",
    "El adjunto de un funtor es otro funtor que establece una biyección natural entre ciertos conjuntos de morfismos.",
    "La categoría opuesta de C invierte la dirección de todos sus morfismos.",
    "Un pullback es un tipo de límite que generaliza la intersección de conjuntos con función común.",
    "Un pushout es un tipo de colímite que generaliza la unión disjunta con identificación.",
    "El Yoneda Lemma relaciona objetos con representaciones vía conjuntos de morfismos.",
    "Todo funtor representable está determinado por el Yoneda embedding.",
    "Una categoría se dice abeliana si tiene estructura suficiente para estudiar homología.",
    "Las categorías enriquecidas tienen hom-sets con estructura adicional, como espacio vectorial o topología.",
    "Los diagramas conmutativos permiten visualizar condiciones en categorías.",
    "La teoría de categorías proporciona un lenguaje unificador para muchas ramas de las matemáticas.",
    "Muchos conceptos algebraicos pueden reformularse categóricamente, como los grupos, anillos y módulos.",
    "tiren paro",
    "paro el tren",
    "El sol brilla en el cielo",
    "La noche es tranquila",
    "Aprender Python es divertido",
    "Hoy hace mucho calor",
    "La música alegra el alma",
    "Estoy leyendo un libro interesante",
    "La tecnología avanza rápido",
    "Me gusta el café por la mañana",
    "El mar es hermoso",
    "La montaña es imponente",
    "Los gatos duermen mucho",
    "Los perros son leales",
    "La lluvia cae suavemente",
    "El viento sopla fuerte",
    "Voy a salir a caminar",
    "La comida está deliciosa",
    "El cielo está nublado",
    "Me encanta viajar",
    "Estoy estudiando programación",
    "La vida es un aprendizaje",
    "El tiempo pasa rápido",
    "La luna está llena",
    "El bosque es misterioso",
    "Las estrellas brillan",
    "Estoy escuchando música",
    "El día fue productivo",
    "La noche es larga",
    "Quiero aprender algo nuevo",
    "La creatividad es importante",
    "La práctica hace al maestro",
    "Estoy escribiendo código",
    "El clima está agradable",
    "Me gusta el cine",
    "El arte es expresión",
    "La lectura abre la mente",
    "El ejercicio es saludable",
    "La ciudad está llena de vida",
    "El campo es tranquilo",
    "Estoy tomando agua",
    "El café está caliente",
    "La sopa está rica",
    "Voy a descansar",
    "Estoy motivado",
    "La energía es positiva",
    "El día comienza bien",
    "La tarde es relajada",
    "La noche invita a pensar",
    "El silencio es paz",
    "La música es vida",
    "Estoy feliz hoy",
    "La tecnología conecta al mundo",
    "El conocimiento es poder",
    "La práctica constante ayuda",
    "El éxito requiere esfuerzo",
    "La paciencia es clave",
    "La disciplina importa",
    "La mente es poderosa",
    "El cuerpo necesita descanso",
    "La naturaleza inspira",
    "La lluvia refresca",
    "El sol calienta",
    "La nieve es fría",
    "El otoño es hermoso",
    "La primavera florece",
    "El verano es intenso",
    "El invierno es tranquilo",
    "La amistad es valiosa",
    "El amor es importante",
    "La familia es apoyo",
    "La educación transforma",
    "La ciencia explica",
    "La historia enseña",
    "La filosofía cuestiona",
    "El arte emociona",
    "La música inspira",
    "El deporte motiva",
    "La salud es prioridad",
    "La comida nutre",
    "El agua da vida",
    "El aire es esencial",
    "La tierra sostiene",
    "El fuego transforma",
    "La mente crea",
    "El cuerpo actúa",
    "La emoción guía",
    "La razón analiza",
    "El tiempo cura",
    "La experiencia enseña",
    "La curiosidad impulsa",
    "La imaginación vuela",
    "La realidad sorprende",
    "El cambio es constante",
    "La vida sigue",
    "El futuro llega",
    "El presente importa",
    "El pasado enseña",
    "La esperanza vive",
    "La fe sostiene",
    "La acción construye",
    "La calma ayuda",
    "La alegría contagia",
    "La paz interior importa"
    "¿Capital de Francia? París",
    "¿Capital de España? Madrid",
    "¿Capital de Italia? Roma",
    "¿Capital de Alemania? Berlín",
    "¿Capital de Portugal? Lisboa",
    "¿Capital de México? Ciudad de México",
    "¿Capital de Estados Unidos? Washington D.C.",
    "¿Capital de Japón? Tokio",
    "¿Capital de China? Pekín",
    "¿Capital de Canadá? Ottawa",
    "¿Capital de Brasil? Brasilia",
    "¿Capital de Argentina? Buenos Aires",
    "¿Capital de Chile? Santiago",
    "¿Capital de Perú? Lima",
    "¿Capital de Colombia? Bogotá",
    "¿Capital de Bolivia? La Paz",
    "¿Capital de Uruguay? Montevideo",
    "¿Capital de Paraguay? Asunción",
    "¿Capital de Ecuador? Quito",
    "¿Capital de Venezuela? Caracas",

    "¿Cuánto es 2+2? 4",
    "¿Cuánto es 3+5? 8",
    "¿Cuánto es 10-4? 6",
    "¿Cuánto es 7×6? 42",
    "¿Cuánto es 81÷9? 9",
    "¿Cuánto es 5 al cuadrado? 25",
    "¿Cuánto es 12+8? 20",
    "¿Cuánto es 100-25? 75",
    "¿Cuánto es 9×9? 81",
    "¿Cuánto es 64÷8? 8",
    "¿Cuánto es 15+15? 30",
    "¿Cuánto es 50-20? 30",
    "¿Cuánto es 11×11? 121",
    "¿Cuánto es 144÷12? 12",
    "¿Cuánto es 7+9? 16",
    "¿Cuánto es 18-3? 15",
    "¿Cuánto es 6×7? 42",
    "¿Cuánto es 49÷7? 7",
    "¿Cuánto es 13+14? 27",
    "¿Cuánto es 20×2? 40",
    "¿Fórmula del agua? H2O",
    "¿Símbolo del oxígeno? O",
    "¿Símbolo del hidrógeno? H",
    "¿Fórmula del dióxido de carbono? CO2",
    "¿El Sol es una estrella? Sí",
    "¿Cuántas lunas tiene la Tierra? 1",
    "¿Cuál es el planeta más grande? Júpiter",
    "¿Planeta rojo? Marte",
    "¿Punto de ebullición del agua? 100°C",
    "¿Punto de congelación del agua? 0°C",
    "¿Cuántos huesos tiene el cuerpo humano? 206",
    "¿Velocidad de la luz aproximada? 300,000 km/s",
    "¿Qué hacen las plantas? Fotosíntesis",
    "¿Qué contiene el ADN? Información genética",
    "¿Qué hace la gravedad? Atrae objetos",
    "¿De qué están hechas las cosas? Átomos",
    "¿Qué es el aire? Mezcla de gases",
    "¿Gas más abundante en el aire? Nitrógeno",
    "¿Qué hacen los pulmones? Respirar",
    "¿Qué hace el corazón? Bombea sangre",
    "¿Cómo se dice hello en español? Hola",
    "¿Cómo se dice goodbye? Adiós",
    "¿Cómo se dice thank you? Gracias",
    "¿Cómo se dice please? Por favor",
    "¿Cómo se dice yes? Sí",
    "¿Cómo se dice no? No",
    "¿Cómo se dice sorry? Lo siento",
    "¿Cómo se dice how are you? Cómo estás",
    "¿Cómo se dice I am fine? Estoy bien",
    "¿Cómo se dice good morning? Buenos días",
    "¿Cómo se dice good night? Buenas noches",
    "¿Cómo se dice water? Agua",
    "¿Cómo se dice food? Comida",
    "¿Cómo se dice house? Casa",
    "¿Cómo se dice dog? Perro",
    "¿Cómo se dice cat? Gato",
    "¿Cómo se dice book? Libro",
    "¿Cómo se dice car? Coche",
    "¿Cómo se dice love? Amor",
    "¿Cómo se dice friend? Amigo",
    "¿Océano más grande? Pacífico",
    "¿Continente más pequeño? Oceanía",
    "¿Montaña más alta? Everest",
    "¿Río más largo? Nilo",
    "¿Animal terrestre más rápido? Guepardo",
    "¿Moneda de México? Peso",
    "¿Moneda de EE.UU.? Dólar",
    "¿Moneda de Japón? Yen",
    "¿Cuántos colores tiene el arcoíris? 7",
    "¿Cuántos continentes hay? 7",
    "¿Cuántos días tiene una semana? 7",
    "¿Cuántos meses tiene un año? 12",
    "¿Cuántas horas tiene un día? 24",
    "¿Cuántos minutos tiene una hora? 60",
    "¿Cuántos segundos tiene un minuto? 60",
    "¿Cuántos ojos tiene un humano? 2",
    "¿Cuántas piernas tiene un humano? 2",
    "¿Cuántos brazos tiene un humano? 2",
    "¿Cuántos planetas hay en el sistema solar? 8",
    "¿Número atómico del hidrógeno? 1"
    "¿Capital de Reino Unido? Londres",
    "¿Capital de Rusia? Moscú",
    "¿Capital de India? Nueva Delhi",
    "¿Capital de Australia? Canberra",
    "¿Capital de Egipto? El Cairo",
    "¿Capital de Sudáfrica? Pretoria",
    "¿Capital de Turquía? Ankara",
    "¿Capital de Grecia? Atenas",
    "¿Capital de Países Bajos? Ámsterdam",
    "¿Capital de Suiza? Berna",
    "¿Capital de Suecia? Estocolmo",
    "¿Capital de Noruega? Oslo",
    "¿Capital de Finlandia? Helsinki",
    "¿Capital de Dinamarca? Copenhague",
    "¿Capital de Irlanda? Dublín",
    "¿Capital de Marruecos? Rabat",
    "¿Capital de Argelia? Argel",
    "¿Capital de Arabia Saudita? Riad",
    "¿Capital de Corea del Sur? Seúl",
    "¿Capital de Indonesia? Yakarta",
    "¿Cuánto es 1+1? 2",
    "¿Cuánto es 2+3? 5",
    "¿Cuánto es 4+4? 8",
    "¿Cuánto es 9-3? 6",
    "¿Cuánto es 8-2? 6",
    "¿Cuánto es 3×3? 9",
    "¿Cuánto es 5×5? 25",
    "¿Cuánto es 10×10? 100",
    "¿Cuánto es 12÷3? 4",
    "¿Cuánto es 20÷5? 4",
    "¿Cuánto es 15+5? 20",
    "¿Cuánto es 18+2? 20",
    "¿Cuánto es 30-10? 20",
    "¿Cuánto es 14-7? 7",
    "¿Cuánto es 6×8? 48",
    "¿Cuánto es 7×7? 49",
    "¿Cuánto es 9×8? 72",
    "¿Cuánto es 81÷9? 9",
    "¿Cuánto es 100÷4? 25",
    "¿Cuánto es 11+11? 22",
    "¿Planeta más cercano al Sol? Mercurio",
    "¿Planeta más caliente del sistema solar? Venus",
    "¿La Tierra tiene atmósfera? Sí",
    "¿Marte tiene lunas? Sí",
    "¿Saturno tiene anillos? Sí",
    "¿Júpiter es un gigante gaseoso? Sí",
    "¿Símbolo químico del oro? Au",
    "¿Símbolo químico de la plata? Ag",
    "¿Símbolo químico del hierro? Fe",
    "¿Símbolo químico del carbono? C",
    "¿El oxígeno es necesario para respirar? Sí",
    "¿El agua es un compuesto? Sí",
    "¿El ADN contiene información genética? Sí",
    "¿La célula es la unidad de vida? Sí",
    "¿Las bacterias son microorganismos? Sí",
    "¿Los virus son seres vivos? Depende",
    "¿La fotosíntesis produce oxígeno? Sí",
    "¿Los humanos necesitan oxígeno? Sí",
    "¿Existe la gravedad en la Tierra? Sí",
    "¿La electricidad es energía? Sí",
    "¿Cómo se dice hola en inglés? Hello",
    "¿Cómo se dice adiós en inglés? Goodbye",
    "¿Cómo se dice por favor en inglés? Please",
    "¿Cómo se dice gracias en inglés? Thanks",
    "¿Cómo se dice sí en inglés? Yes",
    "¿Cómo se dice no en inglés? No",
    "¿Cómo se dice lo siento en inglés? Sorry",
    "¿Cómo se dice buenos días en inglés? Good morning",
    "¿Cómo se dice buenas noches en inglés? Good night",
    "¿Cómo se dice agua en inglés? Water",
    "¿Cómo se dice comida en inglés? Food",
    "¿Cómo se dice casa en inglés? House",
    "¿Cómo se dice perro en inglés? Dog",
    "¿Cómo se dice gato en inglés? Cat",
    "¿Cómo se dice sol en inglés? Sun",
    "¿Cómo se dice luna en inglés? Moon",
    "¿Cómo se dice escuela en inglés? School",
    "¿Cómo se dice libro en inglés? Book",
    "¿Cómo se dice coche en inglés? Car",
    "¿Cómo se dice amigo en inglés? Friend",
    "¿Cuántos días tiene febrero en año común? 28",
    "¿Cuántos días tiene febrero en año bisiesto? 29",
    "¿Cuántos lados tiene un triángulo? 3",
    "¿Cuántos lados tiene un cuadrado? 4",
    "¿Cuántos lados tiene un pentágono? 5",
    "¿Cuántos lados tiene un hexágono? 6",
    "¿Cuántos días tiene una semana? 7",
    "¿Cuántos meses tiene un año? 12",
    "¿Cuántos minutos tiene una hora? 60",
    "¿Cuántos segundos tiene un minuto? 60",
    "¿De qué color es el cielo despejado? Azul",
    "¿Cuál es un animal doméstico común? Perro",
    "¿Capital de México? Ciudad de México",
    "¿Idioma principal de Brasil? Portugués",
    "¿En qué continente está México? América del Norte",
    "¿Océano más grande? Pacífico",
    "¿Metal líquido a temperatura ambiente? Mercurio",
    "¿Gas más abundante en el aire? Nitrógeno",
    "¿Órgano que bombea sangre? Corazón",
    "¿Planeta donde hay vida conocida? Tierra"
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
    app.run(host='0.0.0.0', port=5000, debug=True)
