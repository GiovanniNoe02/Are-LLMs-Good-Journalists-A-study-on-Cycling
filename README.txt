Operational Guide for Reproducibility – Data Science Lab Project  
By Giovanni Noè and Francesco Volpi Ghirardini  
University of Milan Bicocca – Data Science Lab Course


This guide outlines the steps to ensure reproducibility of the Data Science Lab Project carried out by Giovanni Noè an Francesco Volpi Ghirardini for the Data Science Lab course at the University of Milan Bicocca. The aim was to produce AI generated articles about cycling competitions and evaluate them.

The entire project was carried out using Google Colab to facilitate collaboration between the members of the group, this means that, to reproduce exactly the work, the access to Google Drive will be necessary. By the way the Python module containing the functions that represent the output of the developing process is saved in a .py file so it can be used on any Python script or notebook by importing it.


The following files are included in the same folder as this README and are required to reproduce or inspect the project:

- Data Science Lab Project - Data Acquisition.ipynb: Colab Notebook containing the dataset creation process  
- Data Science Lab Project - Function Creation.ipynb: Colab Notebook containing the creation of the module along with some tests
- Data Science Lab Project - Application.ipynb: Colab Notebook containing all the testing and the creation of the articles  
- llm_journalist.py: a Python script that is the output of the "Data Science Lab Project - Function Creation.ipynb" notebook containing all the functions developed through this project
- Articles.docs: All the articles produced through this project


A part of this project is based on the service of the HuggingFace community that provides the access to AI products thanks to a token (HF_Token) that is pesonal and has a limited free use. For this reason the one provided in the code could not have enough uses left to run the entire code again. To avoid this problem the reader should go on the HuggingFace website https://huggingface.co/, create an account and create a token on https://huggingface.co/settings/tokens/new?ownUserPermissions=inference.serverless.write&canReadGatedRepos=true&tokenType=fineGrained with the following setup:
	Token name: anything
	User permissions:
		Inference: Make calls to Inference Providers
		Repositories: Read access to contents of all public gated repos you can access
The token is free but has a limited usage, please keep this in mind.


How to Reproduce the Project:

0. Create the HF_Token following the guide above

1. Create a shortcut to the entire folder on your MyDrive folder (VERY IMPORTANT)

2. There is no need to run the code of "Data Science Lab Project - Data Acquisition.ipynb" since its output (data used in tests) is already saved in the folder. In any case running the two files again won't cause any issue 

3. The "Data Science Lab Project - Function Creation.ipynb" outputs the file "llm_journalist.py". This file can be run again with no problems but, also in this case, it is not necessary sice the output is already present in the folder

4. Insert your personal HugingFace Token in the variable "HF_Token" in "Data Science Lab Project - Application.ipynb" notebook and the run it all. Writing articles with the Qwen LLM takes some time (around 1 minure per request) and sometimes fails, in that case run the cell again. Anyway, all the articles obtained have been previously saved in the "Article.docs" file and can be read there.

5. For more information please read the report of the project