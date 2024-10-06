import re

class ImagemOCR():
    def __init__(self, imagem, leitor):
        self.__imagem = imagem
        self.__leitor = leitor

    def executar_ocr_imagem(self):
        textos = self.__leitor.readtext(image=self.__imagem, detail=0)
        padrao_mercosul = r'\w{3}\d{1}\w{1}\d{2}'  # Ex: ABC1D23
        padrao_antigo =  r'\w{3}[-.]?\d{4}'  # Ex: ABC-1234 ou ABC1234

        for placa in textos:
            if re.match(padrao_mercosul, placa):
                return placa
            
            elif re.match(padrao_antigo, placa):
                return placa
            
        return 'A placa não foi encontrada!'
    