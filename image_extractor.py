# Importa bibliotecas necessárias
import sys  # Permite lidar com argumentos do sistema (como encerrar o programa)
import os   # Usada para manipular caminhos de arquivos no sistema operacional

# Importa componentes gráficos do PyQt5 (biblioteca para criar janelas e botões)
from PyQt5.QtWidgets import (
    QWidget, QPushButton, QLabel, QVBoxLayout,
    QApplication, QLineEdit, QFileDialog
)

# Importa a função 'remove' da biblioteca rembg, que remove o fundo de imagens
from rembg import remove

# Importa o módulo de imagem do PIL (biblioteca Pillow) para abrir e salvar imagens
from PIL import Image
import io  # Usado para manipular dados de imagem em memória (sem salvar arquivos temporários)

# Função para buscar a imagem no computador
def buscar_imagem():
    # Abre uma janela para escolher uma imagem
    caminho, _ = QFileDialog.getOpenFileName(
        janela,
        "Selecione uma imagem",
        "",
        "Imagens (*.png *.jpg *.jpeg)"  # Filtros de arquivos aceitos
    )
    if caminho:
        input_imagem.setText(caminho)  # Mostra o caminho da imagem no campo de texto
        label.setText("Imagem selecionada com sucesso!")  # Atualiza a mensagem para o usuário

# Função que remove o fundo da imagem selecionada
def remover_fundo():
    caminho = input_imagem.text()  # Pega o caminho da imagem do campo de texto
    if not caminho:
        label.setText("Por favor, selecione uma imagem primeiro.")  # Se estiver vazio, mostra aviso
        return

    try:
        # Abre a imagem em modo binário (para leitura)
        with open(caminho, 'rb') as img_file:
            input_data = img_file.read()  # Lê os dados da imagem

            # Remove o fundo da imagem usando a biblioteca rembg
            output_data = remove(input_data)

        # Converte os dados da imagem (sem fundo) para um formato que o PIL entende
        imagem_saida = Image.open(io.BytesIO(output_data))

        # Define o nome do novo arquivo com "_sem_fundo" no nome
        nome_base = os.path.basename(caminho)  # Pega o nome do arquivo original
        nome_saida = os.path.splitext(nome_base)[0] + "_sem_fundo.png"  # Novo nome

        # Caminho completo para salvar a nova imagem
        caminho_saida = os.path.join(os.path.dirname(caminho), nome_saida)

        # Salva a imagem sem fundo no local original
        imagem_saida.save(caminho_saida)

        # Informa ao usuário que deu certo
        label.setText(f"Fundo removido com sucesso!\nImagem salva em:\n{caminho_saida}")
    
    # Caso algo dê errado (por exemplo: imagem inválida), mostra o erro
    except Exception as e:
        label.setText(f"Erro ao remover fundo:\n{str(e)}")

# ------------------- INTERFACE GRÁFICA -------------------

# Cria a aplicação PyQt (obrigatório em todo programa com interface PyQt)
app = QApplication(sys.argv)

# Cria a janela principal do programa
janela = QWidget()
janela.setWindowTitle('Removedor de Fundo de Imagens')  # Título da janela
janela.setGeometry(250, 250, 600, 300)  # Posição e tamanho (x, y, largura, altura)

# Cria os elementos da tela
texto_info = QLabel("Este programa permite selecionar uma imagem e remover o fundo automaticamente.")  # Explicação
label = QLabel("Seja bem-vindo!")  # Mensagem inicial

input_imagem = QLineEdit()  # Campo de texto para mostrar o caminho da imagem
input_imagem.setPlaceholderText("Caminho da imagem selecionada...")  # Texto guia

button_buscar = QPushButton('Buscar Imagem')  # Botão para buscar imagem
button_buscar.clicked.connect(buscar_imagem)  # Quando clicado, chama a função buscar_imagem

button_remover = QPushButton('Remover Fundo')  # Botão para remover o fundo da imagem
button_remover.clicked.connect(remover_fundo)  # Quando clicado, chama a função remover_fundo

# Cria o layout vertical (um embaixo do outro)
layout = QVBoxLayout()
layout.addWidget(texto_info)
layout.addWidget(label)
layout.addWidget(input_imagem)
layout.addWidget(button_buscar)
layout.addWidget(button_remover)

# Aplica o layout na janela principal
janela.setLayout(layout)

# Mostra a janela na tela
janela.show()

# Inicia o loop da aplicação (fica rodando até o usuário fechar)
sys.exit(app.exec_())
