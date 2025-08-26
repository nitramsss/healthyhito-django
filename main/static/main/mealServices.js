API_ENDPOINT = ' http://127.0.0.1:8000/meal-api';

async function sendDataToDjango(data) {
    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    try {
        const response = await fetch(API_ENDPOINT, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrfToken, 
            },
            body: JSON.stringify(data),
        });

        if (!response.ok) {
            throw new Error(`HTTP error! status: ${response.status}`);
        }

        const responseData = await response.json();
        console.log('Data from Django:', responseData);
    } catch (error) {
        console.error('Error sending data:', error);
    }
};

// Example usage:
const myData = {
    name: 'John Doe',
    age: 30
};
sendDataToDjango(myData);