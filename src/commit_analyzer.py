import os
import logging
from langchain.chat_models import ChatOpenAI
from langchain.prompts import ChatPromptTemplate
from langchain.chains import LLMChain

class CommitAnalyzer:
    """Analyzes commit information and generates human-readable descriptions using AI."""
    
    def __init__(self, model_name="gpt-3.5-turbo", max_tokens=500):
        """
        Initialize the commit analyzer.
        
        Args:
            model_name (str, optional): Name of the OpenAI model to use. Defaults to "gpt-3.5-turbo".
            max_tokens (int, optional): Maximum tokens for the response. Defaults to 500.
        """
        self.api_key = os.getenv('OPENAI_API_KEY')
        if not self.api_key:
            raise ValueError("OpenAI API key is required. Set it in .env file.")
        
        self.model_name = model_name
        self.max_tokens = max_tokens
        
        # Initialize the language model
        self.llm = ChatOpenAI(
            model_name=self.model_name,
            temperature=0.7,
            max_tokens=self.max_tokens
        )
        
        # Create the prompt template for commit analysis
        self.prompt_template = ChatPromptTemplate.from_template(
            """You are an expert at explaining technical changes in simple terms.
            
            Analyze the following GitHub commit information and provide a clear, concise explanation 
            that would be understandable to non-technical team members.
            
            Project Description: {project_description}
            
            Commit Message: {commit_message}
            
            Files Changed:
            {files_changed}
            
            Stats:
            - Additions: {additions}
            - Deletions: {deletions}
            - Total Changes: {total_changes}
            
            Please provide:
            1. A summary of what changed in simple terms
            2. The potential impact of these changes on the project
            3. Any important information that non-technical team members should know
            
            Keep your response concise and focused on explaining the changes in plain language.
            """
        )
        
        # Create the chain
        self.chain = LLMChain(llm=self.llm, prompt=self.prompt_template)
    
    def format_files_changed(self, files_changed):
        """
        Format the files changed information for the prompt.
        
        Args:
            files_changed (list): List of dictionaries containing file change information.
            
        Returns:
            str: Formatted string of file changes.
        """
        formatted_files = ""
        for file in files_changed:
            status_map = {
                'added': 'Added',
                'modified': 'Modified',
                'removed': 'Removed',
                'renamed': 'Renamed',
            }
            status = status_map.get(file.get('status', '').lower(), file.get('status', ''))
            formatted_files += f"- {status}: {file.get('filename', '')} "
            formatted_files += f"(+{file.get('additions', 0)}, -{file.get('deletions', 0)})"
            formatted_files += "\n"
        
        return formatted_files
    
    def analyze_commit(self, commit_details, project_description=""):
        """
        Analyze a commit and generate a human-readable description.
        
        Args:
            commit_details (dict): Dictionary containing commit details.
            project_description (str, optional): Description of the project. Defaults to "".
            
        Returns:
            str: Human-readable description of the commit changes.
        """
        if not commit_details:
            logging.error("No commit details provided for analysis.")
            return ""
        
        try:
            # Format the files changed information
            files_changed = self.format_files_changed(commit_details.get('files_changed', []))
            
            # Prepare the input for the chain
            chain_input = {
                'project_description': project_description,
                'commit_message': commit_details.get('message', ''),
                'files_changed': files_changed,
                'additions': commit_details.get('stats', {}).get('additions', 0),
                'deletions': commit_details.get('stats', {}).get('deletions', 0),
                'total_changes': commit_details.get('stats', {}).get('total', 0)
            }
            
            # Run the chain to get the description
            result = self.chain.run(chain_input)
            return result.strip()
        
        except Exception as e:
            logging.error(f"Error analyzing commit: {str(e)}")
            return "Failed to analyze commit due to an error."