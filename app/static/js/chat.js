var socket = io.connect('http://' + document.domain + ':' + location.port);

socket.on( 'connect', function() {
    party_id = document.location.pathname.substr(6)
    socket.emit( 'message', {
        party_id : party_id,
        message : 'COnNECTED USeR'
    })
    var form = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'textarea#message' ).val()
        socket.emit( 'message', {
            message : user_input,
            party_id : party_id
        })
        $( 'input.message' ).val( '' ).focus()
    })
})

window.onbeforeunload(function (e) {
    socket.on('disconnect', function() {
        party_id = document.location.pathname.substr(6)
        socket.emit( 'message', {
            party_id : party_id,
            message : 'dIsCOnNECTED USeR'
        })
    })
})


socket.on( 'recieved message', function( msg ) {
    console.log( msg )
    if( typeof msg.message !== 'undefined' ) {
        $( 'h3' ).remove()
        $( 'div.message_holder' ).append('<div><b style="color:             #000">'+ msg.name +'</b> '+msg.message+'</div>' )
    }
})