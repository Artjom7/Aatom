//SocketIO ühendadamine
var socket = io.connect('http://' + document.domain + ':' + location.port);

// Kellaeg
var kellString = d => ("0" + d.getDate()).slice(-2) + "-" + ("0"+(d.getMonth()+1)).slice(-2) + "-" +
    d.getFullYear() + " " + ("0" + d.getHours()).slice(-2) + ":" + ("0" + d.getMinutes()).slice(-2);

// HTML konteiner sõnumitega
var konteiner = $('#messages-container');

// Võtab vastu ja saadab sõnumeid
function initVestlus(minuNimi, kasutaja_id) {
    saitOnLaadinud()
    // Kuvab sõnumi andmebaasist või kui keegi saadab uue
    function renderdaSonum(msg) {
        var onMinuSonum = msg.id === kasutaja_id;
        // Koostab HTML koodi (sõnum)
        konteiner.append(`
            <div class="${onMinuSonum ? 'chat-message-right' : 'chat-message-left'} mb-4">
                <div>
                    <div class="text-muted small text-nowrap mt-2">${msg.date}</div>
                </div>
                <div class="${onMinuSonum ? 'bg-primary bg-gradient text-light' : 'bg-light'} flex-shrink-1 rounded py-2 px-3 mr-3 me-0" style="filter: hue-rotate(${tulemus_varv}deg)">
                    <div class="font-weight-bold me-0"><b>${msg.user_name}</b></div>
                    <p class="mb-1" style="filter: hue-rotate(-${tulemus_varv}deg)">
                    ${msg.message}
                    </hp>
                </div>
            </div>
        `);
        $(function () {$('[data-bs-toggle="tooltip"]').tooltip()})
        if (onMinuSonum) {
            konteiner.scrollTop(konteiner[0].scrollHeight);
        }
    }

    socket.on( 'connect', function() {
      saitOnLaadinud()
      socket.emit( 'uus_kasutaja')
      var vorm = $( 'form' ).on( 'submit', function( e ) {
        e.preventDefault()
        let user_input = $( 'input.message' ).val()
        if (user_input.length===0) {
            return;
        }
        anonuumne = document.getElementById('anonuumne').checked
        // Saadab kasutaja sõnumi
        socket.emit( 'event', {
          id : kasutaja_id,
          user_name : anonuumne ? 'Anonüümne' : minuNimi,
          message : user_input,
          date: kellString(new Date()),
        } )
        $( 'input.message' ).val( '' ).focus()
      } )
    } )

    // Katkestab kasutaja ühenduse lahkumise korral
    window.addEventListener("beforeunload", function(e){
       socket.disconnect(0);
    }, false);


    // Annab kogu vestluse ajalugu
    socket.on( 'vestluse_lugu', function( msgs, callback ) {
      konteiner.html("");
      msgs.forEach(renderdaSonum);
      konteiner.scrollTop(konteiner[0].scrollHeight);
    });
    // Kui keegi vastab
    socket.on('vastus', renderdaSonum);
}
