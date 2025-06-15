import streamlit as st
import os
from dotenv import load_dotenv
from mcp_agent import DatabaseAssistant

# Load environment variables
load_dotenv()

# Configure Streamlit page
st.set_page_config(
    page_title="🗃️ Database Chat Assistant",
    page_icon="🗃️",
    layout="wide"
)

# Title and description
st.title("🗃️ Database Chat Assistant")
st.markdown("""
This AI assistant can help you query and understand your PostgreSQL database using natural language.
Ask questions about your data, and the assistant will use SQL queries to find the answers.

**Available tables:** `users`, `orders`, `products`

**Example questions:**
- "What tables are available in the database?"
- "Show me the structure of the users table"
- "How many users are there?"
- "What are the top 5 most expensive products?"
- "Show me recent orders"
""")

# Sidebar for configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # OpenAI API Key input
    openai_api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value=os.getenv("OPENAI_API_KEY", ""),
        help="Enter your OpenAI API key. You can also set it in the .env file."
    )
    
    # Database connection status
    st.header("📊 Database Status")
    try:
        import psycopg2
        conn = psycopg2.connect(
            host=os.getenv('PG_HOST', 'localhost'),
            port=os.getenv('PG_PORT', '5432'),
            user=os.getenv('PG_USER', 'postgres'),
            password=os.getenv('PG_PASS', 'password'),
            database=os.getenv('PG_DB', 'knowmydb')
        )
        conn.close()
        st.success("✅ Database Connected")
    except Exception as e:
        st.error(f"❌ Database Error: {str(e)}")
    
    # Clear conversation button
    if st.button("🗑️ Clear Conversation"):
        if "messages" in st.session_state:
            st.session_state.messages = []
        if "assistant" in st.session_state:
            del st.session_state.assistant
        st.rerun()

# Check if API key is provided
if not openai_api_key:
    st.warning("⚠️ Please provide your OpenAI API key in the sidebar to continue.")
    st.info("💡 You can get your API key from [OpenAI Platform](https://platform.openai.com/account/api-keys)")
    st.stop()

# Initialize the assistant
@st.cache_resource
def get_assistant(api_key):
    return DatabaseAssistant(api_key)

try:
    if "assistant" not in st.session_state:
        with st.spinner("🤖 Initializing AI Assistant..."):
            st.session_state.assistant = get_assistant(openai_api_key)
    
    assistant = st.session_state.assistant
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = []
        # Add welcome message
        welcome_msg = """👋 Hello! I'm your database assistant. I can help you explore and query your PostgreSQL database.

I have access to your database with tables containing information about users, orders, and products. 

What would you like to know about your data?"""
        st.session_state.messages.append({"role": "assistant", "content": welcome_msg})
    
    # Display chat history
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    
    # Chat input
    if prompt := st.chat_input("Ask me anything about your database..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)
        
        # Get assistant response
        with st.chat_message("assistant"):
            with st.spinner("🔍 Analyzing your question and querying the database..."):
                try:
                    response = assistant.ask_question(prompt)
                    st.markdown(response)
                    
                    # Add assistant response to chat history
                    st.session_state.messages.append({"role": "assistant", "content": response})
                    
                except Exception as e:
                    error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
                    st.error(error_msg)
                    st.session_state.messages.append({"role": "assistant", "content": error_msg})

except Exception as e:
    st.error(f"❌ Failed to initialize assistant: {str(e)}")
    st.info("💡 Make sure your OpenAI API key is valid and you have sufficient credits.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    🔒 <strong>Security Note:</strong> Only SELECT queries are executed. Results are limited to 5 rows for data protection.
    <br>
    Built with Streamlit • OpenAI Assistants API • PostgreSQL
</div>
""", unsafe_allow_html=True) 