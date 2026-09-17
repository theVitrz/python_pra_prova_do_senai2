import streamlit as st
import database as db

# Garante que a tabela existe no banco assim que o app abre
db.criar_tabela()

st.header("🎮 Minha Coleção de Jogos", text_alignment="center")

# --- FORMULÁRIO DE CADASTRO ---
with st.form("cadastrar_jogo"):
    st.subheader("Adicionar novo jogo")
    titulo = st.text_input("Título do Jogo")
    estudio = st.text_input("Estúdio Desenvolvedor")
    ano_lancamento = st.number_input("Ano de Lançamento", step=1, value=2023)
    
    enviado = st.form_submit_button("Salvar Jogo")
    if enviado:
        msg = db.cadastro_jogo(titulo, estudio, ano_lancamento)
        st.info(msg)

# --- FORMULÁRIOS DE ATUALIZAÇÃO E DELEÇÃO (Lado a lado) ---
col1, col2 = st.columns(2)

with col1:
    with st.form("form_update_status"):
        st.subheader("Atualizar Status")
        id_jogo_up = st.number_input("ID do jogo para atualizar", value=0, step=1)
        novo_status = st.selectbox("Novo status", ["Não Jogado", "Jogando", "Zerado"])
        btn_update = st.form_submit_button("Atualizar")

        if btn_update:
            msg = db.update_status_jogo(id_jogo_up, novo_status)
            st.warning(msg)

with col2:
    with st.form("form_delete_jogo"):
        st.subheader("Deletar Jogo")
        id_jogo_del = st.number_input("ID do jogo para deletar", value=0, step=1)
        btn_deletar = st.form_submit_button("Deletar") 
        
        if btn_deletar:
            msg = db.delete_jogo(id_jogo_del)
            st.error(msg)

# --- EXIBIÇÃO DA TABELA (DATAFRAME) ---
st.divider()
st.subheader("Seu Acervo", text_alignment="center")

# Busca os dados no banco
dados_jogos = db.get_jogos()

# Prepara a lista de dicionários para o Streamlit
lista_formatada = []
for jogo in dados_jogos: 
    # jogo[0]=ID, jogo[1]=titulo, jogo[2]=estudio, jogo[3]=ano, jogo[4]=status
    dicionario_jogo = {
        "ID": jogo[0], 
        "Título": jogo[1], 
        "Estúdio": jogo[2], 
        "Lançamento": jogo[3], 
        "Status": jogo[4]
    }
    lista_formatada.insert(0, dicionario_jogo) # Insere sempre no topo da lista (mais recentes primeiro)

# Desenha o DataFrame
st.dataframe(lista_formatada, use_container_width=True, hide_index=True, 
             column_order=("ID", "Título", "Estúdio", "Lançamento", "Status"))
