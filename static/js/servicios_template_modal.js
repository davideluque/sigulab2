function testcheck(e)
{
    if (jQuery("#checkbox1").prop("checked") || 
        jQuery("#checkbox2").prop("checked") || 
        jQuery("#checkbox3").prop("checked") || 
        jQuery("#checkbox4").prop("checked")){
        return true;
    }     
    else{
        return false;
    }
}


$(document).ready(function () {
    $('.registration-form fieldset:first-child').fadeIn('slow');

    $('.registration-form input[type="text"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $("#checkbox1").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $("#checkbox2").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $("#checkbox3").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $("#checkbox4").click(function() {
        jQuery("#funcion").removeClass('input-error');
    });

    $('.registration-form select[type="select"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('.registration-form textarea[name="propositoDescripcion"]').on('focus', function () {
        $(this).removeClass('input-error');
    });

    $('.registration-form input[name="itemServicio"]').on('focus', function () {
        $(this).removeClass('input-error');
    });


    // next step
    $('.registration-form .btn-next').on('click', function () {
        var parent_fieldset = $(this).parents('fieldset');
        var next_step = true;

        parent_fieldset.find('input[type="text"],input[type="checkbox"],select[type="select"], textarea[name="propositoDescripcion"], input[name="itemServicio"]').each(function () {         

            if ($(this).val() == "") {
                $(this).addClass('input-error');
                next_step = false;
            }
            else {
                $(this).removeClass('input-error');
            }

        });

        // if (!testcheck()){
        //     jQuery("#funcion").addClass('input-error');
        //     next_step = false;
        // }
        // else{
        //      jQuery("#funcion").removeClass('input-error');
        // }

        if (next_step) {
            parent_fieldset.fadeOut(400, function () {
                $(this).next().fadeIn();
            });
        }

    });

    // previous step
    $('.registration-form .btn-previous').on('click', function () {
        $(this).parents('fieldset').fadeOut(400, function () {
            $(this).prev().fadeIn();
        });
    });

    // submit
    $('#submit').on('click', function (e) {
        var parent_fieldset = $(this).parents('fieldset');

        parent_fieldset.find('input[name="itemServicio"]').each(function () {
            if ($(this).val() == "") {
                jQuery("#item_ensayar").addClass('input-error');
                e.preventDefault();
                return false;
            } else {
                $(this).removeClass('input-error');
            }
        });

    });

   
});