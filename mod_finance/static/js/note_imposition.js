//Gestion des taxes
function OnTaxeChanged(){
    var selectedValue = $('#id_taxe').val()
    var periode_id = $('#periode_id').val()
    
    if (selectedValue != "") {
    	$.ajax({
            url : '/finance/note_imposition/helpers/taxe_changed/', //"{% url note_imposition_taxe_changed %}"
            type : "POST",
            data : {"taxe" : selectedValue},
            dataType : "json",
            success : function(data){
                //Load dropdown periode               
                Helpers.BuildDropdown(data.periode, $('#id_periode'), '--------', periode_id, "id");
                
                //Affiher le libellé de la taxe
                $('#id_taxe_libelle').val(data.taxe_libelle);

                //Afficher le montant de la taxe
                $('#id_taxe_montant').val(data.taxe_montant);
            }
        });
    }
}

//---------------------------------------------
//---------------- UPLOAD FILE JS -------------
//---------------------------------------------
function bs_input_file() {
  $(".input-file").before(
    function() {
      if ( ! $(this).prev().hasClass('input-ghost') ) {
        var element = $("<input type='file' class='input-ghost' style='visibility:hidden; height:0'>");
        element.attr("name",$(this).attr("name"));
        element.change(function(){
          element.next(element).find('input').val((element.val()).split('\\').pop());
          ActivateSaveButton();
        });
        $(this).find("button.btn-choose").click(function(){
          element.click();
          ActivateSaveButton();
        });
        $(this).find("button.btn-reset").click(function(){
          element.val(null);
          $(this).parents(".input-file").find('input').val('');
          ActivateSaveButton();
        });
        $(this).find('input').css("cursor","pointer");
        $(this).find('input').mousedown(function() {
          $(this).parents('.input-file').prev().click();
          ActivateSaveButton();
          return false;
        });
        return element;
      }
    }
  );
};

//Activer ou désactiver le bouton enregistrer
function ActivateSaveButton(){
  var file = $("#id_fichier_bordereau").val();
  if (file) {
    $("#id_submit").prop('disabled', false);
  } else {
    $("#id_submit").prop('disabled', true);
  }
}

$(function() {
  bs_input_file();
  ActivateSaveButton();
});