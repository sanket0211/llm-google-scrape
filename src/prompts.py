from langchain import PromptTemplate
from langchain.chains import RetrievalQAWithSourcesChain
#from embeddings import Embeddings
from langchain.chat_models import ChatOpenAI
import os
import json 

class Prompts:
    def __init__(self):

        

        self.template = """
            {context}
            {question}
            
        """
        self.question_product_launch = """
            fill following fields related to New Product Launches news if any based on the given context.
            product_name:<product name> or "not found"
            launch_date:<launch date> or "not found"
        """

        self.question_partnership = """
            fill following fields related to partnership news if any based on the given context.
            names_of_partners:[list of partnet company names] or "not found"
            domains_of_partners:[list of domains of partner companies] or "not found"
            announcement_date:<announcement date> or "not found"
        """

        self.question_investment_received = """
            fill following fields related to investment received news if any based on the given context else write "not found" for each field.
            names_of_investors:[list of investor names] or "not found"
            domains_of_investors:[list of domains of investors] or "not found"
            announcement_date:<announcement date> or "not found"
            amount_of_funding:<amount of funding in millions USD> or "not found"
        """

        self.question_investment_made = """
            fill following fields related to investment made by the company news if any based on the given context else write "not found" for each field.
            investee_name:<name of the company in which the company invested> or "not found"
            investee_domain:<domain of the company in which the company invested> or "not found"
            announcement_date:<announcement date> or "not found"
            amount_of_funding:<amount of funding in millions USD> or "not found"
        """

        self.question_new_hire = """
            fill following fields related to new hires news if any based on the given context else write "not found" for each field.
            name_of_hires:[list of names of hires] or "not found"
            titles_of_hire:[list of titles of the hires] or "not found"
            announcement_date:<announcement date>
        """

        self.question_issues = """
            fill following fields related to company corporate issue news if any based on the given context else write "not found" for each field.
            problems_found:[list of problems found] or "not found"
            announcement_date:<announcement date> or "not found"
            entities_involved:[list of entities involved in the problems found] or "not found"
            titles_of_hire:[list of titles of the hires] or "not found"
        """
        
        self.question_competitor_found = """
            fill following fields related to company's competitor informateion news if any based on the given context else write "not found" for each field.
            competitor_name:[list of partnet competitor company names] or "not found"
            competitor_domain:[list of competitor domains] or "not found"
            article_date:<article date>
        """

        self.questions_dict={
            "product_launch":self.question_product_launch,
            "partnership":self.question_partnership,
            "investment_received":self.question_investment_received,
            "investment_made":self.question_investment_made,
            "new_hire":self.question_new_hire,
            "issues":self.question_issues, 
            "competitor_found": self.question_competitor_found
        }

        self.EVENT_TYPES = ['product_launch', 'partnership', 'investment_received', 'investment_made', 'new_hire', 'issues', 'competitor_found']

        self.llm = ChatOpenAI(temperature=0, model_name='gpt-3.5-turbo')

    # def load_embeddings(self, article_index):
    #     if os.path.exists("../" + article_index):
    #         embed = Embeddings()
    #         article_index = embed.load_article_index("../" +article_index)
    #         return article_index
    #     else:
    #         print("index not available. Please create one.")
    


    def question_answering(self, type, embeddings):
        question_prompt = PromptTemplate(
            input_variables=["question", "context"], template=self.template
        )
        article_chain = RetrievalQAWithSourcesChain.from_llm(
            llm=self.llm,
            retriever=embeddings.as_retriever(k=4),
            question_prompt=question_prompt,
        )

        result = article_chain({"question": self.questions_dict[type]}, 
                                return_only_outputs=True)
        result = self.post_process_output(result)
        return result
        
    def post_process_output(self, output):
        temp = {}
        answers = output['answer']
        answers = answers.split("\n")
        print(answers)
        for answer in answers:
            if ":" in answer:
                answer = answer.split(":")
                temp[answer[0]]=answer[1]
        temp['news_url']=output['sources']
        return temp

if __name__ == "__main__":
    p = Prompts()
    #output = p.question_answering("product_launch", "INDEX-apple.com")
    #print(output)
    events = {}
    #embeddings = p.load_embeddings("INDEX-apple.com")
    for event_type in p.EVENT_TYPES:
        output = p.question_answering(event_type, embeddings)
        events[event_type] = output
    with open("output.json", "w") as outfile:
        json.dump(events, outfile)
    



