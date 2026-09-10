/*main-page*/
async function sendRequest(endpoint) {
  const email = document.getElementById('email').value.trim();
  const password = document.getElementById('password').value.trim();
  const name = document.getElementById('name').value.trim();

  if (!email || !password || (endpoint === 'register' && !name)) {
    displayMessage('Please fill in all required fields.', 'red');
    return;
  }

  const data = { email, password, name };

  try {
    const response = await fetch(`http://127.0.0.1:5000/${endpoint}`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data)
    });

    const result = await response.json();
    const message = document.getElementById('message');

    if (result.success) {
      if (endpoint === 'login') {
        localStorage.setItem('name', result.name);
        localStorage.setItem('level', result.level);
        window.location.href = 'dashboard.html';
      } else {
        displayMessage('Registration successful! You can now log in.', 'lightgreen');
      }
    } else {
      if (endpoint === 'login' && result.message === 'User does not exist') {
        const confirmRegister = confirm('User not found. Would you like to register instead?');
        if (confirmRegister) {
          document.getElementById('registerBtn').click();
        } else {
          displayMessage('Login cancelled. You may try a different email.', 'orange');
        }
      } else {
        displayMessage(result.message, 'red');
      }
    }
  } catch (error) {
    console.error('Error connecting to server:', error);
    displayMessage('Server error. Please try again later.', 'red');
  }
}

function displayMessage(msg, color) {
  const message = document.getElementById('message');
  message.textContent = msg;
  message.style.color = color;
}

document.addEventListener('DOMContentLoaded', () => {
  const loginBtn = document.getElementById('loginBtn');
  const registerBtn = document.getElementById('registerBtn');

  if (loginBtn && registerBtn) {
    loginBtn.onclick = () => sendRequest('login');
    registerBtn.onclick = () => sendRequest('register');
  }
});
