class TrendAnalyzer:
    def __init__(self, analysis_window):
        # Inicialização da classe TrendAnalyzer com a janela de análise especificada
        self.analysis_window = analysis_window

    def analyze_trend(self, data):
        """
        Analisa a tendência com base nos dados fornecidos.

        :param data: Uma lista de registros de dados.
        :return: A cor mais comum nas últimas rotações e um resultado de análise.
        """
        if len(data) < self.analysis_window:
            # Verifica se há dados suficientes para análise
            return None, "Não há dados suficientes para análise de tendência."

        recent_data = data[-self.analysis_window:]  # Obtém os dados mais recentes da janela de análise
        color_counts = {}  # Dicionário para contar as ocorrências de cada cor

        for record in recent_data:
            color = record['color']
            if color in color_counts:
                color_counts[color] += 1
            else:
                color_counts[color] = 1

        most_common_color = max(color_counts, key=color_counts.get)  # Obtém a cor mais comum
        analysis_result = f"A cor mais comum nas últimas {self.analysis_window} rotações foi: {most_common_color}"

        return most_common_color, analysis_result
