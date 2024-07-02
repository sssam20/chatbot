jQuery(document).ready(function($) {
    function appendMessage(message, messageType) {
        var messageElement = $('<div/>', {
            class: messageType + '-message',
            html: message.replace(/\n/g, '<br>')
        });
        $('#chatbot-messages').append(messageElement);
        $('#chatbot-messages').scrollTop($('#chatbot-messages')[0].scrollHeight);
    }

    $('#chatbot-send').click(function() {
        var query = $('#chatbot-input').val();
        if (query.trim() !== '') {
            appendMessage(query, 'user');
            $('#chatbot-input').val('');

            $.ajax({
                url: chatbotAjax.ajax_url,
                method: 'POST',
                data: {
                    action: 'my_chatbot_query',
                    query: query
                },
                success: function(response) {
                    if (response.success) {
                        appendMessage(response.data.response, 'bot');
                    } else {
                        appendMessage('Error: ' + response.data, 'bot');
                    }
                },
                error: function() {
                    appendMessage('Error communicating with the server.', 'bot');
                }
            });
        }
    });
});
