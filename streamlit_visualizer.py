import streamlit as st
import json
from datetime import datetime

st.set_page_config(page_title="Visualizador de Chats", layout="wide")

st.title("📱 Visualizador de Conversaciones")

# Cargar archivo JSON
uploaded_file = st.file_uploader("Selecciona un archivo JSON", type=['json'])

if uploaded_file is not None:
    try:
        # Leer y parsear el JSON
        data = json.load(uploaded_file)

        # Encabezado con información de la conversación
        st.header("📋 Información de la Conversación")

        col1, col2 = st.columns(2)

        with col1:
            st.subheader("Detalles Generales")
            if 'name' in data:
                st.write(f"**Nombre:** {data['name']}")
            if 'scenario' in data:
                st.write(f"**Escenario:** {data['scenario']}")
            if 'expected_outcome' in data:
                st.write(f"**Resultado Esperado:** {data['expected_outcome']}")
            if 'context' in data and data['context']:
                st.write(f"**Contexto:**")
                for ctx in data['context']:
                    st.write(f"- {ctx}")

        with col2:
            st.subheader("Metadata")
            if 'tags' in data and data['tags']:
                st.write(f"**Tags:** {', '.join(data['tags'])}")
            if 'comments' in data and data['comments']:
                st.write(f"**Comentarios:** {data['comments']}")

            # Estadísticas
            if 'turns' in data:
                total_turns = len(data['turns'])
                user_turns = sum(1 for t in data['turns'] if t['role'] == 'user')
                assistant_turns = sum(1 for t in data['turns'] if t['role'] == 'assistant')
                st.write(f"**Total de turnos:** {total_turns}")
                st.write(f"**Turnos del usuario:** {user_turns}")
                st.write(f"**Turnos del asistente:** {assistant_turns}")

        # Descripción del usuario si existe
        if 'user_description' in data and data['user_description']:
            with st.expander("👤 Descripción del Usuario"):
                st.write(data['user_description'].replace("\n", "\n\n"))

        # Rol del chatbot si existe
        if 'chatbot_role' in data and data['chatbot_role']:
            with st.expander("🤖 Rol del Chatbot"):
                st.write(data['chatbot_role'])

        st.divider()

        # Mostrar la conversación
        st.header("💬 Conversación")

        if 'turns' in data:
            for i, turn in enumerate(data['turns']):
                role = turn.get('role', 'unknown')
                content = turn.get('content', '')

                if role == 'user':
                    # Mensaje del usuario (alineado a la derecha)
                    col1, col2 = st.columns([1, 3])
                    with col2:
                        st.markdown(f"""
                        <div style="background-color: #E3F2FD; padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <strong>👤 ProtoFluxer</strong><br/>
                            {content}
                        </div>
                        """, unsafe_allow_html=True)

                elif role == 'assistant':
                    # Mensaje del asistente (alineado a la izquierda)
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f"""
                        <div style="background-color: #F5F5F5; padding: 15px; border-radius: 10px; margin: 10px 0;">
                            <strong>🤖 RunRun</strong><br/>
                            {content}
                        </div>
                        """, unsafe_allow_html=True)

                # Mostrar metadata adicional del turno si existe
                metadata_items = []
                if turn.get('tools_called'):
                    metadata_items.append(f"🔧 Tools: {turn['tools_called']}")
                if turn.get('retrieval_context'):
                    metadata_items.append(f"📚 Context: {turn['retrieval_context']}")

                if metadata_items:
                    with st.expander(f"ℹ️ Metadata del turno {i + 1}"):
                        for item in metadata_items:
                            st.write(item)

        else:
            st.warning("No se encontraron turnos en la conversación")

    except json.JSONDecodeError:
        st.error("❌ Error al leer el archivo JSON. Verifica que el formato sea correcto.")
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")

else:
    st.info("👆 Por favor, carga un archivo JSON para visualizar la conversación")

    # Mostrar instrucciones
    with st.expander("ℹ️ Instrucciones de uso"):
        st.write("""
        1. Haz clic en el botón "Browse files" arriba
        2. Selecciona un archivo JSON con el formato de conversación
        3. La conversación se mostrará automáticamente con:
           - Información general en el encabezado
           - Mensajes del usuario y asistente en formato de chat
           - Metadata adicional disponible en expandibles
        """)