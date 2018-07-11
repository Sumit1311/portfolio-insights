$(document).ready(function(){
    $('.filterable .btn-filter').click(function(event){
        event.preventDefault();
        var $panel = $(this).parents('.filterable'),
            $filters = $panel.find('.filters'),
            $filtersInput = $panel.find('.filters input'),
            $tbody = $panel.find('.table tbody');
        if ($filters.hasClass('hidden') == true) {
            $filters.removeClass('hidden');
            $filtersInput.first().focus();
        } else {
            $filtersInput.val('');
            $filters.addClass('hidden');
            $tbody.find('.no-result').remove();
            $tbody.find('tr').show();
        }
    });

    $('.filterable .filters input').keyup(function(e){
        /* Ignore tab key */
        var code = e.keyCode || e.which;
        if (code == '9') return;
        /* Useful DOM data and selectors */
        var $input = $(this),
        inputContent = $input.val().toLowerCase(),
        $panel = $input.parents('.filterable'),
        column = $panel.find('.filters th').index($input.parents('th')),
        $table = $panel.find('.table'),
        $rows = $table.find('tbody tr');
    /* Dirtiest filter function ever ;) */
        var $filteredRows = $rows.filter(function(){
            var value = $(this).find('td').eq(column)
            var valuesToSearch = [];
            valuesToSearch.push($(value).find("select option:selected").text());
            valuesToSearch.push($(value).find("input").val());
            valuesToSearch.push($(value).find("textarea").text());
            valuesToSearch.push($(value).find("p").text());
            for(var i in valuesToSearch) {
                if(valuesToSearch[i] && valuesToSearch[i] != "") {
                    var index = valuesToSearch[i].toLowerCase().indexOf(inputContent)
                if(index >= 0) {
                    return false;
                    }
                }
            }
            return true;                 });
        /* Clean previous no-result if exist */
        $table.find('tbody .no-result').remove();
        /* Show all rows, hide filtered ones (never do that outside of a demo ! xD) */
        $rows.show();
        $filteredRows.hide();
        /* Prepend no-result row if all rows are filtered */
        if ($filteredRows.length === $rows.length) {
            $table.find('tbody').prepend($('<tr class="no-result text-center"><td colspan="'+ $table.find('.filters th').length +'">No result found</td></tr>'));
        }
    });
});

