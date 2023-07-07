$(document).ready(function() {
    $('input#todo-due-date').datepicker({
        format: "dd/mm/yyyy",
        autoclose: true,
    });
});