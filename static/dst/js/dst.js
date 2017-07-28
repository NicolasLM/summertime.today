$(document).ready(function () {
  $('#activate-all').click(function () {
    $('input[type=checkbox]').checkbox('check');
  });
});
$(document).ready(function () {
  $('#deactivate-all').click(function () {
    $('input[type=checkbox]').checkbox('uncheck');
  });
});
