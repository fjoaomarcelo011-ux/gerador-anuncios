import streamlit as st
from google import genai
from PIL import Image

# Configuração da página
st.set_page_config(page_title="Gerador de Anúncios com IA", page_icon="🚀", layout="centered")

st.title("🚀 Gerador de Anúncios com IA")
st.write("Carrega uma foto para gerar anúncios persuasivos para Meta Ads e Google Ads.")

# Chave da API obtida das configurações secretas
api_key = st.secrets.get("GEMINI_API_KEY")

if not api_key:
    st.error("Chave da API do Gemini não configurada nas definições do Streamlit.")
else:
    client = genai.Client(api_key=api_key)

    uploaded_file = st.file_uploader("Carrega a foto do produto/serviço", type=["jpg", "jpeg", "png"])
    nicho = st.text_input("Qual é o produto ou serviço? (Ex: Barbearia, Moda, Aulas de Inglês)")

    if uploaded_file is not None:
        image = Image.open(uploaded_file)
        st.image(image, caption="Imagem Carregada", use_column_width=True)

        if st.button("Gerar Anúncios"):
            with st.spinner("A analisar a imagem e a criar as copys..."):
                try:
                    prompt = f"""
                    Analisa esta imagem para o seguinte contexto: {nicho}.
                    Cria copys persuasivas para tráfego pago:

                    1. META ADS (Facebook/Instagram):
                       - 2 Opções de Texto Principal (Legenda com gancho forte, corpo e CTA).
                       - 2 Títulos curtos.

                    2. GOOGLE ADS:
                       - 4 Títulos (máximo 30 caracteres cada).
                       - 2 Descrições (máximo 90 caracteres cada).
                    """

                    response = client.models.generate_content(
                        model='gemini-2.5-flash',
                        contents=[image, prompt]
                    )

                    st.success("Anúncios gerados com sucesso!")
                    st.markdown(response.text)
                except Exception as e:
                    st.error(f"Erro ao gerar anúncios: {e}")
