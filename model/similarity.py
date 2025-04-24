import os
import random
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# Enhanced knowledge base with document types, responses, and official resources
knowledge_base = [
    {
        'document_type': 'divorce',
        'keywords': ['divorce', 'separation', 'alimony', 'child custody', 'marital', 'spouse', 'marriage dissolution'],
        'response': "For divorce proceedings, we offer divorce petition forms, property settlement agreements, child custody agreements, and alimony arrangement documents. For official guidance, I recommend visiting the U.S. Courts website (https://www.uscourts.gov/services-forms/divorce) or your state's judicial website. For example, California residents can find resources at https://www.courts.ca.gov/selfhelp-divorce.htm. Would you like me to guide you to a specific divorce form?"
    },
    {
        'document_type': 'will',
        'keywords': ['will', 'testament', 'inheritance', 'estate', 'heir', 'beneficiary', 'executor', 'probate', 'trust'],
        'response': "For wills and testaments, we have last will templates, living will forms, and executor appointment documents. For additional guidance, visit the American Bar Association's estate planning resources at https://www.americanbar.org/groups/real_property_trust_estate/. The AARP also offers excellent will resources at https://www.aarp.org/money/investing/info-2022/complete-guide-to-wills.html. Would you like assistance with a specific type of will?"
    },
    {
        'document_type': 'power_of_attorney',
        'keywords': ['power of attorney', 'poa', 'legal authority', 'representative', 'incapacitation', 'healthcare proxy', 'durable power'],
        'response': "Our Power of Attorney documents include general POA, limited POA, medical POA, and durable POA options. For elder law concerns, visit the National Academy of Elder Law Attorneys at https://www.naela.org/. You can find state-specific information through USA.gov at https://www.usa.gov/legal-docs. The NIH also provides guidance on healthcare POAs at https://www.nia.nih.gov/health/advance-care-planning. Which POA document interests you?"
    },
    {
        'document_type': 'business',
        'keywords': ['business', 'corporation', 'llc', 'partnership', 'startup', 'entrepreneur', 'company', 'incorporation', 'bylaws'],
        'response': "For business documentation, we offer incorporation papers, LLC formation documents, partnership agreements, and business contract templates. The Small Business Administration offers comprehensive guidance at https://www.sba.gov/business-guide/launch-your-business/choose-business-structure. For tax considerations, review the IRS business structures page at https://www.irs.gov/businesses/small-businesses-self-employed/business-structures. What type of business document do you need?"
    },
    {
        'document_type': 'real_estate',
        'keywords': ['real estate', 'property', 'lease', 'rental', 'mortgage', 'tenant', 'landlord', 'deed', 'eviction', 'foreclosure'],
        'response': "Our real estate document collection includes lease agreements, property purchase contracts, mortgage applications, and landlord-tenant forms. For tenants' rights, visit the U.S. Department of Housing and Urban Development at https://www.hud.gov/topics/rental_assistance. For mortgage guidance, consult the Consumer Financial Protection Bureau at https://www.consumerfinance.gov/owning-a-home/. What kind of real estate transaction are you working on?"
    },
    {
        'document_type': 'intellectual_property',
        'keywords': ['copyright', 'trademark', 'patent', 'intellectual property', 'ip', 'creative works', 'invention', 'brand protection'],
        'response': "We have intellectual property documents including copyright registrations, trademark applications, patent documents, and IP assignment agreements. For official filing information, visit the U.S. Patent and Trademark Office at https://www.uspto.gov/ for patents and trademarks, and the U.S. Copyright Office at https://copyright.gov/ for copyright protection. The USPTO also offers guided assistance at https://www.uspto.gov/learning-and-resources. What IP protection are you seeking?"
    },
    {
        'document_type': 'employment',
        'keywords': ['employment', 'job', 'worker', 'employee', 'hiring', 'termination', 'contract', 'labor', 'workplace', 'discrimination'],
        'response': "Our employment documents include employment contracts, non-disclosure agreements, termination letters, and workplace policy templates. The U.S. Department of Labor provides extensive guidance on employment laws at https://www.dol.gov/. For workplace discrimination concerns, visit the Equal Employment Opportunity Commission at https://www.eeoc.gov/. What employment document do you need assistance with?"
    },
    {
        'document_type': 'family',
        'keywords': ['family', 'adoption', 'guardianship', 'name change', 'prenuptial', 'postnuptial', 'paternity', 'child support'],
        'response': "We offer various family law documents including adoption applications, guardianship forms, name change petitions, and marriage agreements. For child support guidelines, visit the Office of Child Support Enforcement at https://www.acf.hhs.gov/css. The Child Welfare Information Gateway also provides resources on adoption and guardianship at https://www.childwelfare.gov/. What family law matter can I help you with?"
    },
    {
        'document_type': 'immigration',
        'keywords': ['immigration', 'visa', 'citizenship', 'naturalization', 'green card', 'permanent resident', 'alien', 'deportation'],
        'response': "For immigration matters, reliable information is critical. The official U.S. Citizenship and Immigration Services website at https://www.uscis.gov/ provides all necessary forms and guidance. For visa information, visit the State Department at https://travel.state.gov/content/travel/en/us-visas.html. While we can help with document organization, we recommend consulting these official sources or an immigration attorney. What immigration document do you need help with?"
    },
    {
        'document_type': 'tax',
        'keywords': ['tax', 'taxes', 'irs', 'deduction', 'credit', 'filing', 'return', 'audit', 'exemption'],
        'response': "For tax matters, the Internal Revenue Service (IRS) provides comprehensive guidance and forms at https://www.irs.gov/. For state taxes, visit your state's department of revenue website. The IRS offers interactive tax assistants at https://www.irs.gov/help/ita to help determine filing status, credits, and deductions. While I can direct you to these resources, specific tax advice should come from a qualified tax professional. What tax information are you seeking?"
    },
    {
        'document_type': 'benefits',
        'keywords': ['benefits', 'medicare', 'medicaid', 'social security', 'disability', 'veteran', 'retirement', 'unemployment', 'welfare'],
        'response': "Government benefit programs have specific requirements and application procedures. For Social Security, visit https://www.ssa.gov/. For Medicare, visit https://www.medicare.gov/. For Medicaid, visit https://www.medicaid.gov/ or your state's health services website. Benefits.gov also offers a benefit finder tool at https://www.benefits.gov/benefit-finder to identify programs you may qualify for. Which benefit program information do you need?"
    },
    {
        'document_type': 'general',
        'keywords': ['document', 'form', 'legal', 'paperwork', 'template', 'agreement', 'contract', 'help', 'guidance'],
        'response': "We offer a wide range of legal documents and forms, along with connections to official government resources. For comprehensive legal information, USA.gov provides resources at https://www.usa.gov/legal-services. To help you better, could you specify what kind of legal matter you need assistance with? I can then direct you to the appropriate forms and official guidance."
    }
]

