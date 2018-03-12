<?php
/**
 * @author kevin.r.jesse@gmail.com
 */
require("/home/ubuntu/chatbox/frontend/backend_connect.php");

if(function_exists($_GET['action'])) {
    echo $_GET['action']($s);
}
socket_close($s);
//die();

function submit($s) {
#    $content = socket_read($s, 2048);
    #socket_close($s);
    return $content;
}

function getJson($s) {
    $json = json_encode(array('getJson' => true));
}

function kill($s) {
    socket_write($s, "log", strlen("log"));
    $content = socket_read($s, 2048);
}
?>
