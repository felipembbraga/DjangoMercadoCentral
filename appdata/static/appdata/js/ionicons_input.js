$(document).ready(function () {
    $('.ionicon-input input').on('change', function(event) {
        var valor = $(this).val() || 'ion-help'
       var button = $(this).siblings('.input-group-btn').find('.show-icon i');
       button.removeAttr('class').addClass('icon ' + valor);

       console.log(button);
    });
    $('.ionicon-input input').trigger('change');

    $('.button-icon').bind('click', function(event) {
        var selectedIcon = $(this).data('icon');

        var modal = $(this).closest('.modal');
        var input = modal.data('id-input');
        console.log('#' + input);
        $('#' + input).val(selectedIcon);
        $('#' + input).trigger('change');
        modal.modal('hide');
      });
    $('.iconModal').on('show.bs.modal', function (event) {
       var input = $(this).data('id-input');
       var icon = $('#' + input).val();
       $(this).find('.button-icon:not([data-icon="'+ icon +'"])').removeClass('btn-primary');
       var selectedButton = $(this).find('.button-icon[data-icon="'+ icon +'"]');
      selectedButton.addClass('btn-primary');
      var scrollable = $(this).find('.pre-scrollable').get(0);
      console.log(scrollable);
      $(scrollable).scrollTo(1000, 300);
      var button = $(event.relatedTarget) // Button that triggered the modal
      // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      var modal = $(this)

    });

    $('.iconModal').on('shown.bs.modal', function (event) {
        var input = $(this).data('id-input');
        var icon = $('#' + input).val();
        var selectedButton = $(this).find('.button-icon[data-icon="'+ icon +'"]');
        var scrollable = $(this).find('.pre-scrollable').get(0);
        $(scrollable).scrollTo(selectedButton, 500);
    });
});