import logging
from game import Double
from data_manager import DataManager
from trend_analyzer import TrendAnalyzer
from logger_manager import LoggerManager

def setup_logging():
    # Configuração do sistema de log
    logging.basicConfig(filename='blaze_double.log', level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def main():
    setup_logging()  # Inicializa a configuração de log

    # Definindo a janela de análise para o TrendAnalyzer
    analysis_window = 5

    # Criando instâncias dos objetos necessários
    data_manager = DataManager()  # Gerenciador de dados
    trend_analyzer = TrendAnalyzer(analysis_window)  # Analisador de tendências
    logger_manager = LoggerManager()  # Gerenciador de logs

    # Iniciando o jogo com os objetos criados
    game = Double(
        data_manager=data_manager,
        trend_analyzer=trend_analyzer,
        logger_manager=logger_manager,
        save_file=True,  # Opção para salvar dados em arquivo
        time_limit_seconds=93600,  # Limite de tempo em segundos
        starting_cash=100,  # Dinheiro inicial
        bet_amount=30  # Valor da aposta
    )
    game.run()  # Inicia a execução do jogo

if __name__ == "__main__":
    main()  # Chama a função main se o script for executado diretamente
