document.addEventListener('DOMContentLoaded', function() {
    const form = document.getElementById('startupForm');
    const loadingSection = document.getElementById('loading');
    const resultSection = document.getElementById('resultSection');
    const feedbackContainer = document.getElementById('feedback');
    const errorContainer = document.getElementById('error');
    
    // Simple Markdown parser for basic formatting
    function parseMarkdown(text) {
        if (!text) return '';
        
        // Handle bold text: **text** -> <strong>text</strong>
        text = text.replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>');
        
        // Handle italic text: *text* -> <em>text</em> (but not if it's already part of bold)
        text = text.replace(/(?<!\*)\*((?!\*).*?)\*(?!\*)/g, '<em>$1</em>');
        
        // Handle headers: # Header -> <h3>Header</h3>
        text = text.replace(/^# (.*?)$/gm, '<h3>$1</h3>');
        text = text.replace(/^## (.*?)$/gm, '<h4>$1</h4>');
        
        // Handle lists: - item -> <li>item</li>
        text = text.replace(/^- (.*?)$/gm, '<li>$1</li>');
        text = text.replace(/(<li>.*?<\/li>\n?)+/g, '<ul>$&</ul>');
        
        // Handle line breaks: \n -> <br>
        text = text.replace(/\n/g, '<br>');
        
        return text;
    }
    
    form.addEventListener('submit', async function(e) {
        e.preventDefault();
        
        // Reset previous results and errors
        errorContainer.textContent = '';
        feedbackContainer.innerHTML = '';
        resultSection.style.display = 'none';
        
        // Show loading
        loadingSection.style.display = 'block';
        
        // Get form data
        const formData = new FormData(form);
        
        try {
            // Send API request
            const response = await fetch('/api/validate', {
                method: 'POST',
                body: formData
            });
            
            // Hide loading
            loadingSection.style.display = 'none';
            
            if (!response.ok) {
                const errorData = await response.json();
                throw new Error(errorData.detail || 'An error occurred');
            }
            
            const data = await response.json();
            
            // Parse and display results with Markdown formatting
            feedbackContainer.innerHTML = parseMarkdown(data.feedback);
            resultSection.style.display = 'block';
            
            // Scroll to results
            resultSection.scrollIntoView({ behavior: 'smooth' });
            
        } catch (error) {
            console.error('Error:', error);
            loadingSection.style.display = 'none';
            errorContainer.textContent = error.message || 'Something went wrong. Please try again.';
            errorContainer.style.display = 'block';
        }
    });
});
