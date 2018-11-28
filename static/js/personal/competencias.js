var limit = 10;
$('.comp-check').on('change', function(evt) {
    if($('.comp-check:checked').length > limit) {
        this.checked = false;
    }
});
