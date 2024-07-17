# Setup
After cloning the repository, run the following commands in a WSL terminal to begin working in the python venv
1. `./env_setup.bash`
2. `. .venv/bin/activate`
Now you should be ready to run the application.

# Varify website using bash file by running separately in bash cell
naz@NAGORI:~/haqathon2024/IrwinEarthens-main/IrwinEarthens-main/scripts$ ./pull_text.bash ./naz_temp_dir https://naaznagori1123.atlassian.net/wiki/rest/api/content/458754?expand=body.storage 1
# refer Retriever.py 
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
