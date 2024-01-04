from ast import main
import time

class Double:
    def __init__(self, data_manager, trend_analyzer, logger_manager, **kwargs):
        # Inicialização da classe Double com argumentos opcionais
        self.save_file = kwargs.get('save_file', False)  # Define se os dados serão salvos em arquivo
        self.time_limit_seconds = kwargs.get('time_limit_seconds', 93600)  # Limite de tempo em segundos
        self.starting_cash = kwargs.get('starting_cash', 100)  # Dinheiro inicial
        self.bet_amount = kwargs.get('bet_amount', 10)  # Valor da aposta
        self.current_cash = self.starting_cash  # Dinheiro atual do jogo

        self.data_manager = data_manager  # Instância do DataManager para gerenciamento de dados
        self.trend_analyzer = trend_analyzer  # Instância do TrendAnalyzer para análise de tendências
        self.logger_manager = logger_manager  # Instância do LoggerManager para registro de eventos

    def check_prediction_accuracy(self, latest_result):
        # Verifica a precisão da previsão em relação ao resultado mais recente
        latest_color = latest_result['color']
        latest_roll = latest_result['roll']

        predicted_color = self.data_manager.predicted_trend_color
        attempt_count = self.data_manager.attempt_count

        if predicted_color is not None:
            if latest_color == predicted_color or (predicted_color == 'branco' and latest_roll == 0):
                # Se a previsão estiver correta, aumenta o dinheiro e registra o acerto
                self.current_cash += self.bet_amount
                self.logger_manager.log_acerto(f"Acerto na tentativa {attempt_count + 1} - Cor: {latest_color}, Roll: {latest_roll}")
                print(f"Acertamos! 🟢 Caixa atual: R${self.current_cash}")
            else:
                # Se a previsão estiver errada, diminui o dinheiro e registra o erro
                self.current_cash -= self.bet_amount
                self.logger_manager.log_erro(f"Erro na tentativa {attempt_count} - Cor: {latest_color}, Roll: {latest_roll}")
                print(f"Previsão errada. 🔴 Caixa atual: R${self.current_cash}")

            self.reset_prediction()  # Reseta a previsão após cada verificação

    def reset_prediction(self):
        # Reseta a previsão de tendência e a contagem de tentativas
        self.data_manager.predicted_trend_color = None
        self.data_manager.attempt_count = 0

    def run(self):
        existing_data = self.data_manager.load_existing_data()  # Carrega dados existentes, se houver
        if existing_data:
            self.data_manager.last_id = existing_data[-1]['id']

        start_time = time.time()  # Marca o tempo de início do jogo
        while True:
            current_time = time.time()
            if current_time - start_time >= self.time_limit_seconds:
                # Verifica se o limite de tempo foi atingido e encerra o jogo
                print("Limite de tempo atingido. Encerrando.")
                break

            data = self.data_manager.get_blaze_data()  # Obtém dados da API
            new_data = self.data_manager.process_new_data(data)  # Processa novos dados

            if new_data:
                existing_data.extend(new_data)  # Adiciona novos dados aos dados existentes

                for record in new_data:
                    print("Novo Resultado:", record)
                    self.check_prediction_accuracy(record)  # Verifica a precisão da previsão para cada novo resultado

                if self.data_manager.predicted_trend_color is None:
                    # Se não houver previsão de tendência, faz uma análise para detectar a tendência
                    most_common_color, analysis_result = self.trend_analyzer.analyze_trend(existing_data)
                    if most_common_color:
                        print(f"Tendência: próxima cor será {most_common_color}")
                        self.data_manager.predicted_trend_color = most_common_color
                        self.data_manager.attempt_count = 0
                        self.logger_manager.log_trend(f"Tendência detectada: próxima cor será {most_common_color}")

                if self.save_file:
                    # Se a opção de salvar em arquivo estiver ativada, salva os dados
                    self.data_manager.save_data_to_file(existing_data)

                time.sleep(10)  # Aguarda 10 segundos antes de obter novos dados

        total_attempts = len(existing_data)  # Calcula o total de tentativas
        total_acertos = total_attempts - self.data_manager.attempt_count  # Calcula o total de acertos
        precisao = (total_acertos / total_attempts) * 100 if total_attempts > 0 else 0  # Calcula a precisão
        print(f"Estatísticas ao final:\nTotal de tentativas: {total_attempts}\nTotal de acertos: {total_acertos}\nPrecisão: {precisao:.2f}%")

if __name__ == "__main__":
    main()
