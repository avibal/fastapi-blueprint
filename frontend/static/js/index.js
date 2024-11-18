document.addEventListener('DOMContentLoaded', function() {    
    
    document.getElementById('submit').addEventListener('click', function() {
        
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

        // Create HTML for each step
        html += stepContent + '<br>';
        
    });

    // Update the HTML content
    document.getElementById('response').innerHTML = html;
}


function populatePartialDataOnlyJson(json_data) {

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