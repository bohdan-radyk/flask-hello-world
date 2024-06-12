$(document).ready(function() {
    var likedMessages = [];

    $('#sendButton').click(function() {
        sendMessage();
    });

    $('#messageInput').keypress(function(e) {
        if (e.which == 13) {
            sendMessage();
        }
    });

    $('#showKnowledgeBaseButton').click(function() {
        showKnowledgeBase();
    });

    $('.close-button').click(function() {
        $('#knowledgeBaseContainer').hide();
    });

    function sendMessage() {
        var message = $('#messageInput').val();
        if (message.trim() !== '') {
            appendMessage('user', 'Анастасія', 'static/user.png', message);
            $('#messageInput').val('');
            askQuestion(message);
             // $.ajax({
             //    url: "https://flask-hello-world-hk41.onrender.com/"+message, 
             //    success: function(result){
             //        // addMessage(result, "AI Assistant");
             //        appendMessage('bot', 'AI Assistant', 'bot.jpg', result);
             //    }
             //  });
        }
    }

    function askQuestion(message) {
        $.ajax({
            // url: 'https://flask-hello-world-hk41.onrender.com/askQuestion',
            url: 'https://flask-hello-world-hk41.onrender.com/askQuestion',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(message),
            success: function(response) {
                var message = response.response.replace(" * ", "<br>").replace(/\*\*(.*?)\*\*/g, '<br><strong>$1</strong>');
                appendMessage('bot', 'AI Асистент', 'static/bot.jpg', message);
            },
            error: function(error) {
                alert('Error saving message:', error);
            }
        });
    }

    function appendMessage(sender, name, photo, message) {
        var time = new Date().toLocaleTimeString();
        var messageElement = $('<div></div>').addClass('message').addClass(sender);

        var imgElement = $('<img>').attr('src', photo);
        var contentElement = $('<div></div>').addClass('message-content');
        var infoElement = $('<div></div>').addClass('message-info').html('<span>' + name + '</span><span>' + time + '</span>');
        var textElement = $('<div>'+message+'</div>');
        var likeButton = $('<button></button>').addClass('like-button').text('Зберегти в базу рішень').click(function() {
            var messageObj = { sender: sender, name: name, message: message, time: time };
            likedMessages.push(messageObj);
            saveMessageToServer(messageObj);
        });

        contentElement.append(infoElement).append(textElement).append(likeButton);
        messageElement.append(imgElement).append(contentElement);
        $('#chatWindow').append(messageElement);
        $('#chatWindow').scrollTop($('#chatWindow')[0].scrollHeight);
    }

    function saveMessageToServer(message) {
        $.ajax({
            url: 'https://flask-hello-world-hk41.onrender.com/saveMessage',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify(message),
            success: function(response) {
                console.log('Message saved successfully:', response);
            },
            error: function(error) {
                console.error('Error saving message:', error);
            }
        });
    }

    function showKnowledgeBase() {
        $.ajax({
            url: 'https://flask-hello-world-hk41.onrender.com/getMessages',
            type: 'GET',
            success: function(response) {
                likedMessages = response;
                var tableBody = $('#knowledgeBaseTable tbody');
                tableBody.empty();
                likedMessages.forEach(function(msg, index) {
                    var row = $('<tr></tr>');
                    row.append('<td>' + msg.sender + '</td>');
                    row.append('<td>' + msg.name + '</td>');
                    row.append('<td>' + msg.message + '</td>');
                    row.append('<td>' + msg.time + '</td>');
                    var removeButton = $('<button></button>').text('Remove').click(function() {
                        removeMessageFromServer(index);
                    });
                    row.append($('<td></td>').append(removeButton));
                    tableBody.append(row);
                });
                $('#knowledgeBaseContainer').show();
            },
            error: function(error) {
                console.error('Error fetching messages:', error);
            }
        });
    }

    function removeMessageFromServer(index) {
        $.ajax({
            url: 'https://flask-hello-world-hk41.onrender.com/deleteMessage',
            type: 'POST',
            contentType: 'application/json',
            data: JSON.stringify({ index: index }),
            success: function(response) {
                likedMessages.splice(index, 1);
                showKnowledgeBase();
                console.log('Message removed successfully:', response);
            },
            error: function(error) {
                console.error('Error removing message:', error);
            }
        });
    }
});
