import openai
import os
from dotenv import dotenv_values
import argparse

PROMPT = """
You will receive a file's contents as text.
Generate a code review for the file.  
Indicate what changes should be made to improve its style, performance, readability, and maintainability.  
If there are any reputable libraries that could be introduced to improve the code, suggest them.  
Be kind and constructive.  
For each suggested change, include line numbers to which you are referring
"""

def code_review(file_path, model_name):
    with open(file_path, "r") as f:
        file_content = f.read()
    
    generated_code_review = review_request(file_content, model_name)
    with open("CodeReview_for_"+file_path[:-3]+".txt","w") as f:
        f.write(generated_code_review)
    print("CODE REVIEW DONE !!!")
    print("Check out this file: "+"CodeReview_for_"+file_path[:-3]+".txt")
    # print(generated_code_review)
    
def review_request(file_content, model_name):
    messages = [
        {'role':'system', 'content':PROMPT},
        {'role':'user', 'content':f"Code Review the following file: {file_content}"}
    ]
    response = openai.ChatCompletion.create(
        model=model_name,
        messages=messages
    )

    return response["choices"][0]["message"]["content"]

def main():
    parser = argparse.ArgumentParser(description="Code reviewer")
    parser.add_argument("file")
    parser.add_argument("--model", default='gpt-3.5-turbo')
    args = parser.parse_args()
    code_review(args.file, args.model)

if __name__ == "__main__":
    openai.api_key = dotenv_values("../../../../.env")['OPENAI_API_KEY']
    main()