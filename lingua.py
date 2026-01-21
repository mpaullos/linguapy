from gtts import gTTS
import os
import re
from pathlib import Path

def limpar_nome_arquivo(texto, max_chars=30):
    """
    Cria um nome de arquivo válido a partir do texto.
    Remove caracteres especiais e limita o tamanho.
    """
    # Remove caracteres inválidos para nomes de arquivo
    caracteres_invalidos = ['<', '>', ':', '"', '/', '\\', '|', '?', '*']
    nome = texto
    for char in caracteres_invalidos:
        nome = nome.replace(char, '')
    
    # Remove espaços extras e limita o tamanho
    nome = ' '.join(nome.split())
    nome = nome[:max_chars].strip()
    
    return nome

def remove_html_txt(frases):
    """
    Remove tags HTML das frases usando regex.
    """
    frases_limpa = []
    for frase in frases:
        # Remover tags HTML usando regex
        frase_sem_html = re.sub(r'<.*?>', '', frase)
        frases_limpa.append(frase_sem_html.strip())
    
    return frases_limpa

def atualizar_txt_sem_html(arquivo_txt):
    """
    Lê o arquivo TXT, remove as tags HTML e sobrescreve o arquivo.
    """
    # Ler o arquivo
    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    # Limpar HTML
    linhas_limpas = remove_html_txt(linhas)
    
    # Sobrescrever o arquivo
    with open(arquivo_txt, 'w', encoding='utf-8') as f:
        for linha in linhas_limpas:
            if linha:  # Não escrever linhas vazias
                f.write(linha + '\n')
    
    print(f"✅ Arquivo '{arquivo_txt}' atualizado (HTML removido)!\n")

def processar_txt_para_tts(arquivo_txt, pasta_saida="audios", idioma="en", limpar_html=True):
    """
    Lê um arquivo TXT linha por linha e gera áudios TTS usando gTTS.
    
    Args:
        arquivo_txt: Caminho do arquivo TXT
        pasta_saida: Pasta onde os áudios serão salvos
        idioma: Código do idioma (en=inglês, pt=português, es=espanhol, etc.)
        limpar_html: Se True, remove tags HTML do arquivo antes de processar
    """
    # Criar pasta de saída se não existir
    Path(pasta_saida).mkdir(exist_ok=True)
    
    # Verificar se o arquivo existe
    if not os.path.exists(arquivo_txt):
        print(f"❌ Erro: Arquivo '{arquivo_txt}' não encontrado!")
        return
    
    # Limpar HTML do arquivo se solicitado
    if limpar_html:
        atualizar_txt_sem_html(arquivo_txt)
    
    # Ler o arquivo TXT
    with open(arquivo_txt, 'r', encoding='utf-8') as f:
        linhas = f.readlines()
    
    print(f"📖 Arquivo carregado: {len(linhas)} linha(s) encontrada(s)\n")
    
    # Processar cada linha
    sucessos = 0
    erros = 0
    
    for i, linha in enumerate(linhas, 1):
        linha = linha.strip()
        
        # Pular linhas vazias
        if not linha:
            print(f"⏭️  Linha {i}: vazia, pulando...\n")
            continue
        
        print(f"🎤 Processando linha {i}: \"{linha}\"")
        
        try:
            # Criar nome do arquivo baseado no texto
            nome_arquivo = limpar_nome_arquivo(linha)
            caminho_audio = os.path.join(pasta_saida, f"{nome_arquivo}.mp3")
            
            # Gerar o áudio usando gTTS
            tts = gTTS(text=linha, lang=idioma, slow=False)
            tts.save(caminho_audio)
            
            print(f"✅ Áudio salvo: {caminho_audio}\n")
            sucessos += 1
            
        except Exception as e:
            print(f"❌ Erro ao processar linha {i}: {str(e)}\n")
            erros += 1
            continue
    
    print(f"\n{'='*50}")
    print(f"🎉 Processo concluído!")
    print(f"✅ Sucessos: {sucessos}")
    print(f"❌ Erros: {erros}")
    print(f"📁 Áudios salvos em: {pasta_saida}/")
    print(f"{'='*50}")

# Exemplo de uso
if __name__ == "__main__":
    # Nome do arquivo TXT que você quer processar
    arquivo_entrada = "frases.txt"
    
    # Pasta onde os áudios serão salvos
    pasta_saida = "audios_gerados"
    
    # Idioma dos áudios (en=inglês, pt=português, es=espanhol, fr=francês, etc.)
    idioma = "en"
    
    # Limpar HTML do arquivo antes de processar? (True/False)
    limpar_html = True
    
    processar_txt_para_tts(arquivo_entrada, pasta_saida, idioma, limpar_html)