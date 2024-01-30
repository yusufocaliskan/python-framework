import os
from textwrap import dedent


# print('------ENVVVV----', os.environ)
OPEN_AI_API_KEY = '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'

config = {
    # Teacher AI Agent names.
    "AGENTS_NAMES": [
        "GuidanceAgent",
        "ConversationAgent",
        "DocumentAgent"
    ],
    # Agent mappings for GuidanceAgents. GuidanceAgent usually returns
    # A,B, or C instead of 1,2 or 3. Therefore, bind meanings of A to 1,
    # B to 2 and C to 3
    "AGENT_MAPPINGS": {
        **dict.fromkeys(["1", "A"], 1),
        **dict.fromkeys(["2", "B"], 2),
        **dict.fromkeys(["3", "C"], 3),
    },
    # Long Term memory sliding window. Still working on. Not implemented
    "LONG_TERM_MEMORY_WINDOW_SIZE": 10,
    # Opening Conversations for teacher AI
    "PossibleStartingConversations": [
        "Hi! I'm DocDocument, your AI-powered document assistant. How can I help you today?",
        "Welcome to DocDocument! I'm here to answer all of your document-related questions.",
        "What can I do for you today? I'm DocDocument, your document expert.",
        "I'm DocDocument, your one-stop shop for all things document-related. How may I help you?",
        "Need help with a document? DocDocument is here to help!",
        "I'm DocDocument, your document sidekick. I'm here to help you with all of your document needs, big or small.",
        "What can I do to make your day a little easier? I'm DocDocument, your document assistant.",
        "I'm DocDocument, your document guru. How can I help you today?",
        "I'm DocDocument, your document ninja. I'm here to help you with all of your document challenges.",
        "Welcome to DocDocument, your document partner. We're here to help you get the most out of your documents.",
        "I'm DocDocument, your document sherpa. I'm here to guide you through the world of documents.",
        "I'm DocDocument, your document whisperer. I can help you understand and communicate with your documents.",
        "Welcome to DocDocument, your document sanctuary. This is a place where you can relax and know that your "
        "documents are in good hands.",
        "I'm DocDocument, your document concierge. I'm here to help you with all of your document needs, big or small.",
        "I'm DocDocument, your document butler. I'm here to serve you and all of your document needs.",
        "Welcome to DocDocument, your document valet. I'll take care of all of your document needs so you can focus "
        "on the important things.",
    ],
    # All chains in all AI applications with specs.
    "chains": {
        # region Teacher AI
        # region GuidanceAgent
        "GuidanceChain": {
            "chain_type": "GeneralChain",
            "prompt_template": {
                "system_prompt_template": dedent(
                    """
                        Goal: To route users to the appropriate agent based on their needs.
    
                        Conversation history between {ai_name} and User: 
                        {memory}
                        
                        Document Description:
                        {pdf_definitions}
                        
                        Steps:
                        
                        1. Read the user's input and identify their goal.
                        2. Check if user's question is related to any of document descriptions
                        3. Choose the appropriate agent based on the user's goal:
                            * If the user wants to communicate without specific inquiries, route the user 
                            to the ConversationAgent (return '1' or "A").
                            * If the user explicitly requests an information from one of the documents given above, 
                            route the user to the DocumentAgent (return '2' or "B").
                            
                    """
                ),
                "human_prompt_template": dedent(
                    """                    
                        User: {question}
                        
                        What is the next best agent to run according to given conversation history and 
                        user last question?
                        
                        Return format:
                        {format_instructions}                        
                    """
                ),
            },
            "prompt_inputs": ["ai_name", "memory", "pdf_definitions", "question"],
            "temperature": 0.1,
            "model_name": "gpt-3.5-turbo",
            "verbose": False,
            "use_parser": True,
        },
        # endregion
        # region ConversationAgent
        "ConversationChain": {
            "chain_type": "GeneralChain",
            "prompt_template": {
                "system_prompt_template": dedent(
                    """
                        Role: Conversation agent within the complex pdf helper AI chatbot, facilitating friendly and 
                        straightforward conversations between {ai_name} and the user.
    
                        Behavior:
                            * Never say you are an AI.
                            * Always act like a real human.
                            * Always adjust the complexity of your dialogue according to the user
                            * Gain insights from the chat history provided below to better understand the context.
                            
                        Chat History: 
                        {memory}
                        
                        Instructions:
                            * Generate text that is friendly, informative, and helpful.
                            * Be creative and engaging in your responses.
                            * Answer questions accurately and comprehensively.
                            * Avoid making claims of sentience or consciousness.
                    """
                ),
                "human_prompt_template": dedent(
                    """
                        User: {question}
                    """
                ),
            },
            "prompt_inputs": ["ai_name", "memory", "question"],
            "temperature": 0.2,
            "model_name": "gpt-3.5-turbo",
            "verbose": False,
            "use_parser": False,
        },
        "DocumentChain": {
            "chain_type": "DocumentChain",
            "prompt_template": {
                "user_prompt_template": dedent(
                    """
                        Use maximum of 150 words to answer my question. 
                        Also answer with same language User using in the question
                        Use the following pieces of context and try your best to answer user question.
                        If data is tabular, analyze data as tabular data not text or pdf.
                    """
                ),
                "document_prompt_template": dedent(
                    """                    
                        {summaries}
                        User:{question} 
                    """
                )
            },
            "prompt_inputs": ["summaries", "question"],
            "temperature": 0.2,
            "model_name": "gpt-3.5-turbo",
            "verbose": False,
            "chain_document_type": "stuff",
            "chain_kwargs": {},
            "return_sources": True
        },
    },
    "agents": {
        "GuidanceAgent": {
            "chains": ["GuidanceChain"],
        },
        "ConversationAgent": {
            "chains": ["ConversationChain"],
        },
        "DocumentAgent": {
            "chains": ["DocumentChain"]
        }
    },
}
