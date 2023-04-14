// <form> pole vaja salvestada, et värskendada lehe
if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

// On vaja, et kasutaja infokast töötaks
//$(function () {
//  $('[data-bs-toggle="popover"]').popover()
//})

var eelmised_haaled = {}
var tulemus
// Kus lehekülg laadib, siis renderdakse kõik küsitlused
$.ajax({url: "/api/kysimustik?sakk="+sakk, success: function(sisend){
    tulemus = sisend
    for (var i = tulemus.length-1; i >= 0; i--) {
        var andmed_kusimus = tulemus[i]
        eelmised_haaled[i] = andmed_kusimus.haal
        var lulitatud = !andmed_kusimus.umberhaalimine && andmed_kusimus.haal != -1 ? 'disabled' : ''
        var haali = Object.values(andmed_kusimus.haaled).reduce((osalineSum, a) => osalineSum + a, 0);
        var valikud_html = ''
        for (var j = 0; j < andmed_kusimus.valikud.length; j++) {
            var valitud_automaatselt = andmed_kusimus.haal == j ? 'checked' : ''
            var protsent =  parseFloat((haali > 0 ? (andmed_kusimus.haaled[j] / haali * 100) : 0).toFixed(1))
            valikud_html += `
                <div class="mt-4">
                    <label style="width: 100%;
                    -webkit-user-select: none;
                    -ms-user-select: none;
                    user-select: none;">
                        <span>
                            <p name="protsent${i+1}" class="card-text mb-1" style="display:inline-block">` + protsent + `%</p>
                            <p class="card-text" style="display:inline-block;"><b>` + andmed_kusimus.valikud[j] + `</b></p>

                        </span>
                        <br>
                        <div style="display: flex; align-items: center;">
                            <input ${lulitatud} ${valitud_automaatselt} onclick="kontrolliVastus(${i+1}, ${j})" type="radio" value="${j}" name="radio${i+1}" class="form-check-input me-2 mt-0" autocomplete="off">
                            <div style="flex: 1 1 auto; height: 10px" class="progress" role="progressbar">
                                <div name="edenemisriba${i+1}" class="progress-bar" style="width: ${protsent}%"></div>
                            </div>
                        </div>
                    </label>
                </div>
            `
        }
        document.getElementById("kusitluse-array").innerHTML += `
            <div id="vorm${i+1}" class="container d-flex justify-content-center mb-4">
                <div class="card col-md-6 p-3 rounded-3 shadow" style="width: 47rem;">
                    <div class="card-body">
                        <h3 class="card-text"><b>${andmed_kusimus.pealkiri}</b></h3>
                        <div class="mb-3">
                            <span class="badge rounded-pill text-bg-secondary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16"
                                     fill="currentColor" class="bi bi-person-fill"
                                     viewBox="0 0 17 17">
                                     <path d="M3 14s-1 0-1-1 1-4 6-4 6 3 6 4-1 1-1 1H3Zm5-6a3 3 0 1 0 0-6 3 3 0 0 0 0 6Z"/>
                                </svg> ${andmed_kusimus.kasutaja}
                            </span>
                            <span class="badge rounded-pill text-bg-secondary">
                                <svg xmlns="http://www.w3.org/2000/svg" width="16" height="16" fill="currentColor" class="bi bi-clock" viewBox="0 0 17 17">
                                  <path d="M8 3.5a.5.5 0 0 0-1 0V9a.5.5 0 0 0 .252.434l3.5 2a.5.5 0 0 0 .496-.868L8 8.71V3.5z"/>
                                  <path d="M8 16A8 8 0 1 0 8 0a8 8 0 0 0 0 16zm7-8A7 7 0 1 1 1 8a7 7 0 0 1 14 0z"/>
                                </svg>
                            ${andmed_kusimus.kuupaev}</span>
                        </div>
                        <h6 class="card-text text-dark-emphasis" style="white-space: pre-wrap;">${andmed_kusimus.info}</h6>
                        ${valikud_html}
                        <h6 class="card-text mt-4 pt-2 ms-0" style="display:inline-block">
                            <span class="badge rounded-pill text-bg-primary">Hääli: ` + haali + `</span>
                        </h6>
                        <button ${lulitatud} type="button" onclick="saataVastus(${i+1})" class="btn btn-primary mt-4 pt-2 float-end">Hääleta</button>
                        <h6 class="card-text  mt-4 pt-2 ms-0 me-3 float-end" style="display:inline-block">
                            <span class="badge rounded-pill text-bg-${andmed_kusimus.umberhaalimine ? 'success' : 'warning'}">Ümberhaaletamine: ` + (andmed_kusimus.umberhaalimine ? 'Lubatud' : 'Pole lubatud') + `</span>
                        </h6>
                    </div>
                </div>
            </div>
        `
        saitOnLaadinud()
    }
}});

