import sys

class Frame:
    def __init__(self, id_frame):
        self.id_frame = id_frame
        self.pagina_alocada = None
        self.ultimo_acesso = 0

class TabelaPaginas:
    def __init__(self, num_frames, sequencia_paginas):
        self.frames = [Frame(i) for i in range(num_frames)]
        self.total_page_faults = 0
        self.total_acessos = 0
        self.sequencia_paginas = sequencia_paginas  
        self.passo_atual = 0   

    def acessar_pagina(self, numero_pagina):
        self.total_acessos += 1
        self.passo_atual += 1

        for frame in self.frames:
            if frame.pagina_alocada == numero_pagina:
                frame.ultimo_acesso = self.passo_atual
                return True, frame.id_frame

        self.total_page_faults += 1

        for frame in self.frames:
            if frame.pagina_alocada is None:
                frame.pagina_alocada = numero_pagina
                frame.ultimo_acesso = self.passo_atual
                return False, frame.id_frame

        frame_vitima_id = self.substituir_pagina(numero_pagina)
        self.frames[frame_vitima_id].ultimo_acesso = self.passo_atual
        return False, frame_vitima_id

    def substituir_pagina(self, nova_pagina):
        futuro = self.sequencia_paginas[self.passo_atual:]

        farthest = -1
        frame_escolhido_id = 0
        nunca_usadas = []

        for frame in self.frames:
            try:
                proxima_vez = futuro.index(frame.pagina_alocada)
                if proxima_vez > farthest:
                    farthest = proxima_vez
                    frame_escolhido_id = frame.id_frame
            except ValueError:
                nunca_usadas.append(frame)

        if nunca_usadas:
            # desempate LRU: substituir a menos recentemente usada
            vitima = min(nunca_usadas, key=lambda f: f.ultimo_acesso)
            frame_escolhido_id = vitima.id_frame

        self.frames[frame_escolhido_id].pagina_alocada = nova_pagina
        return frame_escolhido_id


    def imprimir_mapa_memoria(self, passo, pagina_acessada, foi_hit, frame_alterado=None):
        status = "Hit" if foi_hit else "Page Fault"
        print(
            f"\n--- Passo {passo}: Acesso à Página {pagina_acessada} ({status}) ---")

        for frame in self.frames:
            conteudo = f"Página {frame.pagina_alocada}" if frame.pagina_alocada is not None else "[Vazio]"
            marcador = " <-- Alterado" if frame.id_frame == frame_alterado and not foi_hit else ""
            print(f"[Frame {frame.id_frame}]: {conteudo}{marcador}")

        print("-" * 40)

class Simulador:
    def __init__(self, caminho_arquivo):
        self.caminho_arquivo = caminho_arquivo

    def executar(self):
        try:
            with open(self.caminho_arquivo, 'r') as arquivo:
                linhas = arquivo.readlines()
        except FileNotFoundError:
            print(
                f"Erro: O arquivo '{self.caminho_arquivo}' não foi encontrado.")
            return

        linhas = [l.strip() for l in linhas if l.strip()
                  and not l.strip().startswith('#')]

        if not linhas:
            print("Erro: Arquivo de entrada vazio.")
            return

        num_frames = int(linhas[0])
        sequencia = [int(l) for l in linhas[1:]]
        tabela_paginas = TabelaPaginas(num_frames, sequencia)

        print(f"Iniciando simulação com {num_frames} frames disponíveis.")
        print("=" * 40)

        passo = 1
        for numero_pagina in sequencia:   
            foi_hit, frame_id = tabela_paginas.acessar_pagina(numero_pagina)
            tabela_paginas.imprimir_mapa_memoria(passo, numero_pagina, foi_hit, frame_id)
            passo += 1

        print("\n================ STATS FINAIS ================")
        print(f"Total de Acessos: {tabela_paginas.total_acessos}")
        print(f"Total de Page Faults: {tabela_paginas.total_page_faults}")
        if tabela_paginas.total_acessos > 0:
            taxa_faults = (tabela_paginas.total_page_faults /
                           tabela_paginas.total_acessos) * 100
            print(f"Taxa de Page Faults: {taxa_faults:.2f}%")
        print("==============================================")


if __name__ == "__main__":
    arquivo_entrada = sys.argv[1] if len(sys.argv) > 1 else "entrada.txt"
    simulador = Simulador(arquivo_entrada)
    simulador.executar()