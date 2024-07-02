<?php
/*
Plugin Name: My Chatbot Plugin
Description: A simple chatbot plugin that communicates with a Flask backend server.
Version: 1.0
Author: Your Name
*/

// Enqueue scripts and styles
function my_chatbot_enqueue_scripts() {
    wp_enqueue_style('my-chatbot-css', plugins_url('assets/css/chatbot.css', __FILE__));
    wp_enqueue_script('my-chatbot-js', plugins_url('assets/js/chatbot.js', __FILE__), array('jquery'), null, true);
    wp_localize_script('my-chatbot-js', 'chatbotAjax', array('ajax_url' => admin_url('admin-ajax.php')));
}
add_action('wp_enqueue_scripts', 'my_chatbot_enqueue_scripts');

// Create a shortcode for the chatbot
function my_chatbot_shortcode() {
    return '<div id="chatbot-container">
                <div id="chatbot-messages"></div>
                <input type="text" id="chatbot-input" placeholder="Type your message here..." />
                <button id="chatbot-send">Send</button>
            </div>';
}
add_shortcode('my_chatbot', 'my_chatbot_shortcode');

// Handle AJAX requests
function my_chatbot_handle_ajax() {
    $query = sanitize_text_field($_POST['query']);
    $response = wp_remote_post('http://localhost:5000/chat', array(
        'body' => json_encode(array('query' => $query)),
        'headers' => array('Content-Type' => 'application/json')
    ));

    if (is_wp_error($response)) {
        wp_send_json_error('Error communicating with the chatbot server.');
    } else {
        wp_send_json_success(json_decode(wp_remote_retrieve_body($response)));
    }
}
add_action('wp_ajax_my_chatbot_query', 'my_chatbot_handle_ajax');
add_action('wp_ajax_nopriv_my_chatbot_query', 'my_chatbot_handle_ajax');
