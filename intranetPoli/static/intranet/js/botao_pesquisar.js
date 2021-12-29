$('#pesquisar_button_id').on('click', function () {
    // Esconde o botão de search e revela o formulário de pesquisa.
    $(this).hide()
    $("#pesquisar_id").show()
})
$("button[type='reset']").on('click', function () {
    // Esconde o formulário de pesquisa e revela o botão de search.
    resetarPesquisa();
    $('#pesquisar_button_id').show()
    $("#pesquisar_id").hide()
})
$(document).mouseup(function (event) {
    let container = $("#pesquisar_id");

    // if the target of the click isn't the container nor a descendant of the container
    if (!container.is(event.target) && container.has(event.target).length === 0) {
        $('#pesquisar_button_id').show()
        container.hide()
    }
});
