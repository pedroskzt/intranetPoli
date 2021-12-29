function resetarPesquisa() {
    for (const div of $('div[intranet-catalogo]')) {
        $('#' + div.id).show();
    }
}

$("#form_pesquisar_catalogos_id").on('submit', function (event) {
    event.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        data: {
            pesquisar: $(this).serializeArray()[0]['value'],
        },
        dataType: 'json',
        success: function (data) {
            if (data.catalogo_id) {
                for (const div of $('div[intranet-catalogo]')) {
                    if (data.catalogo_id.includes(div.id)) {
                        $('#' + div.id).show();
                    } else {
                        $('#' + div.id).hide();
                    }
                }
            }
        }
    })
})

$("input[name='pesquisar']").on('search', function () {
    resetarPesquisa();
})
$("button[type='reset']").on('click', function () {
    resetarPesquisa();
    $("input[name='pesquisar']").focus()
})