from flask import Flask, render_template, jsonify, request
import json
import pubchempy as pcp 


app = Flask(__name__)


# Carrega os elementos a partir do arquivo JSON
def load_elements():
    with open('elements.json', 'r') as f:
        return json.load(f)

@app.route('/')
def index():
    elements = load_elements()
    return render_template('index.html', elements=elements)

@app.route('/search', methods=['POST'])
def search():
    str = request.json.get('formula').upper()
    simbolos = list(str)
    dados_molecula = buscar_molecula(simbolos)
    if dados_molecula:
        #print(dados_molecula['cid'])
        c = pcp.Compound.from_cid(dados_molecula['cid'])
        print(c)
        return jsonify({'success': True, 'data': {
            'form': c.molecular_formula,
            'cid': c.cid,
            'peso': c.molecular_weight,
            'iupac': c.iupac_name,
            'sinonimo': c.synonyms,            
        }})
    else:
        return jsonify({'success': False, 'message': 'Composto não encontrado.'})

def buscar_molecula(simb_atomos):
    # Cria uma fórmula a partir dos símbolos atômicos
    formula = ''.join(simb_atomos)
    
    # Busca a molécula no PubChem
    try:
        composto = pcp.get_compounds(formula, 'formula')[0]
        return {
            'nome': composto.iupac_name,
            'cid': composto.cid,
            'peso_molecular': composto.molecular_weight,
            'propriedades': composto.to_dict(properties=['molecular_weight', 'exact_mass'])
        }
    except IndexError:
        return None


if __name__ == '__main__':
    app.run(debug=True)