# Enhanced default responses with references to resources
default_responses = [
    "I'm not sure I understand what legal document you need. For general legal information, USA.gov offers resources at https://www.usa.gov/legal-services. Could you provide more details about your situation?",
    "To better assist you, I need more information about the specific legal document you're looking for. You might find general guidance at the American Bar Association's public resources: https://www.americanbar.org/groups/legal_services/flh-home/",
    "I'd like to help you find the right legal document and relevant government resources. Could you tell me more about your legal needs? This will help me direct you to both our templates and official guidance.",
    "I don't have enough context to recommend specific documents. The Legal Services Corporation can help you find local legal aid at https://www.lsc.gov/about-lsc/what-legal-aid/get-legal-help if you need affordable assistance. Could you explain your legal situation in more detail?"
]

def preprocess_text(text):
    """Preprocess text by converting to lowercase and removing special characters"""
    text = text.lower()
    text = re.sub(r'[^\w\s]', '', text)
    return text

def get_document(user_query):
    """
    Find the most relevant document based on the user query using cosine similarity
    
    Args:
        user_query (str): The user's input message
        
    Returns:
        str: A response message recommending appropriate documents
    """
    if not user_query:
        return "I'm here to help you find the right legal documents. What type of legal matter are you dealing with?"
    
    # Preprocess the user query
    processed_query = preprocess_text(user_query)
    
    # Check for direct keyword matches first (simple approach)
    for item in knowledge_base:
        for keyword in item['keywords']:
            if keyword in processed_query:
                return item['response']
    
    # If no direct matches, use TF-IDF and cosine similarity
    try:
        # Create corpus with knowledge base items
        corpus = [' '.join(item['keywords']) for item in knowledge_base]
        corpus.append(processed_query)
        
        # Calculate TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(corpus)
        
        # Calculate similarity between query and each knowledge base item
        query_vector = tfidf_matrix[-1]
        document_vectors = tfidf_matrix[:-1]
        
        # Calculate cosine similarity
        similarities = cosine_similarity(query_vector, document_vectors).flatten()
        
        # Get index of most similar document
        best_match_index = similarities.argmax()
        
        # If similarity is above threshold, return the response
        if similarities[best_match_index] > 0.1:
            return knowledge_base[best_match_index]['response']
        else:
            return random.choice(default_responses)
            
    except Exception as e:
        # Fallback to simpler matching if there's an error with the similarity calculation
        print(f"Error in similarity calculation: {str(e)}")
        return random.choice(default_responses)
