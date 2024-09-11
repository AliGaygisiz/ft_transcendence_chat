let url = `ws://${window.location.host}/ws/global-chat/`

const chatSocket = new WebSocket(url)

chatSocket.onmessage = function (e) {
  let data = JSON.parse(e.data)
  console.log('Data: ', data)

  if (data.type === 'chat') {
    let messages = document.getElementById('chat-window')
    messages.insertAdjacentHTML('beforeend', `<div>
<p><b>${data.sender}: </b>${data.message}</p>
</div>`)
  } else if (data.type === 'activity' && data.message === 'joined') {
    let activeUsers = document.getElementById('active-users')

    let userElement = document.createElement('p');
    let userLink = document.createElement('a');
    userLink.href = "#";
    userLink.className = "username-link";
    userLink.dataset.username = data.sender;
    userLink.textContent = data.sender;
    console.log('User link: ', data.sender);
    userElement.appendChild(userLink);

    activeUsers.appendChild(userElement);

    userLink.addEventListener('click', function (e) {
      e.preventDefault();
      fetch('/dm/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded',
          'X-CSRFToken': getCsrfToken()  // Add CSRF token
        },
        body: JSON.stringify({
          'username': data.sender
        })
      }).then(response => {
        if (!response.ok) {
          throw new Error('Network response was not ok');
        }
        return response.text();
      }).then(data => {
        // Here you can handle the response data
        // For example, you can replace the current page content with the received data
        document.body.innerHTML = data;
      }).catch(error => {
        console.error('There has been a problem with your fetch operation:', error);
      });
    });
  } else if (data.type === 'activity' && data.message === 'left') {
    let activeUsers = document.getElementById('active-users')
    // find the username as p tag and remove it
    let pTags = activeUsers.getElementsByTagName('p')
    for (let i = 0; i < pTags.length; i++) {
      if (pTags[i].textContent === data.sender) {
        pTags[i].remove()
      }
    }
  }
}

let form = document.getElementById('message-form')
form.addEventListener('submit', (e) => {
  e.preventDefault()
  let message = document.getElementById('message-input').value
  chatSocket.send(JSON.stringify({
    'message': message
  }))
  form.reset()
})
