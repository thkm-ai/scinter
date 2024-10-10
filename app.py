import streamlit as st
import openai
import nbformat
from nbformat import v4 as nbf

# Load notebook and extract relevant code
notebook_path = '/home/azureuser/scinter/Copy_of_llama_relik.ipynb'

def load_notebook_code():
    with open(notebook_path, 'r', encoding='utf-8') as f:
        nb = nbformat.read(f, as_version=4)
    code_cells = [cell['source'] for cell in nb['cells'] if cell['cell_type'] == 'code']
    return "\n".join(code_cells)

# Prepare OpenAI API key (replace with your own or set as environment variable)
openai.api_key = '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'

# Execute extracted code from the notebook
def query_model(user_query):
    local_vars = {}
    exec(load_notebook_code(), {"query": user_query}, local_vars)
    return local_vars.get('response')

# Streamlit app
def main():
    st.title("Notebook Integrated Query App")
    user_query = st.text_input("Enter your query:")

    if st.button("Submit"):
        if user_query:
            response = query_model(user_query)
            st.write(response)

if __name__ == "__main__":
    main()
