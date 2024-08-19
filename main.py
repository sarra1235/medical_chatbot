'''import torch
a=torch.cuda.is_available()
print(a)'''
from langchain_community.document_loaders import PyPDFLoader, DirectoryLoader
from langchain.prompts import PromptTemplate
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit as cl
from langchain_community.llms import Ollama
from RAG_Functions import *
from Geolocation_Functions import*


# Initial count of questions
MAX_QUESTIONS = 3
question_count = 0

# Main function for terminal interaction
def main():
    
    global question_count

    print("ChatBot: Hello, I'm your virtual medical assistant. How can I assist you today?")

    while True:
        if question_count < MAX_QUESTIONS:

            query = input("You: ")
            answer = final_result(query)
            print(f"ChatBot: {answer}")
            question_count += 1

        elif question_count == 3:
             
             print("ChatBot: I have answered the maximum number of questions I can handle for this session.")
             print(" Could you please provide your address so that I can recommend the nearest doctors you can consult?")
             question_count += 1

        elif question_count == 4:

            address_patient = input("You: ")
            Speciality = "Cardiologist" #still searching for a solution to automate the determination of the Speciality
            coordonnee_med = nearest_Doctors(address_patient, Speciality)
            formatted_table = format_table(coordonnee_med)
            print(f"ChatBot: These are the closest {Speciality}s available for you to visit:\n{formatted_table}")
            question_count += 1
        
        else:
            print("ChatBot: I have answered the maximum number of questions I can handle for this session.")


if __name__ == "__main__":
    main()
