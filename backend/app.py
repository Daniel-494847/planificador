from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import torch
import torch.nn as nn
import os
import random

app = Flask(__name__, static_folder='..', static_url_path='')
CORS(app)

# ============================================================
# MODELO DE EJEMPLO CON PYTORCH
# ============================================================
class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.linear = nn.Linear(3, 1)

    def forward(self, x):
        return self.linear(x)

model = SimpleModel()
model.eval()

# Ruta principal: sirve tu archivo HTML
@app.route('/')
def index():
    return send_from_directory('..', 'index.html')

# Ruta de predicción con PyTorch
@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    valores = data.get('valores', [0, 0, 0])  # espera 3 números

    with torch.no_grad():
        entrada = torch.tensor([valores], dtype=torch.float32)
        salida = model(entrada)
        resultado = salida.item()

    return jsonify({'resultado': round(resultado, 4)})

# Ruta para verificar que PyTorch está funcionando
@app.route('/torch-info', methods=['GET'])
def torch_info():
    return jsonify({
        'torch_version': torch.__version__,
        'cuda_available': bool(torch.cuda.is_available()),
        'device': 'cuda' if torch.cuda.is_available() else 'cpu'
    })

# ============================================================
# ENDPOINTS DE IA PARA GENERADOR DE PDC
# ============================================================

@app.route('/clasificar-area', methods=['POST'])
def clasificar_area():
    """Clasifica un objetivo de texto en un área curricular."""
    data = request.get_json()
    texto = data.get('texto', '').lower()

    areas_keywords = {
        'Matemáticas': ['número', 'suma', 'resta', 'multiplicación', 'división', 'fracción', 'geometría', 'problema', 'cálculo'],
        'Lengua y Literatura': ['texto', 'lectura', 'escritura', 'gramática', 'ortografía', 'cuento', 'poema', 'lectura comprensiva'],
        'Ciencias Naturales': ['planta', 'animal', 'cuerpo humano', 'agua', 'tierra', 'espacio', 'experimento', 'naturaleza', 'biología'],
        'Ciencias Sociales': ['bolivia', 'historia', 'cultura', 'mapa', 'colonia', 'revolución', 'pueblo', 'sociedad', 'geografía'],
        'Artes Plásticas y Visuales': ['dibujo', 'pintura', 'color', 'línea', 'forma', 'escultura', 'arte', 'creatividad'],
        'Educación Física': ['deporte', 'movimiento', 'salud', 'juego', 'ejercicio', 'correr', 'saltar', 'actividad física']
    }

    scores = {}
    for area, keywords in areas_keywords.items():
        score = sum(1 for kw in keywords if kw in texto)
        scores[area] = score

    area_sugerida = max(scores, key=scores.get) if max(scores.values()) > 0 else 'General'
    total_keywords = len(areas_keywords.get(area_sugerida, []))
    confianza = scores[area_sugerida] / total_keywords if total_keywords > 0 and scores[area_sugerida] > 0 else 0

    return jsonify({
        'area': area_sugerida,
        'confianza': round(confianza, 2),
        'detalle': scores
    })


ACTIVIDADES_POR_TIPO = {
    'practica': [
        'Resolver ejercicios prácticos en el cuaderno',
        'Realizar un experimento sencillo con materiales del aula',
        'Participar en un debate guiado sobre el tema',
        'Resolver un problema de la vida real en grupos',
        'Trabajar en equipos para resolver una situación problema',
        'Manipular materiales concretos para aprender el concepto',
        'Crear un modelo o representación física del tema',
        'Aplicar el concepto en una situación cotidiana',
        'Realizar una práctica de laboratorio o de campo',
        'Diseñar un juego educativo sobre el contenido visto'
    ],
    'teoria': [
        'Explicar conceptos clave con ejemplos del entorno',
        'Leer un texto informativo y resumir las ideas principales',
        'Ver un video educativo y tomar notas estructuradas',
        'Participar en una clase magistral interactiva con preguntas',
        'Analizar un caso práctico presentado por el docente',
        'Elaborar un esquema o mapa resumen del tema',
        'Investigar información en fuentes confiables y presentarla',
        'Comparar dos teorías o enfoques sobre el mismo tema',
        'Realizar una lectura guiada con preguntas de comprensión',
        'Escuchar una exposición y extraer las ideas centrales'
    ],
    'produccion': [
        'Crear un mapa conceptual del tema estudiado',
        'Redactar un ensayo corto sobre el contenido',
        'Diseñar un afiche informativo para el aula',
        'Elaborar un maquete o modelo tridimensional',
        'Escribir un cuento o poema relacionado con el tema',
        'Crear una presentación digital con diapositivas',
        'Grabar un video explicando el concepto aprendido',
        'Diseñar un infográfico con datos clave del tema',
        'Construir un portafolio de evidencias de aprendizaje',
        'Desarrollar un proyecto creativo que aplique el contenido'
    ],
    'valoracion': [
        'Responder un cuestionario de opción múltiple',
        'Realizar una autoevaluación con rúbrica',
        'Participar en una retroalimentación entre pares',
        'Presentar un proyecto final ante el grupo',
        'Resolver una prueba escrita de comprensión',
        'Demostrar una habilidad en una exhibición práctica',
        'Entregar un diario de aprendizaje semanal',
        'Crear un video resumen de lo aprendido',
        'Resolver un problema de aplicación en tiempo limitado',
        'Participar en una entrevista o defensa oral del tema'
    ]
}

@app.route('/generar-actividad', methods=['POST'])
def generar_actividad():
    """Genera 3 variantes de actividad sugerida según el tipo y área."""
    data = request.get_json()
    tipo = data.get('tipo', 'practica')
    area = data.get('area', 'general')

    lista = ACTIVIDADES_POR_TIPO.get(tipo, ACTIVIDADES_POR_TIPO['practica'])
    sugerencias = random.sample(lista, min(3, len(lista)))

    return jsonify({
        'tipo': tipo,
        'area': area,
        'actividades': sugerencias,
        'actividad_sugerida': sugerencias[0] if sugerencias else '',
        'tiempo_estimado': random.randint(20, 45)
    })


@app.route('/validar-coherencia', methods=['POST'])
def validar_coherencia():
    """Valida coherencia entre objetivo, metodología y evaluación."""
    data = request.get_json()
    objetivo = data.get('objetivo', '').lower()
    metodologia = data.get('metodologia', '').lower()
    evaluacion = data.get('evaluacion', '').lower()

    problemas = []

    if 'resolver' in objetivo and 'leer' in metodologia and 'resolver' not in metodologia:
        problemas.append({
            'campo': 'Metodología',
            'mensaje': 'El objetivo menciona resolver problemas, pero la metodología solo incluye lectura. Considera agregar ejercicios prácticos.'
        })

    if ('crear' in objetivo or 'producir' in objetivo):
        if 'examen' in evaluacion and 'proyecto' not in evaluacion and 'producto' not in evaluacion:
            problemas.append({
                'campo': 'Evaluación',
                'mensaje': 'El objetivo busca crear/producir, pero la evaluación es solo un examen. Considera evaluar el producto creado.'
            })

    return jsonify({
        'coherente': len(problemas) == 0,
        'problemas': problemas,
        'sugerencia': 'Revisa que objetivo, metodología y evaluación estén alineados.' if problemas else '¡Tu PDC está bien estructurado!'
    })


if __name__ == '__main__':
    print("=" * 50)
    print("Servidor Flask + PyTorch iniciado")
    print("URL: http://localhost:5000")
    print("=" * 50)
    app.run(debug=True, port=5000)