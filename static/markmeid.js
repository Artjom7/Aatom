// <form> pole vaja salvestada, et värskendada lehe
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

// Küsib, mida kasutajale näidata, ja renderdab selle
$.ajax({url: "/api/markmeid?postitaja=" + postitaja + "&filter=" + filter, success: function(sisend){
    tabel_dokument = document.getElementById("postitused").innerHTML
    for (i in sisend) {
        i = sisend[i]
        var faili = i.failid_len == 0 ? '' : `<span class="badge rounded-pill text-bg-primary">+ ` +
                        + i.failid_len + (i.failid_len == '1' ? ' Fail ' : ' Faili ') +
                      `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-folder2" viewBox="0 0 17 17">
                        <path d="M1 3.5A1.5 1.5 0 0 1 2.5 2h2.764c.958 0 1.76.56 2.311 1.184C7.985 3.648 8.48 4 9 4h4.5A1.5 1.5 0 0 1 15 5.5v7a1.5 1.5 0 0 1-1.5 1.5h-11A1.5 1.5 0 0 1 1 12.5v-9zM2.5 3a.5.5 0 0 0-.5.5V6h12v-.5a.5.5 0 0 0-.5-.5H9c-.964 0-1.71-.629-2.174-1.154C6.374 3.334 5.82 3 5.264 3H2.5zM14 7H2v5.5a.5.5 0 0 0 .5.5h11a.5.5 0 0 0 .5-.5V7z"/>
                       </svg></span>`
        if (i.privaatne) {
            var privaatne = '<span class="badge rounded-pill text-bg-warning">' +
                `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-lock2" viewBox="0 0 17 17">
                  <path d="M10 7v1.076c.54.166 1 .597 1 1.224v2.4c0 .816-.781 1.3-1.5 1.3h-3c-.719 0-1.5-.484-1.5-1.3V9.3c0-.627.46-1.058 1-1.224V7a2 2 0 1 1 4 0zM7 7v1h2V7a1 1 0 0 0-2 0z"/>
                  <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
                </svg>`
                + ' Privaatne' + `</span>`
        } else {
         var privaatne = i.omanik ? '<span class="badge rounded-pill text-bg-success">' +
                `<svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-file-earmark-check" viewBox="0 0 17 17">
                  <path d="M10.854 7.854a.5.5 0 0 0-.708-.708L7.5 9.793 6.354 8.646a.5.5 0 1 0-.708.708l1.5 1.5a.5.5 0 0 0 .708 0l3-3z"/>
                  <path d="M14 14V4.5L9.5 0H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h8a2 2 0 0 0 2-2zM9.5 3A1.5 1.5 0 0 0 11 4.5h2V14a1 1 0 0 1-1 1H4a1 1 0 0 1-1-1V2a1 1 0 0 1 1-1h5.5v2z"/>
                </svg>`
                + ' Avalik' + `</span>` : ''
        }
        document.getElementById("postitused").innerHTML += `
            <div class="col">
                <div class="card shadow">
                    <div class="card-body">
                        <h5 class="ellipsis-title pb-1 card-title fw-semibold">${i.pealkiri}</h5>
                        <div class="overflow-auto pb-3">
                            <span class="badge rounded-pill text-bg-secondary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-person-fill" viewBox="0 0 17 17">
                                    <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3Zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"></path>
                                </svg>
                                ${i.autor + ' ' + i.autor_lend}
                            </span>
                            <span class="badge rounded-pill text-bg-secondary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock" viewBox="0 0 17 17">
                                  <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                                  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                                </svg> ${i.kuupaev}
                            </span>
                        </div>
                        <h6 class="card-subtitle mb-1 mt-0 text-body-secondary fw-medium">${i.aine}</h6>
                        <p class="ellipsis-content card-text my-2" style="white-space: pre-wrap;">${i.sisu}</p>
                        <div class="d-flex justify-content-between align-items-center">
                            <a href="/markmik/${i.id}" type="button" class="btn btn-sm btn-outline-primary">
                                Vaata
                            </a>
                            <div class="overflow-auto ms-2">
                                ${privaatne}
                                ${faili}
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `
    }
}});

// Muudab tunni teemasid, mida kasutaja näeb
function muutdaFilter(filter) {
    var url = new URL(window.location.href);
    url.searchParams.set('filter', filter);
    window.location.href = url;
}

// Muudab, kelle postitusi näidata
function muudaPostitaja(postitaja) {
    var url = new URL(window.location.href);
    url.searchParams.set('postitaja', postitaja);
    window.location.href = url;
}

// Kontrollib, kas kõik vajalikud väljad on õigesti täidetud
function varskendaFailiTekst() {
    var fail_form = document.getElementById('postitus-fail')
    var failid = fail_form.files
    var faili_tekst = document.getElementById('postitus-faili-tekst')

    // Kustutab veateate
    document.getElementById('error_postitus').innerHTML = '';
    suurus = 0
    for (var i = 0; i < failid.length; i++) {
        suurus += failid[i].size;
    }

    // Failid mida saab laadida üles (peab muuta ka failid markmeid.py)
    lubatud_failid = ['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'xlsx', 'docx', 'pptx'];

    var labis_testi = true
    for (var i = 0; i < failid.length; i++) {
        labis_testi &= lubatud_failid.includes(failid[i].name.split('.').pop())
    }

    // Tagastab vea, kui midagi on valesti
    if (failid.length > 10) {
        document.getElementById('error_postitus').innerHTML = 'Maksimaalselt 10 faili!';
        faili_tekst.value = '';
        fail_form.value = '';
    } else if (!labis_testi) {
        document.getElementById('error_postitus').innerHTML = 'Saab saata ainult järgmised failid: txt, pdf, png, jpg, jpeg, gif, xlsx, docx, pptx.';
        faili_tekst.value = '';
        fail_form.value = '';
    } else if (suurus > 16000000) {
        document.getElementById('error_postitus').innerHTML = 'Maksimaalselt 16 MB!';
        faili_tekst.value = '';
        fail_form.value = '';
    } else if (failid.length == 0) {
        faili_tekst.value = '';
    } else if (failid.length == 1) {
        faili_tekst.value = failid[0].name;
    } else  if (failid.length == 2) {
        faili_tekst.value = failid[0].name + ' ja veel 1 fail';
    } else {
        faili_tekst.value = failid[0].name + ' ja veel ' + (failid.length - 1) + ' faili';
    }
}

// Tagastab viga kui postitusel pole pealkirja
function luuaPostitus() {
    var pealkiri = document.getElementById('postitus-pealkiri').value

    if (pealkiri == '') {
        document.getElementById('error_postitus').innerHTML = 'Pealkiri on kohustuslik!'
    }
}
