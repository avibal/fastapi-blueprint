
var chatMessages = null;
var userInput = null;
var sendButton = null;

document.addEventListener('DOMContentLoaded', function() {    
    chatMessages = document.getElementById('chat-messages');
    userInput = document.getElementById('user_input');    
    sendButton = document.getElementById('sendButton');

    sendButton.addEventListener('click', () => {
        const userMessage = document.getElementById('user_input').value;        
        if (userMessage.trim() !== '') {
            const url = '/process_data?user_input=' + encodeURIComponent(userMessage);
            // Display user message
            const messageElement = document.createElement('div');
            messageElement.classList.add('message-content', 'user-message');
            messageElement.textContent = userMessage;
            chatMessages.appendChild(messageElement);

            // Send message to server (replace with your actual API call)
            fetch(url)
                .then(response => response.json())
                .then(data => {
                    // Display AI response
                    printResponseJSON(data);
                    printBOTIcon(chatMessages);    


                    const aiMessageElement = document.createElement('div');
                    aiMessageElement.classList.add('message-content','ai-message');                                                        
                    
                    // Iterate through each step in the JSON response                    
                    data.steps.forEach(paragraph => {                        
                        printMessgae(paragraph,aiMessageElement)                                                
                    });

                    chatMessages.appendChild(aiMessageElement);

                    // Scroll to the bottom of the chat messages
                    chatMessages.scrollTop = chatMessages.scrollHeight;

                    // Clear user input field
                    userInput.value = '';
                    
                })
                .catch(error => {
                    console.error('Error fetching data:', error);
                });
        }
    });
});


function printMessgae(paragraph,aiMessageElement) {   
    // Extract the step number and content
    const stepNumber = Object.keys(paragraph)[0];
    const stepContent = paragraph[stepNumber];

    // Create a new paragraph element for the step
    const stepElement = document.createElement('p');
    aiMessageElement.appendChild(stepElement);


    let index = 0;

    const typingInterval = setInterval(() => {
        if (index < stepContent.length) {            
            stepElement.textContent += stepContent[index++];
        } else {
            clearInterval(typingInterval);
        }
    }, 10);
}

function printBOTIcon(aiMessageElement) { 
    // Create the image element
    const ImageDivElement = document.createElement('div');
    ImageDivElement.classList.add('ai-icon'); // Add a class for styling
    aiMessageElement.appendChild(ImageDivElement);
    
    const imageElement = document.createElement('img');
    imageElement.src = 'static/images/boticon.png'; // Replace with your image path
    imageElement.alt = 'AI Bot Icon';
    imageElement.classList.add('ai-icon'); // Add a class for styling

    // Append the image to the AI message element
    ImageDivElement.appendChild(imageElement);
}



function printResponseJSON(json_data) {

    const steps = json_data.steps;
        
    // 1. Format the JSON string with indentation
    const formattedJSON = JSON.stringify(json_data, null, 2);

    // 2. Create a `<pre>` element with the formatted JSON
    const preElement = document.createElement('pre');
    preElement.textContent = formattedJSON;

    // 3. Add a CSS class for styling
    preElement.classList.add('json-pretty');

    // 4. Replace the content of the 'responseJSON' div
    document.getElementById('responseJSON').innerHTML = ''; // Clear existing content
    document.getElementById('responseJSON').appendChild(preElement);
}




/*-------------------------------------------------*/

document.addEventListener('DOMContentLoaded', function() {    
    return;
    document.getElementById('send-button').addEventListener('click', function() {
        
        const user_input = document.getElementById('user_input').value;                 
        const url = '/process_data?user_input=' + user_input;
        console.log(user_input)

        fetch(url)
            .then(response => response.json())
            .then(json_data => {                
                console.log(json_data)
                populatePartialData(json_data);
            })
            .catch(error => console.error('Error:', error));
    });
});

function populatePartialData(json_data) {
    
    populatePartialDataOnlyJson(json_data);
    
    const steps = json_data.steps;
    
    let html = '';
    steps.forEach(step => {
        // Extract the step number and content
        const stepNumber = Object.keys(step)[0];
        const stepContent = step[stepNumber];
        
        html += '<br/><div class="message-content">'
        // Create HTML for each step
        html += stepContent + '<br>';
        html += '</div>';

        
    });

    // Update the HTML content
    let messageContent = document.getElementById('message').innerHTML;    
    document.getElementById('message').innerHTML = messageContent +  html;
}






