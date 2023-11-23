from Investing.RasparDados import RaspagemInvesting


# Exemplo de uso da classe e do método
url = "https://br.investing.com/dividends-calendar/"
raspagem = RaspagemInvesting(url)
raspagem.realizar_raspagem()
