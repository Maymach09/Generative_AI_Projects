from langchain_community.llms import OpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain, SimpleSequentialChain, SequentialChain
from langchain.agents import load_tools, initialize_agent, AgentType
import streamlit as st

## This function demonstrates the use of langchain agent
def gk_chatbot(question):

    # Create OpenAI Language Model (LLM) Instance
    llm = OpenAI(temperature=0.6)

    # serpapi key
    #serpapi_key="bb64e4147d0510f6934efe921cd1647014e68efdebb580ccc7abff5d5e2acb57"

    # Load tools
    wiki_tool = load_tools(["wikipedia"], llm=llm)
    #serp_tool =load_tools(["serpapi"],serpapi_api_key=serpapi_key,llm=llm)

    # Initialize Agent
    agent = initialize_agent(
        wiki_tool, llm, agent = AgentType.ZERO_SHOT_REACT_DESCRIPTION, verbose=True
    )

    # Print Output
    output = agent.run(question)
    return output


## This function demonstrates the use of langchain chain
def translator_chain(text, language):   

    # Create OpenAI Language Model (LLM) Instance
    llm = OpenAI(temperature=0.6)
    
    # Define a Prompt Template
    prompt_template = PromptTemplate (
        input_variables = ['text', 'language'],
        template = """Translate {text} to {language}. 
                    If the input is irrelevant then say 'Please input a valid language.'"""
    )

    # Create an LLMChain Instance
    chain = LLMChain(llm=llm, prompt=prompt_template, output_key='text')
    output = chain({'text':text, 'language':language})
    return output

## This function demonstrates the use of langchain's simple sequential chain
def simple_seq_chain(input):

    # Create OpenAI Language Model (LLM) Instance
    llm = OpenAI(temperature=0.5)

    # Define first Prompt Template
    prompt_template_antonym = PromptTemplate (
        input_variables = ['input_word'],
        template = """Give me the opposite of {input_word}. 
                    If the input is irrelevant then say 'Please enter a valid word'"""
    )

    # first chain to provide antonym
    antonym_chain=LLMChain(llm=llm,prompt=prompt_template_antonym)

    # Define second Prompt Template
    prompt_template_sentence = PromptTemplate (
        input_variables = ['derived_word'],
        template = """
                    Give me a sentence which shows the usage of {derived_word}. 
                    If the input is irrelevant then say 'Invalid input!'
                """
    )

    # second chain to create a sentence with the antonym
    sentence_chain=LLMChain(llm=llm,prompt=prompt_template_sentence)

    # combining the chains together
    chain=SimpleSequentialChain(chains=[antonym_chain,sentence_chain])

    # run the chain
    output = chain(input)

    return output

## This function demonstrates the use of langchain's sequential chain
def seq_chain(input):

    # Create OpenAI Language Model (LLM) Instance
    llm = OpenAI(temperature=0.5)

    # Define first Prompt Template
    prompt_template_antonym = PromptTemplate (
        input_variables = ['input_word'],
        template = """Give me the antonym for {input_word}. 
                    If the input is irrelevant then say 'Please enter a valid word'"""
    )

    # first chain to provide antonym
    antonym_chain=LLMChain(llm=llm,prompt=prompt_template_antonym, output_key='derived_word')

    # Define second Prompt Template
    prompt_template_sentence = PromptTemplate (
        input_variables = ['derived_word'],
        template = """
                    Give me a sentence which shows the usage of {derived_word}.
                    Make sure the context of the word is same as an atonym of {input_word}
                    If the input is irrelevant then say 'Invalid input!'
                """
    )

    # second chain to create a sentence with the antonym
    sentence_chain=LLMChain(llm=llm,prompt=prompt_template_sentence, output_key='sentence')

    # combining the chains together
    chain=SequentialChain(chains=[antonym_chain,sentence_chain],
                                input_variables=["input_word"],
                                output_variables=["derived_word","sentence"]
                                )
    
    # run the chain
    output=chain({"input_word":input})

    return output