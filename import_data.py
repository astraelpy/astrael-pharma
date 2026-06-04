import sqlite3
import random

data = [
{"nome":"ALPRAZOLAM","dosagem":"2MG 30CPR","laboratorio":"NOVA QUIMICA GENERICO","preco_venda":90.01},
{"nome":"ALPRAZOLAM","dosagem":"0.5MG 30 COMP","laboratorio":"LEGRAND GENERICOS","preco_venda":25.83},
{"nome":"ALPRAZOLAM","dosagem":"1MG 30 COMP","laboratorio":"ACHE","preco_venda":38.42},
{"nome":"ALPRAZOLAM","dosagem":"0.25MG 30 COMP","laboratorio":"SANOFI MEDLEY","preco_venda":23.24},
{"nome":"AMITRIPTILINA","dosagem":"25MG 30 COMP","laboratorio":"TEUTO","preco_venda":39.98},
{"nome":"ARIPIPRAZOL","dosagem":"10MG 30 COMP","laboratorio":"NOVA QUIMICA GENERICO","preco_venda":284.17},
{"nome":"ARIPIPRAZOL","dosagem":"15MG 60 COMP","laboratorio":"SANDOZ","preco_venda":625.02},
{"nome":"BROMAZEPAM","dosagem":"3MG 30 COMP","laboratorio":"EMS GENERICO","preco_venda":34.43},
{"nome":"BROMAZEPAM","dosagem":"6MG 30 COMP","laboratorio":"NEO QUIMICA","preco_venda":49.12},
{"nome":"BROMAZEPAM","dosagem":"3MG 20 COMP","laboratorio":"ACHE","preco_venda":26.51},
{"nome":"CARBAMAZEPINA","dosagem":"200MG 30 COMP","laboratorio":"TEUTO","preco_venda":38.93},
{"nome":"CARBAMAZEPINA","dosagem":"400MG 30 COMP","laboratorio":"BIOCHIMICO","preco_venda":63.58},
{"nome":"CELECOXIBE","dosagem":"200MG CAPS","laboratorio":"ZYDUS","preco_venda":105.67},
{"nome":"CITALOPRAM","dosagem":"20MG 28 COMP","laboratorio":"BIOLAB GENERICOS","preco_venda":41.17},
{"nome":"CLONAZEPAM","dosagem":"0.5MG 20 COMP","laboratorio":"BIOCHIMICO","preco_venda":19.53},
{"nome":"CLONAZEPAM","dosagem":"0.5MG 30 COMP","laboratorio":"SANOFI MEDLEY","preco_venda":24.53},
{"nome":"DELLER","dosagem":"100MG 30 COMP","laboratorio":"ACHE","preco_venda":123.60},
{"nome":"DESVENLAFAXINA","dosagem":"50MG 30 COMP","laboratorio":"ACHE","preco_venda":130.57},
{"nome":"DIAZEPAM","dosagem":"5MG 30 COMP","laboratorio":"GERMED GENERICOS","preco_venda":26.22},
{"nome":"DIAZEPAM","dosagem":"5MG 30 COMP","laboratorio":"NEO QUIMICA","preco_venda":25.35},
{"nome":"DIAZEPAM","dosagem":"10MG 30 COMP","laboratorio":"GERMED GENERICOS","preco_venda":21.61},
{"nome":"DONEPEZILA","dosagem":"10MG 30 COMP","laboratorio":"MEDQUIMICA","preco_venda":74.58},
{"nome":"ESCITALOPRAM","dosagem":"15MG 30 COMP","laboratorio":"PHARLAB","preco_venda":74.42},
{"nome":"ESCITALOPRAM","dosagem":"10MG 30 COMP","laboratorio":"GEOLAB","preco_venda":67.87},
{"nome":"ESCITALOPRAM","dosagem":"20MG 30 COMP","laboratorio":"TEUTO","preco_venda":135.23},
{"nome":"ESCITALOPRAM","dosagem":"20MG 30 COMP","laboratorio":"PHARLAB","preco_venda":96.20},
{"nome":"FENOBARBITAL","dosagem":"100MG 30 COMP","laboratorio":"UNIAO QUIMICA","preco_venda":12.25},
{"nome":"FLUOXETINA","dosagem":"20MG 30 CAPS","laboratorio":"GERMED GENERICOS","preco_venda":65.60},
{"nome":"GARDENAL","dosagem":"100MG 20 COMP","laboratorio":"SANOFI MEDLEY","preco_venda":23.67},
{"nome":"HALDOL","dosagem":"1MG 20 COMP","laboratorio":"JANSSEN","preco_venda":19.11},
{"nome":"HALDOL","dosagem":"5MG 20 COMP","laboratorio":"JANSSEN","preco_venda":27.43},
{"nome":"HALDOL","dosagem":"2MG 30ML","laboratorio":"JANSSEN","preco_venda":33.80},
{"nome":"HIDANTAL","dosagem":"100MG 25 COMP","laboratorio":"MANTECORP FARMASA","preco_venda":18.60},
{"nome":"LEVETIRACETAM","dosagem":"250MG","laboratorio":"GERMED GENERICOS","preco_venda":69.88},
{"nome":"LISDEXANFETAMINA","dosagem":"70MG 30 CAP","laboratorio":"PHARLAB","preco_venda":370.00},
{"nome":"LISDEXANFETAMINA","dosagem":"30MG 30 CAP","laboratorio":"PHARLAB","preco_venda":285.83},
{"nome":"LORAZEPAM","dosagem":"2MG 20 COMP","laboratorio":"EMS GENERICO","preco_venda":31.61},
{"nome":"MEMANTINA","dosagem":"10MG 30 COMP","laboratorio":"TEUTO","preco_venda":67.93},
{"nome":"MEMANTINA","dosagem":"10MG 30 COMP","laboratorio":"BIOLAB GENERICOS","preco_venda":64.29},
{"nome":"MEMANTINA","dosagem":"10MG 60 COMP","laboratorio":"BIOLAB GENERICOS","preco_venda":72.52},
{"nome":"MIRTAZAPINA","dosagem":"30MG 30 COMP","laboratorio":"PHARLAB","preco_venda":164.01},
{"nome":"OLANZAPINA","dosagem":"2.5MG 30 COMP","laboratorio":"ACHE","preco_venda":89.62},
{"nome":"PARACETAMOL + CODEINA","dosagem":"500MG+30MG 12 COMP","laboratorio":"EMS GENERICO","preco_venda":93.84},
{"nome":"PREGABALINA","dosagem":"150MG 30 CAPS","laboratorio":"TEUTO","preco_venda":87.20},
{"nome":"QUETIAPINA","dosagem":"25MG 30 COMP","laboratorio":"ACHE","preco_venda":55.31},
{"nome":"QUETIAPINA","dosagem":"200MG 30 COMP","laboratorio":"ACHE","preco_venda":290.00},
{"nome":"ROHYDORM","dosagem":"2MG 30 COMP","laboratorio":"SIGMA PHARMA","preco_venda":58.00},
{"nome":"ROHYDORM","dosagem":"1MG 30 COMP","laboratorio":"SIGMA PHARMA","preco_venda":63.09},
{"nome":"SERTRALINA","dosagem":"25MG 30 COMP","laboratorio":"ACHE","preco_venda":39.34},
{"nome":"SERTRALINA","dosagem":"50MG 30 COMP","laboratorio":"PRATI DONADUZZI","preco_venda":73.45},
{"nome":"SIBUTRAMINA","dosagem":"15MG 30 CAP","laboratorio":"ACHE","preco_venda":115.00},
{"nome":"SIBUTRAMINA","dosagem":"10MG 30 CAP","laboratorio":"EUROFARMA","preco_venda":75.60},
{"nome":"TOPIRAMATO","dosagem":"25MG 60 COMP","laboratorio":"GERMED GENERICOS","preco_venda":102.69},
{"nome":"TRAMADOL","dosagem":"50MG 10 COMP","laboratorio":"EUROFARMA","preco_venda":42.18},
{"nome":"TRAZODONA","dosagem":"50MG 60 COMP","laboratorio":"SANOFI MEDLEY","preco_venda":55.21},
{"nome":"VENLAFAXINA","dosagem":"75MG 30 CAPS","laboratorio":"SANOFI MEDLEY","preco_venda":81.33},
{"nome":"VENLAFAXINA","dosagem":"37.5MG 30 CAPS","laboratorio":"SANOFI MEDLEY","preco_venda":42.23}
]

