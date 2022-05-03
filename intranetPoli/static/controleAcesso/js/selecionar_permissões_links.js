function hideSelected(option) {
    /* Esconde as opções do select de permissões que já tiverem sido selecionadas*/
    if (option.selected === true) {
        return;
    }
    return option.text;
};
$(document).ready(function () {
    $('#id_permissoes').select2({
        theme: 'classic',
        templateResult: hideSelected,
    });
});