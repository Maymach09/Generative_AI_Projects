from langchain_community.llms.openai import OpenAI
from langchain.prompts import PromptTemplate, FewShotPromptTemplate
from langchain.chains import LLMChain


## This function demonstrates the use of few shot prompt template
def testcase_fewshot(user_input):

    """
    Generate the test cases based on the requirements provided using OpenAI Language Model.

    Parameters:
    - requirement (str): The input requirement based on which test cases will be generated

    Returns:
    - test case (json): The generated test cases
    """

    # Create OpenAI Language Model (LLM) Instance
    llm = OpenAI(temperature=0.0)

    examples = [
        {"requirement" : "User authentication",
         "test_case" : """
                    Steps to execute:
                        1. Enter valid username and password
                        2. Click on the login button
                    Expected Result:
                        User should be successfully logged in and granted access to the system.
                    """
         },
        
        {"requirement" : "User authentication",
         "test_case" : """
                    Steps to execute:
                        1. Enter invalid username and password
                        2. Click on the login button
                    Expected Result:
                        User should be denied access and prompted to enter valid credentials.
                    """
         },
        
        {"requirement" : "Role-based access control",
         "test_case" : """
                    Steps to execute:
                        1. Log in with user credentials
                        2. Access functionalities relevant to the user's role
                    Expected Result:
                        User should only be able to access functionalities based on their assigned role.    
                    """
         },

         {"requirement" : "Claim submission",
         "test_case" : """
                    Steps to execute:
                        1. Navigate to claim submission section
                        2. Fill in required claim details
                        3. Submit the claim
                    Expected Result:
                        Claim should be successfully submitted and received by the system.    
                    """
         },

         {"requirement" : "Real-time eligibility verification",
         "test_case" : """
                    Steps to execute:
                        1. Enter patient details for eligibility verification
                        2. Verify eligibility in real-time
                    Expected Result:
                        Patient eligibility status should be confirmed instantly before claim submission  
                    """
         },

    ]

    example_prompt = PromptTemplate(
        input_variables=["requirement","test_case"], 
        template="Provide test cases for requirement: {requirement}\n AI answer:{test_case}",
    )

    # Create fewshotprompttemplate object
    few_shot_prompt = FewShotPromptTemplate(
        examples = examples,   #Examples to be given in the prompt
        example_prompt = example_prompt,    #How to format the examples
        prefix = """Provide 2 test cases only for the following requirement.""",    #This is the prefix instruction to be given in the prompt
        suffix = "{input}", #This is where the user input will go
        input_variables = ["input"],    #Actual user input
    )

    # Create LLMChain object
    chain = LLMChain(llm=llm, prompt=few_shot_prompt)

    # Extract the antonym from the generated output
    chain_output = chain.run(user_input)
    
    return chain_output
   