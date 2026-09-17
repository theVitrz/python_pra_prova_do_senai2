import unittest
import sqlite3
import os
import database as db

class TestGerenciamentoJogos(unittest.TestCase):

    def setUp(self):
        # Cria um banco falso só para os testes antes de cada função rodar
        self.banco_teste = "banco_jogos_teste.db"
        db.criar_tabela(self.banco_teste)

    def tearDown(self):
        # Exclui o banco falso depois que o teste acaba
        if os.path.exists(self.banco_teste):
            os.remove(self.banco_teste)

    def test_cadastrar_jogo_com_sucesso(self):
        # Tenta cadastrar um jogo
        db.cadastro_jogo("The Witcher 3", "CD Projekt", 2015, self.banco_teste)

        # Checa diretamente no banco se ele foi salvo
        conn = sqlite3.connect(self.banco_teste)
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM jogos WHERE titulo = 'The Witcher 3'")
        jogo_salvo = cursor.fetchone()
        conn.close()

        # Validações
        self.assertIsNotNone(jogo_salvo, "O jogo deveria ter sido salvo.")
        self.assertEqual(jogo_salvo[1], "The Witcher 3")
        self.assertEqual(jogo_salvo[4], "Não Jogado", "O status inicial deve ser 'Não Jogado'.")

    def test_bloqueio_deletar_jogo_em_andamento(self):
        # Cadastra um jogo
        db.cadastro_jogo("Hades", "Supergiant", 2020, self.banco_teste)
        
        # O ID será 1, pois é o primeiro e único item do banco de teste
        id_jogo = 1 
        
        # Atualiza o status para "Jogando"
        db.update_status_jogo(id_jogo, "Jogando", self.banco_teste)
        
        # Tenta deletar
        msg_delete = db.delete_jogo(id_jogo, self.banco_teste)
        
        # Verifica se o sistema barrou a exclusão corretamente
        self.assertEqual(msg_delete, "Você não pode deletar um jogo que está 'Jogando' no momento!")

if __name__ == "__main__":
    unittest.main()
