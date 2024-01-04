import json
import requests

class DataManager:
    def __init__(self, url="https://blaze-4.com/api/roulette_games/history?page=1"):
        # URL da API da qual você está coletando os dados
        self.url = url
        self.last_id = None  # O último ID de registro processado
        self.predicted_trend_color = None  # A cor da tendência prevista
        self.attempt_count = 0  # Contagem de tentativas para prever a tendência

    def get_blaze_data(self, timeout=10):
        """
        Obtém os dados da API Blaze.
        
        :param timeout: Tempo limite da solicitação HTTP em segundos.
        :return: Uma lista de registros de dados da API.
        """
        try:
            response = requests.get(self.url, timeout=timeout)
            response.raise_for_status()
            data = json.loads(response.text)['records']
            return data
        except requests.exceptions.Timeout:
            print("Erro: Tempo limite da solicitação excedido.")
            return []
        except requests.exceptions.RequestException as e:
            print(f"Erro ao acessar a API: {str(e)}")
            return []
        except json.JSONDecodeError as e:
            print(f"Erro ao decodificar resposta JSON: {str(e)}")
            return []

    def process_new_data(self, data):
        """
        Processa novos dados obtidos da API, evitando registros duplicados.

        :param data: Lista de registros de dados obtidos da API.
        :return: Uma lista de novos registros não duplicados.
        """
        new_data = []
        for record in data:
            if self.last_id is None or record['id'] != self.last_id:
                new_data.append(record)
            else:
                break
        if new_data:
            self.last_id = new_data[0]['id']
        return new_data

    def load_existing_data(self, file_name="result.json"):
        """
        Carrega dados existentes de um arquivo JSON.

        :param file_name: Nome do arquivo JSON a ser carregado.
        :return: Uma lista de dados existentes carregados do arquivo.
        """
        try:
            with open(file_name, "r") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []

    def save_data_to_file(self, new_data, file_name="result.json"):
        """
        Salva dados em um arquivo JSON.

        :param new_data: Os novos dados a serem salvos.
        :param file_name: Nome do arquivo JSON para salvar os dados.
        """
        with open(file_name, "w") as f:
            json.dump(new_data, f, indent=4)
