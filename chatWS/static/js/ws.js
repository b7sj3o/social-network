const user_id = Math.random().toString(16).slice(2);
const message_form = document.getElementById("message__form");
const messages_ul = document.getElementById("messages");

// Send
const socket = new WebSocket("ws://localhost:7000");
socket.onopen = () => {
    console.log("Connected")
}
socket.onmessage = (event) => {
    console.log(event.data);
    const message = JSON.parse(event.data);
    const li_item = document.createElement("li");
    li_item.textContent = message.text;
    li_item.classList.add('to_me')
    messages_ul.appendChild(li_item);
}

message_form.addEventListener('submit', (e) => {
    e.preventDefault()

    const message = message_form.elements['id_message'].value;
    console.log(message);
    // send data to backend
    socket.send(JSON.stringify({ text: message, sender: user_id }));
    // ---
    const li_item = document.createElement("li");
    li_item.classList.add('from_me');
    li_item.textContent = message;
    messages_ul.appendChild(li_item);
})