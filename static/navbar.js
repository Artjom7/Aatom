var tulemus_varv

// Võtab andmebaasist kasutaja saidi teema
function saitOnLaadinud() {
    $.ajax({url: "/api/andmed", success: function(kasutaja_andmed) {
        tulemus_varv = kasutaja_andmed.varv
        tulemus_logo = kasutaja_andmed.logo
        document.getElementById("varvRange").value = tulemus_varv
        muutaVarv(tulemus_varv)
    }});
}

// Muudab värvi teema (tooni nihe)
function muutaVarv(varv) {
    document.getElementById("varvRange").value = varv
    var e = document.querySelectorAll(".bg-primary, .btn-primary, .form-check-input, .text-bg-primary, .progress, .dropdown-item, .form-select, .form-control, .img-fluid, .form-range, .btn-outline-primary")
    for (var i = 0; i < e.length; i++) {
        e[i].style.filter = 'hue-rotate('+varv+'deg)'
    }
}

// Saadab seaded mida kasutaja salvestas (Kasutaja info)
function infoKaitleja(lend, info) { <!--, nimi-->
    data = {lend: lend, info: info}; <!--, nimi: nimi-->
    $.post( "/salvesta_info_navbar", {
        navbar_andmed: JSON.stringify(data)
    });
    $.get("/varskenda", function(data) {
        window.location.reload();
    })
};

// Saadab seaded mida kasutaja salvestas (Saidi valimuse seaded)
function seadedKaitleja(vana_logo, varv_salvesta) {
    data = {vana_logo: vana_logo, varv: varv_salvesta}
    $.post( "/salvesta_info_seaded", {
        seaded_andmed: JSON.stringify(data)
    });
    $.get("/varskenda", function(data) {
        window.location.reload();
    })
}

// Kustutab salvestamata muudatused
function kinniKaitleja() {
    muutaVarv(tulemus_varv)
    document.getElementById('vana_logo').checked = tulemus_logo
}