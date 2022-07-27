$(document).ready(function () {

   let i = 1;
    $(document).on('click', '#btnAddSkills', function () {
        $('#campos-dinamicos').append(`
            <div id="fila${i}" class="row mt-2">
                <div class="col-10">
                    <input type="text" class="form-control" name="txtSkill${i}" placeholder="Nueva Skill">
                </div>
                <div class="col-lg-2">
                    <button type="button" class="btn btn-danger btnRemove" id="${i}"><i class="fas fa-trash"></i></button>
                </div>
            </div>
            
        `);
        $("#txtCantidadSkills").val(i);
        i++;
    });


    $(document).on('click', '.btnRemove', function () {
        let idButton = $(this).attr('id');
        let index = $("#txtCantidadSkills").val();
        $("#txtCantidadSkills").val((index - 1));

        $('#fila' + idButton).remove();
    });

});