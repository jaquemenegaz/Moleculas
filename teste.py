import pubchempy as pcp 

# Função para buscar informações da molécula
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

# Exemplo de uso
simbolos = ['C', 'H', 'O']  # Por exemplo, para o ácido acético (C2H4O2)
dados_molecula = buscar_molecula(simbolos)

if dados_molecula:
    print("Nome:", dados_molecula['nome'])
    print("CID:", dados_molecula['cid'])
    print("Peso Molecular:", dados_molecula['peso_molecular'])
else:
    print("Composto não encontrado.")
