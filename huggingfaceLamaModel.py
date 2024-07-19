import torch
import torch.nn as nn
from transformers import AutoTokenizer, AutoConfig, AutoModelForCausalLM

class LamaModel:
    def init(self): 
        print("Lama model initialized")
        self.tokenizer = AutoTokenizer.from_pretrained("meta-llama/Llama-2-7b-hf", 
                                            cache_dir="/mnt/c",
                                    )        

        self.model = AutoModelForCausalLM.from_pretrained(
        "meta-llama/Llama-2-7b-hf",
        cache_dir="/mnt/c",
        device_map='auto'    
        )

    def init_device(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        print(device)
    
    def get_llama2_reponse(self, prompt, max_new_tokens=50):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        

        #prompt = "answer this question: what is project phoenix? using this data:Project Phoenix aims to develop a cutting-edge AI-driven analytics platform designed to provide real-time insights and data-driven decision-making capabilities. The platform leverages advanced machine learning algorithms to analyze large datasets, delivering actionable intelligence to businesses and users."
        #prompt = "2+8?"
        print(device, "reponding with given prompt", prompt)

        inputs = self.tokenizer(prompt, return_tensors="pt").to(device)
        outputs = self.model.generate(**inputs, max_new_tokens=max_new_tokens, temperature= 0.00001)
        response = self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        print(device, "and response is : ",response)

        return response
