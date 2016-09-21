$(document).ready(function () {
    $('.button-icon').bind('click', function(event) {
        var selectedIcon = $(this).data('icon');

        var modal = $(this).closest('.modal');
        var input = modal.data('id-input');
        console.log('#' + input);
        $('#' + input).val(selectedIcon);
        modal.modal('hide');
      });
    $('.iconModal').on('show.bs.modal', function (event) {
      var button = $(event.relatedTarget) // Button that triggered the modal
      // If necessary, you could initiate an AJAX request here (and then do the updating in a callback).
      // Update the modal's content. We'll use jQuery here, but you could use a data binding library or other methods instead.
      var modal = $(this)

    });
});