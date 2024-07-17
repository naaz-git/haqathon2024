# Setup
After cloning the repository, run the following commands in a WSL terminal to begin working in the python venv
1. `./env_setup.bash`
2. `. .venv/bin/activate`
Now you should be ready to run the application.
# Create your own website first with dummy project details and fictitious data. 
Example: https://naaznagori1123.atlassian.net/wiki/spaces/~71202047467a55ab2f4aaaa9555603c46317e0/pages/458754/Haqathon+Project

# Verify website loads in the project using bash file by running separately in bash cell 
Check contents in the pull_text.bash:

#!/bin/bash

	export CURRENT_TIME=$(date +%Y%m%d%H%M%S)

	if [ ! -d $1 ]; then

	echo "creating temporary directory: $1"
 
	mkdir $1
 
	fi
# curl command
#curl command + userID + token copied from the atlassian website  + website Name + python utility for json file generation
	curl -u naaznagori1123@gmail.com:ATATT3xFfGF0JVGvsx8Qf79HquV5O0lPqeKi2HMbxZzyKG-HAhqJ1-wDtA6-WJt9mAMxWz-c3PBJ7I-kPfa7-tcWTUXLmgkstmJ8jEIcXcJjxcIvUqQ4CAWvhadCCrP0qcCtpaz3nlhij7g0YveOSeVeLTDYwV3XF9HPpn9HV8ALK6t3mtln17I=EA600C61 $2 |

	python3 -mjson.tool > $1/num$3_raw_$CURRENT_TIME.json

# Run in Bash shell (Not in powershell)
naz@NAGORI:~/haqathon2024/IrwinEarthens-main/IrwinEarthens-main/scripts$ ./pull_text.bash ./naz_temp_dir https://naaznagori1123.atlassian.net/wiki/rest/api/content/458754?expand=body.storage 1

# Notes:
In code, return f"https://afreddo.atlassian.net/wiki/rest/api/content/{data_source}?expand=body.storage"
Datasource refers to a number which should be fetched from the website:
data_source = 458754 comes from my little website that I created on confluence pages
https://naaznagori1123.atlassian.net/wiki/spaces/~71202047467a55ab2f4aaaa9555603c46317e0/pages/**458754**/Haqathon+Project

### Refer Retriever.py 
    following code loads the data from website, create temp drectory to store json format file but later generates output text file in the 'model_data' directory and removes json file automatically to save space
    
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
