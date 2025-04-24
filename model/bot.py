import re
import random
import os

# Enhanced response patterns for legal assistance chatbot with government resources
patterns = [
    {
        'pattern': r'(?i)hello|hi|hey',
        'responses': [
            "Hello! I'm your legal documentation assistant. I can help with divorce documents, wills, business formation, or power of attorney forms. I can also direct you to official government resources for additional guidance. How can I assist you today?",
            "Hi there! I'm here to help with legal documents and provide resources from official government websites. Would you like assistance with divorce papers, wills, business contracts, or power of attorney documents?",
            "Greetings! I'm your legal assistant here to guide you through document preparation and connect you with official resources. I can help with divorce, wills, contracts, and power of attorney. What legal matter can I assist you with today?"
        ]
    },
    {
        'pattern': r'(?i)divorce|family law',
        'responses': [
            "I can help with divorce and family law documents. Our templates include divorce petitions, custody agreements, and property division forms. For official guidance, I recommend visiting the U.S. Courts website (https://www.uscourts.gov/services-forms/divorce) or your state's judicial website. Would you like to proceed with our divorce petition form?",
            "Family law matters require careful attention. I can assist with divorce forms, custody agreements, and financial disclosures. For state-specific requirements, check your state court's website. California residents can visit https://www.courts.ca.gov/selfhelp-divorce.htm. What specific forms do you need?",
            "For divorce proceedings, I offer petition forms, custody arrangements, and financial disclosure templates. These should be supplemented with guidance from your state's court website. The American Bar Association also offers free resources at https://www.americanbar.org/groups/family_law/. What aspect of divorce are you dealing with?"
        ]
    },
    {
        'pattern': r'(?i)will|testament|estate',
        'responses': [
            "Estate planning is crucial for protecting your assets and wishes. I offer simple wills, living wills, and comprehensive estate plans. For additional guidance, visit the American Bar Association's estate planning resources at https://www.americanbar.org/groups/real_property_trust_estate/. Would you like to create a basic will or something more comprehensive?",
            "I can help you prepare a will or testament. For state-specific estate laws, consult your state's probate court website. The AARP offers excellent resources at https://www.aarp.org/money/investing/info-2022/complete-guide-to-wills.html. Would you like to start with our Last Will and Testament template?",
            "Estate planning involves wills, trusts, and advance directives. For tax implications, review the IRS estate tax information at https://www.irs.gov/businesses/small-businesses-self-employed/estate-tax. I can help you create these documents, but consulting with a local attorney is also recommended. Which document would you like to start with?"
        ]
    },
    {
        'pattern': r'(?i)contract|agreement',
        'responses': [
            "I can provide various contract templates for business and personal use. For consumer protection guidelines, review the FTC's resources at https://consumer.ftc.gov/. For business contracts, the SBA offers guidance at https://www.sba.gov/business-guide/launch-your-business/write-your-business-plan. What type of agreement do you need?",
            "Contracts should be carefully crafted to protect all parties. I offer templates for employment, services, and sales agreements. The U.S. Department of Labor provides guidance on employment contracts at https://www.dol.gov/. What specific contract are you looking for?",
            "Legal agreements are essential for clear relationships. I can help with business formation, employment, services, and sales contracts. For intellectual property considerations, visit the USPTO at https://www.uspto.gov/. For international contracts, consult the International Trade Administration at https://www.trade.gov/. What type of agreement do you need?"
        ]
    },
    {
        'pattern': r'(?i)power of attorney|poa',
        'responses': [
            "Power of Attorney documents are crucial for proper representation. I offer general, limited, medical, and financial POA templates. For elder law concerns, visit the National Academy of Elder Law Attorneys at https://www.naela.org/. The NIH also provides guidance on healthcare POAs at https://www.nia.nih.gov/health/advance-care-planning. Which type of POA do you need?",
            "POA documents vary by purpose and jurisdiction. Medical POAs (also called healthcare proxies) are governed by state laws. You can find state-specific information through USA.gov at https://www.usa.gov/legal-docs. Would you like to create a general or limited power of attorney?",
            "Power of Attorney documents let you designate someone to make decisions when you cannot. For military members, the Armed Forces Legal Assistance website offers POA guidance at https://legalassistance.law.af.mil/. For seniors, AARP provides resources at https://www.aarp.org/caregiving/financial-legal/. What's your primary concern with creating a POA?"
        ]
    },
    {
        'pattern': r'(?i)business|company|corporation|llc',
        'responses': [
            "I can help with business formation documents for LLCs, corporations, and partnerships. The Small Business Administration offers comprehensive guidance at https://www.sba.gov/business-guide/launch-your-business/choose-business-structure. Your state's Secretary of State website also has specific requirements. Which business structure interests you?",
            "Business formation requires careful planning. I offer templates for articles of organization, operating agreements, and bylaws. For tax considerations, review the IRS business structures page at https://www.irs.gov/businesses/small-businesses-self-employed/business-structures. The SBA also offers free business plan templates at https://www.sba.gov/business-guide/plan-your-business/write-your-business-plan. What type of business are you forming?",
            "Setting up a business involves legal, tax, and regulatory considerations. I can provide templates for LLCs, corporations, and partnerships. For industry-specific requirements, consult the relevant regulatory agency through USA.gov's business section at https://www.usa.gov/business. For startup guidance, the SBA offers resources at https://www.sba.gov/business-guide. What business structure are you considering?"
        ]
    },
    {
        'pattern': r'(?i)custody|child support|visitation',
        'responses': [
            "Child custody matters are sensitive and governed by state laws. I can provide templates for custody agreements and parenting plans. For state guidelines on child support, visit the Office of Child Support Enforcement at https://www.acf.hhs.gov/css. What specific custody document do you need assistance with?",
            "I offer templates for custody agreements, visitation schedules, and parenting plans. Each state has specific child support calculators available through their court websites. The Child Welfare Information Gateway also offers resources at https://www.childwelfare.gov/. Would you like to draft a custody agreement or calculate child support?",
            "Child custody and support are primarily concerned with the child's best interests. I can help with joint custody agreements, sole custody documents, and visitation schedules. For mediation services, visit your state court's family services division or review resources at https://www.uscourts.gov/services-forms/mediation. What aspect of custody are you dealing with?"
        ]
    },
    {
        'pattern': r'(?i)tenant|landlord|lease|rent',
        'responses': [
            "I can provide residential and commercial lease agreements. For tenants' rights, visit the U.S. Department of Housing and Urban Development at https://www.hud.gov/topics/rental_assistance. For landlords, the American Apartment Owners Association offers resources at https://www.american-apartment-owners-association.org/. What type of rental document do you need?",
            "Rental relationships require clear documentation. I offer lease agreements, rental applications, and eviction notices. For fair housing information, visit https://www.hud.gov/program_offices/fair_housing_equal_opp. Your state may also have specific landlord-tenant laws available through your state's housing authority website. Are you a landlord or tenant?",
            "I can help with residential leases, commercial leases, sublease agreements, and rental notices. For eviction procedures, consult your local housing court. During emergencies like COVID-19, special protections may apply; check https://www.consumerfinance.gov/coronavirus/mortgage-and-housing-assistance/ for updates. What rental document do you need to create?"
        ]
    },
    {
        'pattern': r'(?i)tax|taxes|irs',
        'responses': [
            "Tax matters involve both federal and state considerations. While I don't offer tax advice, I can direct you to the IRS website at https://www.irs.gov/ for federal tax forms and information. For state taxes, visit your state's department of revenue. Would you like links to specific tax forms?",
            "For tax guidance, the IRS offers comprehensive resources at https://www.irs.gov/. For small business taxes, visit https://www.irs.gov/businesses/small-businesses-self-employed. Free tax preparation assistance is available through VITA and TCE programs for eligible individuals. What specific tax information are you looking for?",
            "Tax planning involves understanding applicable deductions and credits. The IRS offers interactive tax assistants at https://www.irs.gov/help/ita. For retirement tax questions, visit https://www.irs.gov/retirement-plans. For tax implications of major life events, check https://www.irs.gov/individuals/life-events. What tax-related documents do you need help with?"
        ]
    },
    {
        'pattern': r'(?i)benefit|medicare|medicaid|social security',
        'responses': [
            "Government benefits programs have specific eligibility requirements and application procedures. For Social Security, visit https://www.ssa.gov/. For Medicare, visit https://www.medicare.gov/. For Medicaid, visit https://www.medicaid.gov/ or your state's health services website. Which benefit program are you interested in?",
            "I can help you understand benefit programs. Social Security retirement benefits can be applied for online at https://www.ssa.gov/benefits/retirement/. Medicare enrollment information is available at https://www.medicare.gov/sign-up-change-plans. Benefits.gov also offers a benefit finder tool at https://www.benefits.gov/benefit-finder. What specific benefit are you inquiring about?",
            "Government assistance programs help millions of Americans. For disability benefits, visit https://www.ssa.gov/benefits/disability/. For veterans' benefits, visit https://www.va.gov/. For unemployment insurance, contact your state's unemployment office. USA.gov provides a comprehensive list of benefit programs at https://www.usa.gov/benefits. Which program do you need information about?"
        ]
    },
    {
        'pattern': r'(?i)immigration|visa|citizenship|naturalization',
        'responses': [
            "Immigration matters involve complex federal regulations. The official U.S. Citizenship and Immigration Services website at https://www.uscis.gov/ provides forms, processing times, and status checks. The State Department handles visa information at https://travel.state.gov/content/travel/en/us-visas.html. What immigration document do you need help with?",
            "For immigration guidance, USCIS offers comprehensive resources at https://www.uscis.gov/. For citizenship application information, visit https://www.uscis.gov/citizenship. The immigration courts (EOIR) website is https://www.justice.gov/eoir. Would you like information on a specific immigration process?",
            "Immigration processes vary by visa type and situation. For family-based immigration, visit https://www.uscis.gov/family. For employment-based immigration, check https://www.uscis.gov/working-in-the-united-states. For humanitarian programs, see https://www.uscis.gov/humanitarian. What specific immigration information are you seeking?"
        ]
    },
    {
        'pattern': r'(?i)help|guidance|assist|what can you do',
        'responses': [
            "I can help with legal documents and direct you to government resources. My areas of expertise include: 1) Divorce/family law, 2) Wills/estate planning, 3) Business formation, 4) Power of attorney documents, 5) Landlord-tenant matters, and 6) Government benefits information. I can also provide links to official websites for further guidance. What area interests you?",
            "I assist with legal document preparation and provide links to official government resources. I cover divorce papers, wills, business formation, power of attorney forms, rental agreements, and more. I can also direct you to federal and state websites for additional information. What specific legal matter do you need help with?",
            "My purpose is to help you navigate legal documentation and find official resources. I can guide you through creating documents for divorce, estate planning, business formation, power of attorney, and rental agreements. I also provide links to government websites for authoritative information. What legal area can I help you with today?"
        ]
    },
    {
        'pattern': r'(?i)thank you|thanks',
        'responses': [
            "You're welcome! Remember that while I provide document templates and resources, consulting with a qualified attorney for your specific situation is always recommended. Is there anything else I can help you with?",
            "Happy to help! For ongoing legal updates and resources, consider bookmarking USA.gov's legal section at https://www.usa.gov/legal-services. Is there anything else you'd like to know about our services or legal resources?",
            "My pleasure. For finding local legal aid if you need affordable assistance, the Legal Services Corporation offers a search tool at https://www.lsc.gov/about-lsc/what-legal-aid/get-legal-help. Don't hesitate to ask if you have more questions."
        ]
    },
    {
        'pattern': r'(?i)yes|yes please|sure|okay|please',
        'responses': [
            "Great! To help you better, could you specify which type of legal document or information you're looking for? Our categories include divorce forms, wills, business contracts, power of attorney documents, rental agreements, and government benefits information.",
            "Excellent! Let me know which legal area you need assistance with: divorce/family law, wills/estate planning, business formation, power of attorney, landlord-tenant matters, or government benefits. This will help me guide you to the right templates and resources.",
            "Perfect! To assist you properly, please let me know which legal topic you're interested in: divorce papers, estate planning, business formation, power of attorney forms, rental agreements, or government benefits information. Each area has specific forms and resources."
        ]
    },
    {
        'pattern': r'(?i)bye|goodbye',
        'responses': [
            "Goodbye! Remember that USA.gov (https://www.usa.gov/) is a comprehensive resource for government services and information. Feel free to return if you need more legal document assistance.",
            "Farewell! If you need legal assistance beyond document preparation, the American Bar Association offers a referral service at https://www.americanbar.org/groups/legal_services/flh-home/. I'm here whenever you need help with legal paperwork.",
            "Take care! For legal aid resources if you need affordable assistance, visit https://www.lsc.gov/about-lsc/what-legal-aid/get-legal-help. Don't hesitate to come back for your legal documentation needs."
        ]
    }
]

# Default responses when no pattern matches
default_responses = [
    "I'm not sure I understand. Could you please provide more details about the legal document you need? I can help with divorce forms, wills, business contracts, or power of attorney documents.",
    "I'd like to help you with your legal documentation needs. Could you be more specific? Our most popular categories are divorce/family law, wills/estate planning, business formation, and power of attorney.",
    "I don't have enough information to assist you properly. Could you tell me which category of legal documents you're looking for? Our services include divorce forms, wills, business contracts, and power of attorney documents.",
    "I'm your legal documentation assistant. Please specify what kind of legal forms you need help with. You can say things like 'I need divorce papers' or 'Help me create a will' so I can guide you better."
]

def get_response(message):
    """
    Generate a response based on the input message using pattern matching.
    
    Args:
        message (str): The user's input message
        
    Returns:
        str: A response message
    """
    if not message:
        return "I'm here to help with your legal documentation needs. What can I assist you with today?"
    
    # Check for matches in our patterns
    for item in patterns:
        if re.search(item['pattern'], message):
            return random.choice(item['responses'])
    
    # Return default response if no pattern matches
    return random.choice(default_responses)
