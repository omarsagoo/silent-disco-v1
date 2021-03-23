var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'connect', function() {
    var element = document.getElementById("message-holder");
    element.scrollTop = element.scrollHeight;
    
    party_id = document.location.pathname.substr(6)
    socket.emit( 'connection', {
        party_id : party_id,
    })

    window.onbeforeunload = function () {
        socket.emit( 'disconnection', {
            party_id : party_id,
        })
        return null
    }

    var form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'textarea#message' ).val()
        socket.emit( 'message', {
            message : user_input,
            party_id : party_id
        })
        $( 'textarea#message' ).val("") 
    })
})

socket.on( 'recieved message', function( msg ) {
    if( typeof msg.message !== 'undefined' ) {
        $( 'h3' ).remove()
        $( 'div.message_holder' ).append('<div><b style="color: #000">'+ msg.name +'</b> '+msg.message+'</div>' )

        var element = document.getElementById("message-holder");
        element.scrollTop = element.scrollHeight;
    }
})

$("textarea#message").keypress(function (e) {
    if(e.which === 13 && !e.shiftKey) {
        e.preventDefault();
    
        $(this).closest("form").submit();
    }
});