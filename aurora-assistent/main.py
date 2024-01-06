import speech_recognition as sr
import pyttsx3
import os

def falar(texto):
    motor = pyttsx3.init()
    motor.say(texto)
    motor.runAndWait()

def ouvir():
    reconhecedor = sr.Recognizer()

    with sr.Microphone() as fonte:
        print("Ouvindo...")
        reconhecedor.adjust_for_ambient_noise(fonte)
        audio = reconhecedor.listen(fonte, timeout=5)

    try:
        print("Reconhecendo...")
        comando = reconhecedor.recognize_google(audio, language='pt-BR').lower()
        print("Você disse:", comando)
        return comando
    except sr.UnknownValueError:
        print("Desculpe, não consegui entender.")
        return ""
    except sr.RequestError as e:
        print(f"Não foi possível obter resultados do serviço de reconhecimento de fala do Google; {e}")
        return ""

def abrir_aplicativo(nome_aplicativo):
    try:
        os.system(f"start {nome_aplicativo}")
        falar(f"Abrindo {nome_aplicativo}")
    except Exception as e:
        falar(f"Erro ao abrir {nome_aplicativo}: {str(e)}")

def excluir_pasta(caminho_pasta):
    try:
        os.rmdir(caminho_pasta)
        falar(f"Pasta {caminho_pasta} excluída com sucesso.")
    except Exception as e:
        falar(f"Erro ao excluir {caminho_pasta}: {str(e)}")

if __name__ == "__main__":
    falar("Olá! Como posso ajudar você hoje?")

    while True:
        comando = ouvir()

        if "abrir" in comando:
            nome_app = comando.split("abrir")[1].strip()
            abrir_aplicativo(nome_app)
        elif "excluir" in comando:
            nome_pasta = comando.split("excluir")[1].strip()
            excluir_pasta(nome_pasta)
        elif "sair" in comando or "encerrar" in comando:
            falar("Até logo!")
            break
        else:
            falar("Desculpe, não entendi. Pode repetir, por favor?")
