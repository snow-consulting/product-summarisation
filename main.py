import openai

import streamlit as st

from langchain.llms import OpenAI
from langchain import PromptTemplate




st.set_page_config(page_title="Product Summarisation", page_icon=":robot:", layout="centered")
st.header("Product Summarisation")

st.image(image='product.jpg', width=500)

st.markdown("## Please enter your product description")

# def get_api_key():
#     input_text = st.text_input(label="OpenAI API Key ",  placeholder="Ex: sk-2twmA8tfCb8un4...", key="openai_api_key_input")
#     return input_text

# openai_api_key = get_api_key()

col1, col2 = st.columns(2)
with col1:
    length_prompt = st.selectbox(
        'Short or long description?',
        ('Short', 'Long'))

with col2:
    option_language = st.selectbox(
        'Which language would you like?',
        ('English', 'Swedish', 'French', 'Spanish', 'German'))

def get_text():
    input_text = st.text_area(label="Question", label_visibility='collapsed', placeholder="Please enter the product description...", key="text_input")
    return input_text

text_input = get_text()

if len(text_input.split(" ")) > 500:
    st.write("Please enter a shorter input. The maximum length is 500 words.")
    st.stop()

st.markdown("### Your Answer:")


def summarisation(text_input, prompt, model="text-davinci-003"):
    """
    :output: summarisation of text based on prompt given to model
    :input product: str product name
    :input product_description: str of product description and good to know
    :input prompt: str of prompt given to model
    """
    openai.api_key = st.secrets.OpenAI.key
    
    response = openai.Completion.create(
      model=model,
      prompt=prompt + ': ' + text_input,
      temperature=0.7,
      max_tokens=1200,
      top_p=1.0,
      frequency_penalty=0.0,
      presence_penalty=1
    )

    result = response['choices'][0]['text']
    
    return result

if length_prompt == 'Short':
    template = """Extract key information from the following text and present each point on a separated line. 
    Each point should be no more than 4 words. Can you translate to result to the chosen language? 
    Also present a ranked list of how important each these features are to the product using the context.

    Context: An oven has important features such as: preset cooking programs; touch control; easy installation. Guarantee information is not important.
    Question: {query}
    Language: {option_language}

    Answer: """

else:
    template = """Extract key benefits from the following text and order them based on how valuable it would be for a customer in bullet points. Each bullet point should be on a separate line. Can you translate to result to the chosen language?

    Question: {query}
    Tone: {option_language}

    Answer: """


# if length_prompt == 'Short':
#     prompt = """Extract key information from the following text and present each point on a separated line. Each point should be no more than 6 words and there should only be 5 bullet points. Can you translate to result to the chosen language?

#     Tone: Tone: {option_tone}
#     Language: {option_language}
    
#     Answer: """

# else:
#     prompt = """Extract key benefits from the following text and order them based on how valuable it would be for a customer in bullet points. Each bullet point should be on a separate line. Can you translate to result to the chosen language?
                
#     Tone: {option_tone}
#     Language: {option_language}
    
#     Answer: """

st.write("Summarised text:")

if text_input:
    prompt_template = PromptTemplate(input_variables=["query", "option_language"], template=template)

    llm = OpenAI(model_name="text-davinci-003",
                    openai_api_key=st.secrets.OpenAI.key
                    )

    response = llm(template.format(query=text_input, length_prompt=length_prompt, option_language=option_language))
    # response = summarisation(text_input, prompt).replace('\n', '')

    st.write(response)