var valikud = 2;
// Salvestab kasutaja vastuse
function saataVastus(id) {
    var kas_on_valitud = document.querySelectorAll("input[name=radio" + id + "]:checked").length > 0;
    var haal_valik = kas_on_valitud ? document.querySelector("input[name=radio" + id + "]:checked").value : -1
    var on_muutnud = haal_valik != tulemus[id-1].haal

    if (on_muutnud) {
        var andmed_saata = {
            id: id,
            haal: haal_valik
        }

        $.post( "/salvesta_info_haal", {
            info_haal: JSON.stringify(andmed_saata)
        });

        $.get("/varskenda", function(data) {
            window.location.reload();
        });
    }
}
// Animeerib edenemisriba
function kontrolliVastus(id, nr) {
    var oli_valitud_enne = eelmised_haaled[id-1]
    var koik_objektid = document.querySelectorAll("input[name=radio" + id + "]")
    var vajutatud_objekt = koik_objektid[nr]

    if (oli_valitud_enne == nr) {
        eelmised_haaled[id-1] = -1
        vajutatud_objekt.checked = false
    } else {
        eelmised_haaled[id-1] = nr
    }

    var praegu_valitud = vajutatud_objekt.checked ? vajutatud_objekt.value : -1
    var kas_on_valitud = (praegu_valitud != -1)
    var koik_haaled = tulemus[id-1].haaled
    var protsent_html = document.querySelectorAll('p[name=protsent' + id + ']')
    var edenemisriba_html = document.querySelectorAll('div[name=edenemisriba' + id + ']')
    var eelmine_tulemus = tulemus[id-1].haal

    for (var i = 0; i < koik_objektid.length; i++) {
        var haali = Object.values(koik_haaled).reduce((osalineSum, a) => osalineSum + a, 0);
        var protsent = (koik_haaled[i] + (praegu_valitud == i) - (eelmine_tulemus == i))
            / (haali + kas_on_valitud - (eelmine_tulemus != -1)) * 100
        protsent = isNaN(protsent) ? 0 : parseFloat(protsent.toFixed(1))

        protsent_html[i].innerText = protsent + '%'
        edenemisriba_html[i].style = 'width: '+protsent+'%'
    }

}

// Paneb akna kinni ja kustutab salvestamata andmeid
function kustutaValikud() {
    document.getElementById("valikud").innerHTML = `
        <input id='valik-1' type='text' class='form-control mb-2' placeholder='Valik 1'>
        <input id='valik-2' type='text' class='form-control mb-2' placeholder='Valik 2'>
        <div id="lisa_siia_valikud"></div>
    `
}

// Lähtestab valikute arv
function uusKusim() {
    valikud = 2;
}

// Lisab valiku küsitluse loomumisel
function lisadaValik() {
    valikud++;
    document.getElementById("lisa_siia_valikud").insertAdjacentHTML('beforebegin',
    `<input id="valik-${valikud}" maxlength="45" type="text" class="form-control mb-2" placeholder="Valik ${valikud}">`);
}

// Kontrollib kas kõik vajalikud väljad on täidetud
function kontrolliKusimustik() {
    var sisendid = [document.getElementById('pealkiri')];

    for (var i = 1; i <= valikud; i++) {
        sisendid.push(document.querySelector(`#valik-${i}`));
    }

     for (var i = 0; i < sisendid.length; i++) {
            if(sisendid[i].value == '') {
            return true;
            }
     }
    return false;
}

// Loob küsimustik pärast kontrollimist
function luuaKusimustik() {
    if (kontrolliKusimustik()) {
        document.getElementById("error").innerHTML = 'Väljad "Pealkiri" ja "Valikud" on kohustuslikud'
        return;
    }

    var andmed_saata = {
        pealkiri: document.getElementById('pealkiri').value,
        info: document.getElementById('info').value,
        valikud: [],
        anonuumsus: document.getElementById('markeruutAnonuumne').checked,
        umberhaalimine: document.getElementById('markeruutUmberhaalimine').checked
    }

     for (var i = 1; i <= valikud; i++) {
        andmed_saata.valikud.push(document.getElementById(`valik-${i}`).value);
    }

    $.post( "/salvesta_info_kusitlus", {
        info_kusitlus: JSON.stringify(andmed_saata)
    });

    $.get("/varskenda", function(data) {
        window.location.href = window.location.href;
    });
}