images = [
    "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=800&q=80",
    "https://images.unsplash.com/photo-1585435557343-3b092031a831?w=800&q=80",
    "https://images.unsplash.com/photo-1620916566398-39f1143ab7be?w=800&q=80",
    "https://images.unsplash.com/photo-1573883430697-4c3479aae4b9?w=800&q=80",
    "https://images.unsplash.com/photo-1471864190281-a93a3070b6de?w=800&q=80",
    "https://images.unsplash.com/photo-1550572017-edb79a55e1fc?w=800&q=80",
    "https://images.unsplash.com/photo-1587854692152-cbe660dbde88?w=800&q=80"
]

conn = sqlite3.connect('astrael_pharma.db')
cursor = conn.cursor()

# Limpar produtos anteriores
cursor.execute('DELETE FROM produtos')

for item in data:
    nome = f"{item['nome']} {item['dosagem']}"
    descricao = f"Laboratório: {item['laboratorio']}"
    preco = item['preco_venda']
    quantidade = 50 # Default stock 50
    categoria = "Medicamento Controlado"
    imagem_url = random.choice(images)
    
    cursor.execute('''
        INSERT INTO produtos (nome, descricao, preco, quantidade, categoria, imagem_url, ativo)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (nome, descricao, preco, quantidade, categoria, imagem_url, 1))

conn.commit()
conn.close()

print("Inseridos com sucesso!")
