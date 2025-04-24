document.addEventListener('DOMContentLoaded', function() {
    // DOM elements
    const servicesList = document.getElementById('services-list');
    const formsList = document.getElementById('forms-list');
    const formDetails = document.getElementById('form-details');
    const formTitle = document.getElementById('form-title');
    const formFields = document.getElementById('form-fields');
    const documentForm = document.getElementById('document-form');
    const documentPreview = document.getElementById('document-preview');
    const previewContent = document.getElementById('preview-content');
    const downloadBtn = document.getElementById('download-doc');
    const refreshServicesBtn = document.getElementById('refresh-services');
    const chatInput = document.getElementById('chat-input');
    const sendMessageBtn = document.getElementById('send-message');
    const chatMessages = document.getElementById('chat-messages');
    
    // Log all elements to debug
    console.log("Elements loaded:", {
        servicesList, formsList, formDetails, formTitle, formFields,
        documentForm, documentPreview, previewContent, downloadBtn,
        refreshServicesBtn, chatInput, sendMessageBtn, chatMessages
    });
    
    // Current selections
    let selectedServiceId = null;
    let selectedFormId = null;
    let currentFormData = null;
    
    // Fetch services on page load
    fetchServices();
    
    // Event listeners
    refreshServicesBtn.addEventListener('click', fetchServices);
    
    documentForm.addEventListener('submit', function(e) {
        e.preventDefault();
        generateDocument();
    });
    
    downloadBtn.addEventListener('click', downloadDocument);
    
    sendMessageBtn.addEventListener('click', sendChatMessage);
    
    chatInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendChatMessage();
        }
    });
    
    // Functions
    function fetchServices() {
        servicesList.innerHTML = `
            <div class="col-12 text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        
        fetch('/api/services')
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                displayServices(data);
            })
            .catch(error => {
                servicesList.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger" role="alert">
                            Failed to load services: ${error.message}
                        </div>
                    </div>
                `;
                console.error('Error fetching services:', error);
            });
    }
    
    function displayServices(services) {
        if (services.length === 0) {
            servicesList.innerHTML = `
                <div class="col-12">
                    <p class="text-center text-muted">No services available</p>
                </div>
            `;
            return;
        }
        
        servicesList.innerHTML = '';
        services.forEach(service => {
            const serviceCard = document.createElement('div');
            serviceCard.className = 'col-md-6 col-lg-4';
            serviceCard.innerHTML = `
                <div class="card service-card h-100" data-service-id="${service.service_id}">
                    <div class="card-body">
                        <h5 class="card-title">${service.service_name}</h5>
                        <p class="card-text">${service.service_description || 'No description available'}</p>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-sm btn-outline-primary view-forms-btn">View Forms</button>
                    </div>
                </div>
            `;
            
            servicesList.appendChild(serviceCard);
            
            serviceCard.querySelector('.view-forms-btn').addEventListener('click', function() {
                selectService(service.service_id);
            });
        });
    }
    
    function selectService(serviceId) {
        selectedServiceId = serviceId;
        
        // Clear any existing active service
        document.querySelectorAll('.service-card').forEach(card => {
            card.classList.remove('active');
        });
        
        // Mark selected service as active
        const selectedCard = document.querySelector(`.service-card[data-service-id="${serviceId}"]`);
        if (selectedCard) {
            selectedCard.classList.add('active');
        }
        
        // Reset other sections
        formDetails.classList.add('d-none');
        documentPreview.classList.add('d-none');
        
        // Show loading in forms list
        formsList.innerHTML = `
            <div class="col-12 text-center">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
            </div>
        `;
        
        // Fetch forms for this service
        fetch(`/api/forms?service_id=${serviceId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                displayForms(data);
            })
            .catch(error => {
                formsList.innerHTML = `
                    <div class="col-12">
                        <div class="alert alert-danger" role="alert">
                            Failed to load forms: ${error.message}
                        </div>
                    </div>
                `;
                console.error('Error fetching forms:', error);
            });
    }
    
    function displayForms(forms) {
        console.log("Displaying forms:", forms);
        if (forms.length === 0) {
            formsList.innerHTML = `
                <div class="col-12">
                    <p class="text-center text-muted">No forms available for this service</p>
                </div>
            `;
            return;
        }
        
        formsList.innerHTML = '';
        forms.forEach(form => {
            console.log("Processing form:", form);
            const formCard = document.createElement('div');
            formCard.className = 'col-md-6';
            formCard.innerHTML = `
                <div class="card form-card h-100" data-form-id="${form.form_id}">
                    <div class="card-body">
                        <h5 class="card-title">${form.form_name}</h5>
                        <p class="card-text">Service: ${form.service_name}</p>
                    </div>
                    <div class="card-footer">
                        <button class="btn btn-sm btn-primary fill-form-btn">Fill Form</button>
                    </div>
                </div>
            `;
            
            formsList.appendChild(formCard);
            
            formCard.querySelector('.fill-form-btn').addEventListener('click', function() {
                selectForm(form.form_id, form.form_name);
            });
        });
    }
    
    function selectForm(formId, formName) {
        console.log("Selected form:", formId, formName);
        selectedFormId = formId;
        formTitle.textContent = formName;
        
        // Show loading in form fields
        formFields.innerHTML = `
            <div class="text-center py-3">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-2">Loading form details...</p>
            </div>
        `;
        
        // Show the form details section
        formDetails.classList.remove('d-none');
        
        // Scroll to form details
        formDetails.scrollIntoView({ behavior: 'smooth' });
        
        // Hide document preview
        documentPreview.classList.add('d-none');
        
        // Fetch form details
        console.log("Fetching details for form ID:", formId);
        fetch(`/api/form-details?form_id=${formId}`)
            .then(response => {
                if (!response.ok) {
                    throw new Error('Network response was not ok');
                }
                return response.json();
            })
            .then(data => {
                currentFormData = data;
                displayFormFields(data);
            })
            .catch(error => {
                formFields.innerHTML = `
                    <div class="alert alert-danger" role="alert">
                        Failed to load form details: ${error.message}
                    </div>
                `;
                console.error('Error fetching form details:', error);
            });
    }
    
    function displayFormFields(formData) {
        console.log("Form data received:", formData);
        formFields.innerHTML = '';
        
        // Group questions by category
        const categories = {};
        const questions = [];
        const formDetails = [];
        
        formData.forEach(item => {
            console.log("Processing item:", item);
            if (item.form_id) {
                formDetails.push(item);
            } else if (item.name) {
                categories[item.id] = item;
            } else if (item.ques_id) {
                questions.push(item);
            }
        });
        
        console.log("Categories:", categories);
        console.log("Questions:", questions);
        console.log("Form details:", formDetails);
        
        // Group questions by category
        const questionsByCategory = {};
        questions.forEach(question => {
            const categoryId = question.category_id;
            console.log("Processing question:", question, "in category:", categoryId);
            if (!questionsByCategory[categoryId]) {
                questionsByCategory[categoryId] = [];
            }
            questionsByCategory[categoryId].push(question);
        });
        
        // Create form fields by category
        console.log("Categories by ID:", questionsByCategory);
        
        // Create "Submit" button even if there are no categories or questions
        if (Object.keys(questionsByCategory).length === 0) {
            const noQuestionsMessage = document.createElement('div');
            noQuestionsMessage.className = 'alert alert-info';
            noQuestionsMessage.innerHTML = `
                <p class="mb-0">This form has no input fields. You can still generate the document.</p>
            `;
            formFields.appendChild(noQuestionsMessage);
        }
        
        Object.keys(questionsByCategory).forEach(categoryId => {
            const category = categories[categoryId];
            if (!category) {
                console.error(`Category not found for ID: ${categoryId}`);
                return;
            }
            
            const categoryQuestions = questionsByCategory[categoryId];
            console.log(`Building UI for category ${categoryId}:`, category);
            
            const categoryDiv = document.createElement('div');
            categoryDiv.className = 'form-category mb-4';
            categoryDiv.innerHTML = `
                <h3 class="mb-3">${category.name}</h3>
                <p class="text-muted mb-3">${category.description || ''}</p>
            `;
            
            const questionDiv = document.createElement('div');
            questionDiv.className = 'row g-3';
            
            categoryQuestions.forEach(question => {
                const fieldDiv = document.createElement('div');
                fieldDiv.className = 'col-md-6';
                // Extract just the numeric part of the question ID (e.g., "Q001" -> "001")
                const quesIdNumber = question.ques_id.replace('Q', '');
                fieldDiv.innerHTML = `
                    <div class="form-group">
                        <label for="q-${question.ques_id}" class="form-label">${question.ques_text}</label>
                        <input type="text" class="form-control" id="q-${question.ques_id}" 
                               name="${quesIdNumber}" placeholder="${question.placeholder || ''}" required>
                    </div>
                `;
                questionDiv.appendChild(fieldDiv);
            });
            
            categoryDiv.appendChild(questionDiv);
            formFields.appendChild(categoryDiv);
        });
        
        // Add a hidden input for form_id
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'form_id';
        hiddenInput.value = selectedFormId;
        formFields.appendChild(hiddenInput);
    }
    
    function generateDocument() {
        console.log("Generating document for form ID:", selectedFormId);
        // Collect form data
        const formData = {
            form_id: selectedFormId
        };
        
        // Get values from inputs
        document.querySelectorAll('#form-fields input[name]').forEach(input => {
            if (input.name !== 'form_id') {
                // Extract the question ID from the input name - we need just the numeric part
                const quesId = input.name.replace('Q', '');
                formData[quesId] = input.value;
            }
        });
        
        console.log("Form data to submit:", formData);
        
        // Show loading in preview
        documentPreview.classList.remove('d-none');
        previewContent.innerHTML = `
            <div class="text-center py-5">
                <div class="spinner-border text-primary" role="status">
                    <span class="visually-hidden">Loading...</span>
                </div>
                <p class="mt-3">Generating your document...</p>
            </div>
        `;
        
        // Scroll to preview
        documentPreview.scrollIntoView({ behavior: 'smooth' });
        
        // Call API to generate document
        fetch('/api/final-content', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(formData)
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Network response was not ok');
            }
            return response.json();
        })
        .then(data => {
            // Display the generated document content
            previewContent.innerHTML = data.content;
        })
        .catch(error => {
            previewContent.innerHTML = `
                <div class="alert alert-danger" role="alert">
                    Failed to generate document: ${error.message}
                </div>
            `;
            console.error('Error generating document:', error);
        });
    }
    
    function downloadDocument() {
        // Collect form data again
        const formData = {
            form_id: selectedFormId
        };
        
        // Get values from inputs
        document.querySelectorAll('#form-fields input[name]').forEach(input => {
            if (input.name !== 'form_id') {
                // Extract the question ID from the input name - we need just the numeric part
                const quesId = input.name.replace('Q', '');
                formData[quesId] = input.value;
            }
        });
        
        // Create a temporary form to submit the download request
        const tempForm = document.createElement('form');
        tempForm.method = 'POST';
        tempForm.action = '/api/final-form';
        tempForm.style.display = 'none';
        
        // Add form data as hidden input
        const hiddenInput = document.createElement('input');
        hiddenInput.type = 'hidden';
        hiddenInput.name = 'formData';
        hiddenInput.value = JSON.stringify(formData);
        tempForm.appendChild(hiddenInput);
        
        // Add form to body and submit
        document.body.appendChild(tempForm);
        tempForm.submit();
        
        // Remove the form after submission
        setTimeout(() => {
            document.body.removeChild(tempForm);
        }, 1000);
    }
    
    function sendChatMessage() {
        const userMessage = chatInput.value.trim();
        if (!userMessage) return;
        
        // Clear input
        chatInput.value = '';
        
        // Log for debugging
        console.log("Sending chat message:", userMessage);
        
        // Add user message to chat
        addMessageToChat(userMessage, 'user');
        
        // Show typing indicator
        const typingIndicator = document.createElement('div');
        typingIndicator.className = 'message ai-message typing-indicator';
        typingIndicator.innerHTML = `
            <div class="message-content">
                <span class="spinner-grow spinner-grow-sm"></span>
                <span class="spinner-grow spinner-grow-sm"></span>
                <span class="spinner-grow spinner-grow-sm"></span>
            </div>
        `;
        chatMessages.appendChild(typingIndicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
        
        // Call API for AI response
        fetch('/api/chat', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ user_chat: userMessage })
        })
        .then(response => {
            console.log("Response status:", response.status);
            return response.json();
        })
        .then(data => {
            console.log("Chat response data:", data);
            
            // Remove typing indicator
            chatMessages.removeChild(typingIndicator);
            
            // Add AI response to chat
            addMessageToChat(data.aiMessage, 'ai');
        })
        .catch(error => {
            console.error('Error in chat:', error);
            
            // Remove typing indicator
            try {
                chatMessages.removeChild(typingIndicator);
            } catch (e) {
                console.error("Could not remove typing indicator:", e);
            }
            
            // Add error message
            addMessageToChat('Sorry, I encountered an error. Please try again later.', 'ai');
        });
    }
    
    function addMessageToChat(message, sender) {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${sender}-message`;
        messageDiv.innerHTML = `
            <div class="message-content">${message}</div>
        `;
        
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
});
