function resetarPesquisa() {
    for (div of $('div[intranet-usuarios]')) {
        $('#' + div.id).show();
    }
}

$("#form_pesquisar_usuarios_id").on('submit', function (event) {
    event.preventDefault();
    $.ajax({
        url: $(this).attr('action'),
        data: {
            pesquisar: $(this).serializeArray()[0]['value'],
        },
        dataType: 'json',
        success: function (data) {
            if (data.usuarios_id) {
                for (div of $('div[intranet-usuario]')) {
                    if (data.usuarios_id.includes(div.id)) {
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