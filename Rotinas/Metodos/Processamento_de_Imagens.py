import cv2
import pytesseract

class Leitura_de_Ordem:
    def __init__(self):
        # Configurando o caminho para o executável Tesseract OCR
        pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

    def ler_ordem(self):
        
        # Carregando a imagem
        image = cv2.imread(r'C:\Users\leobr\OneDrive\Documentos\Renda Extra\CapitalTrack\Rotinas\Metodos\Imagens\Nota_2024_02_01_Edited.jpg')

        # Pré-processando a imagem
        processed_image = self.preprocess_image(image)



        # Exibindo a imagem pré-processada
        cv2.imshow('Imagem Processada', processed_image)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        # Aplicando a detecção de texto com Tesseract OCR em português
        text = pytesseract.image_to_string(processed_image, lang='por')

        # Imprimindo o texto encontrado
        print("Texto detectado na imagem:")
        print(text)

    def preprocess_image(self, image):
        # Convertendo a imagem para escala de cinza
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

        # Ajuste do limiar de binarização
        _, binary = cv2.threshold(gray, 230, 250, cv2.THRESH_BINARY)

        # Realce de borda para melhorar a detecção de caracteres
        #edges = cv2.Canny(binary, 50, 150)

        # Suavização para remover ruídos e preservar a largura dos caracteres
        #blurred = cv2.GaussianBlur(image, (5, 5), 0)

        
        
        # Suavização para remover ruídos e preservar a largura dos caracteres
        blurred = cv2.GaussianBlur(binary, (3, 3), 0)

        

        return blurred
    
    def ler_ordem_automatico(self, arquivo):
        # Carregando a imagem
        image = cv2.imread(arquivo)

        # Pré-processando a imagem
        processed_image = self.preprocess_image(image)
        
        # Aplicando a detecção de texto com Tesseract OCR em português
        text = pytesseract.image_to_string(processed_image, lang='por')

        return text

