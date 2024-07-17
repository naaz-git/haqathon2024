import subprocess
import os
import json
import re

class Retriever:
    """
    Class that performs retrieval, processing, and cleaning of data
    from confluece pages for use as LLM prompt
    """

    def __init__(self):
        self._data_sources = []
        self._pulled_data = ""
        self._cleaned_data = ""
        self._tmp_dir = "./tmp_pull"
        self._model_data_dir = "./model_data"
        self._team_id = -1
    
    def retrieve_data(self, team_id):
        """
        Main function for retrieving team data.
        Fetches data from confluence pages, processes data, stores data in 
        txt file for use by model

        Input:
        team_id => String
        Output:
        Text file saved in directory: ./model_data
        """
        
        self._team_id = team_id
        print(f"Retrieving data sources for team: {team_id}")
        self._grab_list(team_id)
        print("Pulling data from data sources...")
        self._pull_data()
        print(f"Storing model data in {self._model_data_dir}/")
        self._store_model_data()
        print(f"Cleaning tmp directory {self._tmp_dir}/")
        self._cleanup_tmp()

    def _grab_list(self, team_id):
        """
        Function that queries the team database on the team_id and stores the s
        recovered sources list in self._data_sources
        """
        #TODO: Add actual query logic
        self._data_sources = [65713, 98308, 131237, 98351]
    
    def _pull_data(self):
        """
        Function that pull raw text data from data sources, cleans the data, and
        updates self._pulled_data with the clean data
        """
        for i, data_source in enumerate(self._data_sources):
            self._raw_pull(data_source, i)
        self._read_data()
        self._clean_data()
    
    def _raw_pull(self, data_source, order_num):
        """
        Function that pulls raw text data from data source and stores it in a temporary directory

        Input:
        data_source => String
        Output:
        String
        """
        data_source_link = self._create_link(data_source)
        subprocess.call(["./scripts/pull_text.bash", self._tmp_dir, data_source_link, f"{order_num}"])

    def _create_link(self, data_source):
        """
        Function that creates confluence link based on data source number.

        Input:
        data_source => String
        Output:
        String
        """
        return f"https://afreddo.atlassian.net/wiki/rest/api/content/{data_source}?expand=body.storage"
    
    def _read_data(self):
        """
        Function that reads out relevant information from confluence page and stores in self._pulled_data
        """
        tmp_files = os.listdir(self._tmp_dir)
        for file in tmp_files:
            with open(f"{self._tmp_dir}/{file}") as current_file:
                data = json.load(current_file)
                self._pulled_data += data["body"]["storage"]["value"]
    
    def _clean_data(self):
        """
        Function that removes tags from self._pulled_data and stores the clean string in self._cleaned_data
        """
        regex = re.compile('<.*?>')
        self._cleaned_data = re.sub(regex, '', self._pulled_data)
    
    def _store_model_data(self):
        """
        Function that stores cleaned data as a text file in model_data/ directory
        """
        current_files = os.listdir(self._model_data_dir)
        for file in current_files:
            subprocess.call(["rm", f"{self._model_data_dir}/{file}"])
        
        new_filepath = self._model_data_dir + '/'
        new_filename = f"{self._team_id}.txt"
        with open(new_filepath + new_filename, "w") as model_data:
            model_data.write(self._cleaned_data)

    def _cleanup_tmp(self):
        """
        Function that removes temporary directories created during data processing
        """
        subprocess.call(["rm", "-rf", self._tmp_dir])

if __name__ == "__main__":
    ret = Retriever()
    ret.retrieve_data("LLVM")